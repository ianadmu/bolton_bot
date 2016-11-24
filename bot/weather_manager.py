#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2

from datetime import datetime, timedelta
from HTMLParser import HTMLParser
import re
import ssl

SUNSET_HOUR = 21
SUNRISE_HOUR = 5
HOUR_DIFFERENCE_DAYLIGHT_SAVINGS = 5  # for Winnipeg
HOUR_DIFFERENCE_NO_DAYLIGHT_SAVINGS = 6  # for Winnipeg


def get_icon(conds):
        if "tornado" in conds or "hurricane" in conds or "cyclone" in conds:
            return ":cyclone:"
        if "light rain" in conds or "patchy rain" in conds:
            return ":closed_umbrella:"
        if "rain" in conds:
            return ":umbrella:"
        if "thunder" in conds:
            return ":zap:"
        if "snow" in conds:
            return ":snowflake:"
        if "fog" in conds or "mist" in conds:
            return ":foggy:"
        if "cloud" in conds or "overcast" in conds:
            return ":cloud:"
        if "sunny" in conds:
            return ":sunny:"
        if "clear" in conds:
            curr_datetime = (
                datetime.utcnow() - timedelta(
                    hours=HOUR_DIFFERENCE_DAYLIGHT_SAVINGS
                )  # change here when daylight savings ends
            )
            curr_time = int(curr_datetime.strftime('%H'))
            if curr_time >= SUNSET_HOUR or curr_time < SUNRISE_HOUR:
                return ":night_with_stars:"
            else:
                return ":sunny:"
        if "drizzle" in conds or "sleet" in conds:
            return ":umbrella:"
        if "tsunami" in conds:
            return ":ocean:"
        if "fire" in conds:
            return ":fire:"
        if "smog" in conds:
            return ":shit:"
        if "wind" in conds:
            return ":flags:"
        if "eclipse" in conds:
            return ":new_moon_with_face:"
        else:
            return ":boltonefron:"


def scrapeItem(html, startString, endString, parser):
    start = html.find(startString) + len(startString)
    end = html[start:].find(endString) + start
    return parser.unescape(html[start:end])


def getCurrentWeather():
    ssl._create_default_https_context = ssl._create_unverified_context
    stringsBeforeGT = re.compile("(\n|.)*>")
    url = "https://weather.gc.ca/city/pages/mb-38_metric_e.html"
    conditionString = 'Condition:'
    temperatureString = 'Temperature:'
    temperatureEnd = '&deg;'
    end = '</dd>'
    parser = HTMLParser()

    response = urllib2.urlopen(url)
    html = response.read()

    condition = scrapeItem(html, conditionString, end, parser)
    temperature = scrapeItem(html, temperatureString, temperatureEnd, parser)
    # these need additional scraping
    condition = re.sub(stringsBeforeGT, "", condition)
    temperature = re.sub(stringsBeforeGT, "", temperature)

    result = (
        "Winnipeg is currently " + temperature + "°C and " + condition + " " +
        get_icon(condition.lower())
    )
    return result
