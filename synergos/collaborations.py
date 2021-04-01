#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
import logging
from typing import Dict, Union

# Libs


# Custom
from .base import BaseTask
from .endpoints import COLLABORATION_ENDPOINTS

##################
# Configurations #
##################


################################################
# Collaboration task Class - CollaborationTask #
################################################

class CollaborationTask(BaseTask):
    """ Interfacing class governing all collaboration-related interactions with
        the remote Synergos grid

    Attributes:
        _type (str): Specifies the type of task
        address (str): Address where Synergos TTP is hosted at
        endpoints (str)): All endpoints governed by this task
    """

    def __init__(self, address: str):
        super().__init__(
            _type="collaboration", 
            address=address,
            endpoints=COLLABORATION_ENDPOINTS
        )
        
        self._catalogue_metadata = {}
        self._logger_metadata = {}
        self._meter_metadata = {}
        self._mlops_metadata = {}
        self._mq_metadata = {}
        self._ui_metadata = {}

    
    ###########
    # Setters #
    ###########

    def configure_catalogue(self, host: str, port: str) -> Dict[str, Union[int, str]]:
        """
        """
        self._catalogue_metadata.update({
            'catalogue_host': host,
            'catalogue_port': port
        })
        return self._catalogue_metadata


    def configure_logger(
        self, 
        host: str,
        sysmetrics_port: int,
        director_port: int,
        ttp_port: int,
        worker_port: int
    ):
        """
        """
        self._logger_metadata.update({
            'logger_host': host,
            'logger_ports': {
                'sysmetrics': sysmetrics_port,
                'director': director_port,
                'ttp': ttp_port,
                'worker': worker_port
            }
        })
        return self._logger_metadata


    def configure_meter(self, host: str, port: str) -> Dict[str, Union[int, str]]:
        """
        """
        self._meter_metadata.update({'meter_host': host, 'meter_port': port})
        return self._meter_metadata


    def configure_mlops(self, host: str, port: str) -> Dict[str, Union[int, str]]:
        """
        """
        self._mlops_metadata.update({'mlops_host': host, 'mlops_port': port})
        return self._mlops_metadata


    def configure_mq(self, host: str, port: str) -> Dict[str, Union[int, str]]:
        """
        """
        self._mq_metadata.update({'mq_host': host, 'mq_port': port})
        return self._mq_metadata


    def configure_ui(self, host: str, port: str) -> Dict[str, Union[int, str]]:
        """
        """
        self._ui_metadata.update({'ui_host': host, 'ui_port': port})
        return self._ui_metadata

    ###########
    # Helpers #
    ###########

    def _generate_bulk_url(self) -> str:
        return self._generate_url(endpoint=self.endpoints.COLLABORATIONS)


    def _generate_single_url(self, collab_id: str) -> str:
        return self._generate_url(
            endpoint=self.endpoints.COLLABORATION,
            collab_id=collab_id
        )


    def _compile_configurations(self) -> Dict[str, Union[str, int, dict]]:
        """
        """
        configurations = {
            **self._catalogue_metadata,
            **self._logger_metadata,
            **self._meter_metadata,
            **self._mlops_metadata,
            **self._mq_metadata,
            **self._ui_metadata
        }
        return configurations


    ##################
    # Core functions #
    ##################

    def create(self, collab_id: str, **kwargs):
        """ Registers a collaboration in the federated grid.

        Args:
            collab_id (str): Identifier of collaboration
            **kwargs
        Returns:
            Collaboration entry
        """
        configurations = self._compile_configurations()
        parameters = {'collab_id': collab_id, **configurations, **kwargs}

        return self._execute_operation(
            operation="post",
            url=self._generate_bulk_url(),
            payload=parameters
        )

    
    def read_all(self):
        """ Retrieves information/configurations of all collaborations created 
            in the federated grid

        Returns:

        """
        return self._execute_operation(
            operation="get",
            url=self._generate_bulk_url(),
            payload=None
        )


    def read(self, collab_id: str):
        """ Retrieves a single collaboration's information/configurations 
            created in the federated grid

        Args:
            collab_id (str): Identifier of collaboration
        Returns:

        """
        return self._execute_operation(
            operation="get",
            url=self._generate_single_url(collab_id=collab_id),
            payload=None
        )
    
    
    def update(self, collab_id: str, **updates):
        """ Updates a collaboration's information/configurations created in the 
            federated grid
        
        Args:
            collab_id (str): Identifier of collaboration
            **updates: Keyword pairs of parameters to be updated
        Returns:

        """
        configurations = self._compile_configurations()
        updated_parameters = {**configurations, **updates}

        return self._execute_operation(
            operation="put",
            url=self._generate_single_url(collab_id=collab_id),
            payload=updated_parameters
        )

    
    def delete(self, collab_id: str):
        """ Removes a collaboration's information/configurations previously 
            created from the federated grid

        Args:
            collab_id (str): Identifier of collaboration
        Returns:

        """
        return self._execute_operation(
            operation="delete",
            url=self._generate_single_url(collab_id=collab_id),
            payload=None
        )


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000
    address = f"http://{host}:{port}"

    collaborations = CollaborationTask(address)
    collab_id_1 = "test_collab_1"
    collab_id_2 = "test_collab_2"

    # Test collaboration creation
    create_response_1 = collaborations.create(collab_id=collab_id_1)
    print("Collaboration 1: Create response:", create_response_1)

    collaborations.configure_logger(
        host="111.222.333.444",
        sysmetrics_port=9100,
        director_port=9200,
        ttp_port=9300,
        worker_port=9400
    )
    create_response_2 = collaborations.create(collab_id=collab_id_2)
    print("Collaboration 2: Create response:", create_response_2)

    # Test collaboration retrieval bulk
    read_all_response = collaborations.read_all()
    print("Read all response:", read_all_response)  

    # Test collaboration retrieval single
    read_response_1 = collaborations.read(collab_id=collab_id_1)
    print("Collaboration 1: Read response:", read_response_1)

    read_response_2 = collaborations.read(collab_id=collab_id_2)
    print("Collaboration 2: Read response:", read_response_2)

    # Test collaboration update
    update_response_1 = collaborations.update(
        collab_id=collab_id_1, 
        mlops_host="222.222.222.222", 
        mlops_port=9876
    )
    print("Collaboration 1: Update response:", update_response_1)

    update_response_2 = collaborations.update(
        collab_id=collab_id_2,
        meter_host="333.333.333.333", 
        meter_port=15790
    )
    print("Collaboration 2: Update response:", update_response_2)

    # Test collaboration deletion
    delete_response_1 = collaborations.delete(collab_id=collab_id_1)
    print("Collaboration 1: delete response:", delete_response_1)

    delete_response_2 = collaborations.delete(collab_id=collab_id_2)
    print("Collaboration 2: delete response:", delete_response_2)

    print("Collaboration left:", collaborations.read_all()) 
