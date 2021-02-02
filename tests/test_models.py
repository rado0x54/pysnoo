"""TestClass for all Snoo Models"""

from unittest import TestCase
import json
from pysnoo import User

from .helpers import load_fixture


class TestSnooModels(TestCase):
    """Snoo Models Test class"""

    def test_user_model_mapping(self):
        """Test successful mapping from json payload"""
        user_payload = json.loads(load_fixture('', 'us_me__get_200.json'))
        user = User.from_dict(user_payload)

        self.assertEqual(user.email, user_payload['email'])
        self.assertEqual(user.given_name, user_payload['givenName'])
        self.assertEqual(user.region, user_payload['region'])
        self.assertEqual(user.surname, user_payload['surname'])
        self.assertEqual(user.user_id, user_payload['userId'])
