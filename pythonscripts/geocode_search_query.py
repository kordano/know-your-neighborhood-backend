def geocode_search_query(user_input_string): 
  ''' returns a geocode from a user's search query) 
  
  Returns: Geocode for input into itinerary
  
  
  '''
  
  import requests

  from urllib.parse import urlencode, quote_plus
  
  
  def run_search_query(user_input_string): # A simple function to use requests.post to make the API call. Note the json= section.
      headers = {'Content-type': 'application/graphql'}
      #parameters = {text: user_input_string} 
      payload = {'text': user_input_string, 'size':1}
      pay_params = urlencode(payload, quote_via=quote_plus)

      request = requests.get('http://api.digitransit.fi/geocoding/v1/search', params=pay_params, headers=headers)

      if request.status_code == 200:
          return request.json()
      else:
          raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, pay_params))

  
  
  result = run_search_query(user_input_string)
  coords = (result['features'][0]['geometry']['coordinates'][1], result['features'][0]['geometry']['coordinates'][0])
  
  return coords