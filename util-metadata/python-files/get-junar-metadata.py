
# coding: utf-8

# In[ ]:

#import required libraries
import requests
import gviz_api


# In[ ]:

#connect to sac county junar open data api, get list of datasets and associated metadata
r=requests.get('http://saccounty.cloudapi.junar.com/api/v2/datasets/?auth_key=781c9953a9165b9e89202094331946fea36b329f&format=json')


# In[ ]:

r #check for response 200


# In[ ]:

r.json() #sneek peek at what the json version looks like


# In[ ]:

var=r.json() #assign "json-ified" data to a variable named var


# In[ ]:

#take a arbitrary element of var, print it to see what it looks like
for x in var[1]:
    print x, ": ",var[1][x]


# In[ ]:

jjlarray=[] #initialize empty list to hold results

#loop through all datasets and put the titles into the array
#datasets will be ordered the same way as they appear on the website
for x in var:
    print x['title']
    jjlarray.append(x['title'])


# In[ ]:

jjlarray.sort() #sort the array


# In[ ]:

for x in jjlarray: print x #one liner to print the dataset titles in alphabetical order, not pythonic

