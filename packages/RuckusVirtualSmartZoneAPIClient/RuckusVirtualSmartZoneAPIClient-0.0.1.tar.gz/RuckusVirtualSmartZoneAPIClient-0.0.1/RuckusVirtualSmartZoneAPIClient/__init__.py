from RuckusVirtualSmartZoneAPIClient.api_interface import APIPlugin
from requests.auth import HTTPBasicAuth
import inspect
import requests


class Client(APIPlugin):
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json;charset=UTF-8'}
    base_url = None
    token = None
    auth = None
    server = None
    controller_version = None
    service_ticket = None

    def connect(self, url: [str, bytes] = '', username: [str, bytes] = '', password: [str, bytes] = ''):
        self.server = url.strip("/")
        self.base_url = f'{self.server}/wsg/api/public/{self.api_version}'
        response = requests.post(f'{self.base_url}/serviceTicket', verify=self.verify, headers=self.headers,
                                 json={'username': username, 'password': password})
        if response.status_code == 200:
            data = response.json()
            self.controller_version = data.get('controllerVersion')
            self.service_ticket = data.get('serviceTicket')

        return response

    def disconnect(self):
        response = requests.delete(f'{self.base_url}/serviceTicket', headers=self.headers, verify=self.verify,
                                   params={'serviceTicket': self.service_ticket})
        return response

    def get(self, url: [str, None] = None, method: [str, bytes] = '', data: dict = None, auth: HTTPBasicAuth = None,
            **kwargs) -> requests.Response:
        """

        :param url: The URL of the resource you are trying to access. Defaults to base_url + method.
        :param method: The method is the part of the url that changes and is appended to basic_url.
        :param data: The data to change or update as a Python dictionary. Defaults to None.
        :param auth: A Requests HTTPBasicAuth with the username and password. Defaults to None.
        :param kwargs: All parameters required by the API call.
        :return: The requests.Response of the API call.
        """
        http_method = inspect.stack()[0][3].upper()
        url = f'{self.base_url}/{method.strip("/")}' if url is None else url
        kwargs.update({'serviceTicket': self.service_ticket})
        return requests.request(http_method, url, headers=self.headers, verify=self.verify, json=data,
                                auth=auth, params=kwargs)

    def post(self, url: [str, None] = None, method: [str, bytes] = '', data: dict = None, auth: HTTPBasicAuth = None,
             **kwargs) -> requests.Response:
        """

        :param url: The URL of the resource you are trying to access. Defaults to base_url + method.
        :param method: The method is the part of the url that changes and is appended to basic_url.
        :param data: The data to change or update as a Python dictionary. Defaults to None.
        :param auth: A Requests HTTPBasicAuth with the username and password. Defaults to None.
        :param kwargs: All parameters required by the API call.
        :return: The requests.Response of the API call.
        """
        http_method = inspect.stack()[0][3].upper()
        url = f'{self.base_url}/{method.strip("/")}' if url is None else url
        kwargs.update({'serviceTicket': self.service_ticket})
        return requests.request(http_method, url, headers=self.headers, verify=self.verify, json=data,
                                auth=auth, params=kwargs)

    def put(self, url: [str, None] = None, method: [str, bytes] = '', data: dict = None, auth: HTTPBasicAuth = None,
            **kwargs) -> requests.Response:
        """

        :param url: The URL of the resource you are trying to access. Defaults to base_url + method.
        :param method: The method is the part of the url that changes and is appended to basic_url.
        :param data: The data to change or update as a Python dictionary. Defaults to None.
        :param auth: A Requests HTTPBasicAuth with the username and password. Defaults to None.
        :param kwargs: All parameters required by the API call.
        :return: The requests.Response of the API call.
        """
        http_method = inspect.stack()[0][3].upper()
        url = f'{self.base_url}/{method.strip("/")}' if url is None else url
        kwargs.update({'serviceTicket': self.service_ticket})
        return requests.request(http_method, url, headers=self.headers, verify=self.verify, json=data,
                                auth=auth, params=kwargs)

    def patch(self, url: [str, None] = None, method: [str, bytes] = '', data: dict = None, auth: HTTPBasicAuth = None,
              **kwargs) -> requests.Response:
        """

        :param url: The URL of the resource you are trying to access. Defaults to base_url + method.
        :param method: The method is the part of the url that changes and is appended to basic_url.
        :param data: The data to change or update as a Python dictionary. Defaults to None.
        :param auth: A Requests HTTPBasicAuth with the username and password. Defaults to None.
        :param kwargs: All parameters required by the API call.
        :return: The requests.Response of the API call.
        """
        http_method = inspect.stack()[0][3].upper()
        url = f'{self.base_url}/{method.strip("/")}' if url is None else url
        kwargs.update({'serviceTicket': self.service_ticket})
        return requests.request(http_method, url, headers=self.headers, verify=self.verify, json=data,
                                auth=auth, params=kwargs)

    def delete(self, url: [str, None] = None, method: [str, bytes] = '', data: dict = None, auth: HTTPBasicAuth = None,
               **kwargs) -> requests.Response:
        """

        :param url: The URL of the resource you are trying to access. Defaults to base_url + method.
        :param method: The method is the part of the url that changes and is appended to basic_url.
        :param data: The data to change or update as a Python dictionary. Defaults to None.
        :param auth: A Requests HTTPBasicAuth with the username and password. Defaults to None.
        :param kwargs: All parameters required by the API call.
        :return: The requests.Response of the API call.
        """
        http_method = inspect.stack()[0][3].upper()
        url = f'{self.base_url}/{method.strip("/")}' if url is None else url
        kwargs.update({'serviceTicket': self.service_ticket})
        return requests.request(http_method, url, headers=self.headers, verify=self.verify, json=data,
                                auth=auth, params=kwargs)
