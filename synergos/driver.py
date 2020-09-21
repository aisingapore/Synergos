#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
import logging

# Libs


# Custom
from .projects import ProjectTask
from .experiments import ExperimentTask
from .runs import RunTask
from .participants import ParticipantTask
from .registrations import RegistrationTask
from .tags import TagTask
from .alignments import AlignmentTask
from .models import ModelTask
from .optimizations import OptimizationTask
from .validations import ValidationTask
from .predictions import PredictionTask

##################
# Configurations #
##################


###################################
# Task Interfacing Class - Driver #
###################################

class Driver:
    """ Main wrapper class that consolidates all tasks under a single 
        abstraction layer.

    Attributes:
        host (str): IP where Synergos TTP are hosted at
        port (int): Port where Synergos TTP REST service is hosted on
        is_secured (bool): Toggles whether a secured connection is used 
                           (i.e. HTTPS if True, HTTP if False)
    """
    def __init__(self, host: str, port: int, is_secured: bool = False):
        self.host = host
        self.port = port
        self.is_secured = is_secured


    @property
    def address(self):
        if self.is_secured:
            return f"https://{self.host}:{self.port}"
        else:
            return f"http://{self.host}:{self.port}"

    @property
    def projects(self):
        return ProjectTask(address=self.address)

    @property
    def experiments(self):
        return ExperimentTask(address=self.address)

    @property
    def runs(self):
        return RunTask(address=self.address)

    @property
    def participants(self):
        return ParticipantTask(address=self.address)

    @property
    def registrations(self):
        return RegistrationTask(address=self.address)

    @property
    def tags(self):
        return TagTask(address=self.address)

    @property
    def alignments(self):
        return AlignmentTask(address=self.address)

    @property
    def models(self):
        return ModelTask(address=self.address)

    # @property
    # def optimizations(self):
    #     return OptimizationTask(address=self.address)

    @property
    def validations(self):
        return ValidationTask(address=self.address)

    @property
    def predictions(self):
        return PredictionTask(address=self.address)


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000

    driver = Driver(host=host, port=port)
    
    # Create project
    driver.projects.create(
        project_id="test_project",
        action="classify",
        incentives={
            'tier_1': [],
            'tier_2': [],
            'tier_3': []
        }
    )

    # Create experiment
    driver.experiments.create(
        project_id="test_project",
        expt_id="test_experiment",
        model=[
            {
                "activation": "sigmoid",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 15, # Arbitrary, will replaced dynamically
                    "out_features": 1  # Arbitrary, will replaced dynamically
                }
            }
        ]
    )

    # driver.experiments.create(
    #     project_id="test_project",
    #     expt_id="test_experiment",
    #     model=[
    #         {
    #             "activation": "sigmoid",
    #             "is_input": True,
    #             "l_type": "Linear",
    #             "structure": {
    #                 "bias": True,
    #                 "in_features": 15,
    #                 "out_features": 1
    #             }
    #         }
    #     ]
    # )

    # Create run
    driver.runs.create(
        project_id="test_project",
        expt_id="test_experiment",
        run_id="test_run",
        rounds=2, 
        epochs=1,
        base_lr=0.0005,
        max_lr=0.005,
        criterion="NLLLoss"#"BCELoss"
    )

    # Create participant(s)
    driver.participants.create(
        participant_id="test_participant_1",
        host='172.17.0.2',
        port=8020,
        f_port=5000,
        log_msgs=True,
        verbose=True
    )

    driver.participants.create(
        participant_id="test_participant_2",
        host='172.17.0.3',
        port=8020,
        f_port=5000,
        log_msgs=True,
        verbose=True
    )

    # Create registration(s)
    driver.registrations.create(
        project_id="test_project",
        participant_id="test_participant_1",
        role="guest"
    )

    driver.registrations.create(
        project_id="test_project",
        participant_id="test_participant_2",
        role="host"
    )

    # Create tag(s)
    driver.tags.create(
        project_id="test_project",
        participant_id="test_participant_1",
        train=[
            # ["non_iid_1"], 
            # ["edge_test_missing_coecerable_vals"],
            ["edge_test_misalign"],
            ["edge_test_na_slices"]
        ],
        evaluate=[["iid_1"]]
    )

    driver.tags.create(
        project_id="test_project",
        participant_id="test_participant_2",
        train=[["non_iid_2"]]
    )
    
    # driver.tags.create(
    #     project_id="test_project",
    #     participant_id="test_participant_1",
    #     train=[['train']],
    #     evaluate=[["evaluate"]]
    # )

    # driver.tags.create(
    #     project_id="test_project",
    #     participant_id="test_participant_2",
    #     train=[['train']],
    #     evaluate=[["evaluate"]]
    # )

    # Create alignment(s)
    driver.alignments.create(project_id="test_project")

    # Create model(s)
    model_resp = driver.models.create(
        project_id="test_project",
        expt_id="test_experiment",
        run_id="test_run"
    )
    print(f"Model response: {model_resp}")

    # Perform validation(s)
    valid_resp = driver.validations.create(
        project_id="test_project",
        expt_id="test_experiment",
        run_id="test_run"
    )
    print(f"Validation response: {valid_resp}")

    # Perform prediction(s)
    pred_resp = driver.predictions.create(
        tags={"test_project": [["iid_1"]]},
        participant_id="test_participant_1",
        project_id="test_project",
        expt_id="test_experiment",
        run_id="test_run"
    )

    # # Perform prediction(s)
    # pred_resp = driver.predictions.create(
    #     tags={"test_project": [["predict"]]},
    #     participant_id="test_participant_1",
    #     project_id="test_project",
    #     expt_id="test_experiment",
    #     run_id="test_run"
    # )

    print(f"Prediction response: {pred_resp}")