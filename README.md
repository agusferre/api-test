# Countries RESTful API

## Index

-Resources

-Usage and endpoints

-Technical test comments


## Resources 

This API has two resources:

/traces
/statics

Being able of handling one method each.

## Usage and endpoints

# Traces resource

**Description**

This resource is used to receive some information about a specific ip address and the country it belongs to and also storing it in a database for later statistical usage.

**Method**

POST /traces, body: {"ip":"XXX.XXX.XXX.XXX"}

**Parameters**

It expects to receive one parameter in the body called "ip" wich contains a string value for a valid ip address.

**Response**

It returns a "200 OK" code on success and a json dictionary containing the data of the ip requested.

The info requested being the following attributes:

-The ip of the request.

-The country that the ip belongs to.

-The ISO codename of the country.

-The IP coordinates (lat and lon).

-An array of the oficial currencies for that country, each one containing the ISO code for the currency, its symbol and the actual conversion rate for that moment from the currency to USD.

-Distance from the country to Uruguay in Kms.

Example JSON:

{
  'ip': '57.74.111.255',
  'name': 'Cuba', 
  'code': 'CU', 
  'lat': 23.1332, 
  'lon': -82.3594, 
  'currencies': 
  [
    {
      'iso': 'CUC', 
      'symbol': '$', 
      'conversion_rate': 1
    }, 
    {
      'iso': 'CUP', 
      'symbol': '$', 
      'conversion_rate': 0.038
    }
  ], 
  'distance_to_uy': 6548.55
}

# Statistics resource

**Description**

This resource is used to receive some statistical info about previous /traces requests made.

**Method**

GET /statistics

**Parameters**

No parameters are required for this request.

**Response**

It returns a "200 OK" code on success and a json dictionary containing the statistical data at that particular moment.

The statistical data being the following attributes:

-Name of the most distant country to Uruguay from which an ip address was used in a /traces request.

-Distance of the most distant country to Uruguay from which an ip address was used in a /traces request.

-Name of the most traced country from which an ip address was used in a /traces request.

-Amount of traces of the most traced country from which an ip address was used in a /traces request.

Example JSON:

{
  'longest_distance': 
  {
    'country': 'Spain', 
    'value': 9693.18
  }, 
  'most_traced': 
  {
    'country': 'Argentina', 
    'value': 19
  }
}

##Technical test comments
