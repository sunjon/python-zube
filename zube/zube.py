import json
import sys
from datetime import datetime, timedelta
from re import match
from urllib.parse import urlencode

import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from jwt import encode


class AccessToken():
    auth_url = 'https://zube.io/api/users/tokens'
    jwt_algorithm = 'RS256'
    jwt_expire_delta = 20

    def __init__(self, client_id=None, key_file=None):
        # TODO: error on missing client_id/key_file values
        self.client_id = client_id
        self.authenticated_token = None
        self._private_key = self._load_key_file(key_file)

    # read the keyfile
    @staticmethod
    def _load_key_file(filename):
        try:
            with open(filename, 'rb') as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                    backend=default_backend()
                )
        except (ValueError, FileNotFoundError) as err:
            sys.stderr.write('%s\n' % err)
            sys.exit(1)

        return private_key

    def _sign_jwt(self):
        payload = {
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(seconds=self.jwt_expire_delta),
            'iss': self.client_id
        }
        # TODO: add exception handling
        token = encode(payload, self._private_key, self.jwt_algorithm)
        return token.decode('utf-8')

    # returns a JWT access token valid for 24 hours
    def authenticate(self):
        # make request for auth token (use 'get' as we don't want 'content-type`)
        headers = RequestHandler(None).get_headers(
            method='get', client_id=self.client_id, signing_token=self._sign_jwt())

        response = RequestHandler(None).make_request(
            self.auth_url, headers, method='post')

        if not match(r'^{"access_token"\:".+"}$', response.text):
            # 200 but not json - happened when at wrong url (http rather than https)
            print('bollocks')
            sys.exit()

        self.authenticated_token = response.json()['access_token']


class RequestHandler():
    def __init__(self, api):
        self.api = api

    def _full_url(self, path):
        return '%s%s%s' % (self.api.host, self.api.base_path, path)

    def _full_url_with_params(self, path, params):
        return self._full_url(path) + self._full_query_with_params(params)

    @staticmethod
    def _full_query_with_params(params):
        return ('?' + urlencode(params)) if params else ''

    def get_headers(self, method, client_id, signing_token=None):
        token = signing_token or self.api.authenticated_token
        headers = {
            'Authorization': 'Bearer %s' % token,
            'X-Client-ID': client_id,
            'Accept': 'application/json'
        }
        if method == 'post':
            headers['Content-Type'] = 'application/json'
        return headers

    def prepare_request(self, method, path, params):
        url = post_data = None
        headers = self.get_headers(method, self.api.client_id)

        if method == 'post':
            url = self._full_url(path)
            post_data = json.dumps(params)
        else:
            url = self._full_url_with_params(path, params)
        return url, headers, post_data

    def make_request(self, url, headers, method='get', post_data=None):
        print('headers: %s' % headers)
        print('url: %s' % url)
        # print('URL: %s' % url)
        # TODO: wrap this in a try/except
        response = getattr(requests, method)(url, headers=headers, data=post_data)
        return self._handle_response(response)

    @staticmethod
    def _handle_response(response):
        if response.status_code != 200:
            # TODO: only exit on certain error codes
            # use logging or pass response anyway
            sys.stderr.write('HTTP Error: %s' % response.status_code)
            if response.reason:
                sys.stderr.write(' %s' % response.reason)
            print('\n')
            # sys.stderr.write(response.text[:300] + '...')
            sys.exit(1)
        return response
