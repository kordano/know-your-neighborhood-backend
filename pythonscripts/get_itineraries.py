def get_itineraries(from_query_string, to_query_string, input_format):

  import requests
  from geocode_search_query import geocode_search_query

  headers = {'Content-type': 'application/json'}

  
  if input_format == 'string': 
    from_coord = geocode_search_query(from_query_string)
    to_coord = geocode_search_query(to_query_string)
    
  else: 
    from_coord = from_query_string
    to_coord = to_query_string
    
      
  
  query = """
  {
    plan(fromPlace: "Helsinki::%s,%s", toPlace: "Helsinki::%s,%s", numItineraries: 10, transportModes: [{mode: BICYCLE, qualifier: RENT}, {mode: TRANSIT}, {mode: TRAM}, {mode:FERRY}, {mode: WALK}]) {
      itineraries {
        walkDistance
        duration
        legs {
          mode
          startTime
          endTime
          from {
            lat
            lon
            name
            bikeRentalStation {
              stationId
              name
            }
          }
          to {
            lat
            lon
            name
            bikeRentalStation {
              stationId
              name
            }
          }
          distance
          legGeometry {
            length
            points
          }
        }
      }
    }
  }

  """ % (from_coord[0],from_coord[1], to_coord[0],to_coord[1])
  
  
  request = requests.post('https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql', json={'query': query}, headers=headers)
  if request.status_code == 200:
      return request.json()
  else:
      raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
