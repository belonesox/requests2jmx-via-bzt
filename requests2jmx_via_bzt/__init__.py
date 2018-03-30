#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of requests2jmx-via-bzt.
# https://github.com/belonesox/requests2jmx-via-bzt

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2018, Stas Fomin <stas-fomin@yandex.ru>

import sys
import os
import optparse
import time
import tempfile
import shutil
import subprocess
import re
import bzt.cli 
import bzt.modules.proxy2jmx
from collections import namedtuple
import traceback
from lxml import etree
from io import StringIO, BytesIO

import codecs
import urllib2
import json
import base64
import ssl
import datetime
import glob

from requests2jmx_via_bzt.version import __version__  # NOQA

def isotime():
    """
    """
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') 
    return now


def filter_jmx(infilename, outfilename):
    # doc = etree.parse(StringIO(infilename))
    domains_to_filter = [
        "cdn.mozilla.net",
        "services.mozilla.com",
        "mozilla.org",
    ]
    
    with codecs.open(infilename, 'r', encoding='utf-8') as utf8_file:
        doc = etree.parse(utf8_file)
        root = doc.getroot()
        result = len(root.xpath(".//*"))        
        for todel in root.findall('.//stringProp[@name="HTTPSampler.domain"]'):
            need_filter = False
            for domain in domains_to_filter:
                if domain in todel.text:
                    need_filter = True
            if need_filter:
                sampler_proxy = todel.xpath('..')[0]
                hashtree = sampler_proxy.getprevious()
                pparent = sampler_proxy.xpath('..')[0]
                pparent.remove(sampler_proxy)
                pparent.remove(hashtree)
  
        open(outfilename, 'w').write(etree.tostring(root))
    pass
    


def process(ymlfilename, externalproxy, jmxfilename, artifacts_dir):
    class BztOptions(object):
        pass
    
    pass

    orig_proxy2jmx_prepare = bzt.modules.proxy2jmx.Proxy2JMX.prepare
    
    def proxy2jmx_prepare(self):
        orig_proxy2jmx_prepare(self)
        
        blazemeter_cfg = self.engine.config.get("modules").get("blazemeter")
        self.proxy.token = self.settings.get("token", blazemeter_cfg.get("token"))

        request = urllib2.Request("https://a.blazemeter.com/api/latest/proxy")
        base64string = base64.encodestring(self.proxy.token).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)   
        response = urllib2.urlopen(request, context=ssl._create_unverified_context())
        data = json.loads(response.read())
        proxy_host = data['result']['host']
        proxy_port = data['result']['port']
        
        self.proxy_addr = "http://127.0.0.1:%s" % proxy_port

        terms = externalproxy.split(":")        
        externalproxy_host = terms[0]
        if len(terms) > 0:
            externalproxy_port = terms[1]
        
        if '@' not in externalproxy_host:
          externalproxy_host = 'root@' + externalproxy_host
        scmd = "ssh %(externalproxy_host)s -p %(externalproxy_port)s -L %(proxy_port)s:%(proxy_host)s:%(proxy_port)s" % vars()
        self.ssh_proc = subprocess.Popen(scmd, shell=True)
        pass
    
    bzt.modules.proxy2jmx.Proxy2JMX.prepare = proxy2jmx_prepare

    options = BztOptions()
    options.__dict__ = {'verbose': None, 'no_system_configs': None, 'quiet': None, 'log': None, 'option': None, 'aliases': []}

    executor = bzt.cli.CLI(options)
    try:
        code = executor.perform([ymlfilename])
    except Exception as ex_:
        str_ex = str(ex_)
        traceback_ = traceback.format_exc()
        print str_ex
        print tracenack_
        
    generated_gmx_filename = "generated_sel.smart.jmx"    
        
    if not artifacts_dir:
        # Iam lazy to many patch something else, just trying to find latest  generated JMX
        indir = os.path.split(os.path.realpath(ymlfilename))[0]
        list_of_jmxes = glob.glob('%s/*/%s' % (indir, generated_gmx_filename)) 
        latest_file = max(list_of_files, key=os.path.getctime)
        artifacts_dir = os.path.split(latest_file)[0]
        
    infilename = os.path.join(artifacts_dir, generated_gmx_filename)    
        
    filter_jmx(infilename, jmxfilename)
    pass


def main():
  if len(sys.argv) < 4:
      print "Call this '%s' 'selenium-script-or-taurus-yml'  'external.proxy.com:port' 'output-generated.jmx'"
      sys.exit(1)

  filename = sys.argv[1]
  ymlfilename = filename
  artifacts_dir = None
  if not filename.endswith('.yml'):
      scriptfilename = os.path.realpath(filename)
      templdir = tempfile.gettempdir()
      artifacts_dir = os.path.join(templdir, "last-jmx-" + isotime() )
      ymlfilename = os.path.join(templdir, 'sel2jmx.yml')
      open(ymlfilename, 'w').write("""
settings:
  artifacts-dir: %s

execution:
- executor: selenium
  iterations: 1
  scenario: sel

scenarios:
  sel:
    script: "%s"

services:
- module: proxy2jmx
""" % (artifacts_dir, scriptfilename))
  
  externalproxy = sys.argv[2]
  outputjmx = sys.argv[3]

  process(ymlfilename, externalproxy, outputjmx, artifacts_dir)

if __name__ == '__main__':
    #filter_jmx(u'/home/stas/projects/modeus-iot-selenium-tests/modified_iot-generated.jmx', u'/home/stas/projects/modeus-iot-selenium-tests/modified_iot-generated-fixed.jmx')
    main()