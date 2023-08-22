from jikanpy import Jikan

def search_jikan(type, name):
    jikan = Jikan()

    search = jikan.search(type, name, parameters={'limit': 18, 'sfw':1})

    results = {}
    for i in range(len(search['data'])):
        names = search['data'][i]["title"]
        images = search['data'][i]["images"]["jpg"]["image_url"]
        results[names] = images
        
    return results

headings  = ("Image", "Name", "Rating", "Notes", "Options")

data = (
    ("https://cdn.myanimelist.net/images/anime/1295/106551.jpg", "Kaguya-sama wa Kokurasetai: Tensai-tachi no Renai Zunousen", 10, "this anime is absolutely goated anime"),
    ("https://cdn.myanimelist.net/images/anime/1295/106551.jpg", "Kaguya-sama wa Kokurasetai: Tensai-tachi no Renai Zunousen", 11, "goated anime")
)

