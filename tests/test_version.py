#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of requests2jmx-via-bzt.
# https://github.com/belonesox/requests2jmx-via-bzt

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2018, Stas Fomin <stas-fomin@yandex.ru>

from preggy import expect

from requests2jmx_via_bzt import __version__
from tests.base import TestCase


class VersionTestCase(TestCase):
    def test_has_proper_version(self):
        expect(__version__).to_equal('0.1.0')
