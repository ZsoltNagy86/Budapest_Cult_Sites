#!/usr/bin/env python
# coding: utf-8

# # <span style="color:darkslategray"> Analysis of Visitors in Budapest </span>

# ### <span style="color:dimgray">Importing packages</span>

# In[1]:


# Importing general packages
import pandas as pd
import numpy as np
from dfply import *

# Importing packages for vizualization
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns

# Importing packages for scraping
#!conda install -c conda-forge wikipedia --yes 
import wikipedia
#!conda install -c conda-forge requests --yes 
import requests
#!conda install -c conda-forge bs4 --yes 
from bs4 import BeautifulSoup

# Importing packages for handling gespatial data
import getpass
#!conda install -c conda-forge geocoder --yes 
import geocoder
#!conda install -c conda-forge geopy --yes 
from geopy.geocoders import Nominatim
import folium # map rendering library

# Importing packages for standardization
from sklearn.preprocessing import MinMaxScaler

# Importing packages for clustering
from sklearn.cluster import KMeans


# ### <span style="color:dimgray">Scraping wiki page for data about Budapest's Neighbourhoods </span>

# In[2]:


html1 = requests.get('https://en.wikipedia.org/wiki/List_of_districts_in_Budapest')

#turn the HTML into a soup text object
bs1 = BeautifulSoup(html1.text, 'lxml')


# In[3]:


#Defining customized replace function
REPLACE_SEQUENCES = ['\n']

def custom_replace(s):
    for to_replace in REPLACE_SEQUENCES:
        s = s.replace(to_replace, '')
    return s.strip()

#Defining a list for the neighbourhoods 
n_list = []

#Filling the list
for i in bs1.find_all(name = 'td'):
    n_list.append(custom_replace(i.get_text()))

#Find the last element of the table of neighbourhoods in the list
matches = [i for i,x in enumerate(n_list) if x=='non-district']

#Dropping elements from the list that is not part of the original wikipedia table
n_list = n_list[0:matches[-1]]
   
#Creating DataFrame from the list
n_list = np.array(n_list)
columns=['District number','District name','Neighborhoods', 'Sights']
df_n = pd.DataFrame(np.reshape(n_list, (int(len(n_list)/4),4)),columns=columns).drop(0)
df_n


# ### <span style="color:dimgray"> Adding Lat and Long to df </span>

# In[4]:


html2 = requests.get('https://hu.wikipedia.org/wiki/Budapest_ker%C3%BCletei')

#turn the HTML into a soup text object
bs2 = BeautifulSoup(html2.text, 'lxml')


# In[5]:


# Finding the wikipedia links for Budapest districts and exrtracting them into a list
links = bs2.find("table", class_='wikitable').find_all("a", href=re.compile("/wiki/Budapest_"))

links_final = []
for lines in links:
    links_final.append('https://hu.wikipedia.org' + str(re.findall('"(.*?)"', str(lines))[0]))


# In[6]:


longitude = []
latitude = []
for links in links_final:
    html = requests.get(links)

    #turn the HTML into a soup text object
    bs = BeautifulSoup(html.text, 'lxml')

    longitude.append(bs.find("span", class_="p-longitude longitude").text)
    latitude.append(bs.find("span", class_="p-latitude latitude").text)


# In[7]:


# Adding geo data to neighbourhood dataframe
df_n['latitude'] = latitude
df_n['longitude'] = longitude
df_n


# In[19]:


# Adding credentials for using Foursquare
CLIENT_ID = getpass.getpass('Enter your Foursquare CLIENT_ID')
CLIENT_SECRET = getpass.getpass('Enter your Foursquare CLIENT_SECRET')
VERSION = '20191105'
LIMIT = 100

print('Your credentials are stored')


# In[20]:


