#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
import logging

# Libs


# Custom
from synergos.endpoints import PROJECT_ENDPOINTS
from conftest import (
    PROJECT_KEY, 
    check_resp_structure, 
    check_availability_in_single_archive,
    check_availability_in_bulk_archives
)

##################
# Configurations #
##################


#######################
# Tests - ProjectTask #
#######################

def test_ProjectTask_generate_bulk_url(init_params, project_task):
    bulk_url = PROJECT_ENDPOINTS.PROJECTS.substitute(init_params)
    assert project_task._generate_bulk_url() == bulk_url


def test_ProjectTask_generate_single_url(init_params, project_task):
    single_url = PROJECT_ENDPOINTS.PROJECT.substitute(
        **PROJECT_KEY, 
        **init_params
    )
    assert project_task._generate_single_url(**PROJECT_KEY) == single_url


def test_ProjectTask_create(project_task, payloads):
    project_payloads = payloads['project']
    for payload in project_payloads:
        create_resp = project_task.create(**payload)
        check_resp_structure(resp=create_resp)
        check_availability_in_single_archive(
            payload=payload, 
            archive=create_resp['data']
        )


def test_ProjectTask_read_all(project_task, payloads):
    read_all_resp = project_task.read_all()
    check_resp_structure(read_all_resp)
    project_payloads = payloads['project']
    check_availability_in_bulk_archives(
        payloads=project_payloads, 
        archives=read_all_resp['data']
    )


def test_ProjectTask_read(project_task, payloads):
    read_resp = project_task.read(**PROJECT_KEY)
    check_resp_structure(read_resp)
    check_availability_in_bulk_archives(
        payloads=payloads['project'], 
        archives=[read_resp['data']]
    )


def test_ProjectTask_update(project_task, payloads):
    modified_payload = {
        'action': "regress",
        'incentives': {
            'tier_1': ["worker_1"],
            'tier_2': ["worker_1"],
            'tier_3': ["worker_1"]
        }
    }
    update_resp = project_task.update(**PROJECT_KEY, **modified_payload)
    check_resp_structure(update_resp)
    check_availability_in_single_archive(
        payload=modified_payload,
        archive=update_resp['data']
    )
    reverse_resp = project_task.update(**payloads['project'][0])
    check_resp_structure(reverse_resp)
    check_availability_in_single_archive(
        payload=payloads['project'][0],
        archive=reverse_resp['data']
    )


def test_ProjectTask_delete(project_task, payloads):
    delete_resp = project_task.delete(**PROJECT_KEY)
    check_resp_structure(delete_resp)
    check_availability_in_bulk_archives(
        payloads=payloads['project'], 
        archives=[delete_resp['data']]
    )
    retrieved_projects = project_task.read_all()['data']
    assert len(retrieved_projects) == 0
