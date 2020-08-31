#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in


# Libs


# Custom
from .projects import ProjectTask

##################
# Configurations #
##################


###################################
# Task Interfacing Class - Driver #
###################################

class Driver:
    """ Main wrapper class that 
    """
    
    def __init__(self, host, port):

        # Private Attributes
        self.__project_task = ProjectTask()

        # Public Attributes
        self.host = host
        self.port = port


    @property
    def projects(self):
        return self.__project_tasks