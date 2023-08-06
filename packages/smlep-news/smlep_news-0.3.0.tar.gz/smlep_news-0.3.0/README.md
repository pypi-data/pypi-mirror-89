[![PyPI version](https://badge.fury.io/py/smlep-news.svg)](https://badge.fury.io/py/smlep-news)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Maintainability](https://api.codeclimate.com/v1/badges/0a7fa5b1833812224f02/maintainability)](https://codeclimate.com/github/Smlep/smlepNews/maintainability)

Essential
=========

This package is a simple gatherer of different news from various APIs.

Currently, it sends all news gathered through e-mails to all the mail addresses from a database.

To send a simple mail to a target without using any database, use the function `prepare_mail` from `mail`.

Currently the gathered news are the following:

- Weather from [Open Weather Map](https://openweathermap.org)
- Top products from [Product Hunt](https://www.producthunt.com)
- Trending repos from [GitHub](https://github.com)
- News from [Guardian](https://www.theguardian.com)
- News from [Le Figaro](http://www.lefigaro.fr) (in French)
- News from the [New York Times](https://www.nytimes.com/)
- Exchange rates from [exchangeratesapi.io](https://exchangeratesapi.io/)
- Stories from [Medium](https://medium.com)
- Stories from [Hacker News](https://news.ycombinator.com/)

The package can be installed through the official pypi repository with:

```
pip install smlep-news
```

Architecture
============

This project is divided in different packages:

- `exchangerates`: fetches currency exchange rates from [exchangeratesapi.io/](https://exchangeratesapi.io/).
- `figaro`: fetches french news from [Le Figaro](http://www.lefigaro.fr).
- `github`: fetches trending repos from [GitHub](https://github.com).
- `guardian`: fetches us news from [Guardian](https://www.theguardian.com).
- `hackernews`: fetches top stories list and stories details from [Hacker News](https://news.ycombinator.com/).
- `mail`: calls gatherer from the other packages, format their content and send mail.
- `medium`: extracts top stories from a specific [Medium](https://medium.com) topic.
- `nytimes`: fetches news from the [New York Times](https://www.nytimes.com/)
- `product_hunt`: fetches top products from [Product Hunt](https://www.producthunt.com).
- `runner`: gathers e-mail addresses from a database and send the gathered news through e-mails. This package configuration is relative to my own setup, if you want to use this program, you should bring changes to this package (or not use it).
- `weather`: fetches weather from [Open Weather Map](https://openweathermap.org). To choose the city you have to provide an ID, a list of city IDs can be downloaded [here](http://bulk.openweathermap.org/sample/).

Credentials
===========

This program uses APIs from different sources, and some of them require authentication.
You'll have to provide API Keys in environment variables:

- `PH_CLIENT_ID`/`PH_CLIENT_SECRET`: Product Hunt Api Client Id/Client Secret.
- `WEATHER_KEY`: Open Weather Map Api Key.
- `GUARDIAN_KEY`: Guardian Api Key.
- `NYT_KEY`: New york times Api key

All these keys can be obtained freely on their respective websites.

To send mails, you need an email account, the default configuration is for `gmail`,
if you need to use another mail server, you should update the code. If you use
`gmail`, you only need to provide some environment variables:

- `EMAIL_NAME`
- `EMAIL_USERNAME`
- `EMAIL_PASSWORD`

Why and how I created this project
==================================

I wrote a small post about this project on my [GitHub Page](https://smlep.github.io), you can read it [here](https://smlep.github.io/jekyll/update/2019/02/01/smlepnews.html).
