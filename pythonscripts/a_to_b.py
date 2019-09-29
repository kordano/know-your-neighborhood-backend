def a_to_b(a_lat, a_lon, b_lat, b_lon):
  ''' Master function to call all the sub-functions
  
  input_format = either 'string' or anything else
  
  '''
  from get_itineraries import get_itineraries
  from summarise_results import summarise_results

  raw_result = get_itineraries(a_lat, a_lon, b_lat, b_lon)
  results = summarise_results(raw_result)
  
  return results