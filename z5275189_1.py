# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 17:21:06 2020

@author: Anjali Unni
"""

import ast
import json
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
import ast

studentid = os.path.basename(sys.modules[__name__].__file__)


#################################################
# Your personal methods can be here ...
#################################################


def log(question, output_df, other):
    print("--------------- {}----------------".format(question))
    if other is not None:
        print(question, other)
    if output_df is not None:
        print(output_df.head(5).to_string())


def question_1(movies, credits):
    """
    :param movies: the path for the movie.csv file
    :param credits: the path for the credits.csv file
    :return: df1
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    
    movies=pd.read_csv("movies.csv")
    credits=pd.read_csv("credits.csv")
    df1 = pd.merge(movies, credits, how="inner", on="id")
    df1
    #################################################

    log("QUESTION 1", output_df=df1, other=df1.shape)
    return df1


def question_2(df1):
    """
    :param df1: the dataframe created in question 1
    :return: df2
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    
    df2=df1[['id', 'title', 'popularity', 'cast', 'crew', 'budget', 'genres', 'original_language', 'production_companies', 'production_countries', 'release_date', 'revenue', 'runtime', 'spoken_languages', 'vote_average', 'vote_count']]
    df2
    #################################################

    log("QUESTION 2", output_df=df2, other=(len(df2.columns), sorted(df2.columns)))
    return df2


def question_3(df2):
    """
    :param df2: the dataframe created in question 2
    :return: df3
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    
    df3 = df2.set_index('id')
    df3
    #################################################

    log("QUESTION 3", output_df=df3, other=df3.index.name)
    return df3


def question_4(df3):
    """
    :param df3: the dataframe created in question 3
    :return: df4
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    
    df4 = df3.drop(df3[df3.budget == 0].index)
    df4
    #################################################

    log("QUESTION 4", output_df=df4, other=(df4['budget'].min(), df4['budget'].max(), df4['budget'].mean()))
    return df4


def question_5(df4):
    """
    :param df4: the dataframe created in question 4
    :return: df5
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    
    success_impact_temp = df4['revenue'] - df4['budget']
    df5=df4.copy()
    df5['success_impact'] = success_impact_temp / df5['budget']
    df5
    #################################################

    log("QUESTION 5", output_df=df5,
        other=(df5['success_impact'].min(), df5['success_impact'].max(), df5['success_impact'].mean()))
    return df5


def question_6(df5):
    """
    :param df5: the dataframe created in question 5
    :return: df6
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    
    df6=df5.copy()
    df6['popularity']=((df6['popularity']-df6['popularity'].min())/(df6['popularity'].max()-df6['popularity'].min()))*100
    df6
    #################################################

    log("QUESTION 6", output_df=df6, other=(df6['popularity'].min(), df6['popularity'].max(), df6['popularity'].mean()))
    return df6


def question_7(df6):
    """
    :param df6: the dataframe created in question 6
    :return: df7
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    
    df7=df6.copy()
    df7['popularity']=df7.popularity.astype('int64')
    df7
    #################################################

    log("QUESTION 7", output_df=df7, other=df7['popularity'].dtype)
    return df7


