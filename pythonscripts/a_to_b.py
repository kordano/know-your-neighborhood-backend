def a_to_b(point_a, point_b, input_format):
  ''' Master function to call all the sub-functions
  
  input_format = either 'string' or anything else
  
  '''
  from get_itineraries import get_itineraries
  from summarise_results import summarise_results


  raw_result = get_itineraries(point_a, point_b, input_format)
  results = summarise_results(raw_result)
  
  return results