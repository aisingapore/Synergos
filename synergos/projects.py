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
from .endpoints import PROJECT_ENDPOINTS

##################
# Configurations #
##################


####################################
# Project task Class - ProjectTask #
####################################

class ProjectTask(BaseTask):
    """ Interfacing class governing all project-related interactions with the 
        remote Synergos grid

    Attributes:
        _type (str): Specifies the type of task
        address (str): Address where Synergos TTP is hosted at
        endpoints (str)): All endpoints governed by this task
    """

    def __init__(self, address: str):
        super().__init__(
            _type="project", 
            address=address,
            endpoints=PROJECT_ENDPOINTS
        )
        
    ###########
    # Helpers #
    ###########

    def _generate_bulk_url(self, collab_id: str) -> str:
        return self._generate_url(
            endpoint=self.endpoints.PROJECTS,
            collab_id=collab_id
        )


    def _generate_single_url(self, collab_id: str, project_id: str) -> str:
        return self._generate_url(
            endpoint=self.endpoints.PROJECT,
            collab_id=collab_id,
            project_id=project_id
        )

    ##################
    # Core functions #
    ##################

    def create(
        self, 
        collab_id: str,
        project_id: str, 
        action: str, 
        incentives: dict, 
        **kwargs
    ):
        """ Registers a project in the federated grid

        Args:
            collab_id (str): Identifier of collaboration
            project_id (str): Identifier of project
            action (str): Type of ML operation to be executed. Supported options
                are as follows:
                1) 'regress': Orchestrates FL grid to perform regression
                2) 'classify': Orchestrates FL grid to perform classification
                3) 'cluster': TBA
                4) 'associate': TBA
            incentives (dict): Tier list for assigning contributions
            **kwargs
        Returns:
            
        """
        parameters = {
            'collab_id': collab_id,
            'project_id': project_id, 
            'action': action,
            'incentives': incentives
        }

        return self._execute_operation(
            operation="post",
            url=self._generate_bulk_url(collab_id=collab_id),
            payload=parameters
        )

    
    def read_all(self, collab_id: str):
        """ Retrieves information/configurations of all projects created in the
            federated grid

        Args:
            collab_id (str): Identifier of collaboration
        Returns:

        """
        return self._execute_operation(
            operation="get",
            url=self._generate_bulk_url(collab_id=collab_id),
            payload=None
        )


    def read(self, collab_id: str, project_id: str):
        """ Retrieves a single project's information/configurations created in 
            the federated grid

        Args:
            collab_id (str): Identifier of collaboration
            project_id (str): Identifier of project
        Returns:

        """
        return self._execute_operation(
            operation="get",
            url=self._generate_single_url(
                collab_id=collab_id,
                project_id=project_id
            ),
            payload=None
        )
    
    
    def update(self, collab_id: str, project_id: str, **updates):
        """ Updates a project's information/configurations created in the 
            federated grid
        
        Args:
            collab_id (str): Identifier of collaboration
            project_id (str): Identifier of project
            **updates: Keyword pairs of parameters to be updated
        Returns:

        """
        return self._execute_operation(
            operation="put",
            url=self._generate_single_url(
                collab_id=collab_id,
                project_id=project_id
            ),
            payload=updates
        )

    
    def delete(self, collab_id: str, project_id: str):
        """ Removes a project's information/configurations previously created 
            from the federated grid

        Args:
            collab_id (str): Identifier of collaboration
            project_id (str): Identifier of project
        Returns:

        """
        return self._execute_operation(
            operation="delete",
            url=self._generate_single_url(
                collab_id=collab_id,
                project_id=project_id
            ),
            payload=None
        )


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000
    address = f"http://{host}:{port}"

    from .collaborations import CollaborationTask

    # Create a reference collaboration
    collaborations = CollaborationTask(address)
    collab_id = "test_collab"
    collaborations.create(collab_id=collab_id)

    projects = ProjectTask(address)
    project_id_1 = "test_project_1"
    project_id_2 = "test_project_2"

    # Test project creation
    create_response_1 = projects.create(
        collab_id=collab_id,
        project_id=project_id_1,
        action="classify",
        incentives={
            'tier_1': [],
            'tier_2': [],
            'tier_3': []
        }
    )
    print("Project 1: Create response:", create_response_1)

    create_response_2 = projects.create(
        collab_id=collab_id,
        project_id=project_id_2,
        action='regress',
        incentives={
            'tier_1': [],
            'tier_2': [],
            'tier_3': []
        }
    )
    print("Project 2: Create response:", create_response_2)   

    # Test project retrieval bulk
    read_all_response = projects.read_all(collab_id=collab_id)
    print("Read all response:", read_all_response)  

    # Test project retrieval single
    read_response_1 = projects.read(
        collab_id=collab_id,
        project_id=project_id_1
    )
    print("Project 1: Read response:", read_response_1)

    read_response_2 = projects.read(
        collab_id=collab_id,
        project_id=project_id_2
    )
    print("Project 2: Read response:", read_response_2)

    # Test project update
    update_response_1 = projects.update(
        collab_id=collab_id,
        project_id=project_id_1, 
        incentives={
            'tier_1': ["worker_1"],
            'tier_2': ["worker_1"],
            'tier_3': ["worker_1"]
        }
    )
    print("Project 1: Update response:", update_response_1)

    update_response_2 = projects.update(
        collab_id=collab_id,
        project_id=project_id_2,
        incentives={
            'tier_1': ["worker_2"],
            'tier_2': ["worker_2"],
            'tier_3': ["worker_2"]
        } 
    )
    print("Project 2: Update response:", update_response_2)

    # Test project deletion
    delete_response_1 = projects.delete(
        collab_id=collab_id,
        project_id=project_id_1
    )
    print("Project 1: delete response:", delete_response_1)

    delete_response_2 = projects.delete(
        collab_id=collab_id,
        project_id=project_id_2
    )
    print("Project 2: delete response:", delete_response_2)

    print("Projects left:", projects.read_all(collab_id=collab_id)) 

    # Clean up
    collaborations.delete(collab_id=collab_id)
