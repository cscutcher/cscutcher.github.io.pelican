Title: How I Built This Site
Tags: web, python, code

[github.io]: https://pages.github.com/
[github]: https://github.com
[pelican]: http://blog.getpelican.com/

A long time ago I had a webpage build with Drupal. It wasn't very good and I never really used
it properly anyway.
After a harddrive failure I couldn't be bothered to recover the thing and left it to RIP.

Recently I wanted to publish a quick python tutorial I wanted somewhere to put it.
Someone suggested [github.io][github.io] for hosting and so I started some research.

This describes some of what I found out and how I constructed this page.
It's brief but I hope it'll help others who hit the same problems.
If I can help anyone else out drop me a comment.


github.io
=========

[github.io][github.io] is pretty neat.
They'll host your content for free. One pushes ones content to a [github][github] repository
called `username/username.github.io` and it'll be hosted automatically at
`https://username.github.io`.

It has one limitation that I've not in the past had to worry about; it only hosts
static content, so writing something in django or pyramid is well out.

I'm awful when it comes to UI and graphick-y design type stuff, so even if it was practical,
writing raw HTML was right out. So I went on the search for a static web generation package.

Pelican
=======
github.io recommends [jekyll](http://jekyllrb.com/).
It looks good but I'm a pythonista so it doesn't appeal to me.

[StaticGen](https://www.staticgen.com/) is a really handy page that allows the comparison of
the various static web generation frameworks out there.
I filtered for Python and basically picked by popularity and simplicity.
Based on this I picked [Pelican][pelican].

I won't repeat the [Pelican docs](http://docs.getpelican.com/en/3.5.0/)
as they are pretty comprehensive. Instead if you want to see my source for generating with pelican
[it's available here](https://github.com/cscutcher/cscutcher.github.io.pelican).

Here's a few of the ways I've deviated from the standard setup;

* [Switched on archiving by date.](https://github.com/cscutcher/cscutcher.github.io.pelican/blob/master/pelicanconf.py#L40)
* [Disable caching as I planned to autogenerate from an environment where I won't be able to store a cache anyway](https://github.com/cscutcher/cscutcher.github.io.pelican/blob/master/pelicanconf.py#L48)
* [Modified the generated Makefile so it can push to my github.io repo. By default it pushes to a project based page which isn't what I want](https://github.com/cscutcher/cscutcher.github.io.pelican/blob/master/Makefile)
* Enabled the filetime_from_git plugin and created a new plugin called permalinks.

filetime_from_git
-----------------
This handy plugin allows the creation and modification times to be extracted from the git repo
based on the first commit introducing that file rather than be manually entered for each pelican
article.

I had a couple of issues with the module as things stood;

Firstly it had a dependency on some versions of the pythongit module.
Unfortunately its not so easy as installing the right pythongit version as that has a dependency
on the binary git version available on ones distro.
So I wanted to make a modification to provide some isolation from the gitpython version.

Secondly the creation and modification times were based on the filename and did not follow a file
through renames. Being the sort of person that is always changing there mind on titles and naming
schemes I wanted creation and modification to be robust to renames and so modified the plugin to
use;
```bash
git log --folow <filename>
```
to discover commits involving that filename.

These changes are in [my private fork](https://github.com/cscutcher/pelican-plugins/commit/47269dd35b9236de7fc84fa99fb9e41c8d975c05)
of pelican-plugins and will hopefully [be merged back at some point in the future](https://github.com/getpelican/pelican-plugins/pull/473).

permalinks
----------
I wanted to be able to generate some sort of permalink for articles that would again be
robust to renames.

I hit on the idea of using the commit sha of the original commit (again using `--follow`)
introducing a file to be a key allowing redirection to whatever it's new path is.

To achieve this I first created a permalinks module which would create an extra file
in `/permalinks/<some_permalink_id>.html` for each article or page on the site. This page
would redirect (using HTML refresh or javascript) to its new location. It uses whatever
arbitrary key is stored in the `permalink_id` metadata for `some_permalink_id`.

Obviously doing redirects this way, rather than pucker HTTP redirects is suboptimal, but it's the
only option I have given the static nature of the site.

Next I modified the filetime_from_git module to use the same mechanism for finding creation
dates to store the original commit sha as the `permalink_id`.

I also modified the theme to include this link at the bottom of each page and article for easy
access.

At the moment this new plugin (and the modifications to filetime_from_git) are only on
[a branch of my private fork of pelican-plugins](https://github.com/cscutcher/pelican-plugins/tree/permalinks).


Theme
=====
After looking through a few of the available themes for pelican I settled on
[pure-single](https://github.com/PurePelicanTheme/pure-single) which I think looks pretty snazzy.

As I want to easily hack in modifications (as I made for permalinks) I use my [own fork available
here](https://github.com/cscutcher/pure-single).

Apart from the permalink modification mentioned above the only other modification I've made
so far is [adding google comments to the bottom of articles and pages](https://github.com/cscutcher/pure-single/blob/master/templates/google.html).


Automatic generation and push to github using TravisCI
======================================================

This site automatically gets updated when I push to either
[cscutcher/cscutcher.github.io.pelican](https://github.com/cscutcher/cscutcher.github.io.pelican)
or to the fork of the pure-single theme at [cscutcher/pure-single](https://github.com/cscutcher/pure-single).

I do this using the wonderful [Travis CI](http://travis-ci.org/) service. Travis CI allows
adding a `.travis.yml` file to any github which can describe a set of steps to get run on
each commit to github.

I use this to rebuild the site every time a commit is pushed to
[cscutcher/cscutcher.github.io.pelican](https://github.com/cscutcher/cscutcher.github.io.pelican)
and then push the result to the
[cscutcher/cscutcher.github.io](https://github.com/cscutcher/cscutcher.github.io)
repo hosting the site.

To see how I do this [see my `.travis.yml`](https://github.com/cscutcher/cscutcher.github.io.pelican/blob/master/.travis.yml).
It took a bunch of trial an error to get working as I couldn't think of how else to experiment
with the Travis CI environment apart from pushing new commits and hoping for the best!

The most notable feature of this `.travis.yml` is that I have to use an encrypted ssh key so that
travis can push to my repo.
This key is encrypted by travis so only travis can decrypt it, and only when building this branch
of my repo.
In short the steps are;

1. Generate a ssh key.
2. Add the public key as a deployment key for the main github.io repo.
   Don't add it to your users keys as this is unnecessary extra risk!
   By adding it as deployment key you only risk one repo rather than you're whole github account!
3. Use the [travis cli](https://github.com/travis-ci/travis#readme) inside your repo to encrypt
   the private key and add the decryption step to your `.travis.yml` with `travis encrypt-file --add`.
4. Commit **only** the encrypted private key and the public key to your repo.

As I also wanted updated to my template fork to trigger updates I also had to create a `.travis.yml`
for my fork that would trigger a rebuild of a different repo on travis.
This works by using an encrypted github api key with restricted access that is added as an encrypted
variable to the `.travis.yml`.
I had some issues getting this to work with the standard travis cli so wrote a quick python
script to trigger the rerun for the other repository.

The `travis.yml` for the theme fork is [here](https://github.com/cscutcher/pure-single/blob/master/.travis.yml)
and the [python script to trigger reruns is here](https://github.com/cscutcher/travis_restart_trigger).
