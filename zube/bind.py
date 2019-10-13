import json
from re import match, search

from .zube import RequestHandler


class ZubeClientError(Exception):
    def __init__(self, error_message, status_code=None):
        self.status_code = status_code
        self.error_message = error_message

    def __str__(self):
        if self.status_code:
            return '[ %s ] %s' % (self.status_code, self.error_message)
        return self.error_message


def bind_method(**config):
    class ZubeAPIMethod():
        path = config['path']
        method = config.get('method', 'get')
        # accepts_parameters = config.get('accepts_parameters', [])
        filter_parameters = config.get('filter_parameters', [])
        # paginates = config.get('paginates', False)
        # TODO: other response types?
        response_type = config.get('response_type', 'list')
        # print('path: %s' % path)
        # print('method: %s' % method)

        def __init__(self, api, **kwargs):
            self.api = api
            # self.as_generator = kwargs.pop("as_generator", False)
            # if self.as_generator:
            #     self.pagination_format = 'next_url'
            # TODO: Need a conditional for GET/POST
            # else:
            #     self.pagination_format = kwargs.pop('pagination_format', 'next_url')
            # self.return_json = kwargs.pop("return_json", False)
            # self.max_pages = kwargs.pop("max_pages", 3)
            # self.with_next_url = kwargs.pop("with_next_url", None)

            self.page = kwargs.pop('page', None)
            self.per_page = kwargs.pop('per_page', None)

            self.parameters = {}
            self._build_parameters(kwargs)

        # @staticmethod
        # def _encode_string(value):
        #     return value.encode('utf-8') if isinstance(value, str) else str(value)

        # build parameters for args in the format `verb[preposition]`
        def _build_parameters(self, kwargs):
            param_match = r'(?P<param>^.*)\[(?P<value>.*)\]'
            filtered = {key: value for key, value in kwargs.items()
                        if match(param_match, key)}

            for key, value in filtered.items():
                m = search(param_match, key)
                if self._validate_filter(m.group('param'), m.group('value'), value):
                    self.parameters[key] = value
                    kwargs.pop(key)

            # any remaining args are redundant
            for key, val in kwargs.items():
                raise ZubeClientError('invalid parameter: %s=%s' % (key, val))

        def _validate_filter(self, filtr, val, target):
            # TODO: need a better word than preposition (and target)
            valid_filters = [
                'order',
                'where',
                'select',
            ]
            # TODO: handle `github_issue`

            rules = {
                'invalid parameter':
                    filtr not in valid_filters,
                'invalid order direction':
                    filtr == 'order' and val == 'direction' and target not in ('asc', 'desc'),
                'invalid order column':
                    filtr == 'order' and val == 'by' and target not in self.filter_parameters,
                'invalid `where` preposition':
                    filtr == 'where' and val not in self.filter_parameters,
                'select takes no preposition':
                    filtr == 'select' and val,
            }

            for error_msg in (key for key, value in rules.items() if value):
                keyval = '%s[%s]=%s' % (filtr, val, target)
                raise ZubeClientError('%s: %s' % (error_msg, keyval))

            return True

        def execute(self):
            url, headers, post_data = RequestHandler(self.api).prepare_request(
                self.method, self.path, self.parameters)
            # print('debug: execute()')
            # print('url: %s' % url)
            # print('method: %s' % method)

            # response, _next = RequestHandler(self.api).make_request(
            response = RequestHandler(self.api).make_request(
                url, headers, method=self.method, post_data=post_data)

            # sanitize json - json.dumps() to fix quotes
            output = json.dumps(response.json())
            output = output.replace(': None', ': "None"')
            output = output.replace(': False', ': "False"')

            # return output
            print(output)
            exit()
            # content, next = self._do_api_request(url, headers, self.method, post_data)
            # if self.paginates:
            #     return content, next
            # else:
            #     return content
            # return 'results list'

    def _call(api, **kwargs):
        method = ZubeAPIMethod(api, **kwargs)
        return method.execute()

    return _call
