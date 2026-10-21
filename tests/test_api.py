import importlib.util
import unittest
from unittest.mock import Mock, patch

AVAILABLE = all(importlib.util.find_spec(name) for name in ['fastapi', 'httpx'])


@unittest.skipUnless(AVAILABLE, 'Install requirements-test.txt for HTTP integration tests')
class ApiTests(unittest.TestCase):
    def setUp(self):
        from fastapi.testclient import TestClient
        from project.api import app
        self.client = TestClient(app)

    def test_health_does_not_generate(self):
        engine = Mock()
        engine.status.return_value = {'generator_loaded': False}
        with patch('project.api.get_engine', return_value=engine):
            response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        engine.generate.assert_not_called()

    def test_invalid_requests(self):
        for data in [{'context': ''}, {'context': '  '}, {'context': 'A', 'language': 'fr'}, {'context': 'x' * 20001}]:
            self.assertEqual(self.client.post('/generate', json=data).status_code, 422)

    def test_response_and_legacy_route(self):
        with patch('project.api.get_engine') as factory:
            factory.return_value.generate.return_value = ['A.', 'B.', 'C.']
            response = self.client.post('/generate', json={'context': 'Opening', 'language': 'en'})
            self.assertEqual(response.json()['continuations'], ['A.', 'B.', 'C.'])
            legacy = self.client.get('/generate_outputs', params={'context': 'Opening', 'language': 'en'})
            self.assertEqual(legacy.json(), [['A.', 'B.', 'C.'], ['A.', 'B.', 'C.']])

    def test_load_failure_is_503(self):
        from project.engine import ModelUnavailable
        with patch('project.api.get_engine') as factory:
            factory.return_value.generate.side_effect = ModelUnavailable('Models unavailable')
            self.assertEqual(self.client.post('/generate', json={'context': 'Opening'}).status_code, 503)
