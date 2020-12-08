# coding: utf-8
"""PySnoo Constants."""

# Base Headers
BASE_HEADERS = {
    'User-Agent': 'SNOO/2.3.2 (com.happiestbaby.snooapp; build:570; iOS 14.2.0) Alamofire/4.9.1',
}

# Snoo API endpoints
SNOO_API_URI = 'https://snoo-api.happiestbaby.com'

# OAuth-related
OAUTH_LOGIN_ENDPOINT = SNOO_API_URI + '/us/login/'
OAUTH_TOKEN_REFRESH_ENDPOINT = SNOO_API_URI + '/us/refresh/'
OAUTH_CLIENT_ID = 'snoo_client'
OAUTH_sSCOPE = ['offline_access']

SNOO_REGISTER_ENDPOINT = '/us/register/'
