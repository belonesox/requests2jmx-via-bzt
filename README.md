

# The problem.

* Jmeter is efficient and industry-standard way for  stress/performance testing.
  * Even modern testing frameworks, like Taurus, used it.
* But:
  * JMeter UI sucks
  * JMeter tests are blind and fragile
    * Even if we parametrise authentification headers etc.
  * JMX format unusable for version control systems.

* Selenium tests (Python-Java-PHP-etc) well known standard for automated functional testing.
  * But using it for performance testing (with jumbo VMs, Selenigum Grids, bunch of VMs and docker containers) — very unefficient.

Lets combine both ways!
* Selenium tests will be first class citizens
* We will automatically generate Jmeter JMX tests from Selenium tests.
* We will run mix of "smart" Selenium tests and bunch of "stupid" generated JMeter tests together, 
  * to create heavy load
  * log specific errors/screenshots, etc using real browser tests.

How to convert Selenium tests to JMX?
* Modern framework [Taurus](http://gettaurus.org) has module proxy2jmx, according with private service [Blazemeter](https://www.blazemeter.com/) to automatically generate JMX from intercepted requests from Selenium Scripts.
   * It is private (but free) service
   * But it need that you have to internet access to non-standard ports like 15521 — such ports frequently banned in "enterprise infrastructure".
      * And no usual way how specify port forwarding to Taurus.
* Also there is no way now, how generated JMX can be filtered from "noisy" requests to browser related services. For example, Firefox, used by Selenium Geckodriver, make a lot of requests to 
    * *.cdn.mozilla.net
    * *.services.mozilla.com
    * *.mozilla.org
* Also there is no way now how to specify output filename for generated JMX.    

This small ugly package solve these problems. 
It use
* monkey-patched Taurus and Blazemeter service
* provided selenium test
* SSH and some provided external VPS

and get:
* Filtered JMX file with given filename

  

# Installation

sudo pip install 
# requests2jmx-via-bzt




