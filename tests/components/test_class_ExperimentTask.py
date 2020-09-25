#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
import logging

# Libs


# Custom
from synergos.endpoints import EXPERIMENT_ENDPOINTS
from conftest import (
    PROJECT_KEY,
    EXPT_KEY_1, EXPT_KEY_2,
    check_resp_structure, 
    check_availability_in_single_archive,
    check_availability_in_bulk_archives
)

##################
# Configurations #
##################


##########################
# Tests - ExperimentTask #
##########################

def test_ExperimentTask_generate_bulk_url(init_params, experiment_task):
    bulk_url = EXPERIMENT_ENDPOINTS.EXPERIMENTS.substitute(
        **PROJECT_KEY, 
        **init_params
    )
    assert experiment_task._generate_bulk_url(**PROJECT_KEY) == bulk_url


def test_ExperimentTask_generate_single_url(init_params, experiment_task):
    single_url_1 = EXPERIMENT_ENDPOINTS.EXPERIMENT.substitute(
        **init_params,
        **EXPT_KEY_1
    )
    assert (experiment_task._generate_single_url(**EXPT_KEY_1) == single_url_1)

    single_url_2 = EXPERIMENT_ENDPOINTS.EXPERIMENT.substitute(
        **init_params,
        **EXPT_KEY_2
    )
    assert (experiment_task._generate_single_url(**EXPT_KEY_2) == single_url_2)


def test_ExperimentTask_create(experiment_task, payloads):
    expt_payloads = payloads['experiment']
    for payload in expt_payloads:
        create_resp = experiment_task.create(**payload)
        check_resp_structure(resp=create_resp)
        check_availability_in_single_archive(
            payload=payload, 
            archive=create_resp['data']
        )


def test_ExperimentTask_read_all(experiment_task, payloads):
    read_all_resp = experiment_task.read_all(**PROJECT_KEY)
    check_resp_structure(read_all_resp)
    expt_payloads = payloads['experiment']
    check_availability_in_bulk_archives(
        payloads=expt_payloads, 
        archives=read_all_resp['data']
    )


def test_ExperimentTask_read(experiment_task, payloads):
    read_resp_1 = experiment_task.read(**EXPT_KEY_1)
    check_resp_structure(read_resp_1)
    check_availability_in_single_archive(
        payload=payloads['experiment'][0],
        archive=read_resp_1['data']
    )
    
    read_resp_2 = experiment_task.read(**EXPT_KEY_2)
    check_resp_structure(read_resp_2)
    check_availability_in_single_archive(
        payload=payloads['experiment'][1],
        archive=read_resp_2['data']
    )

    
def test_ExperimentTask_update(experiment_task, payloads):
    modified_payload_1 = {
        'model': [
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
    }
    update_resp_1 = experiment_task.update(**EXPT_KEY_1, **modified_payload_1)
    check_resp_structure(update_resp_1)
    check_availability_in_single_archive(
        payload=modified_payload_1,
        archive=update_resp_1['data']
    )
    reverse_resp_1 = experiment_task.update(**payloads['experiment'][0])
    check_resp_structure(reverse_resp_1)
    check_availability_in_single_archive(
        payload=payloads['experiment'][0],
        archive=reverse_resp_1['data']
    )

    modified_payload_2 = {
        'model': [
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
    }
    update_resp_2 = experiment_task.update(**EXPT_KEY_2, **modified_payload_2)
    check_resp_structure(update_resp_2)
    check_availability_in_single_archive(
        payload=modified_payload_2,
        archive=update_resp_2['data']
    )
    reverse_resp_2 = experiment_task.update(**payloads['experiment'][1])
    check_resp_structure(reverse_resp_2)
    check_availability_in_single_archive(
        payload=payloads['experiment'][1],
        archive=reverse_resp_2['data']
    )


def test_ExperimentTask_delete(experiment_task, payloads):
    delete_resp_1 = experiment_task.delete(**EXPT_KEY_1)
    check_resp_structure(delete_resp_1)
    check_availability_in_single_archive(
        payload=payloads['experiment'][0], 
        archive=delete_resp_1['data']
    )
    retrieved_expts = experiment_task.read_all(**PROJECT_KEY)['data']
    assert len(retrieved_expts) == 1

    delete_resp_2 = experiment_task.delete(**EXPT_KEY_2)
    check_resp_structure(delete_resp_2)
    check_availability_in_single_archive(
        payload=payloads['experiment'][1], 
        archive=delete_resp_2['data']
    )
    retrieved_expts = experiment_task.read_all(**PROJECT_KEY)['data']
    assert len(retrieved_expts) == 0