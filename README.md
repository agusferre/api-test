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

### Base url

The base url is *https://api-test-01010101.uc.r.appspot.com/*.
So for any resource request it should be done using *https://api-test-01010101.uc.r.appspot.com/{resource}*

### Traces resource

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

```json
{
  "ip": "57.74.111.255",
  "name": "Cuba", 
  "code": "CU", 
  "lat": 23.1332, 
  "lon": -82.3594, 
  "currencies": 
  [
    {
      "iso": "CUC", 
      "symbol": "$", 
      "conversion_rate": 1
    }, 
    {
      "iso": "CUP", 
      "symbol": "$", 
      "conversion_rate": 0.038
    }
  ], 
  "distance_to_uy": 6548.55
}
```

### Statistics resource

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

```json
{
  "longest_distance": 
  {
    "country": "Spain", 
    "value": 9693.18
  }, 
  "most_traced": 
  {
    "country": "Argentina", 
    "value": 19
  }
}
```

## Technical test comments

### Requirements

This solution is uploaded to a github repository.

I prefer to make documentation in some text editor platform like Google Docs or Google Slides besides a readme file, but because of the small size and complexity of this project I think that a readme file is enough. Also I wanted to finish it as soon as possible.

The solution is deployed in a Google App Engine instance as stated in the usage section.

### Recommendations

I used both the suggested APIs for the intended porposes. I decided to use another API as none of the suggested show the complete info requested, specifically with two attributes.  
First, related to the currencies, I used the https://restcountries.eu API as none of the suggested ones lend the full list of currencies for a country. The http://ip-api.com API displays the main currency but for countries with more than one currency it was not enough.  
Another comment with this point is that I thought it was better to show the official currencies, this meaning that I didn't add USD to the list as showed in the example response you shared with me. This applies also to the symbol, as for example the official symbol for Uruguayan pesos is $ instead of $U.  
On the other hand, I used the same API named before to get the country coordinates as stated in the exercise. The suggested APIs didn't show the country coordinates but the ip ones. I would have used those coordinates for the distance to Uruguay calculation but I respected the statement as is.  
Finally, the conversions API has a free requests limit, so this would make the high concurrency environment impossible to satisfy with the current free pricing plan.

Mainly due to the short time I was not able to make the extensive research I would have liked to do and the deployment itself, so I ended up deciding to use BigQuery as the database for this project, as I am pretty used to work with it. I don't think it is the optimal platform for storing the requests data in such high concurrency conditions but it can do a pretty good job nevertheless.

