# Copyright 2010 Jacob Kaplan-Moss
# Copyright 2011 Nebula, Inc.
# Copyright 2013 Alessio Ababilov
# Copyright 2013 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Exception definitions.

Deprecated since v0.7.1. Use 'keystoneclient.exceptions' instead of
this module. This module may be removed in the 2.0.0 release.
"""

from debtcollector import removals

from keystoneclient.exceptions import *     # noqa


removals.removed_module('keystoneclient.apiclient.exceptions',
                        replacement='keystoneclient.exceptions',
                        version='0.7.1',
                        removal_version='2.0')
