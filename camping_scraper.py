"""
Created on Feb 2, 2022
@author: Fletch
"""
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

AVAILABILITY_URL = ("https://www.hipcamp.com/en-US/california/"
                   "{park}/{campground}?search_source=navbar-autocomplete#"
                   "arrive={arrive_date}&depart={depart_date}")

def createHeadlessChromeBrowser():
    """From: https://stackoverflow.com/questions/48537028/selenium-how-to-use-headless-chrome-on-aws"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    return webdriver.Chrome(options=options)


def find_availability_by_month(park, campground, year, month, weekend_only=True):
    """
    Parameters
    ----------
    park : str

    campground : str

    year : str

    month : str

    weekend_only : bool
        whether to search only for weekend vs. any day availability

    Returns
    -------
    list
        list of weekend availability at the given park's campground during the
        given month and year
    """
    # Format date correctly (YY-MM-DD) from year and month given
    start_date = datetime.strptime(year + "-" + month + "-01", "%Y-%m-%d")
    depart_date = (start_date + timedelta(days=1)).strftime("%Y-%m-%d")
    arrive_date = start_date.strftime("%Y-%m-%d")

    url = AVAILABILITY_URL.format(
        park=park,
        campground=campground,
        arrive_date=arrive_date,
        depart_date=depart_date
    )
    browser = createHeadlessChromeBrowser()
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')

    # Find availability calendar
    results = soup.find(id="public-camp-calendar-container")
    days = results.find_all(lambda tag: tag.name == "td" and tag.get("class") == ["day"])

    available = []
    for day in days:
        title = day.get("title")
        if "available" in title and title != "0 available campsites":
            day = day.get_text()
            date = datetime.strptime(year + "-" + month + "-" + day, "%Y-%m-%d")
            # Check if the date is a Friday or Saturday
            if not weekend_only or date.weekday() == 4 or date.weekday() == 5:
                available.append(date)

    return available


def find_availability_by_year(park, campground, year, months=range(1, 13), weekend_only=True):
    """
    Parameters
    ----------
    park : str

    campground : str

    year : str

    months : list
        list of months as str or int. Default is `range(1, 13)`

    weekend_only : bool
        whether to search only for weekend vs. any day availability

    Returns
    -------
    list
        list of weekend availability at the given park's campground during the
        given month and year
    """
    yearly_availability = []
    for month in months:
        if isinstance(month, int):
            month = str(month)
        try:
            monthly_availability = find_availability_by_month(
                park,
                campground,
                year,
                month,
                weekend_only=weekend_only
            )
            yearly_availability.append(monthly_availability)
        except:
            break

    # Flatten list
    yearly_availability = [item for sublist in yearly_availability for item in sublist]
    return yearly_availability
