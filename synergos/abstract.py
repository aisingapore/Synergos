#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
import abc
import logging
from typing import Callable

# Libs


# Custom


##################
# Configurations #
##################

class AbstractTask(abc.ABC):

    @abc.abstractmethod
    def create(self, *args, **kwargs):
        """ Creates a task in the federated grid
        
            As AbstractTask implies, you should never instantiate this class by
            itself. Instead, you should extend AbstractTask in a new class which
            overrides `run`.
        """
        pass


    @abc.abstractmethod
    def read_all(self, *args, **kwargs):
        """ Retrieves information/configurations of all all tasks created in the
            federated grid

            As AbstractTask implies, you should never instantiate this class by
            itself. Instead, you should extend AbstractTask in a new class which
            overrides `read`.
        """
        pass

    
    @abc.abstractmethod
    def read(self, *args, **kwargs):
        """ Retrieves a single task's information/configurations created in the 
            federated grid

            As AbstractTask implies, you should never instantiate this class by
            itself. Instead, you should extend AbstractTask in a new class which
            overrides `read`.
        """
        pass
    
    
    @abc.abstractmethod
    def update(self, *args, **kwargs):
        """ Updates task information/configurations created in the federated
            grid
        
            As AbstractTask implies, you should never instantiate this class by
            itself. Instead, you should extend AbstractTask in a new class which
            overrides `update`.
        """
        pass
        
    
    @abc.abstractmethod
    def delete(self, *args, **kwargs):
        """ Removes task information/configurations previously created from the 
            federated grid

            As AbstractTask implies, you should never instantiate this class by
            itself. Instead, you should extend AbstractTask in a new class which
            overrides `delete`.
        """
        pass