#Definging function for using API of Foursquare
def getNearbyVenues(names, latitudes, longitudes, radius=3000):
    
    venues_list=[]
    for name, lat, lng in zip(names, latitudes, longitudes):
        #print(name)
            
        # create the API request URL
        url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
            CLIENT_ID, 
            CLIENT_SECRET, 
            VERSION, 
            lat, 
            lng, 
            radius, 
            LIMIT)
            
        # make the GET request
        results = requests.get(url).json()["response"]['groups'][0]['items']
        
        # return only relevant information for each nearby venue
        venues_list.append([(
            name, 
            lat, 
            lng,
            v['venue']['id'],
            v['venue']['name'], 
            v['venue']['location']['lat'], 
            v['venue']['location']['lng'],  
            v['venue']['categories'][0]['name']) for v in results])

    nearby_venues = pd.DataFrame([item for venue_list in venues_list for item in venue_list])
    nearby_venues.columns = ['Neighbourhood', 
                             'Neighbourhood_Latitude',
                             'Neighbourhood_Longitude',
                             'Venue_ID',
                             'Venue', 
                             'Venue_Latitude',
                             'Venue_Longitude',
                             'Venue_Category']
    
    return(nearby_venues)


# In[21]:


# Creating Df by adding vanues to df of Budapest's Neighbourhoods
df_n_ven = getNearbyVenues(df_n['Neighborhoods'], df_n['latitude'], df_n['longitude'], 1500)

len(df_n_ven)


# In[22]:


pd.options.display.max_rows = 9999
display(df_n_ven >> group_by(X.Venue_Category) >> summarize(N=n(X.Venue)))


# In[23]:


ven_cat = ['Art Gallery', 
           'Art Museum',  
           'Castle', 
           'College Arts Building', 
           'Concert Hall', 
           'Cultural Center',
           'Historic Site', 
           'History Museum', 
           'Monument / Landmark', 
           'Theater']


# In[24]:


df_n_ven = df_n_ven[df_n_ven['Venue_Category'].isin(ven_cat)]
df_n_ven = df_n_ven >> distinct(X.Venue)
len(df_n_ven)


# In[25]:


#Defining function for using API of Foursquare
def getVenuesStat(VenueID):
    
    stats_list=[]
    for ID in VenueID:
        print(ID)   
        
        # create the API request URL
        url = 'https://api.foursquare.com/v2/venues/{}?&client_id={}&client_secret={}&v={}'.format(
            ID, 
            CLIENT_ID, 
            CLIENT_SECRET, 
            VERSION)
        print(url)    
        # make the GET request
        results = requests.get(url).json()["response"]['venue']
        
        #Checking whether fields are in JSON and initializing base value      
        likes = []
        stats =[]
        rating = []
        
        if 'likes' in results:
            likes = results['likes']['count']
        else:
            likes = np.nan
        if 'stats' in results:
            stats = results['stats']['tipCount']
        else:
            stats = np.nan
        if 'rating' in results:
            rating = results['rating']
        else:
            rating = np.nan
        
        # return only relevant information for each venue
        stats_list.append([
            ID,
            likes,
            stats,
            rating])
        
        
    #venues_stat = pd.DataFrame([item for stats_list in stats_list for item in stats_list])
    columns = ['Venue_ID', 'likes', 'tipCount', 'rating']
    venues_stat = pd.DataFrame(stats_list, columns=columns)
    
    return(venues_stat)


# In[26]:


df_n_ven_stat = getVenuesStat(df_n_ven['Venue_ID'])


# In[27]:


df_n_ven = df_n_ven.reset_index(drop=True)
df_cult_ven = df_n_ven >> inner_join(df_n_ven_stat, by="Venue_ID")
df_cult_ven >> arrange(X.likes, ascending=False)


# In[28]:


df_cultven_stat = df_cult_ven >> group_by(X.Venue_Category) >> summarize(mean_likes = mean(X.likes), mean_tip = mean(X.tipCount), mean_rating = mean(X.rating)) 
df_cultven_stat = df_cultven_stat.sort_values(['mean_likes'], ascending=False).reset_index(drop=True)
sns.set(style="whitegrid")
plt.figure(figsize=(15,12))
ax = sns.barplot(x="Venue_Category", y="mean_likes", data=df_cultven_stat, palette="Blues_d")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)


# In[29]:


df_cultven_stat = df_cultven_stat.sort_values(['mean_tip'], ascending=False).reset_index(drop=True)
sns.set(style="whitegrid")
plt.figure(figsize=(15,12))
ax = sns.barplot(x="Venue_Category", y="mean_tip", data=df_cultven_stat, palette="Reds_d")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)


