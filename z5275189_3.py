#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 15:53:09 2020

@author: z5275189
"""

import pandas as pd  
import scipy.stats
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import ast
import csv
from sklearn.neighbors import KNeighborsClassifier
import sys
from sklearn.metrics import precision_score, accuracy_score, recall_score

training  = sys.argv[1]
validation  = sys.argv[2]

df = pd.read_csv(training)
df1= df.copy()
df = df.fillna(method='ffill')
df.isnull().any()
df = df.drop_duplicates()

df['cast'] = df['cast'].apply(ast.literal_eval)
new_df = pd.concat({k:pd.DataFrame(v) for k, v in df['cast'].items()})
df = df.join(new_df.reset_index(level=1, drop=False)).reset_index(drop=False)
df = df.sort_values('character',ascending=True)
df=df.groupby('movie_id')['character'].apply(lambda tags: ','.join(tags))
df = df1.merge(df.to_frame(), left_on='movie_id', right_index=True)
df2 = df.copy()

df['genres'] = df['genres'].apply(ast.literal_eval)
new_df = pd.concat({k:pd.DataFrame(v) for k, v in df['genres'].items()})
df = df.join(new_df.reset_index(level=1, drop=False)).reset_index(drop=False)
df = df.sort_values('name',ascending=True)
df=df.groupby('movie_id')['name'].apply(lambda tags: ','.join(tags))
df = df2.merge(df.to_frame(), left_on='movie_id', right_index=True)

df['charac_count'] = df.character.str.count(',') + 1
df['genres_count'] = df.name.str.count(',') + 1
del df['name']
del df['character']
df3= df.copy()

df['release_date'] = pd.to_datetime(df['release_date'])
df['day_of_week'] = df['release_date'].dt.day_name()
df['Month'] = pd.to_datetime(df.release_date, format='%d/%m/%Y').dt.month_name()
df['year'] = pd.DatetimeIndex(df['release_date']).year

df['production_companies'] = df['production_companies'].fillna('[]').apply(ast.literal_eval).apply(lambda x:[i['name'] for i in x]if isinstance(x,list)else[])
df['company_count'] = df['production_companies'].map(len)

df['spoken_languages'] = df['spoken_languages'].fillna('[]').apply(ast.literal_eval).apply(lambda x:[i['name'] for i in x]if isinstance(x,list)else[])
df['lang_count'] = df['spoken_languages'].map(len)

df['keywords'] = df['keywords'].fillna('[]').apply(ast.literal_eval).apply(lambda x:[i['name'] for i in x]if isinstance(x,list)else[])
df['key_count'] = df['keywords'].map(len)

df['crew_n'] = df['crew'].fillna('[]').apply(ast.literal_eval).apply(lambda x:[i['name'] for i in x]if isinstance(x,list)else[])
df['crew_count'] = df['crew_n'].map(len)

df['production_countries'] = df['production_countries'].fillna('[]').apply(ast.literal_eval).apply(lambda x:[i['name'] for i in x]if isinstance(x,list)else[])
df['country_count'] = df['production_countries'].map(len)

df['overview_count'] = df['overview'].str.count(" ") + 1
df['homepage_count'] = df['homepage'].str.len()
df['homepage_count'] = df['homepage_count'].fillna(0)

vdf = pd.read_csv(validation)
vdf1= vdf.copy()
vdf = vdf.fillna(method='ffill')
vdf.isnull().any()
vdf = vdf.drop_duplicates()

vdf['cast'] = vdf['cast'].apply(ast.literal_eval)
new_df = pd.concat({k:pd.DataFrame(v) for k, v in vdf['cast'].items()})
vdf = vdf.join(new_df.reset_index(level=1, drop=False)).reset_index(drop=False)
vdf = vdf.sort_values('character',ascending=True)
vdf=vdf.groupby('movie_id')['character'].apply(lambda tags: ','.join(tags))
vdf = vdf1.merge(vdf.to_frame(), left_on='movie_id', right_index=True)
vdf2 = vdf.copy()

vdf['genres'] = vdf['genres'].apply(ast.literal_eval)
new_df = pd.concat({k:pd.DataFrame(v) for k, v in vdf['genres'].items()})
vdf = vdf.join(new_df.reset_index(level=1, drop=False)).reset_index(drop=False)
vdf = vdf.sort_values('name',ascending=True)
vdf=vdf.groupby('movie_id')['name'].apply(lambda tags: ','.join(tags))
vdf = vdf2.merge(vdf.to_frame(), left_on='movie_id', right_index=True)

vdf['charac_count'] = vdf.character.str.count(',') + 1
vdf['genres_count'] = vdf.name.str.count(',') + 1
del vdf['name']
del vdf['character']
vdf3= vdf.copy()

vdf['release_date'] = pd.to_datetime(vdf['release_date'])
vdf['day_of_week'] = vdf['release_date'].dt.day_name()
vdf['Month'] = pd.to_datetime(vdf.release_date, format='%d/%m/%Y').dt.month_name()
vdf['year'] = pd.DatetimeIndex(vdf['release_date']).year

vdf['production_companies'] = vdf['production_companies'].fillna('[]').apply(ast.literal_eval).apply(lambda x:[i['name'] for i in x]if isinstance(x,list)else[])
vdf['company_count'] = vdf['production_companies'].map(len)

vdf['spoken_languages'] = vdf['spoken_languages'].fillna('[]').apply(ast.literal_eval).apply(lambda x:[i['name'] for i in x]if isinstance(x,list)else[])
vdf['lang_count'] = vdf['spoken_languages'].map(len)

vdf['keywords'] = vdf['keywords'].fillna('[]').apply(ast.literal_eval).apply(lambda x:[i['name'] for i in x]if isinstance(x,list)else[])
vdf['key_count'] = vdf['keywords'].map(len)

vdf['crew'] = vdf['crew'].fillna('[]').apply(ast.literal_eval).apply(lambda x:[i['name'] for i in x]if isinstance(x,list)else[])
vdf['crew_count'] = vdf['crew'].map(len)

vdf['production_countries'] = vdf['production_countries'].fillna('[]').apply(ast.literal_eval).apply(lambda x:[i['name'] for i in x]if isinstance(x,list)else[])
vdf['country_count'] = vdf['production_countries'].map(len)

vdf['overview_count'] = vdf['overview'].str.count(" ") + 1
vdf['homepage_count'] = vdf['homepage'].str.len()
vdf['homepage_count'] = vdf['homepage_count'].fillna(0)

vmovie = vdf.movie_id

#######regression#################

X_train=df[['genres_count', 'charac_count', 'runtime','budget'   , 'Month', 'lang_count' ,'key_count' ,'country_count','overview_count','homepage_count' , 'crew_count' ,'year']]
y_train=df['revenue'].values

X_train["Month"].replace({"January": 1, "February": 2 , "March": 3,"April": 4,"May": 5,"June": 6,"July": 7,"August": 8,"September": 9,"October": 10,"November": 11,"December": 12}, inplace=True)

X_test=vdf[['genres_count', 'charac_count', 'runtime', 'budget'   , 'Month', 'lang_count' ,'key_count' ,'country_count','overview_count','homepage_count' , 'crew_count' , 'year']]
y_test=vdf['revenue'].values

X_test["Month"].replace({"January": 1, "February": 2 , "March": 3,"April": 4,"May": 5,"June": 6,"July": 7,"August": 8,"September": 9,"October": 10,"November": 11,"December": 12}, inplace=True)

regressor = LinearRegression()  
regressor.fit(X_train, y_train)

y_pred = regressor.predict(X_test)

#for i in range(len(y_test)):
#        print("Expected:", y_test[i], "Predicted:", y_pred[i])
        
coeff = scipy.stats.pearsonr(y_pred, y_test)
coeff = round(coeff[0], 2)
#print("Coeff is: " , coeff)

mean = metrics.mean_squared_error(y_test, y_pred)
#print('Mean Squared Error:',mean )   

with open('z5275189.PART1.output.csv', 'w', newline='') as file1o:
        writer = csv.writer(file1o)
        writer.writerow(["Movie_id", "Predicted_Revenue"])
        for i in range(len(y_test)):
            writer.writerow([vmovie[i], y_pred[i]])  
            
with open('z5275189.PART1.summary.csv', 'w', newline='') as file1s:
        writer = csv.writer(file1s)
        writer.writerow(["zid", "MSR" , "correlation"])
        writer.writerow(["z5275189"  , mean,coeff])            

#########classification###########

X_trainc=df[['genres_count', 'charac_count', 'runtime', 'budget' ,'company_count' , 'lang_count'  , 'crew_count' ]]
y_trainc= df['rating'].values

X_testc=vdf[['genres_count', 'charac_count', 'runtime', 'budget'  ,'company_count' , 'lang_count'  , 'crew_count' ]]
y_testc= vdf['rating'].values

knn = KNeighborsClassifier()
knn.fit(X_trainc, y_trainc)
predictions = knn.predict(X_testc)

#for i in range(len(y_testc)):
#        print("Expected:", y_testc[i], "Predicted:", predictions[i])

accuracy = accuracy_score(y_testc, predictions)
accuracy = round(accuracy, 2)
#print("accuracy:\t",accuracy )

precision = precision_score(y_testc, predictions, average='macro')
precision = round(precision, 2)
#print("precision:\t",precision )

recall = recall_score(y_testc, predictions, average='macro')
recall = round(recall, 2)
#print("recall:\t\t",recall )

with open('z5275189.PART2.output.csv', 'w', newline='') as file2o:
        writer = csv.writer(file2o)
        writer.writerow(["Movie_id", "Predicted_Rating"])
        for i in range(len(y_testc)):
            writer.writerow([ vmovie[i], predictions[i]])            
            
with open('z5275189.PART2.summary.csv', 'w', newline='') as file2s:
        writer = csv.writer(file2s)
        writer.writerow(["zid","average_precision","average_recall","accuracy"])
        writer.writerow(["z5275189",precision, recall,accuracy])            