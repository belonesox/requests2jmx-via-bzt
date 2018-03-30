

# The problem.

* [Jmeter](https://jmeter.apache.org/) is efficient and industry-standard way for  stress/performance testing.
  * Even modern testing frameworks like [Taurus](http://gettaurus.org) use it.
* But:
  * JMeter UI sucks.
  * JMeter tests are blind and fragile.
    * Even if we parametrize authentication headers etc.
  * JMX format unusable for version control systems.

* Selenium tests (Python-Java-PHP-etc) is a well known standard for automated functional testing.
  * But using it for performance testing (with jumbo VMs, Selenigum Grids, a bunch of VMs and docker containers) is very inefficient.

---
Let's combine both ways!
* Selenium tests will be first class citizens (regularly updated, tested, etc.).
* We will automatically generate fresh Jmeter JMX tests from Selenium tests.
* We will run a mix of "smart" Selenium tests and a bunch of "stupid" generated JMeter tests together: 
  * to create heavy load from JMeter tests.
  * to log specific errors/screenshots, etc. using real browser tests.

How to convert Selenium tests to JMX?
* [Taurus](http://gettaurus.org), a modern testing framework, has a module ``proxy2jmx``, which together with with a private service from [Blazemeter](https://www.blazemeter.com/) can automatically generate JMX file from intercepted requests of Selenium Scripts.
   * This service is private but free.
   * It requires you to have internet access to non-standard ports like ``15521`` — such non-privileged ports are frequently banned in "enterprise infrastructure" (only 80 and 443 allowed).
      * And there is no usual way to specify port forwarding in Taurus.
* Currently there is no way to filter generated JMX from "noisy" requests to browser related services. For example, Firefox that is used by Selenium Geckodriver, makes a lot of requests to 
    * ``*.cdn.mozilla.net``
    * ``*.services.mozilla.com``
    * ``*.mozilla.org``
* There is also no way at the moment now how to specify output filename for generated JMX.    

This small ugly package solves aforementioned problems. 
It employs
* monkey-patched Taurus and Blazemeter service
* provided Selenium test
* SSH and some provided external VPS

Its output is:
* Filtered JMX file with a specified filename filename

  

# Installation

It has been tested and right now works on Linuxes (because it need to run commandline ``ssh`` client).

Installation:

```
sudo pip install bzt
sudo pip install git+https://github.com/belonesox/requests2jmx-via-bzt.git 
```
or checkout the project and run usual
```
python setup.py install
```


* Register on Blazemeter service
* Put token/secret from settings to ``~/.bzt-rc``
```
modules:
  blazemeter:
    token: "… token … :… secret … "
```

* Get some VPS outside your enterprise infrastructure. 
  * Even $1 VPS from http://lowendstock.com/ will be OK.
* Setup some linux on it, with SSH daemon
  * Put your ssh keys for some user on it.
  * Enable SSH port forwarding, if your linux distro does not enable it by default.


Run script like 
```
requests2jmx-via-bzt  selenum_script.py  yourvps.somewhere.com:ssh_port generated.jmx
```

# Demo
Look at the project folder ``example``.

* ``0x1tv.py`` — sample selenium test on python. 
  * If you are new in Selenium testing:
    * You have to install 
```
  sudo pip install selenium
```
  * Put ``geckodriver`` in PATH.
* ``refresh-jmx.sh`` — script for generating ``generated-firefox.jmx``. 
  * You have to replace my ``discopal.ispras.ru:2224`` to your VPS, like ``forwardinguser@somewhere.com:someportifnot22``
* ``0x1tv.yml`` — script for testing using Taurus. You can run it even like
```
./0x1tv.yml
```
or 
```
  bzt 0x1tv.yml -report
```
Look at Taurus docs.

BTW, better, if you run heavy load (>10 sessions) on any other site.

* http://0x1.tv — it is my video conference hobby and it is not heavy load ready now.

# ToDo
I hope that all this stuff will become unnecessary if Taurus owners add a couple of extra settings/features.

Actually, I do not like the idea that we have to 
push all requests (including real authentication info)
to some private services. Also we cannot use external service if our testing targets also located inside a corporate network.

I think it is better to write an independent open source local proxy with filtering for JMX generation.

# Contacts
* Issues, patches — welcomed.
* mailto:stas-fomin@yandex.ru