# In[30]:


df_cultven_stat = df_cultven_stat.sort_values(['mean_rating'], ascending=False).reset_index(drop=True)
sns.set(style="whitegrid")
plt.figure(figsize=(15,12))
ax = sns.barplot(x="Venue_Category", y="mean_rating", data=df_cultven_stat, palette="Greens_d")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)


# In[31]:


pd.options.display.max_colwidth = 2000
# Grouping by Neighbourhoods
df_neigh = df_cult_ven >> group_by(X.Neighbourhood) >> summarize(n=n(X.Venue_ID)) 
df_neigh.sort_values(by=['n'], ascending=False)


# In[33]:


color_theme = {
    'Buda Castle, Tabán, Gellérthegy, Krisztinaváros, southern Víziváros': 'red',
    'Terézváros': 'blue',
    'Adyliget, Budakeszierdő, Budaliget, Csatárka, Erzsébetliget, Erzsébettelek, Felhévíz, Gercse, Hársakalja, Hárshegy, Hűvösvölgy, Kővár, Kurucles, Lipótmező, Máriaremete, Nyék, Országút, Pálvölgy, Pasarét, Pesthidegkút-Ófalu, Petneházy-rét, Remetekertváros, Rézmál, Rózsadomb, Szemlőhegy, Széphalom, Szépilona, Szépvölgy, Törökvész, Újlak, Vérhalom, northern Víziváros, Zöldmál.': 'green',
    'Ferencváros, Gubacsidűlő, József Attila-lakótelep': 'orange', 
    'Újpest, Megyer, Káposztásmegyer, Székesdűlő, Istvántelek.': 'darkred',
    'Óbuda, Aquincum, Aranyhegy, Békásmegyer, Csillaghegy, Csúcshegy, Filatorigát, Hármashatár-hegy, Kaszásdűlő, Mátyáshegy, Mocsárosdűlő, Óbudai-sziget, Remetehegy, Rómaifürdő, Solymárvölgy, Szépvölgy, Táborhegy, Testvérhegy, Törökkő, Ürömhegy, Újlak.': 'gray', 
    'Rákospalota, Pestújhely, Újpalota': 'purple', 
    'Albertfalva, Dobogó, Gazdagrét, Gellérthegy, Hosszúrét, Kamaraerdő, Kelenföld, Kelenvölgy, Kőérberek, Lágymányos, Madárhegy, Őrmező, Örsöd, Péterhegy, Pösingermajor, Sasad, Sashegy, Spanyolrét, Tabán': 'darkpurple', 
    'Alsórákos, Herminamező, Istvánmező, Kiszugló, Nagyzugló, Rákosfalva, Törökőr, City Park': 'lightgray', 
    'Budatétény, Nagytétény, Budafok': 'black',
    'Budakeszierdő, Csillebérc, Farkasrét, Farkasvölgy, Istenhegy, Jánoshegy, Kissvábhegy, Krisztinaváros, Kútvölgy, Magasút, Mártonhegy, Németvölgy, Orbánhegy, Sashegy, Svábhegy, Széchenyihegy, Virányos.': 'lightblue',
    'Felsőrákos, Gyárdűlő, Keresztúridűlő, Kőbánya-Kertváros': 'beige', 
    'Inner City, Lipótváros': 'pink',
    'Erzsébetváros': 'black',
    'Józsefváros, Kerepesdűlő, Tisztviselőtelep': 'darkred', 
    'Mátyásföld, Sashalom, Cinkota, Rákosszentmihály, Árpádföld, Kisszentmihály, Ilonatelep, Petőfikert, Nagyiccetelep, Szentgyörgytelep, Szabadságtelep, Huszkatelep': 'darkgreen', 
    'Rákoskeresztúr, Rákoscsaba, Rákoscsaba-Újtelep, Rákosliget, Rákoshegy, Rákoskert, Akadémiaújtelep, Madárdomb, Régiakadémiatelep': 'lightred', 
    'Újlipótváros, Angyalföld, Vizafogó, Népsziget, Göncz Árpád városközpont': 'cadetblue'}

