# Budapest_Cult_Sites
 Analysing Foursquare data of cultural sights in Budapest

## Business problem/Introduction (fictional)
### Commissioned by: 
Central Government of Capital City, Budapest
### Need Assessment:
In connection with the new cultural policy directives, the study aims at the investigation of cultural sights in Budapest. For the more efficient usage of development resources, it is necessary to have an insight into the popularity of cultural sights and institutions in Budapest. With that resources detailed plans can be set: 
1. Identifying the most freqently visited categories/areas/places for maintaining high quality services
2. Identifying frequently visited places for rising awareness even further
3. Understanding the reasons why certain places are rarely visited

### Analytical plan
#### Step 1 
Scraping wikipedia to create dataframe about District, Neighbourhoods and geolocations of Budapest
#### Step 2 
By using Foursquare API (PacesAPI, explore endpint), adding venues located in the district of Budapest
#### Step 3 
By using Foursquare API (PacesAPI, details endpoint), it can be investigated how popular and recommended certain cultural venues are and what are their 
#### Step 4 
Marking cultural sights on the map of Budapest by neighbourhoods, adding labels with their names

