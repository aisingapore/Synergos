#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
import logging
import pytest

# Libs


# Custom
from synergos import (
    ProjectTask,
    ExperimentTask,
    RunTask,
    ParticipantTask,
    RegistrationTask,
    TagTask,
    AlignmentTask,
    ModelTask,
    OptimizationTask,
    ValidationTask,
    PredictionTask,
    Driver
)

##################
# Configurations #
##################

HOST = '0.0.0.0'
PORT = '5000'
IS_SECURED = False
ADDRESS = f"https://{HOST}:{PORT}" if IS_SECURED else f"http://{HOST}:{PORT}"

project_id = "test_project"
expt_id_1 = "test_expt_1"
expt_id_2 = "test_expt_2"
run_id_1 = "test_run_1"
run_id_2 = "test_run_2"
participant_id_1 = "test_participant_1"
participant_id_2 = "test_participant_2"

PROJECT_KEY = {'project_id': project_id}
EXPT_KEY_1 = {'project_id': project_id, 'expt_id': expt_id_1}
EXPT_KEY_2 = {'project_id': project_id, 'expt_id': expt_id_2}
RUN_KEY_1 = {'project_id': project_id, 'expt_id': expt_id_1, 'run_id': run_id_1}
RUN_KEY_2 = {'project_id': project_id, 'expt_id': expt_id_1, 'run_id': run_id_2}
RUN_KEY_3 = {'project_id': project_id, 'expt_id': expt_id_2, 'run_id': run_id_2}
PARTICIPANT_KEY_1 = {'participant_id': participant_id_1}
PARTICIPANT_KEY_2 = {'participant_id': participant_id_2}
REG_KEY_1 = {'project_id': project_id, 'participant_id': participant_id_1}
REG_KEY_2 = {'project_id': project_id, 'participant_id': participant_id_2}
TAG_KEY_1 = {'project_id': project_id, 'participant_id': participant_id_1}
TAG_KEY_2 = {'project_id': project_id, 'participant_id': participant_id_2}

###########
# Helpers #
###########

def check_resp_structure(resp):
    assert 'apiVersion' in resp.keys()
    assert 'success' in resp.keys()
    assert 'status' in resp.keys()
    assert 'method' in resp.keys()
    assert 'params' in resp.keys()


def check_availability_in_single_archive(payload, archive):
    for key, value in payload.items():
        if "_id" not in key:
            assert value == archive[key]


def check_availability_in_bulk_archives(payloads, archives):
    assert len(archives) == len(payloads)
    for archive in archives:
        is_valid = False
        for payload in payloads:
            try:
                check_availability_in_single_archive(
                    payload=payload, 
                    archive=archive
                )
                is_valid = True
                break
            except AssertionError:
                continue
        assert is_valid

######################
# Component Fixtures #
######################

@pytest.fixture
def init_params():
    return {
        'host': HOST, 
        'port': PORT, 
        'is_secured': IS_SECURED, 
        'address': ADDRESS
    }


@pytest.fixture
def payloads():
    project_payload = {
        **PROJECT_KEY, 
        'action': "classify",
        'incentives': {
            'tier_1': [],
            'tier_2': []
        }
    }

    expt_payload_1 = {
        **EXPT_KEY_1,
        'model': [
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
    }
    expt_payload_2 = {
        **EXPT_KEY_2,
        'model': [
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
    }

    param_set_1 = {
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
        'criterion': "MSELoss", 
        'lr_scheduler': "CyclicLR", 
        'delta': 0.001,
        'patience': 10,
        'seed': 100,
        'is_snn': False, 
        'precision_fractional': 7,
        'base_lr': 0.0001,
        'max_lr': 0.001
    }
    param_set_2 = {
        'rounds': 2, 
        'epochs': 1,
        'base_lr': 0.0005,
        'max_lr': 0.005,
        'criterion': "NLLLoss"
    }
    run_payload_1 = {**RUN_KEY_1, **param_set_1}
    run_payload_2 = {**RUN_KEY_2, **param_set_2}
    run_payload_3 = {**RUN_KEY_3, **param_set_2}

    participant_payload_1 = {
        **PARTICIPANT_KEY_1,
        'host': '172.17.0.2',
        'port': 8020,
        'f_port': 5000,
        'log_msgs': True,
        'verbose': True
    }
    participant_payload_2 = {
        **PARTICIPANT_KEY_2,
        'host': '172.17.0.3',
        'port': 8020,
        'f_port': 5000,
        'log_msgs': True,
        'verbose': True
    }

    registration_payload_1 = {**REG_KEY_1, 'role': "host"}
    registration_payload_2 = {**REG_KEY_2, 'role': "guest"}

    tag_payload_1 = {
        **TAG_KEY_1,
        'train': [
            ["non_iid_1"], 
            ["edge_test_missing_coecerable_vals"],
            ["edge_test_misalign"],
            ["edge_test_na_slices"]
        ],
        'evaluate': [["iid_1"]]
    }
    tag_payload_2 = {
        **TAG_KEY_2,
        'train': [["non_iid_2"]]
    }

    alignment_payload = {**PROJECT_KEY}

    # Specific combination: project|expt_2|run_2
    combination_single_payload = {**RUN_KEY_3}
    
    # All combinations under expt_1
    combination_expts_payload = {**EXPT_KEY_1}
    
    # All combinations under project
    combination_project_payload = {**PROJECT_KEY}

    prediction_payload_1 = {
        'tags': {"test_project": [["iid_2"]]},
        'participant_id': "test_participant_2",
        **combination_single_payload
    }
    prediction_payload_2 = {
        'tags': {"test_project": [["iid_2"]]},
        'participant_id': "test_participant_2",
        **combination_expts_payload
    }
    prediction_payload_3 = {
        'tags': {"test_project": [["iid_2"]]},
        'participant_id': "test_participant_2",
        **combination_project_payload
    }

    return {
        'project': [project_payload],
        'experiment': [expt_payload_1, expt_payload_2],
        'run': [run_payload_1, run_payload_2, run_payload_3],
        'participant': [participant_payload_1, participant_payload_2],
        'registration': [registration_payload_1, registration_payload_2],
        'tag': [tag_payload_1, tag_payload_2],
        'alignment': [alignment_payload],
        'model': [
            combination_single_payload, 
            combination_expts_payload, 
            combination_project_payload
        ],
        'validation': [
            combination_single_payload, 
            combination_expts_payload, 
            combination_project_payload
        ],
        'prediction': [
            prediction_payload_1, 
            prediction_payload_2, 
            prediction_payload_3
        ]
    }


@pytest.fixture
def project_task():
    return ProjectTask(address=ADDRESS)


@pytest.fixture
def experiment_task():
    return ExperimentTask(address=ADDRESS)


@pytest.fixture
def run_task():
    return RunTask(address=ADDRESS)


@pytest.fixture
def participant_task():
    return ParticipantTask(address=ADDRESS)


@pytest.fixture
def registration_task():
    return RegistrationTask(address=ADDRESS)


@pytest.fixture
def tag_task():
    return TagTask(address=ADDRESS)


@pytest.fixture
def alignment_task():
    return AlignmentTask(address=ADDRESS)


@pytest.fixture
def model_task():
    return ModelTask(address=ADDRESS)


@pytest.fixture
def optimization_task():
    return OptimizationTask(address=ADDRESS)


@pytest.fixture
def validation_task():
    return ValidationTask(address=ADDRESS)


@pytest.fixture
def prediction_task():
    return PredictionTask(address=ADDRESS)


@pytest.fixture
def driver():
    return Driver(host=HOST, port=PORT, is_secured=IS_SECURED)
