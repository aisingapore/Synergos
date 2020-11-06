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

###########
# Helpers #
###########

def generate_minimal_keys(
    project_id: str,
    expt_id_1: str,
    expt_id_2: str,
    run_id_1: str,
    run_id_2: str,
    participant_id_1: str,
    participant_id_2: str
) -> dict:
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
    return (
        PROJECT_KEY, 
        EXPT_KEY_1, EXPT_KEY_2, 
        RUN_KEY_1, RUN_KEY_2, RUN_KEY_3,
        PARTICIPANT_KEY_1, PARTICIPANT_KEY_2, 
        REG_KEY_1, REG_KEY_2, 
        TAG_KEY_1, TAG_KEY_2
    )

def generate_extra_keys(
    project_id: str,
    expt_id_1: str,
    expt_id_2: str,
    expt_id_3: str,
    run_id_1: str,
    run_id_2: str,
    run_id_3: str,
    run_id_4: str,
    run_id_5: str,
    run_id_6: str,
    run_id_7: str,
    participant_id_1: str,
    participant_id_2: str
) -> dict:
    (
        PROJECT_KEY, 
        EXPT_KEY_1, EXPT_KEY_2, 
        RUN_KEY_1, RUN_KEY_2, RUN_KEY_3,
        PARTICIPANT_KEY_1, PARTICIPANT_KEY_2, 
        REG_KEY_1, REG_KEY_2, 
        TAG_KEY_1, TAG_KEY_2
    ) = generate_minimal_keys(
        project_id,
        expt_id_1, expt_id_2,
        run_id_1, run_id_2,
        participant_id_1, participant_id_2
    )

    EXPT_KEY_3 = {'project_id': project_id, 'expt_id': expt_id_2}

    RUN_KEY_4 = {'project_id': project_id, 'expt_id': expt_id_1, 'run_id': run_id_3}
    RUN_KEY_5 = {'project_id': project_id, 'expt_id': expt_id_1, 'run_id': run_id_4}
    RUN_KEY_6 = {'project_id': project_id, 'expt_id': expt_id_1, 'run_id': run_id_5}
    RUN_KEY_7 = {'project_id': project_id, 'expt_id': expt_id_1, 'run_id': run_id_6}
    RUN_KEY_8 = {'project_id': project_id, 'expt_id': expt_id_3, 'run_id': run_id_7}

    return (
        PROJECT_KEY, 
        EXPT_KEY_1, EXPT_KEY_2, EXPT_KEY_3,
        RUN_KEY_1, RUN_KEY_2, RUN_KEY_3, RUN_KEY_4, 
        RUN_KEY_5, RUN_KEY_6, RUN_KEY_7, RUN_KEY_8,
        PARTICIPANT_KEY_1, PARTICIPANT_KEY_2, 
        REG_KEY_1, REG_KEY_2, 
        TAG_KEY_1, TAG_KEY_2
    )

########################
# Integration Fixtures #
########################

