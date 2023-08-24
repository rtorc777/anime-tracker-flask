from jikanpy import Jikan

def search_jikan(type, name):
    jikan = Jikan()

    search = jikan.search(type, name, parameters={'limit': 12, 'sfw':1})

    results = {}
    for i in range(len(search['data'])):
        names = search['data'][i]["title"]
        images = search['data'][i]["images"]["jpg"]["image_url"]
        results[names] = images
        
    return results

