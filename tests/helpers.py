# -*- coding: utf-8 -*-
"""Helper Module for the PySnoo tests."""
import os
import json


def load_fixture(folder, filename, mode='r'):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__),
                        'fixtures', folder, filename)
    with open(path, mode) as fdp:
        return fdp.read()

# Login and Refresh Token response are the same.
def get_token(expires_in=None):
    """Get an OAuth2 Token with variable expires_in"""
    token_string = load_fixture('', 'us_login__post_200.json')
    token = json.loads(token_string)
    if expires_in is not None:
        token['expires_in'] = expires_in

    return token, token_string
