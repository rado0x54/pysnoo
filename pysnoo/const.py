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
OAUTH_SCOPE = ['offline_access']

SNOO_REGISTER_ENDPOINT = SNOO_API_URI + '/us/register/'
SNOO_ME_ENDPOINT = SNOO_API_URI + '/us/me/'
SNOO_DEVICES_ENDPOINT = SNOO_API_URI + '/ds/me/devices/'
SNOO_BABY_ENDPOINT = SNOO_API_URI + '/us/v3/me/baby/'
SNOO_SESSIONS_LAST_ENDPOINT = SNOO_API_URI + '/ss/v2/sessions/last/'
SNOO_SESSIONS_AGGREGATED_ENDPOINT = SNOO_API_URI + '/ss/v2/sessions/aggregated/'
SNOO_SESSIONS_AGGREGATED_AVG_ENDPOINT = SNOO_API_URI + '/ss/v2/babies/{}/sessions/aggregated/avg/'
SNOO_SESSIONS_TOTAL_TIME_ENDPOINT = SNOO_API_URI + '/ss/v2/babies/{}/sessions/total-time/'

# Snoo Pubnub Variables
SNOO_PUBNUB_SUBSCRIBE_KEY = "sub-c-97bade2a-483d-11e6-8b3b-02ee2ddab7fe"
SNOO_PUBNUB_PUBLISH_KEY = "pub-c-699074b0-7664-4be2-abf8-dcbb9b6cd2bf"

DATETIME_FMT_AGGREGATED_SESSION = '%Y-%m-%d %H:%M:%S.%f'
