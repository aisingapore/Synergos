#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
from typing import Dict, List

# Libs


# Custom
from .base import BaseTask
from .endpoints import PARTICIPANT_ENDPOINTS

##################
# Configurations #
##################


############################################
# Participant task Class - ParticipantTask #
############################################

class ParticipantTask(BaseTask):
    """ Interfacing class governing all participant-related interactions with 
        the remote Synergos grid

    Attributes:
        _type (str): Specifies the type of task
        address (str): Address where Synergos TTP is hosted at
        endpoints (str)): All endpoints governed by this task
    """

    def __init__(self, address: str):
        super().__init__(
            _type="participant", 
            address=address,
            endpoints=PARTICIPANT_ENDPOINTS
        )
        
    ###########
    # Helpers #
    ###########

    def _generate_bulk_url(self) -> str:
        return self._generate_url(endpoint=self.endpoints.PARTICIPANTS)

    def _generate_single_url(self, participant_id: str) -> str:
        return self._generate_url(
            endpoint=self.endpoints.PARTICIPANT,
            participant_id=participant_id
        )

    ##################
    # Core functions #
    ##################

    def create(
        self, 
        participant_id: str, 
        category: List[str] = [],
        summary: str = "",
        phone: int = None,
        email: str = None,
        socials: Dict[str, str] = {},
        **kwargs
    ):
        """ Registers a participant in the federated grid

        Args:
            participant_id (str): Identifier of participant
            **kwargs
        Returns:
            
        """
        parameters = {
            'id': participant_id,
            'category': category,
            'summary': summary,
            'phone': phone,
            'email': email,
            'socials': socials
        }

        return self._execute_operation(
            operation="post",
            url=self._generate_bulk_url(),
            payload=parameters
        )

    
    def read_all(self):
        """ Retrieves information/configurations of all participants created in 
            the federated grid

        Returns:

        """
        return self._execute_operation(
            operation="get",
            url=self._generate_bulk_url(),
            payload=None
        )


    def read(self, participant_id: str):
        """ Retrieves a single participant's information/configurations created in 
            the federated grid

        Args:
            participant_id (str): Identifier of participant
        Returns:

        """
        return self._execute_operation(
            operation="get",
            url=self._generate_single_url(participant_id=participant_id),
            payload=None
        )
    
    
    def update(self, participant_id: str, **updates):
        """ Updates a participant's information/configurations created in the 
            federated grid
        
        Args:
            participant_id (str): Identifier of participant
            **updates: Keyword pairs of parameters to be updated
        Returns:

        """
        return self._execute_operation(
            operation="put",
            url=self._generate_single_url(participant_id=participant_id),
            payload=updates
        )

    
    def delete(self, participant_id: str):
        """ Removes a participant's information/configurations previously created 
            from the federated grid

        Args:
            participant_id (str): Identifier of participant
        Returns:

        """
        return self._execute_operation(
            operation="delete",
            url=self._generate_single_url(participant_id=participant_id),
            payload=None
        )


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000
    address = f"http://{host}:{port}"
    
    from .collaborations import CollaborationTask
    from .projects import ProjectTask

    # Create a reference collaboration
    collaborations = CollaborationTask(address)
    collab_id = "test_collab"
    collaborations.create(collab_id=collab_id)

    # Create reference project
    projects = ProjectTask(address)
    project_id = "test_project"
    projects.create(
        collab_id=collab_id,
        project_id=project_id,
        action="classify", 
        incentives={
            'tier_1': [],
            'tier_2': []
        }
    )

    participants = ParticipantTask(address)
    participant_id_1 = "test_participant_1"
    participant_id_2 = "test_participant_2"

    # Test participant creation
    parameter_set_1 = {}
    create_response_1 = participants.create(
        participant_id=participant_id_1,
        **parameter_set_1
    )
    print("Participant 1: Create response:", create_response_1)

    parameter_set_2 = {}
    create_response_2 = participants.create(
        participant_id=participant_id_2,
        **parameter_set_2
    )
    print("Participant 2: Create response:", create_response_2)   

    # Test participant retrieval bulk
    read_all_response = participants.read_all()
    print("Read all response:", read_all_response)  

    # Test participant retrieval single
    read_response_1 = participants.read(participant_id=participant_id_1)
    print("Participant 1: Read response:", read_response_1)

    read_response_2 = participants.read(participant_id=participant_id_2)
    print("Participant 2: Read response:", read_response_2)

    # Test participant update
    update_response_1 = participants.update(
        participant_id=participant_id_1
    )
    print("Participant 1: Update response:", update_response_1)

    update_response_2 = participants.update(
        participant_id=participant_id_2
    )
    print("Participant 2: Update response:", update_response_2)

    # Test participant deletion
    delete_response_1 = participants.delete(participant_id=participant_id_1)
    print("Participant 1: delete response:", delete_response_1)

    delete_response_2 = participants.delete(participant_id=participant_id_2)
    print("Participant 2: delete response:", delete_response_2)

    print("Participants left:", participants.read_all()) 

    # Clean up
    collaborations.delete(collab_id=collab_id)