def question_8(df7):
    """
    :param df7: the dataframe created in question 7
    :return: df8
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    
    
    df8=df7.copy()
    df7d=df7.copy()
    df8['cast'] = df8['cast'].apply(ast.literal_eval)
    new_df = pd.concat({k:pd.DataFrame(v) for k, v in df8['cast'].items()})
    df8 = df8.join(new_df.reset_index(level=1, drop=False)).reset_index(drop=False)
    df8 = df8.sort_values('character',ascending=True)
    df8=df8.groupby('title')['character'].apply(lambda tags: ','.join(tags))
    df8 = pd.merge(df7, df8, how="inner", on="title")
    df8=df8[[ 'title', 'popularity',  'crew', 'budget', 'genres', 'original_language', 'production_companies', 'production_countries', 'release_date', 'revenue', 'runtime', 'spoken_languages', 'vote_average', 'vote_count' , 'success_impact' , 'character']]
    df7d['id'] = df7.index
    df8a=df8.merge(df7d, how='inner')
    df8a=df8a.set_index('id')
    df8=df8a.copy()
    df8
    #################################################

    log("QUESTION 8", output_df=df8, other=df8["cast"].head(10).values)
    return df8


def question_9(df8):
    """
    :param df9: the dataframe created in question 8
    :return: movies
            Data Type: List of strings (movie titles)
            Please read the assignment specs to know how to create the output
    """

    #################################################
    # Your code goes here ...
    
    df9=df7.copy()
    df9['cast'] = df9['cast'].apply(ast.literal_eval)
    new_df1 = pd.concat({k:pd.DataFrame(v) for k, v in df9['cast'].items()})
    df9 = df9.join(new_df1.reset_index(level=1, drop=False)).reset_index(drop=False)
    df9 = df9.sort_values('character',ascending=True)
    df9=df9.groupby('title')['character'].apply(list)
    #df9 = pd.Series(sum([item for item in df9.character], [])).value_counts()
    df9 = pd.merge(df7, df9, how="inner", on="title")
    df9['count']=df9.character.apply(len)
    df9=df9.sort_values(by='count', ascending=False, na_position='first')
    df9=df9.head(10)
    movies=df9.title.to_list()
    movies
    #################################################

    log("QUESTION 9", output_df=None, other=movies)
    return movies


def question_10(df8):
    """
    :param df8: the dataframe created in question 8
    :return: df10
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    
    df10=df8.copy()
    df10.release_date = pd.to_datetime(df8.release_date)
    df10=df10.sort_values(by='release_date', ascending=False, na_position='first')
    df10
    #################################################

    log("QUESTION 10", output_df=df10, other=df10["release_date"].head(5).to_string().replace("\n", " "))
    return df10


def question_11(df10):
    """
    :param df10: the dataframe created in question 10
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    
    df11=df10.copy()
    # df7d=df7.copy()
    df7a=df10.copy()
    df11['genres'] = df11['genres'].apply(ast.literal_eval)
    new_df_2 = pd.concat({k:pd.DataFrame(v) for k, v in df11['genres'].items()})
    df11 = df11.join(new_df_2.reset_index(level=1, drop=False)).reset_index(drop=False)
    df11 = df11.name.str.get_dummies().sum().plot.pie(label='name', autopct='%1.2f%%' , radius=5)
    df11.plot(kind='pie' , subplots=True)
    #plt.show()
    #################################################

    plt.savefig("{}-Q11.png".format(studentid))


def question_12(df10):
    """
    :param df10: the dataframe created in question 10
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    
    df12=df10.copy()
    df7a=df10.copy()
    df12['production_countries'] = df12['production_countries'].apply(ast.literal_eval)
    new_df_2 = pd.concat({k:pd.DataFrame(v) for k, v in df12['production_countries'].items()})
    df12 = df12.join(new_df_2.reset_index(level=1, drop=False)).reset_index(drop=False)
    df12.name.value_counts().sort_index(ascending=True).plot(kind = 'bar')
    #################################################

    plt.savefig("{}-Q12.png".format(studentid))


def question_13(df10):
    """
    :param df10: the dataframe created in question 10
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    
    df13=df10.copy()
    new=df13.groupby('original_language')
    fig, ax = plt.subplots()
    for name, group in new:
        ax.plot(group.vote_average, group.success_impact, marker='o', linestyle='', ms=8, label=name)
    ax.legend(numpoints=1, loc='upper right')    
    #################################################

    plt.savefig("{}-Q13.png".format(studentid))


if __name__ == "__main__":
    df1 = question_1("movies.csv", "credits.csv")
    df2 = question_2(df1)
    df3 = question_3(df2)
    df4 = question_4(df3)
    df5 = question_5(df4)
    df6 = question_6(df5)
    df7 = question_7(df6)
    df8 = question_8(df7)
    movies = question_9(df8)
    df10 = question_10(df8)
    question_11(df10)
    question_12(df10)
    question_13(df10)