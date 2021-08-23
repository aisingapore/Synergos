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
from .endpoints import RUN_ENDPOINTS

##################
# Configurations #
##################


############################
# Run task Class - RunTask #
############################

class RunTask(BaseTask):
    """ Interfacing class governing all run-related interactions with the 
        remote Synergos grid

    Attributes:
        _type (str): Specifies the type of task
        address (str): Address where Synergos TTP is hosted at
        endpoints (str)): All endpoints governed by this task
    """

    def __init__(self, address: str):
        super().__init__(
            _type="run", 
            address=address,
            endpoints=RUN_ENDPOINTS
        )
        
    ###########
    # Helpers #
    ###########

    def _generate_bulk_url(
        self, 
        collab_id: str, 
        project_id: str, 
        expt_id: str
    ) -> str:
        return self._generate_url(
            endpoint=self.endpoints.RUNS,
            collab_id=collab_id,
            project_id=project_id,
            expt_id=expt_id
        )


    def _generate_single_url(
        self, 
        collab_id: str,
        project_id: str,
        expt_id: str,
        run_id: str
    ) -> str:
        return self._generate_url(
            endpoint=self.endpoints.RUN,
            collab_id=collab_id,
            project_id=project_id,
            expt_id=expt_id,
            run_id=run_id
        )

    ##################
    # Core functions #
    ##################

    def create(
        self, 
        collab_id: str,
        project_id: str, 
        expt_id: str,
        run_id: str,
        algorithm: str = "FedProx", 
        batch_size: int = None, 
        rounds: int = 10, 
        epochs: int = 100,
        lr: float = 0.001, 
        weight_decay: float = 0.0,
        lr_decay: float = 0.1, 
        mu: float = 0.1, 
        l1_lambda: float = 0.0, 
        l2_lambda: float = 0.0,
        optimizer: str = "SGD", 
        criterion: str = "BCELoss", 
        lr_scheduler: str = "CyclicLR", 
        delta: float = 0.0,
        patience: int = 10,
        seed: int = 42,
        is_condensed: bool = True,
        is_snn: bool = False, 
        precision_fractional: int = 5,
        **kwargs
    ):
        """ Registers a run in the federated grid for a specific experiment 
            under a specific project

        Args:
            collab_id (str): Identifier of collaboration
            project_id (str): Identifier of project experiment is under
            expt_id (str): Identifier of experiment
            model (list): Layer architectures of an experiment model
            algorithm (str): Algorithm to use for federated training 
            batch_size (int): Batch size of data to use for federated training 
            rounds (int): No. of global rounds of federated training to execute  
            epochs (int): No. of local epochs of local training to execute
            lr (float): Learning rate to use for federated training 
            weight_decay (float): Deprecated artifact for L2 regularization used
                by PyTorch optimizers. Set l2_lambda instead.
            lr_decay (float): Learning rate decay for adapting learning rate 
            mu (float): Fedprox regularization coefficient
            l1_lambda (float): L1 regularization coefficient
            l2_lambda (float): L2 regularization coefficient
            optimizer (str): Optimizer to use for federated training 
            criterion (str): Criterion to use for federated training 
            lr_scheduler (str): Learning rate scheduler chosen for adapting lr 
            delta (float): Minimum loss difference required to be considered as 
                a successful round/epoch of training.
            patience (int): No. of buffer rounds to allow performance stagnation
                before early stopping takes effect
            seed (int): Seed for locking random states in the federated grid
            is_snn (bool): Toggles if split neural networks are to be used in
                place of regular federated aggregation variants 
            precision_fractional (int): Minimum decimal precision required when
                enforcing encryption methods (i.e. SMPC and/or HE)
            **kwargs
        Returns:
            
        """
        parameters = {
            'run_id': run_id, 
            'algorithm': algorithm, 
            'batch_size': batch_size, 
            'rounds': rounds, 
            'epochs':epochs,
            'lr': lr, 
            'weight_decay': weight_decay,
            'lr_decay': lr_decay, 
            'mu': mu, 
            'l1_lambda': l1_lambda, 
            'l2_lambda': l2_lambda,
            'optimizer': optimizer, 
            'criterion': criterion, 
            'lr_scheduler': lr_scheduler, 
            'delta': delta,
            'patience': patience,
            'seed': seed,
            'is_snn': is_snn, 
            'precision_fractional': precision_fractional,
        }
        # Prune null default values
        parameters = {k:v for k,v in parameters.items() if v is not None} 
        parameters.update(kwargs)

        return self._execute_operation(
            operation="post",
            url=self._generate_bulk_url(
                collab_id=collab_id,
                project_id=project_id, 
                expt_id=expt_id
            ),
            payload=parameters
        )

    
    def read_all(self, collab_id: str, project_id: str, expt_id: str):
        """ Retrieves information/configurations of all runs created in the
            federated grid for an experiment under a specific project

        Args:
            collab_id (str): Identifier of collaboration
            project_id (str): Identifier of project experiment is under
            expt_id (str): Identifier of experiment
        Returns:

        """
        return self._execute_operation(
            operation="get",
            url=self._generate_bulk_url(
                collab_id=collab_id,
                project_id=project_id, 
                expt_id=expt_id
            ),
            payload=None
        )


    def read(self, collab_id: str, project_id: str, expt_id: str, run_id: str):
        """ Retrieves a single run's information/configurations created for an 
            experiment under a specific project

        Args:
            collab_id (str): Identifier of collaboration
            project_id (str): Identifier of project experiment is under
            expt_id (str): Identifier of experiment run is under
            run_id (str): Identifier of run
        Returns:

        """
        return self._execute_operation(
            operation="get",
            url=self._generate_single_url(
                collab_id=collab_id,
                project_id=project_id, 
                expt_id=expt_id,
                run_id=run_id
            ),
            payload=None
        )
    
    
    def update(
        self, 
        collab_id: str, 
        project_id: str, 
        expt_id: str, 
        run_id: str, 
        **updates
    ):
        """ Updates a run's information/configurations created in the federated
            grid
        
        Args:
            collab_id (str): Identifier of collaboration
            project_id (str): Identifier of project experiment is under
            expt_id (str): Identifier of experiment run is under
            run_id (str): Identifier of run
            **updates: Keyword pairs of parameters to be updated
        Returns:

        """
        return self._execute_operation(
            operation="put",
            url=self._generate_single_url(
                collab_id=collab_id,
                project_id=project_id, 
                expt_id=expt_id,
                run_id=run_id
            ),
            payload=updates
        )

    
    def delete(
        self, 
        collab_id: str,
        project_id: str, 
        expt_id: str, 
        run_id: str
    ):
        """ Removes a run's information/configurations previously created from 
            the federated grid

        Args:
            collab_id (str): Identifier of collaboration
            project_id (str): Identifier of project experiment is under
            expt_id (str): Identifier of experiment run is under
            run_id (str): Identifier of run
        Returns:

        """
        return self._execute_operation(
            operation="delete",
            url=self._generate_single_url(
                collab_id=collab_id,
                project_id=project_id, 
                expt_id=expt_id,
                run_id=run_id
            ),
            payload=None
        )


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5001
    address = f"http://{host}:{port}"

    from .collaborations import CollaborationTask
    from .projects import ProjectTask
    from .experiments import ExperimentTask

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

    # Create reference experiment
    experiments = ExperimentTask(address)
    expt_id = "test_experiment"
    experiments.create(
        collab_id=collab_id,
        project_id=project_id,
        expt_id=expt_id,
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

    runs = RunTask(address)
    run_id_1 = "test_run_1"
    run_id_2 = "test_run_2"

    # Test run creation
    parameter_set_1 = {
        'algorithm': "FedProx", 
        'batch_size': 32, 
        'rounds': 2, 
        'epochs': 1,
        'lr': 0.001, 
        'weight_decay': 0.001,
        'lr_decay': 0.001, 
        'mu': 0.001, 
        'l1_lambda': 0.001, 
        'l2_lambda': 0.001,
        'optimizer': "SGD", 
        'criterion': "BCELoss", 
        'lr_scheduler': "CyclicLR", 
        'delta': 0.001,
        'patience': 10,
        'seed': 100,
        'is_snn': False, 
        'precision_fractional': 7,
    }
    create_response_1 = runs.create(
        collab_id=collab_id,
        project_id=project_id,
        expt_id=expt_id,
        run_id=run_id_1,
        **parameter_set_1
    )
    print("Run 1: Create response:", create_response_1)

    create_response_2 = runs.create( # Use default parameter set
        collab_id=collab_id,
        project_id=project_id,
        expt_id=expt_id,
        run_id=run_id_2
    ) 
    print("Run 2: Create response:", create_response_2)

    # Test run retrieval bulk
    read_all_response = runs.read_all(
        collab_id=collab_id,
        project_id=project_id,
        expt_id=expt_id
    )
    print("Read all response:", read_all_response)  

    # Test run retrieval single
    read_response_1 = runs.read(
        collab_id=collab_id,
        project_id=project_id, 
        expt_id=expt_id,
        run_id=run_id_1
    )
    print("Run 1: Read response:", read_response_1)

    read_response_2 = runs.read(
        collab_id=collab_id,
        project_id=project_id, 
        expt_id=expt_id,
        run_id=run_id_2
    )
    print("Run 2: Read response:", read_response_2)

    # Test run update
    update_response_1 = runs.update(
        collab_id=collab_id,
        project_id=project_id,
        expt_id=expt_id,
        run_id=run_id_1,
        batch_size=32, 
        rounds=20, 
        epochs=10,
        lr=0.009 
    )
    print("Run 1: Update response:", update_response_1)

    update_response_2 = runs.update(
        collab_id=collab_id,
        project_id=project_id,
        expt_id=expt_id,
        run_id=run_id_2,
        weight_decay=0,
        lr_decay=0, 
        mu=0, 
        l1_lambda=0, 
        l2_lambda=0
    )
    print("Run 2: Update response:", update_response_2)

    # Test run deletion
    delete_response_1 = runs.delete(
        collab_id=collab_id,
        project_id=project_id, 
        expt_id=expt_id,
        run_id=run_id_1
    )
    print("Run 1: delete response:", delete_response_1)

    delete_response_2 = runs.delete(
        collab_id=collab_id,
        project_id=project_id, 
        expt_id=expt_id,
        run_id=run_id_2
    )
    print("Run 2: delete response:", delete_response_2)

    print("Runs left:", runs.read_all(
        collab_id=collab_id,
        project_id=project_id, 
        expt_id=expt_id
    ))

    # Clean up
    collaborations.delete(collab_id=collab_id)