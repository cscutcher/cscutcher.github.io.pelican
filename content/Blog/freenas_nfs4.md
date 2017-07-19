Title: Tips and Hints for Setting up NFSv4 with Kerberos with FreeIPA and FreeNAS
Tags: notes, linux, freebsd, freenas, nfs, kerberos

I have a FreeIPA server setup in my homelab which provides Kerberos and identity
services.
It seems like overkill, and it probably is, but I wanted to be able to use NFS
which means that I need a way to keep user and groups in sync across my various
machines and VMs.

This also allows me to use the krb5 support in NFSv4 allowing various security
improvements up to full encryption. From the man page;

> Specifying sec=krb5 provides cryptographic proof of a user's identity in each
> RPC request.
> This provides strong verification of the identity of users accessing data on
> the server.
> Note that additional configuration besides adding this mount option is
> required in order  to  enable Kerberos security.
> Refer to the rpc.gssd(8) man page for details.
>
> Two additional flavors of Kerberos security are supported: krb5i and krb5p.
> The krb5i security flavor provides a cryptographically strong guarantee that
> the data in each RPC request has not been tampered with.
> The krb5p security flavor encrypts every RPC request to prevent data exposure
> during network transit; however, expect some performance impact when using
> integrity checking or  encryption.
> Similar support for other forms of cryptographic security is also available.

My NAS box at the moment is running FreeNAS [^freenas-reserved],
which is based on FreeBSD. For reasons I won't go into I needed to do a fresh
install of FreeNAS 11.

Pain Points
===========
Getting everything working has caused me a fair bit of pain. FreeIPA is a damn
sight easier to get going than setting up OpenLDAP and Kerberos manually, but
it still takes a while to get to grips with the many moving parts if you're
unfamiliar. While RedHat has some great high level documentation which applies
to RedHat and CentOS, I found documentation lacking in general for NFSv4,
Kerberos and IPA. FreeNAS's documentation too is a bit lacking.

Also I found it really difficult to get at useful debug information and logs
which made it difficult to progress.

Useful info for fellow travellers
=================================
Frankly, I'm not entirely sure how I got everything working in the end, but I
did find a few little tips that might help others going along the same path.

### Setup everything with CentOS/Redhat only to start with

I found it really useful to get a working setup using only CentOS for the client
and NFS server to start with.

The whole FreeIPA ecosystem is very RH/CentOS friendly and it's much easier to
get going. Everything's a little better [documented][0] and a little more
reliable.

When you've got everything working like this it's easier to bring in FreeNAS or
clients based on other distributions.

### DNS is important

Make sure that all clients and servers can resolve each other with both forward
and reverse DNS lookups.

### Time must be in sync

Kerberos requires that time be in sync for everything involved.
Make sure everything is pointing at the NTP server on the FreeIPA master.

### Test kinit
Make sure you can do;

```
kinit user@IPA.DOMAIN
```

on everything. If that doesn't work you're going to have a bad time.

### Enable more verbose logging for NFS on Linux

This can be very useful when trying to understand why a NFS mount is failing.

Enable NFS debug;

```bash
# Client
rpcdebug -m nfs -s all
# Server
rpcdebug -m nfsd -s all
```

Disable NFS debug;

```bash
# Client
rpcdebug -m nfs -c all
# Server
rpcdebug -m nfsd -c all
```

I can never get useful information out of FreeNAS. It could be my unfamiliarity
with FreeBSD.

### Man Pages
The man pages are some of the best documentation you'll find.

On FreeNAS/FreeBSD;

```bash
man nfsd
man gssd
man exports
man nfsv4
man nfsuserd
```

On Linux;

```bash
man nfs
man exports
man nfsd
```

### Misc Useful Tips and Links
Sorry this is not more organised, but hopefully it'll give clues to others
struggling with related problems.

* On FreeNAS ensure "Require Kerberos for NFSv4" is checked. [See source][1]
* [Useful debug information from IBM][2]
* [Useful debug information from Ubuntu][3]
* [Unread but promising troubleshooting tips][4]
* [NFS and FreeIPA][5]
* [Linux NFS Official FAQ](http://nfs.sourceforge.net/)
* [Introduction to Kerberos](https://www.freeipa.org/page/Kerberos)
* [Linux Domain Identity and Authentication and Policy Guide][6]
* [FreeIPA Troubleshooting Guide](https://www.freeipa.org/page/Troubleshooting)

[^freenas-reserved]: I've been very happy with FreeNAS in the past, but I can't
really 100% recommend it today. If I was rebuilding my NAS box I'd probably look
quite hard at the alternatives. It's still a really nice bit of software, but
it's got some downsides. In any case I'm sorta stuck with it for the moment.

[0]: https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Linux_Domain_Identity_Authentication_and_Policy_Guide/
[1]: https://github.com/freenas/middleware/blob/88136c0d8893c690ff00bbd076b9eb0616d86593/src/dispatcher/libexec/nfsd_wrapper
[2]: https://www.ibm.com/support/knowledgecenter/en/SSLTBW_2.1.0/com.ibm.zos.v2r1.idan400/kerlinx.htm
[3]: https://help.ubuntu.com/community/NFSv4Howto
[4]: http://stromberg.dnsalias.org/~strombrg/NFS-troubleshooting-2.html
[5]: http://wiki.linux-nfs.org/wiki/index.php/NFS_and_FreeIPA
[6]: https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Linux_Domain_Identity_Authentication_and_Policy_Guide/
