DEBUG = False

# These add security to the application and should be sent with all requests.
# X-Frame-Options: protects against clickjacking attacks, prevents patio from
#   being rendered in an iFrame
# X-XSS-Protection: ensures supporting browsers are preventing reflective XSS
#   attacks, thus making it harder for attackers. This is by default on in
#   modern browsers.
# Content Security Policy: Blocks all content not on the whitelist of domains
#   and sources. This needs to be changed if using a third party to host any
#   sort of content including scripts, stylesheets, images, and objects.
HEADERS = {
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Content-Security-Policy': "default-src 'self'",
    'X-Content-Type-Options': 'nosniff'
}

# Security headers related to caching.
# These should not apply to static documents
# Pragma: Prevents sensitive data returned in web responses from being cached by
#   intermediate proxies or browsers.
# Cache-Control: Prevents sensitive data returned in web responses from being
#   cached by intermediate proxies or browsers.
# Expires: Prevents sensitive data returned in web responses from being
#   cached by intermediate proxies or browsers.
CACHE_HEADERS = {
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Expires': 'Thu, 01 Jan 1970 00:00:00 GMT'
}

# These headers should be added when SSL is enabled
#
# This is seperate from the above headers because developers should be able to
# access their devapps without having strict transport security set. This may be
# preferable to do from apache or whatever is doing the conversion from http to
# https on patio.coldbrewlabs.com.
#
# Strict-Transport-Security: browser will only allow requests to https version
#   of site until the max-age has been reached.
SSL_HEADERS = {
    'Strict-Transport-Security': 'max-age=631138519'
}

YAHOO_FINANCE_URL = 'http://biz.yahoo.com/research/earncal/'

SECRET_KEY = '\xda\xbetl\xa4Nr\x17\xd7\xd1E\xed"\xee\x02\r\x0e\xe8]\x9bl\xf3\r\xb9'

# Expiration time of 5 days
SESSION_EXPIRE_TIME = 5 * 24 * 60 * 60 


MYSQL_DB_NAME = 'stockinterest'
