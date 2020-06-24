from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from .models import Search

BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/?query='


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    Search.objects.create(search=search)

    response = requests.get(f'{BASE_CRAIGSLIST_URL}{search}')
    soup = BeautifulSoup(response.text, 'html.parser')

    posts = soup.find_all('li', {'class', 'result-row'})

    allPosts = []
    for post in posts:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(
                class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = f'{BASE_CRAIGSLIST_URL}{post_image_id}'
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        allPosts.append((post_title, post_url, post_price, post_image_url))

    print(allPosts[1:3])
    frontend_stuff = {
        'search': search,
        'allPosts': allPosts
    }

    return render(request, 'my_app/new_search.html', frontend_stuff)