color_dict = pd.DataFrame.from_dict(color_theme, orient='index')
color_dict = color_dict.reset_index()
color_dict = color_dict.rename(columns={"index": "Neighbourhood", 0: "Color"})

df_cult_ven = df_cult_ven.reset_index(drop=True)
#df_cult_ven = df_cult_ven >> drop(X.Color)
df_cult_ven = df_cult_ven >> left_join(color_dict, by='Neighbourhood')
df_cult_ven['Color'] = df_cult_ven['Color'].fillna('lightgray')
df_cult_ven


# In[34]:


m = folium.Map(
    location=[47.498333, 19.040833],
    zoom_start=12
)

for lat, long, name, color in zip(df_cult_ven['Venue_Latitude'],
                                           df_cult_ven['Venue_Longitude'],
                                           df_cult_ven['Venue'],
                                           df_cult_ven['Color']):
    
    folium.Marker(
        location=[lat, long],
        popup=name,
        icon=folium.Icon(color=color)
    ).add_to(m)

m


# In[35]:


# K-means clusters to find segments of cultural sights of Budapest

# Creating dataframe for clustering 
df_clust = df_cult_ven >> select(X.likes, X.tipCount, X.rating)
df_clust = df_clust.fillna(np.nanmedian(df_clust['rating']))
df_columns = df_clust.columns

# Standardizing data to ensure that unit of dimension does not distort relative near-ness of observations
mms = MinMaxScaler()
df_clust = mms.fit_transform(df_clust)
df_clust = pd.DataFrame(df_clust, columns=df_columns)

# Running K-means clusters
clusters_range = [2,3,4,5,6,7,8,9,10,11,12,13,14]
inertias =[] 
for c in clusters_range:
    kmeans = KMeans(n_clusters=c, random_state=0).fit(df_clust)
    inertias.append(kmeans.inertia_)
plt.figure()
plt.plot(clusters_range,inertias, marker='o')


# In[36]:


# Running K-means cluster on the encoded dataframe with 3 clusters based on elbow method
kmens = KMeans(n_clusters=4, random_state=0).fit(df_clust)

# Adding cluster variable to dataframe df_cult_ven
df_cult_ven['Clusters'] = kmens.labels_

# Investigating the cluster characterestics
df_cult_ven >> group_by(X.Clusters) >> summarize(mean_likes=mean(X.likes), mean_tipCount=mean(X.tipCount), mean_rating=mean(X.rating))


# <b>Cluster1</b>: Rarely liked places with low recommendation and rating <br/>
# <b>Cluster2</b>: Frequently liked places with high reccomendation and rating <br/>
# <b>Cluster3</b>: Most frequently liked places with very high recommendation and rating <br/>
# <b>Cluster4</b>: Less frequently liked places with low number of recommendation but fairly good rating <br/>

# In[39]:


#Adding cluster color to df
color_theme_clust = {'gray': 0,
                     'blue': 1,
                     'red': 2,
                     'green': 3}


color_dict_clast = pd.DataFrame.from_dict(color_theme_clust, orient='index')
color_dict_clast = color_dict_clast.reset_index()
color_dict_clast = color_dict_clast.rename(columns={"index": "Cluster_Colors", 0: "Clusters"})
color_dict_clast

df_cult_ven = df_cult_ven.reset_index(drop=True)
#df_cult_ven = df_cult_ven >> drop(X.Cluster_Colors)
df_cult_ven = df_cult_ven >> left_join(color_dict_clast, by='Clusters')
df_cult_ven            
                 


# In[40]:


# Marking sights by cluster membership

m = folium.Map(
    location=[47.498333, 19.040833],
    zoom_start=12
)

for lat, long, name, color in zip(df_cult_ven['Venue_Latitude'],
                                           df_cult_ven['Venue_Longitude'],
                                           df_cult_ven['Venue'],
                                           df_cult_ven['Cluster_Colors']):
    
    folium.Marker(
        location=[lat, long],
        popup=name,
        icon=folium.Icon(color=color)
    ).add_to(m)

m


# In[ ]:





# In[ ]:




