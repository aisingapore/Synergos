#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
import logging
from typing import Dict, List

# Libs


# Custom
from .base import BaseTask
from .endpoints import TAG_ENDPOINTS

##################
# Configurations #
##################


############################
# Tag task Class - TagTask #
############################

class TagTask(BaseTask):
    """ Interfacing class governing all tag-related interactions with 
        the remote Synergos grid

    Attributes:
        _type (str): Specifies the type of task
        address (str): Address where Synergos TTP is hosted at
        endpoints (str)): All endpoints governed by this task
    """

    def __init__(self, address: str):
        super().__init__(
            _type="tag", 
            address=address,
            endpoints=TAG_ENDPOINTS
        )
        
    ###########
    # Helpers #
    ###########

    def _generate_url(self, project_id: str, participant_id: str) -> str:
        return super()._generate_url(
            endpoint=self.endpoints.TAGS,
            project_id=project_id,
            participant_id=participant_id
        )

    ##################
    # Core functions #
    ##################

    def create(
        self,
        project_id: str,
        participant_id: str, 
        train: List[List[str]],
        evaluate: List[List[str]] = [],
        predict: List[List[str]] = [],
        **kwargs
    ):
        """ Registers tags for the participant under a specific 
            project in the federated grid

        Args:
            project_id (str): Identifier of project
            participant_id (str): Identifier of participant
            train (list(list(str))): Filepath tokens to training data
            evaluate (list(list(str))): Filepath tokens to validation data
            predict (list(list(str))): Filepath tokens to inference data
            **kwargs
        Returns:
            
        """
        parameters = {'train': train, 'evaluate': evaluate, 'predict': predict}

        return self._execute_operation(
            operation="post",
            url=self._generate_url(
                project_id=project_id, 
                participant_id=participant_id
            ),
            payload=parameters
        )


    def read(self, project_id: str, participant_id: str):
        """ Retrieves a single set of tags' information/configurations created
            in the federated grid

        Args:
            project_id (str): Identifier of project
            participant_id (str): Identifier of participant
        Returns:

        """
        return self._execute_operation(
            operation="get",
            url=self._generate_url(
                project_id=project_id, 
                participant_id=participant_id
            ),
            payload=None
        )
    
    
    def update(self, project_id: str, participant_id: str, **updates):
        """ Updates a a single set of tags' information/configurations created 
            in the federated grid
        
        Args:
            project_id (str): Identifier of project
            participant_id (str): Identifier of participant
            **updates: Keyword pairs of parameters to be updated
        Returns:

        """
        return self._execute_operation(
            operation="put",
            url=self._generate_url(
                project_id=project_id, 
                participant_id=participant_id
            ),
            payload=updates
        )

    
    def delete(self, project_id: str, participant_id: str):
        """ Removes a single set of tags' information/configurations previously 
            created from the federated grid

        Args:
            project_id (str): Identifier of project
            participant_id (str): Identifier of participant
        Returns:

        """
        return self._execute_operation(
            operation="delete",
            url=self._generate_url(
                project_id=project_id, 
                participant_id=participant_id
            ),
            payload=None
        )
    

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000
    address = f"http://{host}:{port}"

    from .projects import ProjectTask
    from .participants import ParticipantTask
    from .registrations import RegistrationTask
    
    # Create reference project
    projects = ProjectTask(address)
    project_id = "test_project"
    projects.create(
        project_id=project_id, 
        action="classify",
        incentives={
            'tier_1': [],
            'tier_2': []
        }
    )

    # Create reference participants
    participants = ParticipantTask(address)
    participant_id_1 = "test_participant_1"
    participant_id_2 = "test_participant_2"

    parameter_set_1 = {
        'host': '123.456.789.0',
        'port': 12345,
        'f_port': 6789,
        'log_msgs': True,
        'verbose': True
    }
    participants.create(participant_id=participant_id_1, **parameter_set_1)

    parameter_set_2 = {
        'host': '123.456.789.1',
        'port': 9876,
        'f_port': 54321,
        'log_msgs': True,
        'verbose': True
    }
    participants.create(participant_id=participant_id_2, **parameter_set_2)  

    registrations = RegistrationTask(address)

    # Create reference registrations
    registrations.create(
        project_id=project_id,
        participant_id=participant_id_1,
        role='host'
    )

    registrations.create(
        project_id=project_id,
        participant_id=participant_id_2,
        role='guest'
    )
  
    tags = TagTask(address)

    # Test tag creation
    create_response_1 = tags.create(
        project_id=project_id,
        participant_id=participant_id_1,
        train=[["train"]],
        evaluate=[["evaluate"]]
    )
    print("Tags 1: Create response:", create_response_1)

    create_response_2 = tags.create(
        project_id=project_id,
        participant_id=participant_id_2,
        train=[["train"]],
        evaluate=[["evaluate"]]
    )
    print("Tags 2: Create response:", create_response_2)   

    # Test tag retrieval single
    single_read_response_1 = tags.read(
        project_id=project_id,
        participant_id=participant_id_1
    )
    print("Tags 1: Read response:", single_read_response_1)

    single_read_response_2 = tags.read(
        project_id=project_id,
        participant_id=participant_id_2
    )
    print("Tags 2: Read response:", single_read_response_2)

    # Test tag update
    update_response_1 = tags.update(
        project_id=project_id,
        participant_id=participant_id_1, 
        predict=[["predict"]]
    )
    print("Tags 1: Update response:", update_response_1)

    update_response_2 = tags.update(
        project_id=project_id,
        participant_id=participant_id_2, 
        predict=[["predict"]]
    )
    print("Tags 2: Update response:", update_response_2)

    # Test tag deletion
    delete_response_1 = tags.delete(
        project_id=project_id,
        participant_id=participant_id_1
    )
    print("Tags 1: delete response:", delete_response_1)

    delete_response_2 = tags.delete(
        project_id=project_id,
        participant_id=participant_id_2
    )
    print("Tags 2: delete response:", delete_response_2)

    # Clean up
    projects.delete(project_id=project_id)