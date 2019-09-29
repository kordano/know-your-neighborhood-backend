def get_itineraries(a_lat, a_lon, b_lat, b_lon):

  import requests
  from geocode_search_query import geocode_search_query

  headers = {'Content-type': 'application/json'}

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

  """ % (a_lat, a_lon, b_lat, b_lon)
  
  
  request = requests.post('https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql', json={'query': query}, headers=headers)
  if request.status_code == 200:
      return request.json()
  else:
      raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
