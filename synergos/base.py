#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
from string import Template
from typing import Callable

# Libs
import requests

# Custom
from .abstract import AbstractTask

##################
# Configurations #
##################



##############################
# Base Task Class - BaseTask #
##############################

class BaseTask(AbstractTask):
    """
    Contains baseline functionality to all tasks. Other specific tasks will
    inherit all functionality for communicating/triggering remote Synergos
    grid operations. Extensions of this class will need to override 4 key methods 
    (i.e. `create`, `read`, `update`, `delete`)

    IMPORTANT:
    This class SHOULD NOT be instantiated by itself! instead, use it to subclass
    other algorithms.

    Attributes:
        _type (str): Specifies the type of task
        address (str): Address where Synergos TTP is hosted at
        endpoints (str)): All endpoints governed by this task
    """
    def __init__(self, _type: str, address: str, endpoints: Callable):
        self._type = _type
        self.address = address
        self.endpoints = endpoints()

    ###########
    # Helpers #
    ###########

    @staticmethod
    def _execute_operation(
        operation: str, 
        url: str, 
        payload: dict = None
    ) -> dict:
        """ Sends a specified request operation to an endpoint url to trigger
            a remote process in the federated grid. Payloads are parameters to
            be communicated over the network required for process execution

        Args:
            operation (str): Name of operation to be performed
            url (str): URL endpoint of remote trigger
            payload (dict): Parameter sets required for running remote trigger
        Returns:
            JSON status (dict)
        """
        op_function = getattr(requests, operation)
        status = op_function(url=url, json=payload)
        assert status.status_code in [200, 201]
        return status.json()


    def _generate_url(self, endpoint: Template, **keys) -> str:
        """ Given a endpoint template, generate a full url to be used to
            communicate with the federated grid

        Args:
            endpoint (Template): Endpoint template for generating string url
            **keys: All relevant keys required for filling the endpoint template
        """
        keys['address'] = self.address
        return endpoint.substitute(keys)


    ##################
    # Core Functions #
    ##################

    def create(self, *args, **kwargs):
        """ Creates a task in the federated grid """
        raise NotImplementedError(
            f"Current {self._type} task does not support 'create' operation!"
        )


    def read_all(self, *args, **kwargs):
        """ Retrieves information/configurations of all tasks created in the
            federated grid
        """
        raise NotImplementedError(
            f"Current {self._type} task does not support 'read_all' operation!"
        )


    def read(self, *args, **kwargs):
        """ Retrieves a single task's information/configurations created in the 
            federated grid
        """
        raise NotImplementedError(
            f"Current {self._type} task does not support 'read' operation!"
        )
    
    
    def update(self, *args, **kwargs):
        """ Updates task information/configurations created in the federated
            grid
        """
        raise NotImplementedError(
            f"Current {self._type} task does not support 'update' operation!"
        )

    
    def delete(self, *args, **kwargs):
        """ Removes task information/configurations previously created from the 
            federated grid
        """
        raise NotImplementedError(
            f"Current {self._type} task does not support 'delete' operation!"
        )
