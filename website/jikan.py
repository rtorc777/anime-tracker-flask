from jikanpy import Jikan

jikan = Jikan()

search = jikan.search('anime', 'kaguya', parameters={'limit': 10})

for i in range(len(search['data'])):
    results = search['data'][i]["title"]
    images = search['data'][i]["images"]["jpg"]["image_url"]

    print(results, images)