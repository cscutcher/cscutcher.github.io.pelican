Title: Research Spike on Docker Volume Permission
Tags: notes, docker, linux, lxc, research

I love Docker. Who doesn't! But it's got one issue that continue to bugs me, and
is always biting me in the arse. 

![Docker Logo]({filename}/images/docker.svg)

In many environments, such as on a dev box or a build slave, it can be useful to
use docker to wrap a build tool, or some other one-shot app.
In other words you have some folder on your host machine that you want to modify
and update using a dockerised app.

The usually way to do this is use `--volume` to mount in the host's directory
into the container. However this causes problems.

Most dockerised apps are designed to run as root.
(There is a `--user` flag for `docker run` which I'll get to later but it
doesn't seem to be used all that often.)
This means that any files or folders added by the app in your volume end up
belonging to the root user, rather than the user running `docker run`. 

While it's possible to compensate for this, it's awkward as hell.
I've done a short research spike into some possible solutions and workarounds
that I've explored in the past, or have discovered more recently.

I thought this is a good a place as any to store that research for myself and
others.

*Note: This is really only an initial research spike so don't expect to find
all the answers!*

Using `--user` flag with `docker run`
=====================================
This seems like the obvious answer at first. However it's not quite so perfect
as it seems.

The problem is that the docker image itself doesn't know what user id you're
going to use when you `docker run`. So say you're uid is 1111 there will be no
entry in /etc/passwd, no home directory, nothing, unless you rebuild the docker
image and add it there. 

Without /etc/passwd and other bits, many common linux commands start acting
squirely. For example python gets upset looking for site packages if there's no
home directory. 
SSH can misbehave too, even if it has a valid `$HOME` if there is no entry in 
`/etc/passwd` although I never got to the bottom of why. 
You really can't blame the apps for this though, it's not entirely mad to assume
that the user owning the process has a minimal footprint on the system, but it
does complicate matters.

This means you've got to potentially rebuild your docker image for every
potential user you intend to use in `--user`.

It also means that if you want to safely do "root-like" things, one of the big
advantages of using docker, you can't do so.

Wrapping script inside the docker image
=======================================
You could add a script in your docker image that wraps whatever command you
intend to run with some clean up code to ensure any written files are chmodded
back to the external users uid:gid. 

This works well enough, but unless every image you want to use already does it,
it will probably mean you have to create your own image for almost every image
you use.

Said script also needs to know what the external UID is, so you've now got to
pass that into the `docker run` command.
Then you've got to standardise how you do this in multiple images, and chances
are you'll occasionally get something wrong and litter the volume with root
files.

Wrapping script outside the docker image
========================================
Same principle as above, but instead of writing a script that's part of the
docker image you have a script that wraps the `docker run` command and fixes the
files afterwards.

On the upside you no longer have to do anything special when you run docker, but
on the downside it likely wont work without using sudo which might not be
available.

A colleague got around this problem by calling `docker run` a second time to do
whatever privileged cleanup steps he needed aka docker as a sudo replacement, 
which is a pretty novel solution, but obviously completely mad.

Also, as with the previous 'solution' things also get trickier if you want to
have multiple non-root uids in play. I think it's possible but a lot more
gnarly.

Using bindfs
============
[bindfs](http://bindfs.org/docs/bindfs.1.html) can be used to bind mount one
directory in another location and map between users on one side and the other.

So for example if one had folder `/foo` one could mount it in `/bar` with the
option `--map=jblogs/root`.
If there are files in `/foo` owned by jblogs they will appear in `/bar` as owned
by root. If new files are created by root in `/bar` they will appear on `/foo`
as owned by jblogs.

So rather than just adding a working directory as a volume to docker, one would
first create a bindfs mount of the working directory with a mapping and use that
mount point as the volume with `docker run`. 

IMO this is a nicer solution than any of the above, as it still allows you to be
root inside the container, but without polluting the working directory.

It has a bunch of downsides though;
* It still requires you to do some scripting around the docker
  commands to make it work cleanly. 
* You need bindfs (or something like it) on the host system and permission to
  use it.
* Bindfs in particular is apparently dog slow so I have read
  ([Admittedly in a random github comment](https://github.com/docker/docker/issues/7198#issuecomment-71644946)).
* I'm not sure how bindfs works if you try and use a user id not covered by the
  mappings. This could cause problems.

Using `docker volume create`
==============================
This command can be used to manually create a docker volume which can be later
mounted into the container. 
When creating this volume one seems to be able to use any of the options
normally present on the "mount" command. 
This presumably would allow one to use something like bindfs above but keeping
the config within docker world. 

That being said, it equally shares all of the problems with the previous 
approach.

It is however the closest thing we've got to an official solution to the
problem.
The bug
[Make uid & gid configurable for shared volumes #7198](https://github.com/docker/docker/issues/7198)
was [closed](https://github.com/docker/docker/issues/7198#issuecomment-191990887)
when the local volumes feature appeared;

    "You can do this by creating local volumes, it just landed in master #20262
     ... Closing this as fixed."


Unfortunately how exactly local volumes could be used to achieve this was never
explained and the rest of the bug is people trying to work out what this cryptic
message meant. 
It's possible there is some way to use local volumes to achieve this affect
without bringing bindfs into the picture, but it's not obvious from my brief
investigation.

User Namespaces
===============
I'm going to be slightly vague here because I'm no expert on lxc and this
feature in particular.

User Namespaces allow a kernel level mapping between users inside and outside
the container. 

So if we mapped out container to a namespace starting at 10000, the root user
(uid=0) inside the container maps to uid 10000 outside. User with uid=1 inside
maps to 10001 outside and so on.

Immediately its obvious how this is almost exactly what we want.
I haven't yet had a chance to try it out, but it seems like you could setup a
pretty nice solution.

To enable it's use in dockerd see
[this help page](https://docs.docker.com/engine/reference/commandline/dockerd/#/starting-the-daemon-with-user-namespaces-enabled).
Or for a more complete guide there's
[a good blog post here](https://coderwall.com/p/s_ydlq/using-user-namespaces-on-docker).

It's not without it's disadvantages though;
Firstly it requires user namespaces to be compiled and enabled on the kernel.
It's not in the stock arch kernel yet, and afaik it's not in ubuntu or redhat
either. 

It also requires host system configuration changes including careful planning of
user id ranges. 

I'm also unclear on the relationship between the owning uid, the subuid and
if/how they overlap.
It may still be possible that you end up with files owned by the wrong user, but
at least it wont be root. 


Conclusion
==========
Unfortunately, I ran out of time about here so I couldn't really play with user
namespaces, but if I get the chance to do more it's probably the approach I'll
try next.

If I do I'll try and follow up with how well it went. 


**Other useful links**

* [Docker bug on this issue](https://github.com/docker/docker/issues/7198)
* [What’s Next for Containers? User Namespaces](http://rhelblog.redhat.com/2015/07/07/whats-next-for-containers-user-namespaces/)
* [man user_namespaces](http://man7.org/linux/man-pages/man7/user_namespaces.7.html)
* [Docker help on --userns-remap](https://docs.docker.com/engine/reference/commandline/dockerd/#/starting-the-daemon-with-user-namespaces-enabled)
* [Using User Namespaces on Docker](https://coderwall.com/p/s_ydlq/using-user-namespaces-on-docker)
