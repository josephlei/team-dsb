
# coding: utf-8

# Outstanding issues:
# * remove inspection "NA" rows

# In[ ]:

import csv
import re
import pandas as pd
import numpy as np
pd.__version__


# In[ ]:

raw=pd.read_csv('raw_data.csv')
raw #peek


# In[ ]:

biz=raw.drop(['Report ID','Inspection Type','Last Inspection Date','Data Last Updated','Result'],1) #drop un-needed cols
biz.Coordinates.replace(" ","", regex=True, inplace=True) #drop all non-numbers from phone
coords=biz.Coordinates.str.split(',', expand=True) #pull off coords
biz=pd.concat([biz, coords], axis=1) #add back coords
biz.rename(columns={'Facility ID':'business_id','Facility Name':'name','Address':'address','City':'city',
                    'Zip':'postal_code','Phone':'phone_number',0:'latitude', 1:'longitude'},inplace=True)
#rename to match specs
biz.insert(4,'state','CA') #add col for state
biz=biz.drop(['Coordinates'],1) #drop original coordinates


# In[ ]:

print type(biz.phone_number[0]) #peek, these are strings


# In[ ]:

biz.phone_number.replace("\D","", regex=True, inplace=True) #drop all non-numbers from phone


# In[ ]:

biz['phone_number'] = "+1" + biz['phone_number'] #add country prefix to all phone numbers


# In[ ]:

biz


# In[ ]:

print "n before dedup:", len(biz.index)
biz.drop_duplicates(subset='business_id', inplace=True)
print "n after dedup:", len(biz.index)


# In[ ]:

#biz['lat'], biz['long'] = zip(*biz['Coordinates'].str.split().tolist())

#df["flips"], df["row_name"] = zip(*df["row"].str.split().tolist())
#del df["row"]  


# In[ ]:

#pd.DataFrame(biz.Coordinates.str.split(',').tolist(), columns=['lat','long'])
#pd.DataFrame(df.row.str.split(' ',1).tolist(), columns = ['flips','row'])


# In[ ]:

biz


# In[ ]:

biz.to_csv('businesses.csv', index=False)


# In[ ]:

#df1['Coordinates'].str.split(',')
#type(df1['Coordinates'].str.split(',')) #iam series


# In[ ]:

insp=raw.drop(['Facility Name', 'Address','City', 'Zip', 'Phone', 'Report ID', 'Coordinates','Data Last Updated'],1)
insp.rename(columns={'Facility ID':'business_id','Result':'result', 'Last Inspection Date':'date', 'Inspection Type': 'type'},inplace=True)
insp=insp[['business_id','date','result','type']] #cheater re-order


# In[ ]:

insp #peek at results


# In[ ]:

print insp.result.unique() #peek
print insp.type.unique() #peek


# In[ ]:

insp.result.replace(['GN','YW','RD'],['Pass','Cond','Fail'], inplace='yes')
insp.type.replace(['ROUTINE INSPECTION', 'REINSPECTION','ADMINISTRATIVE HEARING CLOSURE', 'B- FOLLOW-UP', 'N- NOT APPLICABLE','INITIAL/PERMIT INSPECTION'],
                  ['routine'           , 'followup'    ,'followup'                      , 'followup'    , 'NA'               ,'routine'],inplace='yes')

#need to find a way to delete na, insignificant


# In[ ]:

print insp.result.unique() #peek
print insp.type.unique() #peek


# In[ ]:

insp.date=pd.to_datetime(insp.date) #convert column to datetime dtype
insp.date=insp.date.map(lambda x: x.strftime('%Y%m%d')) #change to YYYYMMDD format per YELP LIVES spec


# In[ ]:

insp


# In[ ]:

insp.to_csv('inspections.csv', index=False)


# #####START OF feed_info.csv section!

# In[ ]:

feed=raw[[11]].drop_duplicates() #take only feed date, unique (always all the same)


# In[ ]:

feed.rename(columns={'Data Last Updated': 'feed_date'},inplace=True)


# In[ ]:

feed.insert(1,'feed_version','2.0')
feed.insert(2,'municipality_name','Sacramento County')
feed.insert(3,'municipality_url','https://emdinspections.saccounty.net/food.aspx')
feed.insert(4,'contact_email','EMDinfo@Saccounty.net')


# In[ ]:

feed.feed_date=pd.to_datetime(feed.feed_date) #convert column to datetime dtype


# In[ ]:

#df2.date=df2.date.map(lambda x: x.strftime('%Y%m%d'))
feed.feed_date=feed.feed_date.map(lambda x: x.strftime('%Y%m%d')) #change to YYYYMMDD format per YELP LIVES spec


# In[ ]:

feed #look at it before exporting


# In[ ]:

feed.to_csv('feed_info.csv', index=False) #export it


# In[ ]:

wget=raw.drop(['Facility Name', 'Address','City', 'Zip', 'Result', 'Phone', 'Coordinates','Data Last Updated', 'Inspection Type'],1)
wget.rename(columns={'Facility ID':'id', 'Report ID':'report_id', 'Last Inspection Date':'date'},inplace=True)
wget.to_csv('wget.csv', index=True)

