#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
from string import Template

# Libs


# Custom


##################
# Configurations #
##################

connect_prefix = "$address/ttp/connect"
train_prefix = "$address/ttp/train"
evaluate_prefix = "$address/ttp/evaluate"

####################
# Endpoint Classes #
####################

# Phase 1: Connection -> /ttp/connect/

class COLLABORATION_ENDPOINTS:
    COLLABORATIONS = Template(f"{connect_prefix}/collaborations")
    COLLABORATION = Template(f"{connect_prefix}/collaborations/$collab_id")


class PROJECT_ENDPOINTS:
    PROJECTS = Template(f"{connect_prefix}/collaborations/$collab_id/projects")
    PROJECT = Template(f"{connect_prefix}/collaborations/$collab_id/projects/$project_id")


class EXPERIMENT_ENDPOINTS:
    EXPERIMENTS = Template(f"{connect_prefix}/collaborations/$collab_id/projects/$project_id/experiments")
    EXPERIMENT = Template(f"{connect_prefix}/collaborations/$collab_id/projects/$project_id/experiments/$expt_id")


class RUN_ENDPOINTS:
    RUNS = Template(f"{connect_prefix}/collaborations/$collab_id/projects/$project_id/experiments/$expt_id/runs")
    RUN = Template(f"{connect_prefix}/collaborations/$collab_id/projects/$project_id/experiments/$expt_id/runs/$run_id")


class PARTICIPANT_ENDPOINTS:
    PARTICIPANTS = Template(f"{connect_prefix}/participants")
    PARTICIPANT = Template(f"{connect_prefix}/participants/$participant_id")


class REGISTRATION_ENDPOINTS:
    PARTICIPANT_REGISTRATIONS = Template(f"{connect_prefix}/participants/$participant_id/registrations")
    PARTICIPANT_COLLAB_REGISTRATIONS = Template(f"{connect_prefix}/participants/$participant_id/collaborations/$collab_id/registrations")
    COLLABORATION_REGISTRATIONS = Template(f"{connect_prefix}/collaborations/$collab_id/registrations")
    PROJECT_REGISTRATIONS = Template(f"{connect_prefix}/collaborations/$collab_id/projects/$project_id/registrations")
    REGISTRATION = Template(f"{connect_prefix}/collaborations/$collab_id/projects/$project_id/participants/$participant_id/registration")


class TAG_ENDPOINTS:
    TAGS = Template(f"{connect_prefix}/collaborations/$collab_id/projects/$project_id/participants/$participant_id/registration/tags")


# Phase 2: Training -> /ttp/train/

class ALIGNMENT_ENDPOINTS:
    ALIGNMENTS = Template(f"{train_prefix}/collaborations/$collab_id/projects/$project_id/alignments")


class MODEL_ENDPOINTS:
    PROJECT_COMBINATIONS = Template(f"{train_prefix}/collaborations/$collab_id/projects/$project_id/models")
    EXPERIMENT_COMBINATIONS = Template(f"{train_prefix}/collaborations/$collab_id/projects/$project_id/models/$expt_id")
    RUN_COMBINATION = Template(f"{train_prefix}/collaborations/$collab_id/projects/$project_id/models/$expt_id/$run_id")


class OPTIMIZATION_ENDPOINTS:
    OPTIMIZATIONS = Template(f"{train_prefix}/collaborations/$collab_id/projects/$project_id/models/$expt_id/optimizations/")


# Phase 3: Training -> /ttp/evaluate/

class VALIDATION_ENDPOINTS:
    PROJECT_COMBINATIONS = Template(f"{evaluate_prefix}/collaborations/$collab_id/projects/$project_id/validations")
    EXPERIMENT_COMBINATIONS = Template(f"{evaluate_prefix}/collaborations/$collab_id/projects/$project_id/validations/$expt_id")
    RUN_COMBINATIONS = Template(f"{evaluate_prefix}/collaborations/$collab_id/projects/$project_id/validations/$expt_id/$run_id")
    PARTICIPANT_COMBINATION = Template(f"{evaluate_prefix}/collaborations/$collab_id/projects/$project_id/validations/$expt_id/$run_id/$participant_id")


class PREDICTION_ENDPOINTS:
    # Participant intialised inference (ONLY for Horizontal FL)
    PARTICIPANT_COMBINATIONS = Template(f"{evaluate_prefix}/participants/$participant_id/collaborations/$collab_id/predictions")
    PROJECT_COMBINATIONS = Template(f"{evaluate_prefix}/participants/$participant_id/collaborations/$collab_id/predictions/$project_id")
    EXPERIMENT_COMBINATIONS = Template(f"{evaluate_prefix}/participants/$participant_id/collaborations/$collab_id/predictions/$project_id/$expt_id")
    RUN_COMBINATION = Template(f"{evaluate_prefix}/participants/$participant_id/collaborations/$collab_id/predictions/$project_id/$expt_id/$run_id")

#########
# Tests #
#########

if __name__ == "__main__":

    from string import Template

    test_template = Template("/projects/$project_id/models/$expt_id/optimizations/")
    test_endpoint = test_template.safe_substitute({'project_id': "test_project", 'expt_id': "test_expt"})
    print(test_endpoint)