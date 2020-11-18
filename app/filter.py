import os, sys, django
from numpy.lib.npyio import save
# sys.path.append(
#     os.path.join(os.path.dirname(
#         os.path.dirname(os.path.abspath(__file__))), "..")
# )
sys.path.append("..")
os.environ["DJANGO_SETTINGS_MODULE"] = "best_movies.settings"
django.setup()

from movie_ranking.models import PttMovie, Movie, CountGoodAndBad
from django.db.models import F

import pandas as pd
import numpy as np


class FilterAndInsertData():
    """Analysis scrapy data"""

    movies = pd.read_csv("ptt_movies.csv").dropna(how="all")
    titles = pd.read_csv("yahoo.csv")

    movies["title"] = movies["title"].astype("category")
    key_word = titles.iloc[:, 8]

    # 找到含有相同電影名稱的title 並新增一個新欄位'key_word' 最後insert to database
    newDF = pd.DataFrame()
    for key in key_word:
        mask = movies["title"].str.contains(key)  # string compare
        movies["key_word"] = key  # Add new column
        newDF = newDF.append(movies[mask], ignore_index=True)

    # To assign as a column use transform
    newDF['good_ray'] = newDF.groupby(['key_word'])['title'].transform(lambda x: x[x.str.contains('好雷')].count())
    newDF['bad_ray'] = newDF.groupby(['key_word'])['title'].transform(lambda x: x[x.str.contains('負雷')].count())
    # newDF.to_csv('output.csv')

    # count title欄位 有包含 '好雷' and '負雷' 字眼的標題
    ptt_coun_ray = pd.DataFrame()
    ptt_coun_ray['title'] = titles.iloc[:, 8]

    # merge newDF and title DataFrame and duplicates title
    df = ptt_coun_ray.merge(newDF, left_on='title', right_on='key_word', how='left').drop(
            ['author', 'key_word', 'contenttext', 'date', 'title_y'], axis=1)
    df2 = df.drop_duplicates(subset=['title_x'])
    df2 = df2.fillna(0) # Transfer NaN to 0
    # df2.to_csv('count_good_or_bad.csv')
    inser_pttcomment = newDF.to_dict("records")
    inser_goodandbad = df2.to_dict('records2')

    # Insert ptt comment Data to DataBase
    def InsertPttComment(inser_pttcomment):
        for record in inser_pttcomment:
            identifyer = PttMovie.objects.filter(
                                                author=record['author'],
                                                title=record['title']
                                                ).exists()

            if identifyer:
                print('{} {} Data is already exists!!'.format(record['author'], record['title']))
            else:
                try:
                    PttMovie.objects.create(
                        author=record["author"],
                        contenttext=record["contenttext"],
                        date=record["date"],
                        title=record["title"],
                        key_word=Movie.objects.get(title=record["key_word"]), # foreign key
                    )
                except:
                    print(record["key_word"] + ' is not match any movie title!!')
                # print('Not exist')

    # Insert Count comment good and bad Data to DataBase
    def InsertGoodAndBadRay(inser_goodandbad):
        for record2 in inser_goodandbad:
            # check there is any CountGoodAndBad any movie__title match record2['title_x']
            # if match just update else create new movie good and bad ray
            identifyer =  CountGoodAndBad.objects.filter(movie__title=record2['title_x']).exists()
            if identifyer:
                CountGoodAndBad.objects.filter(
                    movie=Movie.objects.get(title=record2['title_x'])
                ).update(
                    good_ray=F('good_ray') + record2['good_ray'],
                    bad_ray=F('bad_ray') + record2['bad_ray'],
                )
            else:
                try:
                    CountGoodAndBad.objects.create(
                        good_ray=record2["good_ray"],
                        bad_ray=record2["bad_ray"],
                        movie=Movie.objects.get(title=record2["title_x"]), # foreign key
                    )
                except:
                    print(record2["title_x"] + ' is not match any movie title!!')

    InsertPttComment(inser_pttcomment)
    InsertGoodAndBadRay(inser_goodandbad)
