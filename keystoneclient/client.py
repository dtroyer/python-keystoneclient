# vim: tabstop=4 shiftwidth=4 softtabstop=4

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

from keystoneclient import httpclient
from keystoneclient import lib_api
from keystoneclient import session


LOG = logging.getLogger(__name__)

# NOTE(dtroyer): We need to know the supported/available API client
#                versions somewhere, it might as well be here where you
#                would expect to find client bits...

API_NAME = 'identity'
API_VERSIONS = {
    '2.0': 'keystoneclient.v2_0.client.Client',
    '3': 'keystoneclient.v3.client.Client',
}


# Using client.HTTPClient is deprecated. Use httpclient.HTTPClient instead.
HTTPClient = httpclient.HTTPClient


def Client(version=None, unstable=False, **kwargs):
    """Factory function to create a new identity service client.

    :param tuple version: The required version of the identity API. If
                          specified the client will be selected such that the
                          major version is equivalent and an endpoint provides
                          at least the specified minor version. For example to
                          specify the 3.1 API use (3, 1).
    :param bool unstable: Accept endpoints not marked as 'stable'. (optional)
    :param kwargs: Additional arguments are passed through to the client
                   that is being created.
    :returns: New keystone client object
              (keystoneclient.v2_0.Client or keystoneclient.v3.Client).

    :raises: DiscoveryFailure if the server's response is invalid
    :raises: VersionNotAvailable if a suitable client cannot be found.
    """

    # TODO(dtroyer): Get the usual setup stuff for SSL, no auth needed here
    api_session = session.Session()

    (s_version, c_version) = lib_api.match_api(
        api_session,
        kwargs['auth_url'],
        API_NAME,
        API_VERSIONS,
        version,
    )
    LOG.debug("Identity server versions: %s" % s_version)
    LOG.debug("Identity client versions: %s" % c_version)
    if not s_version and not c_version:
        # We're at the top level exception-handler-wise, be nice and exit
        raise SystemExit("ERROR: Identity API version negotiation failed")
    for link in s_version.links:
        if link['rel'] == 'self':
            kwargs['auth_url'] = link['href']
    LOG.debug("using client %s (%s) for server %s: %s" % (
        c_version.id,
        c_version.class_name,
        s_version.id,
        kwargs['auth_url'],
    ))

    identity_client = get_client_class(
        API_NAME,
        c_version.id,
        API_VERSIONS,
    )
    return identity_client(**kwargs)


def import_class(import_str):
    """Returns a class from a string including module and class

    :param import_str: a string representation of the class name
    :rtype: the requested class
    """
    mod_str, _sep, class_str = import_str.rpartition('.')
    __import__(mod_str)
    return getattr(sys.modules[mod_str], class_str)


def get_client_class(api_name, version, version_map):
    """Returns the client class for the requested API version

    :param api_name: the name of the API, e.g. 'compute', 'image', etc
    :param version: the requested API version
    :param version_map: a dict of client classes keyed by version
    :rtype: a client class for the requested API version
    """
    try:
        client_path = version_map[str(version)]
    except (KeyError, ValueError):
        msg = "Invalid %s client version '%s'. must be one of: %s" % (
              (api_name, version, ', '.join(version_map.keys())))
        raise exceptions.UnsupportedVersion(msg)

    return import_class(client_path)
