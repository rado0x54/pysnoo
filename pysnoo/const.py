# coding: utf-8
"""PySnoo Constants."""

# Base Headers
BASE_HEADERS = {
    'User-Agent': 'okhttp/4.7.2',
}

# Snoo API endpoints
SNOO_API_URI = 'https://snoo-api.happiestbaby.com'

# OAuth-related
OAUTH_LOGIN_ENDPOINT = SNOO_API_URI + '/us/login/'
OAUTH_TOKEN_REFRESH_ENDPOINT = SNOO_API_URI + '/us/refresh/'
OAUTH_CLIENT_ID = 'snoo_client'
OAUTH_sSCOPE = ['offline_access']

SNOO_REGISTER_ENDPOINT = SNOO_API_URI + '/us/register/'
SNOO_ME_ENDPOINT = SNOO_API_URI + '/us/me/'
SNOO_DEVICES_ENDPOINT = SNOO_API_URI + '/ds/me/devices/'
SNOO_BABY_ENDPOINT = SNOO_API_URI + '/us/v3/me/baby/'
