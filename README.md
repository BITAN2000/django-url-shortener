# Django URL Shortener API

A simple URL shortener REST API built using Django and Django REST Framework.

## Features
- Shorten long URLs
- Custom aliases
- Expiry support
- Redirect tracking
- Stats endpoint

## API Endpoints

### POST /shorten
Create a short URL.

### GET /{code}
Redirect to original URL.

### GET /stats/{code}
View URL statistics.

## Setup

```bash
git clone https://github.com/BITAN2000/django-url-shortener.git
cd django-url-shortener
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
