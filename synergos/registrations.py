#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
import logging
from typing import Dict

# Libs


# Custom
from .base import BaseTask
from .endpoints import REGISTRATION_ENDPOINTS

##################
# Configurations #
##################


##############################################
# Registration task Class - RegistrationTask #
##############################################

class RegistrationTask(BaseTask):
    """ Interfacing class governing all registration-related interactions with 
        the remote Synergos grid

    Attributes:
        _type (str): Specifies the type of task
        address (str): Address where Synergos TTP is hosted at
        endpoints (str)): All endpoints governed by this task
    """

    def __init__(self, address: str):
        super().__init__(
            _type="registration", 
            address=address,
            endpoints=REGISTRATION_ENDPOINTS
        )
        
    ###########
    # Helpers #
    ###########

    def _generate_url(
        self, 
        project_id: str = None, 
        participant_id: str = None
    ) -> str:
        if project_id and participant_id:
            return super()._generate_url(
                endpoint=self.endpoints.REGISTRATION,
                project_id=project_id,
                participant_id=participant_id
            )

        elif project_id and not participant_id:
            return super()._generate_url(
                endpoint=self.endpoints.PROJECT_REGISTRATIONS,
                project_id=project_id
            )

        elif not project_id and participant_id:
            return super()._generate_url(
                endpoint=self.endpoints.PARTICIPANT_REGISTRATIONS,
                participant_id=participant_id
            )

        else:
            raise ValueError("Registrations have dependencies. Specify at least 1 key!")

    ##################
    # Core functions #
    ##################

    def create(
        self,
        project_id: str,
        participant_id: str, 
        role: str,
        **kwargs
    ):
        """ Creates a registration entry for the participant under a specific 
            project in the federated grid

        Args:
            project_id (str): Identifier of project
            participant_id (str): Identifier of participant
            role (str): Role of participant in the federated grid for this 
                particular project. Possible values are 
                1) 'guest'   - Participating to get an enhanced model
                2) 'host'    - Primarily contributing data only
                3) 'arbiter' - Trusted third party overseeing orchestration
            **kwargs
        Returns:
            
        """
        parameters = {'role': role}

        return self._execute_operation(
            operation="post",
            url=self._generate_url(
                project_id=project_id, 
                participant_id=participant_id
            ),
            payload=parameters
        )

    
    def read_all(self, project_id: str = None, participant_id: str = None):
        """ Retrieves information/configurations of all registrations created in 
            the federated grid.
            
            Note:
            AT LEAST ONE KEY MUST BE SPECIFIED! 
            If only the project is specified, retrieve all registrations 
            involving said project. If only the participant is specified, 
            retrieve all registrations involving said participant.

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


    def read(self, project_id: str, participant_id: str):
        """ Retrieves a single registration's information/configurations created
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
        """ Updates a participant's information/configurations created in the 
            federated grid
        
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
        """ Removes a participant's information/configurations previously created 
            from the federated grid

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
    
    # Create reference project
    projects = ProjectTask(address)
    project_id = "test_project"
    projects.create(
        project_id=project_id, 
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

    # Test registration creation
    create_response_1 = registrations.create(
        project_id=project_id,
        participant_id=participant_id_1,
        role='host'
    )
    print("Registration 1: Create response:", create_response_1)

    create_response_2 = registrations.create(
        project_id=project_id,
        participant_id=participant_id_2,
        role='guest'
    )
    print("Registration 2: Create response:", create_response_2)   

    # Test registration retrieval bulk
    project_read_all_response = registrations.read_all(project_id=project_id)
    print("Project perspective - Read all response:", project_read_all_response)  

    participant_read_all_response_1 = registrations.read_all(participant_id=participant_id_1)
    print("Participant 1 perspective - Read all response:", participant_read_all_response_1) 

    participant_read_all_response_2 = registrations.read_all(participant_id=participant_id_2)
    print("Participant 2 perspective - Read all response:", participant_read_all_response_2) 

    # Test registration retrieval single
    single_read_response_1 = registrations.read(
        project_id=project_id,
        participant_id=participant_id_1
    )
    print("Registration 1: Read response:", single_read_response_1)

    single_read_response_2 = registrations.read(
        project_id=project_id,
        participant_id=participant_id_2
    )
    print("Registration 2: Read response:", single_read_response_2)

    # Test registration update
    update_response_1 = registrations.update(
        project_id=project_id,
        participant_id=participant_id_1, 
        role='arbiter'
    )
    print("Registration 1: Update response:", update_response_1)

    update_response_2 = registrations.update(
        project_id=project_id,
        participant_id=participant_id_2, 
        role='host'
    )
    print("Registration 2: Update response:", update_response_2)

    # Test registration deletion
    delete_response_1 = registrations.delete(
        project_id=project_id,
        participant_id=participant_id_1
    )
    print("Registration 1: delete response:", delete_response_1)

    delete_response_2 = registrations.delete(
        project_id=project_id,
        participant_id=participant_id_2
    )
    print("Registration 2: delete response:", delete_response_2)

    print("Registrations left:", registrations.read_all(project_id=project_id)) 

    # Clean up
    projects.delete(project_id=project_id)