@pytest.fixture
def tabular_regress_cycle_payloads():
    project_id = "tabular_regress_project"
    expt_id_1 = "tabular_regress_expt_1"
    expt_id_2 = "tabular_regress_expt_2"
    run_id_1 = "tabular_regress_run_1"
    run_id_2 = "tabular_regress_run_2"
    participant_id_1 = "tabular_regress_participant_1"
    participant_id_2 = "tabular_regress_participant_2"

    (
        PROJECT_KEY, 
        EXPT_KEY_1, EXPT_KEY_2, 
        RUN_KEY_1, RUN_KEY_2, RUN_KEY_3,
        PARTICIPANT_KEY_1, PARTICIPANT_KEY_2, 
        REG_KEY_1, REG_KEY_2, 
        TAG_KEY_1, TAG_KEY_2
    ) = generate_minimal_keys(
        project_id,
        expt_id_1, expt_id_2,
        run_id_1, run_id_2,
        participant_id_1, participant_id_2
    )
    project_payload = {
        **PROJECT_KEY, 
        'action': 'regress',
        'incentives': {
            'tier_1': [],
            'tier_2': []
        }
    }

    expt_payload_1 = {
        **EXPT_KEY_1,
        'model': [
            {
                "activation": None,
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 0,   # placeholder
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
                    "in_features": 0,   # placeholder
                    "out_features": 10
                }
            },
            {
                "activation": "sigmoid",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 10,
                    "out_features": 90
                }
            },
            {
                "activation": "sigmoid",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 90,
                    "out_features": 80
                }
            },
            {
                "activation": "sigmoid",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 80,
                    "out_features": 70
                }
            },
            {
                "activation": "sigmoid",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 70,
                    "out_features": 60
                }
            },
            {
                "activation": "sigmoid",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 60,
                    "out_features": 50
                }
            },
            {
                "activation": "sigmoid",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 50,
                    "out_features": 40
                }
            },
            {
                "activation": "sigmoid",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 40,
                    "out_features": 30
                }
            },
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
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 20,
                    "out_features": 10
                }
            },
            {
                "activation": None,
                "is_input": True,
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
        'batch_size': 500, 
        'rounds': 2, 
        'epochs': 1,
        'lr': 0.01, 
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
        'criterion': "L1Loss"
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
        'train': [["train"]],
        'evaluate': [["evaluate"]]
    }
    tag_payload_2 = {
        **TAG_KEY_2,
        'train': [["train"]],
        'evaluate': [["evaluate"]]
    }

    alignment_payload = {**PROJECT_KEY}

    # Specific combination: project|expt_2|run_2
    combination_single_payload = {**RUN_KEY_1}
    
    # All combinations under expt_1
    combination_expts_payload = {**EXPT_KEY_1}
    
    # All combinations under project
    combination_project_payload = {**PROJECT_KEY}

    prediction_payload_1 = {
        'tags': {project_id: [["predict"]]},
        **PARTICIPANT_KEY_2,
        **combination_single_payload
    }
    prediction_payload_2 = {
        'tags': {project_id: [["predict"]]},
        **PARTICIPANT_KEY_2,
        **combination_expts_payload
    }
    prediction_payload_3 = {
        'tags': {project_id: [["predict"]]},
        **PARTICIPANT_KEY_2,
        **combination_project_payload
    }

    return {
        'project': project_payload,
        'experiment': [expt_payload_1, expt_payload_2],
        'run': [run_payload_1, run_payload_2, run_payload_3],
        'participant': [participant_payload_1, participant_payload_2],
        'registration': [registration_payload_1, registration_payload_2],
        'tag': [tag_payload_1, tag_payload_2],
        'alignment': alignment_payload,
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
def tabular_classify_cycle_binary_payloads():
    project_id = "tabular_classify_binary_project"
    expt_id_1 = "tabular_classify_binary_expt_1"
    expt_id_2 = "tabular_classify_binary_expt_2"
    expt_id_3 = "tabular_classify_binary_expt_3"
    run_id_1 = "tabular_classify_binary_run_1"
    run_id_2 = "tabular_classify_binary_run_2"
    run_id_3 = "tabular_classify_binary_run_3"
    run_id_4 = "tabular_classify_binary_run_4"
    run_id_5 = "tabular_classify_binary_run_5"
    run_id_6 = "tabular_classify_binary_run_6"
    run_id_7 = "tabular_classify_binary_run_7"
    participant_id_1 = "tabular_classify_binary_participant_1"
    participant_id_2 = "tabular_classify_binary_participant_2"

    (
        PROJECT_KEY, 
        EXPT_KEY_1, EXPT_KEY_2, EXPT_KEY_3,
        RUN_KEY_1, RUN_KEY_2, RUN_KEY_3, RUN_KEY_4, 
        RUN_KEY_5, RUN_KEY_6, RUN_KEY_7, RUN_KEY_8,
        PARTICIPANT_KEY_1, PARTICIPANT_KEY_2, 
        REG_KEY_1, REG_KEY_2, 
        TAG_KEY_1, TAG_KEY_2
    ) = generate_extra_keys(
        project_id,
        expt_id_1, expt_id_2, expt_id_3,
        run_id_1, run_id_2, run_id_3, run_id_4, run_id_5, run_id_6, run_id_7,
        participant_id_1, participant_id_2
    )

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
                    "in_features": 0,   # placeholder
                    "out_features": 1   # placeholder
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
                    "in_features": 0,   # placeholder
                    "out_features": 10
                }
            },
            {
                "activation": "sigmoid",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 10,
                    "out_features": 90
                }
            },
            {
                "activation": "sigmoid",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 90,
                    "out_features": 80
                }
            },
            {
                "activation": "sigmoid",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 80,
                    "out_features": 70
                }
            },
            {
                "activation": "sigmoid",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 70,
                    "out_features": 60
                }
            },
            {
                "activation": "sigmoid",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 60,
                    "out_features": 50
                }
            },
            {
                "activation": "sigmoid",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 50,
                    "out_features": 40
                }
            },
            {
                "activation": "sigmoid",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 40,
                    "out_features": 30
                }
            },
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
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 10,
                    "out_features": 1   # Placeholder
                }
            }
        ]
    }
    expt_payload_3 = {
        **EXPT_KEY_3,
        'model': [
            {
                "activation": None,
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 0,   # placeholder
                    "out_features": 1   # placeholder
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
        'criterion': "L1Loss", 
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
        'criterion': "MSELoss"
    }
    param_set_3 = {
        'rounds': 2, 
        'epochs': 1,
        'base_lr': 0.0005,
        'max_lr': 0.005,
        'criterion': "PoissonNLLLoss"
    }
    param_set_4 = {
        'rounds': 2, 
        'epochs': 1,
        'base_lr': 0.0005,
        'max_lr': 0.005,
        'criterion': "KLDivLoss"
    }
    param_set_5 = {
        'rounds': 2, 
        'epochs': 1,
        'base_lr': 0.0005,
        'max_lr': 0.005,
        'criterion': "BCELoss"
    }
    param_set_6 = {
        'rounds': 2, 
        'epochs': 1,
        'base_lr': 0.0005,
        'max_lr': 0.005,
        'criterion': "SmoothL1Loss"
    }
    param_set_7 = {
        'rounds': 2, 
        'epochs': 1,
        'base_lr': 0.0005,
        'max_lr': 0.005,
        'criterion': "BCEWithLogitsLoss"
    }
    run_payload_1 = {**RUN_KEY_1, **param_set_1}
    run_payload_2 = {**RUN_KEY_2, **param_set_2}
    run_payload_3 = {**RUN_KEY_3, **param_set_2}
    run_payload_4 = {**RUN_KEY_4, **param_set_3}
    run_payload_5 = {**RUN_KEY_5, **param_set_4}
    run_payload_6 = {**RUN_KEY_6, **param_set_5}
    run_payload_7 = {**RUN_KEY_7, **param_set_6}
    run_payload_8 = {**RUN_KEY_8, **param_set_7}

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
        'train': [["train"]],
        'evaluate': [["evaluate"]]
    }
    tag_payload_2 = {
        **TAG_KEY_2,
        'train': [["train"]],
        'evaluate': [["evaluate"]]
    }

    alignment_payload = {**PROJECT_KEY}

    # Specific combination: project|expt_2|run_2
    combination_single_payload = {**RUN_KEY_3}
    
    # All combinations under expt_1
    combination_expts_payload = {**EXPT_KEY_1}
    
    # All combinations under project
    combination_project_payload = {**PROJECT_KEY}

    prediction_payload_1 = {
        'tags': {project_id: [["predict"]]},
        **PARTICIPANT_KEY_2,
        **combination_single_payload
    }
    prediction_payload_2 = {
        'tags': {project_id: [["predict"]]},
        **PARTICIPANT_KEY_2,
        **combination_expts_payload
    }
    prediction_payload_3 = {
        'tags': {project_id: [["predict"]]},
        **PARTICIPANT_KEY_2,
        **combination_project_payload
    }

    return {
        'project': project_payload,
        'experiment': [expt_payload_1, expt_payload_2, expt_payload_3],
        'run': [
            run_payload_1, run_payload_2, run_payload_3, run_payload_4,
            run_payload_5, run_payload_6, run_payload_7, run_payload_8
        ],
        'participant': [participant_payload_1, participant_payload_2],
        'registration': [registration_payload_1, registration_payload_2],
        'tag': [tag_payload_1, tag_payload_2],
        'alignment': alignment_payload,
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
def tabular_classify_cycle_multiclass_payloads():
    project_id = "tabular_classify_mulitclass_project"
    expt_id_1 = "tabular_classify_mulitclass_expt_1"
    expt_id_2 = "tabular_classify_mulitclass_expt_2"
    expt_id_3 = "tabular_classify_mulitclass_expt_3"
    run_id_1 = "tabular_classify_mulitclass_run_1"
    run_id_2 = "tabular_classify_mulitclass_run_2"
    run_id_3 = "tabular_classify_mulitclass_run_3"
    run_id_4 = "tabular_classify_mulitclass_run_4"
    run_id_5 = "tabular_classify_mulitclass_run_5"
    run_id_6 = "tabular_classify_mulitclass_run_6"
    run_id_7 = "tabular_classify_mulitclass_run_7"
    participant_id_1 = "tabular_classify_mulitclass_participant_1"
    participant_id_2 = "tabular_classify_mulitclass_participant_2"

    (
        PROJECT_KEY, 
        EXPT_KEY_1, EXPT_KEY_2, EXPT_KEY_3,
        RUN_KEY_1, RUN_KEY_2, RUN_KEY_3, RUN_KEY_4, 
        RUN_KEY_5, RUN_KEY_6, RUN_KEY_7, RUN_KEY_8,
        PARTICIPANT_KEY_1, PARTICIPANT_KEY_2, 
        REG_KEY_1, REG_KEY_2, 
        TAG_KEY_1, TAG_KEY_2
    ) = generate_extra_keys(
        project_id,
        expt_id_1, expt_id_2, expt_id_3,
        run_id_1, run_id_2, run_id_3, run_id_4, run_id_5, run_id_6, run_id_7,
        participant_id_1, participant_id_2
    )


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
                    "in_features": 0,   # placeholder
                    "out_features": 3   # placeholder
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
                    "in_features": 0,   # placeholder
                    "out_features": 10
                }
            },
            {
                "activation": "sigmoid",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 10,
                    "out_features": 90
                }
            },
            {
                "activation": "sigmoid",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 90,
                    "out_features": 80
                }
            },
            {
                "activation": "sigmoid",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 80,
                    "out_features": 70
                }
            },
            {
                "activation": "sigmoid",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 70,
                    "out_features": 60
                }
            },
            {
                "activation": "sigmoid",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 60,
                    "out_features": 50
                }
            },
            {
                "activation": "sigmoid",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 50,
                    "out_features": 40
                }
            },
            {
                "activation": "sigmoid",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 40,
                    "out_features": 30
                }
            },
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
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 10,
                    "out_features": 3   # Placeholder
                }
            }
        ]
    }
    expt_payload_3 = {
        **EXPT_KEY_3,
        'model': [
            {
                "activation": None,
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 0,   # placeholder
                    "out_features": 3   # placeholder
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
    param_set_2 = {
        'rounds': 2, 
        'epochs': 1,
        'base_lr': 0.0005,
        'max_lr': 0.005,
        'criterion': "MultiLabelMarginLoss"
    }
    param_set_3 = {
        'rounds': 2, 
        'epochs': 1,
        'base_lr': 0.0005,
        'max_lr': 0.005,
        'criterion': "MultiLabelSoftMarginLoss"
    }
    param_set_4 = {
        'rounds': 2, 
        'epochs': 1,
        'base_lr': 0.0005,
        'max_lr': 0.005,
        'criterion': "CrossEntropyLoss"
    }
    param_set_5 = {
        'rounds': 2, 
        'epochs': 1,
        'base_lr': 0.0005,
        'max_lr': 0.005,
        'criterion': "HingeEmbeddingLoss"
    }

    run_payload_1 = {**RUN_KEY_1, **param_set_1}
    run_payload_2 = {**RUN_KEY_2, **param_set_2}
    run_payload_3 = {**RUN_KEY_3, **param_set_2}
    run_payload_4 = {**RUN_KEY_4, **param_set_3}
    run_payload_5 = {**RUN_KEY_4, **param_set_4}
    run_payload_6 = {**RUN_KEY_8, **param_set_5}

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
        'train': [["non_iid_1"]],
        'evaluate': [["iid_1"]]
    }
    tag_payload_2 = {
        **TAG_KEY_2,
        'train': [["non_iid_2"]],
        'evaluate': [["iid_2"]]
    }

    alignment_payload = {**PROJECT_KEY}

    # Specific combination: project|expt_2|run_2
    combination_single_payload = {**RUN_KEY_3}
    
    # All combinations under expt_1
    combination_expts_payload = {**EXPT_KEY_1}
    
    # All combinations under project
    combination_project_payload = {**PROJECT_KEY}

    prediction_payload_1 = {
        'tags': {project_id: [["edge_test_missing_coecerable_vals"]]},
        **PARTICIPANT_KEY_1,
        **combination_single_payload
    }
    prediction_payload_2 = {
        'tags': {project_id: [["edge_test_missing_coecerable_vals"]]},
        **PARTICIPANT_KEY_1,
        **combination_expts_payload
    }
    prediction_payload_3 = {
        'tags': {project_id: [["edge_test_missing_coecerable_vals"]]},
        **PARTICIPANT_KEY_1,
        **combination_project_payload
    }

    return {
        'project': project_payload,
        'experiment': [expt_payload_1, expt_payload_2, expt_payload_3],
        'run': [
            run_payload_1, run_payload_2, run_payload_3, 
            run_payload_4, run_payload_5, run_payload_6
        ],
        'participant': [participant_payload_1, participant_payload_2],
        'registration': [registration_payload_1, registration_payload_2],
        'tag': [tag_payload_1, tag_payload_2],
        'alignment': alignment_payload,
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
def image_classify_cycle_binary_payloads():
    project_id = "image_classify_binary_project"
    expt_id_1 = "image_classify_binary_expt_1"
    expt_id_2 = "image_classify_binary_expt_2"
    expt_id_3 = "image_classify_binary_expt_3"
    run_id_1 = "image_classify_binary_run_1"
    run_id_2 = "image_classify_binary_run_2"
    run_id_3 = "image_classify_binary_run_3"
    run_id_4 = "image_classify_binary_run_4"
    run_id_5 = "image_classify_binary_run_5"
    run_id_6 = "image_classify_binary_run_6"
    run_id_7 = "image_classify_binary_run_7"
    participant_id_1 = "image_classify_binary_participant_1"
    participant_id_2 = "image_classify_binary_participant_2"

    (
        PROJECT_KEY, 
        EXPT_KEY_1, EXPT_KEY_2, EXPT_KEY_3,
        RUN_KEY_1, RUN_KEY_2, RUN_KEY_3, RUN_KEY_4, 
        RUN_KEY_5, RUN_KEY_6, RUN_KEY_7, RUN_KEY_8,
        PARTICIPANT_KEY_1, PARTICIPANT_KEY_2, 
        REG_KEY_1, REG_KEY_2, 
        TAG_KEY_1, TAG_KEY_2
    ) = generate_extra_keys(
        project_id,
        expt_id_1, expt_id_2, expt_id_3,
        run_id_1, run_id_2, run_id_3, run_id_4, run_id_5, run_id_6, run_id_7,
        participant_id_1, participant_id_2
    )

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
            # Input: N, C, Height, Width [N, 1, 28, 28]
            {
                "activation": "relu",
                "is_input": True,
                "l_type": "Conv2d",
                "structure": {
                    "in_channels": 1, 
                    "out_channels": 4, # [N, 4, 28, 28]
                    "kernel_size": 3,
                    "stride": 1,
                    "padding": 1
                }
            },
            {
                "activation": None,
                "is_input": False,
                "l_type": "Flatten",
                "structure": {}
            },
            # ------------------------------
            {
                "activation": "sigmoid",
                "is_input": False,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 4 * 28 * 28,
                    "out_features": 1
                }
            }
        ]
    }
    expt_payload_2 = {
        **EXPT_KEY_2,
        'model': [

            ##################################
            # Section 1 - Feature Extraction #
            ##################################

            # Input: N, C, Height, Width [N, 1, 28, 28]
            {
                "activation": None,
                "is_input": True,
                "l_type": "Conv2d",
                "structure": {
                    "in_channels": 1, 
                    "out_channels": 6,  # [N, 6, 28, 28]
                    "kernel_size": 5,
                    "stride": 1,
                    "padding": 2,
                    "bias": True
                }
            },
            {
                "activation": None,
                "is_input": False,
                "l_type": "Tanh",
                "structure": {}
            },
            {
                "activation": None,
                "is_input": False,
                "l_type": "AvgPool2d",
                "structure": {
                    "kernel_size": 2
                }
            },
            {
                "activation": None,
                "is_input": True,
                "l_type": "Conv2d",
                "structure": {
                    "in_channels": 6, 
                    "out_channels": 16, # [N, 6, 28, 28]
                    "kernel_size": 5,
                    "stride": 1,
                    "padding": 0,
                    "bias": True
                }
            },
            {
                "activation": None,
                "is_input": False,
                "l_type": "Tanh",
                "structure": {}
            },
            {
                "activation": None,
                "is_input": False,
                "l_type": "AvgPool2d",
                "structure": {
                    "kernel_size": 2
                }
            },
            {
                "activation": None,
                "is_input": True,
                "l_type": "Conv2d",
                "structure": {
                    "in_channels": 16, 
                    "out_channels": 120, # [N, 6, 28, 28]
                    "kernel_size": 5,
                    "stride": 1
                }
            },
            {
                "activation": None,
                "is_input": False,
                "l_type": "Tanh",
                "structure": {}
            },
            {
                "activation": None,
                "is_input": False,
                "l_type": "Flatten",
                "structure": {}
            },

            ####################################
            # Section 2 - Sequential Encodings #
            ####################################

            {
                "activation": "relu",
                "is_input": False,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 120,
                    "out_features": 84
                }
            },
            {
                "activation": "sigmoid",
                "is_input": False,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 84,
                    "out_features": 1
                }
            }
        ]
    }
    expt_payload_3 = {
        **EXPT_KEY_3,
        'model': [
            # Input: N, C, Height, Width [N, 1, 28, 28]
            {
                "activation": "relu",
                "is_input": True,
                "l_type": "Conv2d",
                "structure": {
                    "in_channels": 1, 
                    "out_channels": 4, # [N, 4, 28, 28]
                    "kernel_size": 3,
                    "stride": 1,
                    "padding": 1
                }
            },
            {
                "activation": None,
                "is_input": False,
                "l_type": "Flatten",
                "structure": {}
            },
            # ------------------------------
            {
                "activation": None,
                "is_input": False,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 4 * 28 * 28,
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
        'criterion': "L1Loss", 
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
        'criterion': "MSELoss"
    }
    param_set_3 = {
        'rounds': 2, 
        'epochs': 1,
        'base_lr': 0.0005,
        'max_lr': 0.005,
        'criterion': "PoissonNLLLoss"
    }
    param_set_4 = {
        'rounds': 2, 
        'epochs': 1,
        'base_lr': 0.0005,
        'max_lr': 0.005,
        'criterion': "KLDivLoss"
    }
    param_set_5 = {
        'rounds': 2, 
        'epochs': 1,
        'base_lr': 0.0005,
        'max_lr': 0.005,
        'criterion': "BCELoss"
    }
    param_set_6 = {
        'rounds': 2, 
        'epochs': 1,
        'base_lr': 0.0005,
        'max_lr': 0.005,
        'criterion': "SmoothL1Loss"
    }
    param_set_7 = {
        'rounds': 2, 
        'epochs': 1,
        'base_lr': 0.0005,
        'max_lr': 0.005,
        'criterion': "BCEWithLogitsLoss"
    }
    run_payload_1 = {**RUN_KEY_1, **param_set_1}
    run_payload_2 = {**RUN_KEY_2, **param_set_2}
    run_payload_3 = {**RUN_KEY_3, **param_set_2}
    run_payload_4 = {**RUN_KEY_4, **param_set_3}
    run_payload_5 = {**RUN_KEY_5, **param_set_4}
    run_payload_6 = {**RUN_KEY_6, **param_set_5}
    run_payload_7 = {**RUN_KEY_7, **param_set_6}
    run_payload_8 = {**RUN_KEY_8, **param_set_7}

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
        'train': [["train"]],
        'evaluate': [["evaluate"]]
    }
    tag_payload_2 = {
        **TAG_KEY_2,
        'train': [["train"]],
        'evaluate': [["evaluate"]]
    }

    alignment_payload = {**PROJECT_KEY}

    # Specific combination: project|expt_2|run_2
    combination_single_payload = {**RUN_KEY_1, **RUN_KEY_3}
    
    # All combinations under expt_1
    combination_expts_payload = {**EXPT_KEY_1}
    
    # All combinations under project
    combination_project_payload = {**PROJECT_KEY}

    prediction_payload_1 = {
        'tags': {project_id: [["predict"]]},
        **PARTICIPANT_KEY_2,
        **combination_single_payload
    }
    prediction_payload_2 = {
        'tags': {project_id: [["predict"]]},
        **PARTICIPANT_KEY_2,
        **combination_expts_payload
    }
    prediction_payload_3 = {
        'tags': {project_id: [["predict"]]},
        **PARTICIPANT_KEY_2,
        **combination_project_payload
    }

    return {
        'project': project_payload,
        'experiment': [expt_payload_1, expt_payload_2, expt_payload_3],
        'run': [
            run_payload_1, run_payload_2, run_payload_3, run_payload_4,
            run_payload_5, run_payload_6, run_payload_7, run_payload_8
        ],
        'participant': [participant_payload_1, participant_payload_2],
        'registration': [registration_payload_1, registration_payload_2],
        'tag': [tag_payload_1, tag_payload_2],
        'alignment': alignment_payload,
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
def image_classify_cycle_multiclass_payloads():
    project_id = "image_classify_mulitclass_project"
    expt_id_1 = "image_classify_mulitclass_expt_1"
    expt_id_2 = "image_classify_mulitclass_expt_2"
    expt_id_3 = "image_classify_mulitclass_expt_3"
    run_id_1 = "image_classify_mulitclass_run_1"
    run_id_2 = "image_classify_mulitclass_run_2"
    run_id_3 = "image_classify_mulitclass_run_3"
    run_id_4 = "image_classify_mulitclass_run_4"
    run_id_5 = "image_classify_mulitclass_run_5"
    run_id_6 = "image_classify_mulitclass_run_6"
    run_id_7 = "image_classify_mulitclass_run_7"
    participant_id_1 = "image_classify_mulitclass_participant_1"
    participant_id_2 = "image_classify_mulitclass_participant_2"

    (
        PROJECT_KEY, 
        EXPT_KEY_1, EXPT_KEY_2, EXPT_KEY_3,
        RUN_KEY_1, RUN_KEY_2, RUN_KEY_3, RUN_KEY_4, 
        RUN_KEY_5, RUN_KEY_6, RUN_KEY_7, RUN_KEY_8,
        PARTICIPANT_KEY_1, PARTICIPANT_KEY_2, 
        REG_KEY_1, REG_KEY_2, 
        TAG_KEY_1, TAG_KEY_2
    ) = generate_extra_keys(
        project_id,
        expt_id_1, expt_id_2, expt_id_3,
        run_id_1, run_id_2, run_id_3, run_id_4, run_id_5, run_id_6, run_id_7,
        participant_id_1, participant_id_2
    )


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
            # Input: N, C, Height, Width [N, 1, 28, 28]
            {
                "activation": "relu",
                "is_input": True,
                "l_type": "Conv2d",
                "structure": {
                    "in_channels": 1, 
                    "out_channels": 4, # [N, 4, 28, 28]
                    "kernel_size": 3,
                    "stride": 1,
                    "padding": 1
                }
            },
            {
                "activation": None,
                "is_input": False,
                "l_type": "Flatten",
                "structure": {}
            },
            # ------------------------------
            {
                "activation": "sigmoid",
                "is_input": False,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 4 * 28 * 28,
                    "out_features": 3   # placeholder
                }
            }
        ]
    }
    expt_payload_2 = {
        **EXPT_KEY_2,
        'model': [

            ##################################
            # Section 1 - Feature Extraction #
            ##################################

            # Input: N, C, Height, Width [N, 1, 28, 28]
            {
                "activation": None,
                "is_input": True,
                "l_type": "Conv2d",
                "structure": {
                    "in_channels": 1, 
                    "out_channels": 6,  # [N, 6, 28, 28]
                    "kernel_size": 5,
                    "stride": 1,
                    "padding": 2,
                    "bias": True
                }
            },
            {
                "activation": None,
                "is_input": False,
                "l_type": "Tanh",
                "structure": {}
            },
            {
                "activation": None,
                "is_input": False,
                "l_type": "AvgPool2d",
                "structure": {
                    "kernel_size": 2
                }
            },
            {
                "activation": None,
                "is_input": True,
                "l_type": "Conv2d",
                "structure": {
                    "in_channels": 6, 
                    "out_channels": 16, # [N, 6, 28, 28]
                    "kernel_size": 5,
                    "stride": 1,
                    "padding": 0,
                    "bias": True
                }
            },
            {
                "activation": None,
                "is_input": False,
                "l_type": "Tanh",
                "structure": {}
            },
            {
                "activation": None,
                "is_input": False,
                "l_type": "AvgPool2d",
                "structure": {
                    "kernel_size": 2
                }
            },
            {
                "activation": None,
                "is_input": True,
                "l_type": "Conv2d",
                "structure": {
                    "in_channels": 16, 
                    "out_channels": 120, # [N, 6, 28, 28]
                    "kernel_size": 5,
                    "stride": 1
                }
            },
            {
                "activation": None,
                "is_input": False,
                "l_type": "Tanh",
                "structure": {}
            },
            {
                "activation": None,
                "is_input": False,
                "l_type": "Flatten",
                "structure": {}
            },

            ####################################
            # Section 2 - Sequential Encodings #
            ####################################

            {
                "activation": "relu",
                "is_input": False,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 120,
                    "out_features": 84
                }
            },
            {
                "activation": "relu",
                "is_input": False,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 84,
                    "out_features": 3   # placeholder
                }
            }
        ]
    }
    expt_payload_3 = {
        'project_id': project_id,
        'expt_id': expt_id_3,
        'model': [
            # Input: N, C, Height, Width [N, 1, 28, 28]
            {
                "activation": "relu",
                "is_input": True,
                "l_type": "Conv2d",
                "structure": {
                    "in_channels": 1, 
                    "out_channels": 4, # [N, 4, 28, 28]
                    "kernel_size": 3,
                    "stride": 1,
                    "padding": 1
                }
            },
            {
                "activation": None,
                "is_input": False,
                "l_type": "Flatten",
                "structure": {}
            },
            # ------------------------------
            {
                "activation": None,
                "is_input": False,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 4 * 28 * 28,
                    "out_features": 3   # placeholder
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
    param_set_2 = {
        'rounds': 2, 
        'epochs': 1,
        'base_lr': 0.0005,
        'max_lr': 0.005,
        'criterion': "NLLLoss" #"MultiLabelMarginLoss"
    }
    param_set_3 = {
        'rounds': 1, 
        'epochs': 2,
        'base_lr': 0.0005,
        'max_lr': 0.005,
        'criterion': "CrossEntropyLoss" #"MultiLabelSoftMarginLoss"
    }
    param_set_4 = {
        'rounds': 2, 
        'epochs': 1,
        'base_lr': 0.0005,
        'max_lr': 0.005,
        'criterion': "CrossEntropyLoss"
    }
    param_set_5 = {
        'rounds': 2, 
        'epochs': 1,
        'base_lr': 0.0005,
        'max_lr': 0.005,
        'criterion': "HingeEmbeddingLoss"
    }

    run_payload_1 = {**RUN_KEY_1, **param_set_1}
    run_payload_2 = {**RUN_KEY_2, **param_set_2}
    run_payload_3 = {**RUN_KEY_3, **param_set_2}
    run_payload_4 = {**RUN_KEY_4, **param_set_3}
    run_payload_5 = {**RUN_KEY_5, **param_set_4}
    run_payload_6 = {**RUN_KEY_8, **param_set_5}

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
        'train': [["train"]],
        'evaluate': [["evaluate"]]
    }
    tag_payload_2 = {
        **TAG_KEY_2,
        'train': [["train"]],
        'evaluate': [["evaluate"]]
    }

    alignment_payload = {**PROJECT_KEY}

    # Specific combination: project|expt_2|run_2
    combination_single_payload = {**RUN_KEY_2}
    
    # All combinations under expt_1
    combination_expts_payload = {**EXPT_KEY_1}
    
    # All combinations under project
    combination_project_payload = {**PROJECT_KEY}

    prediction_payload_1 = {
        'tags': {project_id: [["predict"]]},
        **PARTICIPANT_KEY_2,
        **combination_single_payload
    }
    prediction_payload_2 = {
        'tags': {project_id: [["predict"]]},
        **PARTICIPANT_KEY_2,
        **combination_expts_payload
    }
    prediction_payload_3 = {
        'tags': {project_id: [["predict"]]},
        **PARTICIPANT_KEY_2,
        **combination_project_payload
    }

    return {
        'project': project_payload,
        'experiment': [expt_payload_1, expt_payload_2, expt_payload_3],
        'run': [
            run_payload_1, run_payload_2, run_payload_3, 
            run_payload_4, run_payload_5, run_payload_6
        ],
        'participant': [participant_payload_1, participant_payload_2],
        'registration': [registration_payload_1, registration_payload_2],
        'tag': [tag_payload_1, tag_payload_2],
        'alignment': alignment_payload,
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
def driver():
    return Driver(host=HOST, port=PORT, is_secured=IS_SECURED)