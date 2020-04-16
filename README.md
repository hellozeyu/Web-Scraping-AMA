# Web-Scraping-AMA
This is a curated collections of **WORKING** spiders written in Python.

## [metacritic.com](https://www.metacritic.com/)

---
Scraped the following fields of each movie using the Scrapy package.
- movie_title
- genre
- release_date
- metascore
- meta_positive
- meta_mixed
- meta_negative
- userscore
- user_positive
- user_mixed
- user_negative

## [realtor.com](https://www.realtor.com/)

---
Scraped the listings of four example regions in NYC area using the Selenium package. Each listing contains the following fields.

*Note*: this website uses [Distil Networks](https://www.distilnetworks.com/) or similar technology to ban automated browser like Selenium. To bypass that, follow the solution [here](https://stackoverflow.com/a/52108199) to change the `cdc_` variable in your chromedriver otherwise you will see the reCAPTCHA after a few pages.

- property
- bed
- bath
- sqft
- price
