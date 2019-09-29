def postcode_lookup(lat=60.1692942, lon=24.9258062): # A simple function to use requests.post to make the API call. Note the json= section.
  ''' Takes lat and long coordinates, calls the HSL enpoint and returns a postcode. 
  Input: lat & long as floats
  Output: postcode as string
  '''
  import requests
  from urllib.parse import urlencode, quote_plus
  
  headers = {'Content-type': 'application/graphql'}
  #parameters = {text: user_input_string} 
  payload = {'point.lat': lat, 'point.lon':lon, 'size':1}
  pay_params = urlencode(payload, quote_via=quote_plus)

  request = requests.get('http://api.digitransit.fi/geocoding/v1/reverse', params=pay_params, headers=headers)
  r = request.json()
  r = r['features'][0]['properties']['postalcode']


  if request.status_code == 200:
      return r
  else:
      raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, pay_params))