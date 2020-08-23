import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from requests.compat import quote_plus
from . import models

BASE_CRAIGLIST_URL = 'https://mumbai.craigslist.org/search/?query={}'
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
        final_postings.append((post_title, post_url, post_price))

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
