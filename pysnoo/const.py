# coding: utf-8
"""PySnoo Constants."""

# Base Headers
BASE_HEADERS = {
    'User-Agent': 'SNOO/2.3.2 (com.happiestbaby.snooapp; build:570; iOS 14.2.0) Alamofire/4.9.1',
}

# Snoo API endpoints
SNOO_API_URI = 'https://snoo-api.happiestbaby.com'

# Oauth-related
class OAuth:
    """OAuth class constants"""
    LOGIN_ENDPOINT = SNOO_API_URI + '/us/login/'
    TOKEN_REFRESH_ENDPOINT = SNOO_API_URI + '/us/refresh/'
    CLIENT_ID = 'snoo_client'
    SCOPE = ['offline_access']




SNOO_REGISTER_ENDPOINT = '/us/register/'



#####################
# number of attempts to refresh token
# RETRY_TOKEN = 3

# default suffix for session cache file
# CACHE_ATTRS = {'account': None, 'alerts': None, 'token': None}
#
# try:
#     CACHE_FILE = os.path.join(os.getenv('HOME'),
#                               '.carson_living-session.cache')
# except (AttributeError, TypeError):
#     CACHE_FILE = os.path.join('.', '.carson_living-session.cache')






C_ME_ENDPOINT = '/me/'

C_DOOR_OPEN_ENDPOINT = '/doors/{}/open/'
C_EEN_SESSION_ENDPOINT = '/properties/buildings/{}/eagleeye/session/'

# Eagle Eye API endpoints
# Beware URLs DO NOT end in '/', otherwise it returns a 500
EEN_API_URI = 'https://{}.eagleeyenetworks.com'
EEN_DEVICE_ENDPOINT = '/g/device'
EEN_DEVICE_LIST_ENDPOINT = '/g/device/list'
EEN_GET_IMAGE_ENDPOINT = '/asset/{}/image.jpeg'
EEN_GET_VIDEO_ENDPOINT = '/asset/play/video.{}'
EEN_IS_AUTH_ENDPOINT = '/g/aaa/isauth'

# Eagle Eye Network Interface options
EEN_ASSET_REF_ASSET = 'asset'
EEN_ASSET_REF_PREV = 'prev'
EEN_ASSET_REF_NEXT = 'next'
EEN_ASSET_REF_AFTER = 'after'

EEN_ASSET_CLS_ALL = 'all'
EEN_ASSET_CLS_PRE = 'pre'
EEN_ASSET_CLS_THUMB = 'thumb'

EEN_VIDEO_FORMAT_FLV = 'flv'
EEN_VIDEO_FORMAT_MP4 = 'mp4'
