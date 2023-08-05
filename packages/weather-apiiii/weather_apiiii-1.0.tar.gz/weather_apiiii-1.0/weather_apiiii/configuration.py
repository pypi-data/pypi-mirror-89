# -*- coding: utf-8 -*-

"""
    weather_apiiii

    This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io ).
"""

from weather_apiiii.api_helper import APIHelper


class Configuration(object):

    """A class used for configuring the SDK by a user.

    This class need not be instantiated and all properties and methods
    are accessible without instance creation.

    """

    # Set the array parameter serialization method
    # (allowed: indexed, unindexed, plain, csv, tsv, psv)
    array_serialization = "indexed"

    # The base Uri for API calls
    base_uri = 'http://api.openweathermap.org/data/2.5'

    # app key
    appid = 'e7b16ebe3fbe47e6b97f6821cff80e5d'

