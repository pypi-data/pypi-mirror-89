#!/usr/bin/env python

from zscalertools import api
import logging
import yaml
import unittest
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)

stream = open(Path(__file__).parent / 'test_api.yml', 'r')
config = yaml.load(stream, yaml.SafeLoader)

class TestSequenceFunctions(unittest.TestCase):
  def setUp(self):
    self.api = api.zia(config['url'], config['username'], config['password'], config['cloud_api_key'])
    
  def test_login(self):
    login = self.api.login()
    self.assertEqual(login['authType'], 'ADMIN_LOGIN')

    
if __name__ == "__main__":
  unittest.main()