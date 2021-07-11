# Webscraper Bestbuy

Webscraper Bestbuy for learning how to use libraries in python for webscraping. The webscraper currently scraps bestbuy's gpu listing and stores the data to a local postgres database. There is also an email service to send out notifications to user defined emails if a matching gpu pattern is available.

# Setup

## ChromeDriver

Get latest `chromedriver` from this [link](https://chromedriver.chromium.org/downloads) and place it in the script directory(`/webscraper/`).

On Mac, go to the script directory and run the following command to allow `chromedriver` to be executed:

`xattr -d com.apple.quarantine chromedriver`

## Python

Python 3.9.4

virtualenv, if not installed run below command to install:

$ pip install virtualenv

## Database

Create a new postgres database then dump the `webscrapeDb.sql` into that database to initialize it.

`$ psql webscrapeDb < webscrapeDb.sql`

## Installation

Make sure to setup the virtual environment and install the `requirements.txt`

To do this follow the steps below:

`$ virtualenv .env`

`$ source .env/bin/activate`

`$ pip install -r requirements.txt`

## Configuration

The webscraper/webserver/email service depends on a config file `config.yml`

To create the config file follow the below commands:

`$ touch config.yml`

Use the following template to fill out the necessary fields for the servers/services to operate then copy it to the config file.

```
input:
  url: https://www.bestbuy.com/site/searchpage.jsp?st=gpu+cards
  url_by_page: https://www.bestbuy.com/site/searchpage.jsp?st=gpu+cards&cp={n}
db_connection:
  postgres: postgresql://username:password@localhost/webscrapeDb
emailer:
  server: smtp.gmail.com
  username: email@gmail.com
  password: email_password
  port: 465
```

# Run Webserver

The webserver is used for allowing users to check the database in realtime

`$ cd ~/path/to/webscraper_bestbuy`

`$ python run_webserver.py`

# Run Scheduler

The scheduler is used for scheduling the webscraper and email service

`$ cd ~/path/to/webscraper_bestbuy`

`$ python run_scheduler.py`
