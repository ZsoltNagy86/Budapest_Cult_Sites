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
#### Step 5
Clustering based on popularity, recommendation and rating. Marking cultural places according to cluster membership

### Data
#### Sources
<b>Budapest districts and Neighbourhoods:</b> https://en.wikipedia.org/wiki/List_of_districts_in_Budapest</br>
<b>Geospatial data:</b> https://hu.wikipedia.org/wiki/Budapest_ker%C3%BCletei</br>
<b>Venues in districts:</b> Foursquare PacesAPI, explore endpint</br>
<b>Popularity of venues:</b> Foursquare PacesAPI, details endpoint</br>

#### Features/Variables:
<b>Neighbourhood</b> 	- Neighbourhoods of Districts in Budapest</br>
<b>Neighbourhood_Latitude</b> - Latitude value of given Neighbourhood</br>
<b>Neighbourhood_Longitude</b> 	-  Longitude value of given Neighbourhood</br>
<b>Venue_ID</b> - Venue's unique ID</br>
<b>Venue</b> 	- Venue's name</br>
<b>Venue_Latitude</b> - Latitude value of given Venue</br>	
<b>Venue_Longitude</b> - Longitude value of given Venue</br>	
<b>Venue_Category</b> - type of Venue</br>
<b>likes</b> - Number of likes for given venue</br>
<b>tipCount</b> - Number of tips for given venue</br>
<b>rating</b> - Rating of venue	</br>
<b>Color</b> - Colorcode for map marker by neighbourhoods</br>
