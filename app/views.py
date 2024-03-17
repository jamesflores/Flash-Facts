from django.shortcuts import render
from datetime import datetime, timedelta
import requests

from flashfacts import settings


def index(request, month=None, day=None):
    # get month and day if provided
    now = datetime.now()
    if not month or not day:
        month = now.month
        day = now.day

    # check if the month and day are valid
    if month < 1 or month > 12:
        return render(request, 'flashfacts/index.html', {
            'error': 'Error: Invalid month provided.'
        })
    if day < 1 or day > 31:
        return render(request, 'flashfacts/index.html', {
            'error': 'Error: Invalid day provided.'
        })
    
    # get the current date, next day, and previous day
    try:
        current_date = datetime(year=int(now.year), month=int(month), day=int(day))
        next_day = current_date + timedelta(days=1)
        prev_day = current_date - timedelta(days=1)
    except ValueError:
        return render(request, 'flashfacts/index.html', {
            'error': 'Error: Invalid date provided.'
        })

    # make API call to get fact for the provided date
    url = f"{settings.RAPID_API_URL}/{month}/{day}/date"
    querystring = {"fragment":"true","json":"true"}
    headers = {
        "X-RapidAPI-Key": settings.RAPID_API_KEY,
        "X-RapidAPI-Host": settings.RAPID_API_HOST
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        print(f'Error {response.status_code}: {response.text}')
        return render(request, 'flashfacts/index.html', {
            'error': 'An error occurred while fetching the fact. Please try again later.'
        })
    fact = response.json()
    print(f'Fact: {fact}')

    # get stock image for the fact
    image = get_stock_image(fact.get('text'))
    print(f'Image: {image}')

    # render the template with the fact and image
    return render(request, 'flashfacts/index.html', {
        'fact': fact.get('text'),
        'day': day,
        'month': month,
        'month_name': datetime(2000, month, 1).strftime('%B'),
        'year': fact.get('year'),
        'number': fact.get('number'),
        'found': fact.get('found'),
        'type': fact.get('type'),
        'image': image.get('src').get('large'),
        'photographer': image.get('photographer'),
        'photographer_url': image.get('photographer_url'),
        'image_url': image.get('url'),
        'next_day': next_day,
        'prev_day': prev_day,
        'current_date': current_date.strftime('%Y-%m-%d'),
        'today_day': now.day,
        'today_month': now.month,
    })


# get a stock image for the provided query from Pexels
def get_stock_image(query):
    url = "https://api.pexels.com/v1/search"
    querystring = {"query": query, "per_page": "1"}
    headers = {
        'Authorization': settings.PEXELS_API_KEY
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()['photos'][0]

    '''
    {
    "total_results": 10000,
    "page": 1,
    "per_page": 1,
    "photos": [
        {
        "id": 3573351,
        "width": 3066,
        "height": 3968,
        "url": "https://www.pexels.com/photo/trees-during-day-3573351/",
        "photographer": "Lukas Rodriguez",
        "photographer_url": "https://www.pexels.com/@lukas-rodriguez-1845331",
        "photographer_id": 1845331,
        "avg_color": "#374824",
        "src": {
            "original": "https://images.pexels.com/photos/3573351/pexels-photo-3573351.png",
            "large2x": "https://images.pexels.com/photos/3573351/pexels-photo-3573351.png?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
            "large": "https://images.pexels.com/photos/3573351/pexels-photo-3573351.png?auto=compress&cs=tinysrgb&h=650&w=940",
            "medium": "https://images.pexels.com/photos/3573351/pexels-photo-3573351.png?auto=compress&cs=tinysrgb&h=350",
            "small": "https://images.pexels.com/photos/3573351/pexels-photo-3573351.png?auto=compress&cs=tinysrgb&h=130",
            "portrait": "https://images.pexels.com/photos/3573351/pexels-photo-3573351.png?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=800",
            "landscape": "https://images.pexels.com/photos/3573351/pexels-photo-3573351.png?auto=compress&cs=tinysrgb&fit=crop&h=627&w=1200",
            "tiny": "https://images.pexels.com/photos/3573351/pexels-photo-3573351.png?auto=compress&cs=tinysrgb&dpr=1&fit=crop&h=200&w=280"
        },
        "liked": false,
        "alt": "Brown Rocks During Golden Hour"
        }
    ],
    "next_page": "https://api.pexels.com/v1/search/?page=2&per_page=1&query=nature"
    }
    '''


def about(request):
    return render(request, 'flashfacts/about.html')