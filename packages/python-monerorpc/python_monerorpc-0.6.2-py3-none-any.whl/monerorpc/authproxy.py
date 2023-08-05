"""
  Copyright 2011 Jeff Garzik

  Forked by Norman Schenck from python-bitcoinrpc in 09/2018.
  python-monerorpc is based on this fork.


  AuthServiceProxy has the following improvements over python-jsonrpc's
  ServiceProxy class:

  - HTTP connections persist for the life of the AuthServiceProxy object
    (if server supports HTTP/1.1)
  - sends protocol 'jsonrpc', per JSON-RPC 2.0
  - sends proper, incrementing 'id'
  - sends Digest HTTP authentication headers
  - parses all JSON numbers that look like floats as Decimal
  - uses standard Python json lib

  Previous copyright, from python-jsonrpc/jsonrpc/proxy.py:

  Copyright (c) 2007 Jan-Klaas Kollhof

  This file is part of jsonrpc.

  jsonrpc is free software; you can redistribute it and/or modify
  it under the terms of the GNU Lesser General Public License as published by
  the Free Software Foundation; either version 2.1 of the License, or
  (at your option) any later version.

  This software is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public License
  along with this software; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import decimal
import json
import logging
import urllib.parse as urlparse

from requests import auth, Session, codes
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError, Timeout, RequestException


USER_AGENT = "AuthServiceProxy/0.1"

HTTP_TIMEOUT = 30
MAX_RETRIES = 3

log = logging.getLogger("MoneroRPC")


class JSONRPCException(Exception):
    def __init__(self, rpc_error):
        parent_args = []
        if "message" in rpc_error:
            parent_args.append(rpc_error["message"])
        Exception.__init__(self, *parent_args)
        self.error = rpc_error
        self.code = rpc_error["code"] if "code" in rpc_error else None
        self.message = rpc_error["message"] if "message" in rpc_error else None

    def __str__(self):
        return f"{self.code}: {self.message}"

    def __repr__(self):
        return f"<{self.__class__.__name__} '{self}'>"


def EncodeDecimal(o):
    if isinstance(o, decimal.Decimal):
        return float(round(o, 12))
    raise TypeError(repr(o) + " is not JSON serializable.")


class AuthServiceProxy(object):
    """Extension of python-jsonrpc
    to communicate with Monero (monerod, monero-wallet-rpc)
    """

    retry_adapter = HTTPAdapter(max_retries=MAX_RETRIES)

    __id_count = 0

    def __init__(
        self,
        service_url,
        username=None,
        password=None,
        service_name=None,
        timeout=HTTP_TIMEOUT,
        connection=None,
    ):
        """
        :param service_url: Monero RPC URL, like http://user:passwd@host:port/json_rpc.
        :param service_name: Method name of Monero RPC.
        """

        self.__service_url = service_url
        self.__service_name = service_name
        self.__timeout = timeout
        self.__url = urlparse.urlparse(service_url)

        port = self.__url.port if self.__url.port else 80
        self.__rpc_url = (
            self.__url.scheme
            + "://"
            + self.__url.hostname
            + ":"
            + str(port)
            + self.__url.path
        )

        if connection:
            # Callables re-use the connection of the original proxy
            self.__conn = connection
        else:
            headers = {
                "Content-Type": "application/json",
                "User-Agent": USER_AGENT,
                "Host": self.__url.hostname,
            }

            user = username if username else self.__url.username
            passwd = password if password else self.__url.password
            # Digest Authentication
            authentication = None
            if user is not None and passwd is not None:
                authentication = auth.HTTPDigestAuth(user, passwd)

            self.__conn = Session()
            self.__conn.mount(
                f"{self.__url.scheme}://{self.__url.hostname}", self.retry_adapter
            )
            self.__conn.auth = authentication
            self.__conn.headers = headers

    def __getattr__(self, name):
        """Return the properly configured proxy according to the given RPC method.

        This maps requested object attributes to Monero RPC methods
        passed to the request.

        This is called before '__call__'.

        :param name: Method name of Monero RPC.
        """

        if name.startswith("__") and name.endswith("__"):
            # Python internal stuff
            raise AttributeError
        if self.__service_name is not None:
            name = f"{self.__service_name}.{name}"
        return AuthServiceProxy(
            service_url=self.__service_url,
            service_name=name,
            connection=self.__conn,
        )

    def __call__(self, *args):
        """Return the properly configured proxy according to the given RPC method.

        This maps requested object attributes to Monero RPC methods
        passed to the request.

        This is called on the object '__getattr__' returns.
        """

        AuthServiceProxy.__id_count += 1

        log.debug(
            f"-{AuthServiceProxy.__id_count}-> {self.__service_name} {json.dumps(args, default=EncodeDecimal)}"
        )
        # args is tuple
        # monero RPC always gets one dictionary as parameter
        if args:
            args = args[0]

        postdata = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": self.__service_name,
                "params": args,
                "id": AuthServiceProxy.__id_count,
            },
            default=EncodeDecimal,
        )
        return self._request(postdata)

    def batch_(self, rpc_calls):
        """Batch RPC call.
        Pass array of arrays: [ [ "method", params... ], ... ]
        Returns array of results.

        No real implementation of JSON RPC batch.
        Only requesting every method one after another.
        """
        results = []
        for rpc_call in rpc_calls:
            method = rpc_call.pop(0)
            params = rpc_call.pop(0) if rpc_call else {}
            try:
                results.append(self.__getattr__(method)(params))
            except (JSONRPCException) as e:
                log.error(f"Error: '{str(e)}'.")
                results.append(None)

        return results

    def _request(self, postdata):
        log.debug(f"--> {postdata}")
        request_err_msg = None
        try:
            r = self.__conn.post(
                url=self.__rpc_url, data=postdata, timeout=self.__timeout
            )
        except (ConnectionError) as e:
            request_err_msg = (
                f"Could not establish a connection, original error: '{str(e)}'."
            )
        except (Timeout) as e:
            request_err_msg = f"Connection timeout, original error: '{str(e)}'."
        except (RequestException) as e:
            request_err_msg = f"Request error: '{str(e)}'."

        if request_err_msg:
            raise JSONRPCException({"code": -341, "message": request_err_msg})

        response = self._get_response(r)
        if response.get("error", None) is not None:
            raise JSONRPCException(response["error"])
        elif "result" not in response:
            raise JSONRPCException(
                {"code": -343, "message": "Missing JSON-RPC result."}
            )
        else:
            return response["result"]

    def _get_response(self, r):
        if r.status_code != codes.ok:
            raise JSONRPCException(
                {
                    "code": -344,
                    "message": f"Received HTTP status code '{r.status_code}'.",
                }
            )
        http_response = r.text
        if http_response is None:
            raise JSONRPCException(
                {"code": -342, "message": "Missing HTTP response from server."}
            )

        try:
            response = json.loads(http_response, parse_float=decimal.Decimal)
        except (json.JSONDecodeError) as e:
            raise ValueError(f"Error: '{str(e)}'. Response: '{http_response}'.")

        if "error" in response:
            if response.get("error", None) is None:
                log.debug(
                    f"<-{response['id']}- {json.dumps(response['result'], default=EncodeDecimal)}"
                )
            else:
                log.error(f"Error: '{response}'")
        else:
            log.debug(f"<-- {response}")
        return response
