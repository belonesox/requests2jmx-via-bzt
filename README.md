

# The problem.

* [Jmeter](https://jmeter.apache.org/) is efficient and industry-standard way for  stress/performance testing.
  * Even modern testing frameworks, like [Taurus](http://gettaurus.org), used it.
* But:
  * JMeter UI sucks.
  * JMeter tests are blind and fragile.
    * Even if we parametrise authentification headers etc.
  * JMX format unusable for version control systems.

* Selenium tests (Python-Java-PHP-etc) are well known standard for automated functional testing.
  * But using it for performance testing (with jumbo VMs, Selenigum Grids, bunch of VMs and docker containers) is very unefficient.

---
Lets combine both ways!
* Selenium tests will be first class citizens (regularly updated, tested, etc).
* We will automatically generate fresh Jmeter JMX tests from Selenium tests.
* We will run mix of "smart" Selenium tests and bunch of "stupid" generated JMeter tests together: 
  * to create heavy load from JMeter tests.
  * log specific errors/screenshots, etc using real browser tests.

How to convert Selenium tests to JMX?
* Modern framework [Taurus](http://gettaurus.org) has module ``proxy2jmx``, which with with private service [Blazemeter](https://www.blazemeter.com/) can automatically generate JMX file from intercepted requests of Selenium Scripts.
   * It is private (but free) service.
   * But it need that you have internet access to non-standard ports like ``15521`` — such nonprivileged ports frequently banned in "enterprise infrastructure" (only 80 and 443 allowed).
      * And no usual way how to specify port forwarding to Taurus.
* Also there is no way now how generated JMX can be filtered from "noisy" requests to browser related services. For example, Firefox, used by Selenium Geckodriver, make a lot of requests to 
    * ``*.cdn.mozilla.net``
    * ``*.services.mozilla.com``
    * ``*.mozilla.org``
* Also there is no way now how to specify output filename for generated JMX.    

This small ugly package solve these problems. 
It use
* monkey-patched Taurus and Blazemeter service
* provided selenium test
* SSH and some provided external VPS

and get:
* Filtered JMX file with given filename

  

# Installation

Right now worked and tested on Linuxes (need to run commandline ``ssh`` client)
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

* Get some VPS outside enterprise infrastructure. 
  * Even $1 VPS from http://lowendstock.com/ will be OK.
* Setup some linux on it, with SSH daemon
  * Put your ssh keys for some user on it.
  * Enable SSH port forwarding, if your linux distro does not enable it by default.


Run script like 
```
requests2jmx-via-bzt  selenum_script.py  yourvps.somewhere.com:ssh_port generated.jmx
```

# Demo
Look at project folder ``example``.

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

BTW, better, if you will run heavy load (>10 sessions) on any other site.

* http://0x1.tv — it is my video conference hobby, it is not ready now for heavy load.

# ToDo
I hope that all this stuff will became unusual if Taurus owners add couple of settings/features.

But I do not like the idea, that we have to 
push all requests (including real authentification info)
to some private services.
Also, we cannot use external service if our testing targets also located inside a corporate network.

I think will be better to wrote independent
open source local proxy with filtering
to generate JMX.

# Contacts
* Issues, patches — welcomed.
* mailto:stas-fomin@yandex.ru





