# -*- encoding: utf-8 -*-
from uuid import uuid4
import unittest
import six
import nutshell
from flake8.engine import get_style_guide

if six.PY2:
    from mock import patch, Mock
else:
    from unittest.mock import patch, Mock


class TestFlake8Compliance(unittest.TestCase):
    def test_flake8(self):
        report = get_style_guide(parse_argv=True, paths=".").check_files()
        self.assertEquals(report.get_state()["total_errors"], 0)


@patch('nutshell.requests')
class TestAPIClient(unittest.TestCase):

    @patch('nutshell.NutshellAPI._api_endpoint_for_user')
    def test_init(self, mock_get_api_endpoint, mock_requests):
        mock_requests.Session.return_value = mock_session = Mock()
        mock_get_api_endpoint.return_value = user_endpoint = '/url'
        username = 'username'
        api_key = 'api_key'

        client = nutshell.NutshellAPI(username, api_key)

        self.assertTrue(mock_requests.Session.called)
        self.assertEqual(client.session, mock_session)
        self.assertEqual(mock_session.auth, (username, api_key))
        mock_get_api_endpoint.assert_called_with(username)
        self.assertEqual(client.user_endpoint, user_endpoint)

    @patch('nutshell.NutshellAPI.json_rpc')
    def test_api_endpoint_for_user(self, mock_json_rpc, mock_requests):
        user_endpoint = 'api.example.com'
        mock_json_rpc.return_value = {'api': user_endpoint}
        username = 'username'

        client = nutshell.NutshellAPI(username, '')

        mock_json_rpc.assert_called_with(
            url=u'https://api.nutshell.com/v1/json',
            method='getApiForUsername',
            params={'username': username}
        )
        self.assertEqual(client.user_endpoint, 'https://api.example.com/api/v1/json')

    @patch('nutshell.NutshellAPI._api_endpoint_for_user')
    @patch('nutshell.NutshellAPI.json_rpc')
    def test_api_called_without_params(self, mock_json_rpc, mock_get_endpoint, mock_requests):
        mock_get_endpoint.return_value = endpoint = '/url'
        mock_json_rpc.return_value = expected_result = Mock()
        method_name = 'findAccounts'
        client = nutshell.NutshellAPI('', '')

        actual_result = client.findAccounts()

        self.assertEqual(expected_result, actual_result)
        mock_json_rpc.assert_called_with(url=endpoint, method=method_name, params={})

    @patch('nutshell.NutshellAPI._api_endpoint_for_user')
    @patch('nutshell.NutshellAPI.json_rpc')
    def test_api_called_with_params(self, mock_json_rpc, mock_get_endpoint, mock_requests):
        mock_get_endpoint.return_value = endpoint = '/url'
        mock_json_rpc.return_value = expected_result = Mock()
        method_name = 'getLead'
        lead_id = 123
        client = nutshell.NutshellAPI('', '')

        actual_result = client.getLead(leadId=lead_id)

        self.assertEqual(expected_result, actual_result)
        mock_json_rpc.assert_called_with(
            url=endpoint,
            method=method_name,
            params={"leadId": lead_id}
        )

    @patch('nutshell.NutshellAPI._api_endpoint_for_user')
    def test_json_rpc_bad_url(self, mock_get_endpoint, mock_requests):
        client = nutshell.NutshellAPI('', '')
        self.assertRaises(nutshell.NutshellApiException, client.json_rpc, {}, 'method', {})

    @patch('nutshell.NutshellAPI._api_endpoint_for_user')
    def test_json_rpc_bad_method(self, mock_get_endpoint, mock_requests):
        client = nutshell.NutshellAPI('', '')
        self.assertRaises(nutshell.NutshellApiException, client.json_rpc, '/u', {}, {})

    @patch('nutshell.NutshellAPI._api_endpoint_for_user')
    def test_json_rpc_bad_params(self, mock_get_endpoint, mock_requests):
        client = nutshell.NutshellAPI('', '')
        self.assertRaises(nutshell.NutshellApiException, client.json_rpc, '/u', 'm', [])

    @patch('nutshell.uuid4')
    @patch('nutshell.NutshellAPI._api_endpoint_for_user')
    def test_normal_request(self, mock_get_endpoint, mock_uuid, mock_requests):
        mock_requests.Session.return_value = mock_session = Mock()
        mock_uuid.return_value = mock_id = uuid4()
        mock_session.post.return_value = mock_response = Mock()
        mock_response.status_code = 200
        expected_result = {'key': 'value'}
        mock_response.json.return_value = {'result': expected_result, 'error': False}
        url = '/u'
        method = 'getLead'
        params = {'leadId': 123}

        client = nutshell.NutshellAPI('', '')
        actual_result = client.json_rpc(url, method, params)

        self.assertEqual(expected_result, actual_result)
        expected_payload = {'method': method, 'params': params, 'id': six.text_type(mock_id)}
        mock_session.post.assert_called_with(url, json=expected_payload)
        self.assertTrue(mock_response.json.called)

    @patch('nutshell.NutshellAPI._api_endpoint_for_user')
    def test_http_error(self, mock_get_endpoint, mock_requests):
        mock_requests.Session.return_value = mock_session = Mock()
        mock_session.post.return_value = mock_response = Mock()
        mock_response.status_code = 401

        client = nutshell.NutshellAPI('', '')
        self.assertRaises(
            nutshell.NutshellApiException,
            client.json_rpc,
            '/u',
            'getLead',
            {'leadId': 123}
        )
        self.assertFalse(mock_response.json.called)

    @patch('nutshell.NutshellAPI._api_endpoint_for_user')
    def test_nutshell_error(self, mock_get_endpoint, mock_requests):
        mock_requests.Session.return_value = mock_session = Mock()
        mock_session.post.return_value = mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'error': {'message': 'Bad Lead ID'}}

        client = nutshell.NutshellAPI('', '')
        self.assertRaises(
            nutshell.NutshellApiException,
            client.json_rpc,
            '/u',
            'getLead',
            {'leadId': 123}
        )
        self.assertTrue(mock_response.json.called)
