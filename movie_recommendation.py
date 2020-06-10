import pandas as pd
df = pd.read_csv("movie_dataset.csv")

import json
df['spoken_languages'] = df['spoken_languages'].apply(json.loads)
df['production_companies'] = df['production_companies'].apply(json.loads)
df['production_countries'] = df['production_countries'].apply(json.loads)

def iso_639_1_name(row):
    spoken_languages = ''
    for i in row:
        try:
            spoken_languages += i['iso_639_1'] + ' '
        except:
            pass
        try:
            spoken_languages += i['name'] + ' '
        except:
            pass
    return spoken_languages
def production_companies_name(row):
    production_companies = ''
    for i in row:
        try:
            production_companies += i['name'] + ' '
        except:
            pass
    return production_companies
def iso_3166_1_name(row):
    country = ''
    for i in row:
        try:
            country += i['iso_3166_1'] + ' '
        except:
            pass
        try:
            country += i['name'] + ' '
        except:
            pass
    return country

df['spoken_languages'] = df['spoken_languages'].apply(iso_639_1_name)
df['production_companies'] = df['production_companies'].apply(production_companies_name)
df['production_countries'] = df['production_countries'].apply(iso_3166_1_name)

features = ['overview', 'genres', 'keywords', 'production_companies', 'production_countries', 'spoken_languages','tagline', 'cast', 'director']
for feature in features:
    df[feature] = df[feature].fillna('') 
def combine_features(row):
    try:
        return row['overview'] + ' ' + row['genres'] + ' ' + row['keywords'] + ' ' + row['production_companies'] + ' ' + row['production_countries'] + ' ' + row['spoken_languages'] + ' ' + row['tagline'] + ' ' + row['cast'] + ' ' + row['director']
    except Exception as ex:
        print (ex, row)
df["combined_features"] = df.apply(combine_features,axis=1)

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
count_matrix = cv.fit_transform(df["combined_features"])

from sklearn.metrics.pairwise import cosine_similarity
similarity_score = cosine_similarity(count_matrix)

df.to_pickle("movie_data_frame.pkl")

import numpy
numpy.save("similarity_score", similarity_score)