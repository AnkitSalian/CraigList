import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from requests.compat import quote_plus
from . import models

BASE_CRAIGLIST_URL = 'https://mumbai.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    trigger_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
    response = requests.get(trigger_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_listing = soup.find_all('li', {'class': 'result-row'})
    final_postings = []
    for post in post_listing:
        title = post.find(class_='result-title')
        post_title = 'Title Not Specified' if title is None else title.text
        post_url = post.find('a').get('href')
        price = post.find(class_='result-price')
        post_price = 'Not Specified' if price is None else price.text
        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTiHqFLMP_n6u8RhHsT-ERKE4xXGiKs6VdqCw&usqp=CAU'
        final_postings.append((post_title, post_url, post_price, post_image_url))

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
