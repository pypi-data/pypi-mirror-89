import RuckusVirtualSmartZoneAPIClient
import unittest
import os
import json

url = 'https://localhost:8443'
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')


def run_full_test():
    client = RuckusVirtualSmartZoneAPIClient.Client()

    print(f'***** Testing: Login '.ljust(60, '*'))
    client.connect(url, username, password)

    print(f'***** Testing: GET method '.ljust(60, '*'))
    response = client.get(method='/domains')
    print(json.dumps(response.json(), indent=4))

    response = client.post(method='/domains', data={'name': 'APITestDomainDeleteAfter'})
    print(json.dumps(response.json(), indent=4))
    domain_id = response.json()['id']

    response = client.patch(method=f'/domains/{domain_id}',
                            data={'description': 'I updated this description. Now you can delete it.'})
    print(response.status_code)

    print(f'***** Testing: GET method '.ljust(60, '*'))
    response = client.get(method=f'/domains/{domain_id}')
    print(json.dumps(response.json(), indent=4))

    response = client.delete(method=f'/domains/{domain_id}')
    print(response.status_code)

    print(f'***** Testing: GET method '.ljust(60, '*'))
    response = client.get(method='/domains')
    print(json.dumps(response.json(), indent=4))

    print(f'***** Testing: Logout '.ljust(60, '*'))
    client.disconnect()


class TestRuckusAPIWrapper(unittest.TestCase):

    def test_authentication(self):
        client = RuckusVirtualSmartZoneAPIClient.Client()

        response = client.connect(url, username, password)
        self.assertEqual(response.status_code, 200)

        client.disconnect()
        self.assertEqual(response.status_code, 200)

    def test_methods_get(self):
        client = RuckusVirtualSmartZoneAPIClient.Client()

        client.connect(url, username, password)

        response = client.get(method='/domains')
        self.assertEqual(response.status_code, 200)

        response = client.post(method='/domains', data={'name': 'APITestDomainDeleteAfter'})
        self.assertEqual(response.status_code, 201)
        domain_id = response.json()['id']

        response = client.patch(method=f'/domains/{domain_id}',
                                data={'description': 'I updated this description. Now you can delete it.'})
        self.assertEqual(response.status_code, 204)

        response = client.delete(method=f'/domains/{domain_id}')
        self.assertEqual(response.status_code, 204)

        client.disconnect()


if __name__ == '__main__':
    unittest.main()
