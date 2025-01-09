#!/bin/bash
# Uruchomienie serwera Gunicorn
gunicorn photo_app.wsgi:application --bind=0.0.0.0:$PORT
