from jikanpy import Jikan

jikan = Jikan()

search = jikan.search('anime', 'kaguya', parameters={'limit': 10})

for i in range(len(search['data'])):
    results = search['data'][i]["title"]
    images = search['data'][i]["images"]["jpg"]["image_url"]

    print(results, images)

headings  = ("Image", "Name", "Rating", "Notes", "Options")

data = (
    ("https://cdn.myanimelist.net/images/anime/1295/106551.jpg", "Kaguya-sama wa Kokurasetai: Tensai-tachi no Renai Zunousen", 10, "this anime is absolutely goated anime"),
    ("https://cdn.myanimelist.net/images/anime/1295/106551.jpg", "Kaguya-sama wa Kokurasetai: Tensai-tachi no Renai Zunousen", 11, "goated anime")
)

