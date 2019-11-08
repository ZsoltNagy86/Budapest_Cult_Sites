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
<b>Venue_Category</b> - type of Venue: Art Gallery, Art Museum, Castle, College Arts Building, Concert Hall, Cultural Center,     Historic Site, History Museum, Monument / Landmark, Theater</br>
<b>likes</b> - Number of likes for given venue</br>
<b>tipCount</b> - Number of tips for given venue</br>
<b>rating</b> - Rating of venue	</br>
<b>Color</b> - Colorcode for map marker by neighbourhoods</br>

### Methodology
#### Bivariate analysis
After scraping wikipedia pages for information about districts and neighbourhoods, geospatial data of districts in Budapest was added to the dataframe.<br/> 
Using Foursquare data to find venues in Budapest made it possible to enrich the data. On that data a filter was applied in order to find cultural sights in the capitol city. 
The main dataframe was created by adding additional fields to that dataframe, that contained the number of likes, tips and average ratings coming from visitors using Foursquare. <br/>
Bivariate analysis was applied to see the distribution of likes, tips and average ratings by types of cultural sights. 
Types of vanues were marked on the map of Budapest using Folium package. Names of vanues were also available.
Finally, cluster analysis was run to see how cutural sights are segmented based on popularity (using likes, tips and rating fields).

### Results
Starting with the bivariate analysis, the charts about the average likes, tips and ratings by the types of cultural sights are the following:<br/>
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
In general, it can be seen likes, tips and ratings are more or less interconnected. Having high value in one dimension makes likely to get high average value on the other dimensions as well. Also interesting that the Castle of Budapest is the most frequently liked sights, and it is highly rated and widely recommended as wel. On the contrary, Landmarks/monuments, art galleries and the History Museum got little attention (low average likes and tips) and rating. Based on that analysis, we can anticipate that we can find clusters with fairly distinct characteristics. <br/>
After that sights were marked on the map of Budapest by neighbourhoods showing that Buda Castle, Inner City and Terézváros are the neighbourhoods where most of the cultural institutions are situated. Also, cultural sihgts are often close to each other constituted a block (e.g. neighbourhood of Ferencváros, Gubacsidűlő, József Attila-lakótelep or Buda Castle). That makes the channelling of development resources easier. <br/>
<br/>Find the map in the notebook:<br/>
https://github.com/ZsoltNagy86/Budapest_Cult_Sites/blob/master/Code/Budapest_Cult_Sights.ipynb
<br/>Finally, the cluster analysis showed that there are four distinctive clusters when it comes to segment cultural sights by popularity.<br/>
<b>Cluster1</b>: Rarely liked places with low recommendation and rating <br/>
<b>Cluster2</b>: Frequently liked places with high reccomendation and rating <br/>
<b>Cluster3</b>: Most frequently liked places with very high recommendation and rating <br/>
<b>Cluster4</b>: Less frequently liked places with low number of recommendation but fairly good rating <br/>
<br/>The cultural venues marked again on the map of Budapest, this time based on the cluster membership. The map can be found in the Notebook:<br/>
https://github.com/ZsoltNagy86/Budapest_Cult_Sites/blob/master/Code/Budapest_Cult_Sights.ipynb
<br/> Not surprisingly, the less frequently visited places were situated far from the city centre, while places from the other three clusters condensed close to the centre of Buda and Pest. Some sights from cluster 4 also fall far from the city centre, that may be the interest of another analysis that aims at how these places could attract more visitors than those that belonged to Cluster 1.<br/>

### Discussion
#### Recommendations regarding channelling developmental resources
1. Considering the volume of visits and recommendations, it is crucial to provide enough resources for upkeeping high level of services at cultural sights belongs to Cluster 3 (Castle, Halászbástya).<br/>
2. Since most of the cultural sights situated in the inner city of Pest and Buda, concentrating on these areas is important, that should cover maintainance of roads, renovation/conservation of historic building and providing welcoming environment (tidy and clean places) should be a priority.<br/>
3. Distant institutions, places and sights get little attention. Public transportation and advertisement should be improved to connect these places to the centre making them benefit better from tourism. In that regard, sights from cluster 4 falling far from the city centre could be the centre of interest to find out there potential in attracting some attention. <br/>
#### Recommendations regarding future analysis
1. Adding data coming from other services beside Foursquare would be important to balance, contrast and compare the results regarding popularity. Also, official data about the number of visitors would be a great addition to the analysis.<br/>
2. Validating that venues belongs to the given neighbourhood and clusters should be recognized as being of paramount importance.<br/>
3. Adding traffic data may explain some assumption of the analysis, especially in connection with the access to the less frequently liked and recommended places. <br/>
### Conclusion 
The analysis aimed at investigating popularity, recommendation and rating of cultural sites in Budapest in order to have better understanding of how development resources should be channelled by the capitol city's government to fulfill the goals of the new cultural policy. The data coming from Foursquare shed light on the following strategies seems feasible:
1. Concentrating maintaining high level services at most frequently visited places
2. Aiming resources on those areas where the concentration of cultural places high (Inner city)
3. Connect distant places to the centre by improving public transportation and information provided.
