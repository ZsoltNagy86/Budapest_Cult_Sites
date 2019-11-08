 # Analysing popularity of cultural sights and places of Budapest
 

## Business problem/Introduction (fictional)
### Commissioned by: 
Central Government of Capital City, Budapest

### Background/Need Assessment:
In connection with the new cultural policy directives, the study aims at the investigation of popularity of cultural sights in Budapest. Considering the scarse resources, local government could better allocate resources if it gets an insight into how cultural sights are segmented regarding popularity. With that, detailed plans can be set: 
1. Identifying the most freqently visited categories/areas/places for maintaining high quality services, like roads, info points, the condition of buildings, etc.
2. Identifying frequently visited places for rising awareness of tourists and locals with media campaigns to raise visits even further
3. Understanding the reasons why certain places are rarely visited
4. Understanding how popularity of cultural sights are linked to their geospatial places

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

### Methodology
#### Univariate analysis
After scraping wikipedia pages for information about districts and neighbourhoods, geospatial data of districts in Budapest was added to the dataframe. 
Using Foursquare data to find venues in Budapest made it possible to enrich the data. On that data a filter was applied in order to find cultural sights in the capitol. 
The main dataframe was created by adding additional fields to that dataframe, that contained the number of likes, tips and average ratings coming from visitors using Foursquare. 
The charts about the average likes, tips and ratings by the types of cultural sights are the following:<br/>
<br/>Likes by Types of Cultural Sights: <br/>
<p align="center">
  <img src="https://github.com/ZsoltNagy86/Budapest_Cult_Sites/blob/master/Charts/likes_by_cat.png" width="450" title="Likes by Types of Cultural Sights">
</p>
<br/>Tips by Types of Cultural Sights: <br/>
<p align="center">
  <img src="https://github.com/ZsoltNagy86/Budapest_Cult_Sites/blob/master/Charts/tips_by_cat.png" width="450" title="Tips by Types of Cultural Sights">
</p>
<br/>Ratings by Types of Cultural Sights: <br/>
<p align="center">
  <img src="https://github.com/ZsoltNagy86/Budapest_Cult_Sites/blob/master/Charts/rating_by_cat.png" width="450" title="Ratings by Types of Cultural Sights">
</p>
