#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
import logging

# Libs


# Custom

##################
# Configurations #
##################



###################################
# Response Parser Class - Results #
###################################

class Results:
    """ Parser class for converting responses into a resuable object """
    def __init__(self, response: dict):
        for attribute, value in response.items():
            setattr(self, attribute, value)
