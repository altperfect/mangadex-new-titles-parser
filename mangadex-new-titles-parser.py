import requests


# getting genres for each title
def get_genres(data, title_id: int) -> list:
    i = 0
    output = []
    while True:
        try:
            genre = data['data'][title_id]['attributes']['tags'][i]['attributes']['name']['en']
            output.append(genre)
            i += 1
        except IndexError:
            break

    return output


# formatting the link
def get_link(data, title_id: int) -> str:
    id = data['data'][title_id]['id']
    link = f'https://mangadex.org/title/{id}'

    return link


# забираем описание (optional since Discord has a 4000 symbols limit per message)
# def get_description(data, title_id: int) -> str:
#     try:
#         description = data['data'][title_id]['attributes']['description']['en']
#         return description
#     except (TypeError, KeyError):
#         return 'Описания нет.'


def make_request():
    url = 'https://api.mangadex.org/manga?limit=15&offset=0&includes[]=cover_art&includes[]=author&includes[]=artist&contentRating[]=safe&contentRating[]=suggestive&contentRating[]=erotica&order[createdAt]=desc'
    response = requests.get(url)
    data = response.json()

    return data


def parse() -> str:
    i = 0
    data = make_request()
    output = ''
    article = ''

    for item in data['data']:
        title = item['attributes']['title']['en']
        original_language = item['attributes']['originalLanguage']
        translated_language = item['attributes']['availableTranslatedLanguages']
        # description = get_description(data, i)
        genres = get_genres(data, i)
        link = get_link(data, i)
        i += 1

        # adding to final output if title's conditions match 
        if original_language == 'ja' and 'en' in translated_language:
            genres = ', '.join(genres)
            article = f'**Title:** {title}\n**Genres:** {genres}\n**Link:** {link}\n\n'
            output = output + article

    return output

