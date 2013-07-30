"""Command line interface to the Yelp Search API."""

import json
import oauth2
import optparse
import urllib
import urllib2

url_params = {
    'll':'43.654863,-79.401372',
    'term':'food'
}

options = {
    'consumer_key':'dU2R4gR_UzIDuIiOg0ue9w',
    'consumer_secret':'kwpJ2uOUzm9r-aVI1NlQwN4cd9I',
    'token':'F0TCvDD9-bwnDwqO2qMUHXOtd9YzCNty', 
    'token_secret':'PY0NIPzKyBeU4Y1aM4qMVR8GgcY',
    'host':'api.yelp.com'
}


def request(host, path, url_params, consumer_key, consumer_secret, token, token_secret):
  """Returns response for API request."""
  # Unsigned URL
  encoded_params = ''
  if url_params:
    encoded_params = urllib.urlencode(url_params)
  url = 'http://%s%s?%s' % (host, path, encoded_params)
  print 'URL: %s' % (url,)

  # Sign the URL
  consumer = oauth2.Consumer(consumer_key, consumer_secret)
  oauth_request = oauth2.Request('GET', url, {})
  oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
                        'oauth_timestamp': oauth2.generate_timestamp(),
                        'oauth_token': token,
                        'oauth_consumer_key': consumer_key})

  token = oauth2.Token(token, token_secret)
  oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
  signed_url = oauth_request.to_url()
  print 'Signed URL: %s\n' % (signed_url,)

  # Connect
  try:
    conn = urllib2.urlopen(signed_url, None)
    try:
      response = json.loads(conn.read())
    finally:
      conn.close()
  except urllib2.HTTPError, error:
    response = json.loads(error.read())

  return response


def make_request(location=None, term=None):
    if location: url_params['ll'] = location
    if term: url_params['term'] = term
    response = request(options['host'], '/v2/search', url_params, options['consumer_key'], options['consumer_secret'], options['token'], options['token_secret'])
    #print json.dumps(response, sort_keys=True, indent=2)
    d = response.values()[2]
    print d[0]['name']
    return response

if __name__=='__main__':
    make_request()
