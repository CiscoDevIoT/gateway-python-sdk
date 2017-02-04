# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import logging
import sys


__author__ = 'DevIoT Team <deviot.external@cisco.com>'
__version__ = '1.0.0'


def get_logger(name, level=logging.INFO):
    formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)7s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(console_handler)
    return logger

logger = get_logger("DevIoT")

print """
   ___           ________  ______
  / _ \___ _  __/  _/ __ \/_  __/
 / // / -_) |/ // // /_/ / / /
/____/\__/|___/___/\____/ /_/"""
