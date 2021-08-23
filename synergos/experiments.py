#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
import logging
from typing import Dict, List, Union

# Libs


# Custom
from .base import BaseTask
from .endpoints import EXPERIMENT_ENDPOINTS

##################
# Configurations #
##################


##########################################
# Experiment task Class - ExperimentTask #
##########################################

class ExperimentTask(BaseTask):
    """ Interfacing class governing all experiment-related interactions with the 
        remote Synergos grid

    Attributes:
        _type (str): Specifies the type of task
        address (str): Address where Synergos TTP is hosted at
        endpoints (str)): All endpoints governed by this task
    """

    def __init__(self, address: str):
        super().__init__(
            _type="experiment", 
            address=address,
            endpoints=EXPERIMENT_ENDPOINTS
        )
        
    ###########
    # Helpers #
    ###########

    def _generate_bulk_url(self, collab_id: str, project_id: str) -> str:
        return self._generate_url(
            endpoint=self.endpoints.EXPERIMENTS,
            collab_id=collab_id,
            project_id=project_id
        )

    def _generate_single_url(
        self,
        collab_id: str, 
        project_id: str, 
        expt_id: str
    ) -> str:
        return self._generate_url(
            endpoint=self.endpoints.EXPERIMENT,
            collab_id=collab_id,
            project_id=project_id,
            expt_id=expt_id
        )

    ##################
    # Core functions #
    ##################

    def create(
        self, 
        collab_id: str,
        project_id: str, 
        expt_id: str,
        model: List[Dict[str, Union[str, bool, int, float]]],
        **kwargs
    ):
        """ Registers an experiment in the federated grid

        Args:
            collab_id (str): Identifier of collaboration
            project_id (str): Identifier of project experiment is under
            expt_id (str): Identifier of experiment
            model (list): Layer architectures of an experiment model
            **kwargs
        Returns:
            
        """
        parameters = {'expt_id': expt_id, 'model': model}

        return self._execute_operation(
            operation="post",
            url=self._generate_bulk_url(
                collab_id=collab_id,
                project_id=project_id
            ),
            payload=parameters
        )

    
    def read_all(self, collab_id: str, project_id: str):
        """ Retrieves information/configurations of all experiments created in 
            the federated grid under a specific project

        Args:
            collab_id (str): Identifier of collaboration
            project_id (str): Identifier of project experiment is under
        Returns:

        """
        return self._execute_operation(
            operation="get",
            url=self._generate_bulk_url(
                collab_id=collab_id,
                project_id=project_id
            ),
            payload=None
        )


    def read(self, collab_id: str, project_id: str, expt_id: str):
        """ Retrieves a single experiment's information/configurations created 
            in the federated grid under a specific project

        Args:
            collab_id (str): Identifier of collaboration
            project_id (str): Identifier of project experiment is under
            expt_id (str): Identifier of experiment
        Returns:

        """
        return self._execute_operation(
            operation="get",
            url=self._generate_single_url(
                collab_id=collab_id,
                project_id=project_id, 
                expt_id=expt_id
            ),
            payload=None
        )
    
    
    def update(self, collab_id: str, project_id: str, expt_id: str, **updates):
        """ Updates an experiment's information/configurations created in the 
            federated grid under a specific project
        
        Args:
            collab_id (str): Identifier of collaboration
            project_id (str): Identifier of project experiment is under
            expt_id (str): Identifier of experiment
            **updates: Keyword pairs of parameters to be updated
        Returns:

        """
        return self._execute_operation(
            operation="put",
            url=self._generate_single_url(
                collab_id=collab_id,
                project_id=project_id, 
                expt_id=expt_id
            ),
            payload=updates
        )

    
    def delete(self, collab_id: str, project_id: str, expt_id: str):
        """ Removes an experiment's information/configurations previously 
            created from the federated grid

        Args:
            collab_id (str): Identifier of collaboration
            project_id (str): Identifier of project experiment is under
            expt_id (str): Identifier of experiment
        Returns:

        """
        return self._execute_operation(
            operation="delete",
            url=self._generate_single_url(
                collab_id=collab_id,
                project_id=project_id, 
                expt_id=expt_id
            ),
            payload=None
        )


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5001
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
        action='classify',
        incentives={
            'tier_1': [],
            'tier_2': []
        }
    )

    experiments = ExperimentTask(address)
    expt_id_1 = "test_expt_1"
    expt_id_2 = "test_expt_2"

    # Test experiment creation
    create_response_1 = experiments.create(
        collab_id=collab_id,
        project_id=project_id,
        expt_id=expt_id_1,
        model=[
            {
                "activation": "sigmoid",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 15,
                    "out_features": 1
                }
            }
        ]
    )
    print("Experiment 1: Create response:", create_response_1)

    create_response_2 = experiments.create(
        collab_id=collab_id,
        project_id=project_id,
        expt_id=expt_id_2,
        model=[
            {
                "activation": "sigmoid",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 30,
                    "out_features": 20
                }
            },
            {
                "activation": "sigmoid",
                "is_input": False,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 20,
                    "out_features": 10
                }
            },
            {
                "activation": "sigmoid",
                "is_input": False,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 10,
                    "out_features": 1
                }
            }
        ]
    ) 
    print("Experiment 2: Create response:", create_response_2)

    # Test experiment retrieval bulk
    read_all_response = experiments.read_all(
        collab_id=collab_id,
        project_id=project_id
    )
    print("Read all response:", read_all_response)  

    # Test experiment retrieval single
    read_response_1 = experiments.read(
        collab_id=collab_id,
        project_id=project_id,
        expt_id=expt_id_1
    )
    print("Experiment 1: Read response:", read_response_1)

    read_response_2 = experiments.read(
        collab_id=collab_id,
        project_id=project_id,
        expt_id=expt_id_2
    )
    print("Experiment 2: Read response:", read_response_2)

    # Test experiment update
    update_response_1 = experiments.update(
        collab_id=collab_id,
        project_id=project_id,
        expt_id=expt_id_1,
        model=[
            {
                "activation": "sigmoid",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 20,
                    "out_features": 10
                }
            },
            {
                "activation": "sigmoid",
                "is_input": False,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 10,
                    "out_features": 1
                }
            }
        ]
    )
    print("Experiment 1: Update response:", update_response_1)

    update_response_2 = experiments.update(
        collab_id=collab_id,
        project_id=project_id,
        expt_id=expt_id_2,
        model=[
            {
                "activation": "relu",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": False,
                    "in_features": 15,
                    "out_features": 1
                }
            }
        ] 
    )
    print("Experiment 2: Update response:", update_response_2)

    # Test experiment deletion
    delete_response_1 = experiments.delete(
        collab_id=collab_id,
        project_id=project_id, 
        expt_id=expt_id_1
    )
    print("Experiment 1: delete response:", delete_response_1)

    delete_response_2 = experiments.delete(
        collab_id=collab_id,
        project_id=project_id, 
        expt_id=expt_id_2
    )
    print("Experiment 2: delete response:", delete_response_2)

    print("Experiments left:", experiments.read_all(
        collab_id=collab_id, 
        project_id=project_id
    ))

    # Clean up
    collaborations.delete(collab_id=collab_id)