# IMDb Web Scrapper

from bs4 import BeautifulSoup
import requests
import csv


def fetch_movies():
    # Downloads IMDB Top 250 data
    url = 'http://www.imdb.com/chart/top'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    movie_id = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]

    top_five_movies = []
    for index in range(5):
        # Separating Movie ID from href of movies
        top_five_movies.append(movie_id[index][7:16])

    return top_five_movies


def fetch_synopsis(movies):
    synopsis = []
    for movie in movies:
        url = 'https://www.imdb.com/title/' + movie + '/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        description = soup.find("meta", property="og:description")
        synopsis.append(description["content"])
    return synopsis


def create_dictionary(movie_id, movie_synopsis):
    imdb = []
    # Store each item into dictionary (data), then put those into a list (imdb)
    for index in range(5):
        data = {
            "movie_id": movie_id[index],
            "movie_synopsis": movie_synopsis[index]
        }
        imdb.append(data)

    return imdb


def export_to_csv(data):
    field_names = ['movie_id', 'movie_synopsis']

    with open('Top5Movies.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(data)


def top_ten_directors():
    url = 'https://www.imdb.com/list/ls008344500/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.find_all('h3', {"class": "lister-item-header"})
    directors = {}
    directors['Director_name'] = []
    directors['director_url'] = []
    for item in range(10):
        director_tag = str(data[item].select('h3 a'))
        # director_tag = data[item].select('h3 a')
        directors['Director_name'].append(director_tag[28:-5])
        # directors['Director_name'].append(director_tag.get_text())

        # print('Director_name',directors['Director_name'][item])

        directors['director_url'].append('https://www.imdb.com' + director_tag[10:25] + '/')

    # print('director_url', directors['director_url'][item])
    return directors


def directors_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.find_all('div', {"class": "filmo-category-section"})
    more_details = []
    for item in range(len(data)):
        director_movies = data[item].select('div b a')
        movie_list = []
        for movie in director_movies:
            movie_list.append(movie.get_text())
        more_details.append(movie_list)
    return more_details


def director_movies(directors):
    topTen = {}
    for item in range(1, 11):
        temp = {
            'Director': directors['Director_name'][item - 1][:-2],
            'Movies': directors_details(directors['director_url'][item - 1])
        }
        topTen[item] = temp

    return topTen


def dataToTextFile(data):
    f = open("Top10Directors.txt", "w")
    f.write(str(data))
    f.close()


if __name__ == '__main__':
    top_five_movies = fetch_movies()                                        # Milestone 1

    top_five_synopsis = fetch_synopsis(top_five_movies)                     # Milestone 2

    imdb = create_dictionary(top_five_movies, top_five_synopsis)            # Milestone 3

    export_to_csv(imdb)                                                     # Milestone 4

    directors = top_ten_directors()                                         # Milestone 5
    topTenDirectors = director_movies(directors)
    dataToTextFile(topTenDirectors)
