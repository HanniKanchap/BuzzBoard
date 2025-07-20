import pandas as pd

def filter_thumbnail(data):
    if data['thumbnail'] in ['thumbnail','self','default','nsfw','spoiler']:
        return None
    else:
        return data['thumbnail']
        

def clean_RedditData(data):
    data['publishedAt'] = pd.to_datetime(data['publishedAt'])
    data['Date_Format'] = data['publishedAt'].dt.date
    data['Time_Format'] = data['publishedAt'].dt.time
    data['thumbnail'] = data.apply(filter_thumbnail,axis = 1)
    data.drop_duplicates()

    return data
    