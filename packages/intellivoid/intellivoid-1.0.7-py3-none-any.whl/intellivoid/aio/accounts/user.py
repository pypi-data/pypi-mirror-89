#  Intellivoid - COA API Interface
#  Copyright (C) 2020 Intellivoid <https://github.com/intellivoid>
#
#  This file is part of the Intellivoid package.
#
#  This package is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This package is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this package.  If not, see <http://www.gnu.org/licenses/>.

from intellivoid import exceptions as service_exceptions
import httpx
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


class User(object):

    """
    Public user object

    :param application_id:
    :param secret_key:
    :param access_token:
    :param endpoint:
    """

    def __init__(self, application_id, secret_key, access_token,
                 endpoint="https://api.intellivoid.net/intellivoid/v1/accounts"):
        """
        User Public Constructor
        """

        self.endpoint = endpoint
        self.application_id = application_id
        self.secret_key = secret_key
        self.access_token = access_token

    async def _send(self, path, **payload):
        """
        Sends a basic HTTP POST Request to the endpoint and handles any exceptions

        :param path:
        :param payload:
        :return:
        """

        payload["application_id"] = self.application_id
        payload["secret_key"] = self.secret_key,
        payload["access_token"] = self.access_token
        async with httpx.AsyncClient() as http_client:
            response = await http_client.post("{}/{}".format(self.endpoint, path), data=payload)
            request_id = None
            if "x-request-id" in response.headers:
                request_id = response.headers["x-request-id"]
            return service_exceptions.ServiceException.parse_and_raise(response.status_code,
                                                                       response.text,
                                                                       request_id)

    async def get_information(self, **parameters):
        """
        Returns basic information about the user such as it's ID, Username and Public Avatar URLs

        :param parameters:
        :return:
        """

        return (await self._send("get_user", **parameters))["results"]

    async def get_email(self, **parameters):
        """
        Returns the user's email address, requires permission to view the email address

        :param parameters:
        :return:
        """

        return (await self._send("get_email", **parameters))["results"]["email_address"]

    async def get_personal_information(self, **parameters):
        """
        Returns the user's email address, requires permission to view personal information

        :param parameters:
        :return:
        """

        return (await self._send("get_personal_information", **parameters))["results"]
