#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
from typing import Dict, Union, Any

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
        self._reset_cache()

    
    ###########
    # Setters #
    ###########

    def _reset_cache(self):
        """ Initialises a blank state of a collaboration """
        self._catalogue_metadata = {}
        self._logger_metadata = {}
        self._meter_metadata = {}
        self._mlops_metadata = {}
        self._mq_metadata = {}


    def configure_catalogue(
        self, 
        host: str, 
        port: int,
        ui_port: int = 0,
        secure: bool = False
    ) -> Dict[str, Union[str, bool, Dict[str, int]]]:
        """ Declares & formats connection inforamation required to access a 
            deployed Synergos Catalogue instance

        Args:
            host (str): IP address/alias which Synergos Catalogue is hosted on
            port (int): Main interfacing port used for backend interactions
            ui_port (int): Port at which UI is hosted on
            secure (bool): Whether deployed component is secured (eg. TLS)
        Returns:
            Catalogue specific metadata (dict)
        """
        self._catalogue_metadata.update({
            'catalogue': {
                'host': host,
                'ports': {'main': port, 'ui': ui_port},
                'secure': secure
            }
        })
        return self._catalogue_metadata


    def configure_logger(
        self, 
        host: str,
        port: int,
        sysmetrics_port: int,
        director_port: int,
        ttp_port: int,
        worker_port: int,
        ui_port: int = 0,
        secure: bool = False
    ) -> Dict[str, Union[str, bool, Dict[str, int]]]:
        """ Declares & formats connection inforamation required to access a 
            deployed Synergos Logger instance

        Args:
            host (str): IP address/alias which Synergos Logger is hosted on
            port (int): Main interfacing port used for backend interactions
            sysmetrics_port (int): Port listening for distributed system metrics
            director_port (int): Port listening for distributed director logs
            ttp_port (int): Port listening for distributed TTP logs
            worker_port (int): Port listening for distributed worker logs
            ui_port (int): Port at which Synergos Logger UI is hosted on
            secure (bool): Whether deployed component is secured (eg. TLS)
        Returns:
            Logger specific metadata (dict)
        """
        self._logger_metadata.update({
            'logs': {
                'host': host,
                'ports': {

                    # Primary ports for interaction
                    'main': port,    
                    'ui': ui_port,

                    # Backend ports for partitioning incoming logs explicitly
                    'sysmetrics': sysmetrics_port,
                    'director': director_port,
                    'ttp': ttp_port,
                    'worker': worker_port
                },
                'secure': secure
            }
        })
        return self._logger_metadata


    def configure_meter(
        self, 
        host: str, 
        port: int,
        ui_port: int = 0,
        secure: bool = False
    ) -> Dict[str, Union[str, bool, Dict[str, int]]]:
        """ Declares & formats connection inforamation required to access a 
            deployed Synergos Meter instance

        Args:
            host (str): IP address/alias which Synergos Meter is hosted on
            port (int): Main interfacing port used for backend interactions
            ui_port (int): Port at which UI is hosted on
            secure (bool): Whether deployed component is secured (eg. TLS)
        Returns:
            Meter specific metadata (dict)
        """
        self._meter_metadata.update({
            'meter': {
                'host': host, 
                'ports': {'main': port, 'ui': ui_port},
                'secure': secure
            }
        })
        return self._meter_metadata


    def configure_mlops(
        self, 
        host: str, 
        port: str,
        ui_port: int = 0,
        secure: bool = False
    ) -> Dict[str, Union[str, bool, Dict[str, int]]]:
        """ Declares & formats connection inforamation required to access a 
            deployed Synergos MLOps instance

        Args:
            host (str): IP address/alias which Synergos MLOps is hosted on
            port (int): Main interfacing port used for backend interactions
            ui_port (int): Port at which UI is hosted on
            secure (bool): Whether deployed component is secured (eg. TLS)
        Returns:
            MLOps specific metadata (dict)
        """
        self._mlops_metadata.update({
            'mlops': {
                'host': host,
                'ports': {'main': port, 'ui': ui_port},
                'secure': secure
            }
        })
        return self._mlops_metadata


    def configure_mq(
        self, 
        host: str, 
        port: str,
        ui_port: int = 0,
        secure: bool = False
    ) -> Dict[str, Union[str, bool, Dict[str, int]]]:
        """ Declares & formats connection inforamation required to access a 
            deployed Synergos MQ (i.e. message queue) instance

        Args:
            host (str): IP address/alias which Synergos MQ is hosted on
            port (int): Main interfacing port used for backend interactions
            ui_port (int): Port at which UI is hosted on
            secure (bool): Whether deployed component is secured (eg. TLS)
        Returns:
            MQ specific metadata (dict)
        """
        self._mq_metadata.update({
            'mq': {
                'host': host, 
                'ports': {'main': port, 'ui': ui_port},
                'secure': secure
            }
        })
        return self._mq_metadata

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
        """ Compiles all declared component metadata into a single entry
            ready for submission to Synergos REST

        Returns:
            Compiled configurations (dict)
        """
        configurations = {
            **self._catalogue_metadata,
            **self._logger_metadata,
            **self._meter_metadata,
            **self._mlops_metadata,
            **self._mq_metadata
        }

        return configurations


    ##################
    # Core functions #
    ##################

    def create(self, collab_id: str, **kwargs) -> Dict[str, Any]:
        """ Registers a collaboration in the federated grid.

        Args:
            collab_id (str): Identifier of collaboration
            **kwargs
        Returns:
            Collaboration record (dict)
        """
        configurations = self._compile_configurations()
        parameters = {'collab_id': collab_id, **configurations, **kwargs}
        create_resp = self._execute_operation(
            operation="post",
            url=self._generate_bulk_url(),
            payload=parameters
        )
        self._reset_cache() # Must be resetted here to prevent carry over!
        return create_resp

    
    def read_all(self) -> Dict[str, Any]:
        """ Retrieves information/configurations of all collaborations created 
            in the federated grid

        Returns:
            Bulk collaboration payload (dict)
        """
        return self._execute_operation(
            operation="get",
            url=self._generate_bulk_url(),
            payload=None
        )


    def read(self, collab_id: str) -> Dict[str, Any]:
        """ Retrieves a single collaboration's information/configurations 
            created in the federated grid

        Args:
            collab_id (str): Identifier of collaboration
        Returns:
            A single collaboration record (dict)
        """
        return self._execute_operation(
            operation="get",
            url=self._generate_single_url(collab_id=collab_id),
            payload=None
        )
    
    
    def update(self, collab_id: str, **updates) -> Dict[str, Any]:
        """ Updates a collaboration's information/configurations created in the 
            federated grid
        
        Args:
            collab_id (str): Identifier of collaboration
            **updates: Keyword pairs of parameters to be updated
        Returns:
            Updated collaboration record (dict)
        """
        ###########################
        # Implementation Footnote #
        ###########################

        # [Cause]
        # To allow new component registration, a component's metadata needs to 
        # be declared & assembled on the client's machine first, before sending
        # it out to the orchestrating node.

        # [Problems]
        # This results in possible state alignment issues. For example, after
        # a series of nodes have been submitted to the orchestrator, the client
        # may face issues where previously cached attributes unintentionally
        # override the current values!

        # [Solution]
        # Instead of implementing custom state alignment code, only load in
        # non-default (i.e. no empty declarations) updates.

        configurations = self._compile_configurations()
        updated_parameters = {**configurations, **updates}

        update_resp = self._execute_operation(
            operation="put",
            url=self._generate_single_url(collab_id=collab_id),
            payload=updated_parameters
        )
        self._reset_cache() # Must be resetted here to prevent carry over!
        return update_resp

    
    def delete(self, collab_id: str) -> Dict[str, Any]:
        """ Removes a collaboration's information/configurations previously 
            created from the federated grid

        Args:
            collab_id (str): Identifier of collaboration
        Returns:
            Deleted collaboration record (dict)
        """
        return self._execute_operation(
            operation="delete",
            url=self._generate_single_url(collab_id=collab_id),
            payload=None
        )


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5001
    address = f"http://{host}:{port}"

    collaborations = CollaborationTask(address)
    collab_id_1 = "test_collab_1"
    collab_id_2 = "test_collab_2"

    # Test collaboration creation
    create_response_1 = collaborations.create(collab_id=collab_id_1)
    print("Collaboration 1: Create response:", create_response_1)

    collaborations.configure_logger(
        host="111.222.333.444",
        port=9000,
        sysmetrics_port=9100,
        director_port=9200,
        ttp_port=9300,
        worker_port=9400,
        ui_port=9000,
        secure=True
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
    collaborations.configure_mlops(
        host="222.222.222.222",
        port=9876,
        ui_port=9877,
        secure=False
    )
    update_response_1 = collaborations.update(collab_id=collab_id_1)
    print("Collaboration 1: Update response:", update_response_1)

    collaborations.configure_meter(
        host="333.333.333.333",
        port=15790,
        ui_port=15791,
        secure=True
    )
    update_response_2 = collaborations.update(collab_id=collab_id_2)
    print("Collaboration 2: Update response:", update_response_2)

    # Test collaboration deletion
    delete_response_1 = collaborations.delete(collab_id=collab_id_1)
    print("Collaboration 1: delete response:", delete_response_1)

    delete_response_2 = collaborations.delete(collab_id=collab_id_2)
    print("Collaboration 2: delete response:", delete_response_2)

    print("Collaboration left:", collaborations.read_all()) 
