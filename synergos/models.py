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
from .endpoints import MODEL_ENDPOINTS

##################
# Configurations #
##################


################################
# Model task Class - ModelTask #
################################

class ModelTask(BaseTask):
    """ Interfacing class governing all model-related interactions with 
        the remote Synergos grid.

        Note: 
        This is a phase 2 process (i.e. training), meaning that unlike those in 
        phase 1 (i.e. connection), the objective is to trigger a remote process.
        Hence, options to update or delete attributes are removed, since the
        system detects and adapts to base configurations dynamically.
        

    Attributes:
        _type (str): Specifies the type of task
        address (str): Address where Synergos TTP is hosted at
        endpoints (str)): All endpoints governed by this task
    """

    def __init__(self, address: str):
        super().__init__(
            _type="model", 
            address=address,
            endpoints=MODEL_ENDPOINTS
        )
        
    ###########
    # Helpers #
    ###########

    def _generate_url(
        self, 
        collab_id: str,
        project_id: str, 
        expt_id: str = None,
        run_id: str = None,
    ) -> str:
        if collab_id and project_id and expt_id and run_id:
            return super()._generate_url(
                endpoint=self.endpoints.RUN_COMBINATION,
                collab_id=collab_id,
                project_id=project_id,
                expt_id=expt_id,
                run_id=run_id
            )

        elif collab_id and project_id and expt_id:
            return super()._generate_url(
                endpoint=self.endpoints.EXPERIMENT_COMBINATIONS,
                collab_id=collab_id,
                project_id=project_id,
                expt_id=expt_id
            )

        elif collab_id and project_id:
            return super()._generate_url(
                endpoint=self.endpoints.PROJECT_COMBINATIONS,
                collab_id=collab_id,
                project_id=project_id
            )

        else:
            raise ValueError("Training triggers are restricted to the project scope. Specify at least 1 valid project!")


    ##################
    # Core functions #
    ##################

    def create(
        self, 
        collab_id: str,
        project_id: str, 
        expt_id: str = None,
        run_id: str = None,
        auto_align: bool = True,
        dockerised: bool = True,
        verbose: bool = True,
        log_msgs: bool = True,
        **kwargs
    ):
        """ Triggers multiple feature alignment for the participant under a 
            specific project in the federated grid

        Args:
            collab_id (str): Identifier of collaboration
            project_id (str): Identifier of project
            expt_id (str): Identifier of experiment run is under
            run_id (str): Identifier of run
            auto_align (bool): Toggles if multiple feature alignments will be used
            dockerised (bool): Toggles if orchestrations are dockerised
            log_msgs (bool): Toggles if computation operations should be logged
            verbose (bool): Toggles verbosity of computation logging
            **kwargs
        Returns:
            
        """
        parameters = {
            "auto_align": auto_align,
            "dockerised": dockerised,
            "verbose": verbose,
            "log_msgs": log_msgs
        }

        return self._execute_operation(
            operation="post",
            url=self._generate_url(
                collab_id=collab_id,
                project_id=project_id,
                expt_id=expt_id,
                run_id=run_id
            ),
            payload=parameters
        )


    def read(
        self,
        collab_id: str, 
        project_id: str, 
        expt_id: str = None,
        run_id: str = None,
    ):
        """ Retrieves a single set of tags' information/configurations created
            in the federated grid

        Args:
            collab_id (str): Identifier of collaboration
            project_id (str): Identifier of project
            expt_id (str): Identifier of experiment run is under
            run_id (str): Identifier of run
        Returns:

        """
        return self._execute_operation(
            operation="get",
            url=self._generate_url(
                collab_id=collab_id,
                project_id=project_id,
                expt_id=expt_id,
                run_id=run_id
            ),
            payload=None
        )
    

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000
    address = f"http://{host}:{port}"

    from .collaborations import CollaborationTask
    from .projects import ProjectTask
    from .experiments import ExperimentTask
    from .runs import RunTask
    from .participants import ParticipantTask
    from .registrations import RegistrationTask
    from .tags import TagTask
    from .alignments import AlignmentTask
    
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

    # Create reference experiments
    experiments = ExperimentTask(address)
    expt_id_1 = "test_expt_1"
    expt_id_2 = "test_expt_2"

    experiments.create(
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

    experiments.create(
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

    # Create reference runs
    runs = RunTask(address)
    run_id_1 = "test_run_1"
    run_id_2 = "test_run_2"

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
        'criterion': "NLLLoss", 
        'lr_scheduler': "CyclicLR", 
        'delta': 0.001,
        'patience': 10,
        'seed': 100,
        'is_snn': False, 
        'precision_fractional': 7,
        'base_lr': 0.0001,
        'max_lr': 0.001
    }
    runs.create(
        collab_id=collab_id,
        project_id=project_id,
        expt_id=expt_id_1,
        run_id=run_id_1,
        **parameter_set_1
    )

    runs.create( # Use default parameter set on model 1
        collab_id=collab_id,
        project_id=project_id,
        expt_id=expt_id_1,
        run_id=run_id_2,
        rounds=2, 
        epochs=1,
        base_lr=0.0005,
        max_lr=0.005,
        criterion="NLLLoss"
    ) 

    runs.create( # Use default parameter set on model 2
        collab_id=collab_id,
        project_id=project_id,
        expt_id=expt_id_2,
        run_id=run_id_2,
        rounds=2, 
        epochs=1,
        base_lr=0.0005,
        max_lr=0.005,
        criterion="NLLLoss"
    ) 

    # Create reference participants
    participants = ParticipantTask(address)
    participant_id_1 = "test_participant_1"
    participant_id_2 = "test_participant_2"

    parameter_set_1 = {}
    participants.create(participant_id=participant_id_1, **parameter_set_1)

    parameter_set_2 = {}
    participants.create(participant_id=participant_id_2, **parameter_set_2)  

    # Create reference registrations
    registrations = RegistrationTask(address)

    registrations.add_node(**{
        'host': '172.17.0.2',
        'port': 8020,
        'f_port': 5000,
        'log_msgs': True,
        'verbose': True
    })
    registrations.create(
        collab_id=collab_id,
        project_id=project_id,
        participant_id=participant_id_1,
        role='host'
    )

    registrations.add_node(**{
        'host': '172.17.0.3',
        'port': 8020,
        'f_port': 5000,
        'log_msgs': True,
        'verbose': True
    })
    registrations.create(
        collab_id=collab_id,
        project_id=project_id,
        participant_id=participant_id_2,
        role='guest'
    )

    # Create reference tags
    tags = TagTask(address)
    tags.create(
        collab_id=collab_id,
        project_id=project_id,
        participant_id=participant_id_1,
        train=[
            ["tabular", "abalone", "data1", "train"]
            # ["tabular", "heart_disease", "data1", "edge_test_misalign"],
            # ["tabular", "heart_disease", "data1", "edge_test_na_slices"]
        ],
        evaluate=[["tabular", "abalone", "data1", "evaluate"]]
    )

    tags.create(
        collab_id=collab_id,
        project_id=project_id,
        participant_id=participant_id_2,
        train=[["tabular", "abalone", "data2", "train"]],
        evaluate=[["tabular", "abalone", "data2", "evaluate"]]
    )

    # Create reference alignments
    alignments = AlignmentTask(address)
    create_response = alignments.create(
        collab_id=collab_id, 
        project_id=project_id
    )
    print("Alignments: Create response:", create_response)
    print(f"Aligned Experiments: {experiments.read_all(collab_id=collab_id, project_id=project_id)}")

    models = ModelTask(address)

    # Test model(s) creation
    create_response_1 = models.create( # A single combination
        collab_id=collab_id,
        project_id=project_id,
        expt_id=expt_id_2,
        run_id=run_id_2
    )
    print("Models: Create response 1:", create_response_1)

    create_response_2 = models.create( # All combinations under an experiment
        collab_id=collab_id,
        project_id=project_id,
        expt_id=expt_id_1
    )
    print("Models: Create response 2:", create_response_2)

    create_response_3 = models.create( # All combinations under a project
        collab_id=collab_id,
        project_id=project_id
    )
    print("Models: Create response 3:", create_response_3)

    # Test model(s) retrieval
    read_response_1 = models.read( # A single combination
        collab_id=collab_id,
        project_id=project_id,
        expt_id=expt_id_2,
        run_id=run_id_2
    )
    print("Models: Read response 1:", read_response_1)

    read_response_2 = models.read( # All combinations under an experiment
        collab_id=collab_id,
        project_id=project_id,
        expt_id=expt_id_1
    )
    print("Models: Read response 2:", read_response_2)

    read_response_3 = models.read( # All combinations under a project
        collab_id=collab_id,
        project_id=project_id
    )
    print("Models: Read response 3:", read_response_3)

    # Clean up
    collaborations.delete(collab_id=collab_id)