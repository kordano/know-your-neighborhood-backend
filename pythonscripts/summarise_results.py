def summarise_results(result):
  import pandas as pd

  
  parsed_results = []
  iid = 0
  for x in range(0,len(result['data']['plan']['itineraries'])):

    temp = ""
   

    for y in range(0, len(result['data']['plan']['itineraries'][x]['legs'])):
      if y == len(result['data']['plan']['itineraries'][x]['legs'])-1: 
        temp = temp + result['data']['plan']['itineraries'][x]['legs'][y]['mode']

      else: 
        temp = temp + result['data']['plan']['itineraries'][x]['legs'][y]['mode'] + ", "
            
    leg_geometries = []
    
    co2 = 0
    

    for leg in range(0,len(result['data']['plan']['itineraries'][x]['legs'])):
      leg_geometries.append({ 'from_coord': (result['data']['plan']['itineraries'][x]['legs'][leg]['from']['lat'], result['data']['plan']['itineraries'][0]['legs'][0]['from']['lon']),
                              'to_coord': (result['data']['plan']['itineraries'][x]['legs'][leg]['to']['lat'], result['data']['plan']['itineraries'][0]['legs'][0]['to']['lon']),
                              'legGeometry': result['data']['plan']['itineraries'][x]['legs'][leg]['legGeometry']})

      if result['data']['plan']['itineraries'][x]['legs'][leg]['mode'] == 'TRAM':
        co2 = co2 + (26* (result['data']['plan']['itineraries'][x]['legs'][leg]['distance']/1000))
      elif result['data']['plan']['itineraries'][x]['legs'][leg]['mode'] == 'BUS':
        co2 = co2 + (70* (result['data']['plan']['itineraries'][x]['legs'][leg]['distance']/1000))


    

    #it_desc = stringify_legs(temp)
    parsed_result = {'Itinerary_ID':iid,
                     'Itinerary_Desc': temp,
                    'Duration_mins': round(result['data']['plan']['itineraries'][x]['duration']/60,0),
                     'Total_Legs': len(result['data']['plan']['itineraries'][x]['legs']),
                     'Geometry': leg_geometries,
                     'co2_emissions':co2}


    parsed_results.append(parsed_result)
    iid += 1

  return parsed_results
