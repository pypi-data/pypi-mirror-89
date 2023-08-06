# @copyright: AlertAvert.com (c) 2015. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from os import getenv
from pathlib import Path

__author__ = "Marco Massenzio"
__email__ = "marco@alertavert.com"
__version__ = '0.7.3'

DEFAULT_CONF_FILE = "conf.yml"
DEFAULT_CONF_DIF = ".crytto"
FILECRYPT_CONF_YML = Path(getenv("HOME")) / DEFAULT_CONF_DIF / DEFAULT_CONF_FILE

BACKUP_EXT = ".bak"
