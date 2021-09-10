# Synergos

Interfacing package for interacting with TTP container in a Synergos network.

![REST-RPC Endpoint interactions](./docs/images/payload_interactions-[V4]_URL_Interactions.png)*REST-RPC Endpoint interactions supported in the Synergos Grid [V4]*

The Synergos grid prides itself on its modular system of deployment, comprizing of a duet of 2 packages - *Synergos-TTP* & *Synergos-Worker*. By having users install different components depending on their supposed role within the federated grid, most of the complexity associated with federated orchestrations are obscured completely from the users. 

However, this meant that the REST-RPC interface itself had many options and variations, and ironically, becoming somewhat of a complex beast itself, with 11 endpoints each supporting 4 variant operations, for a total of more than 40 routes to choose from! 

Thus, this inspired the creation of the Synergos Driver package, as a means to further simplify this interface.

## Installation
As Synergos is still under development, it has yet to be deployed on PyPi. Hence, the best way to use it is to install it in development mode in a local virtualenv.

```
# Download source repository
git clone https://gitlab.int.aisingapore.org/aims/federatedlearning/synergos.git
git checkout dev
cd ./synergos

# Setup virtual environment
conda create -n synergos_env python=3.7

# Install in development mode
pip install -e .
```

## How to use?
Submitting jobs to the Synergos grid is simple with the driver interface.

```
from synergos import Driver

host = "0.0.0.0"
port = 5000

driver = Driver(host=host, port=port)

############################################################
# Phase 1: CONNECT - Submitting TTP & Participant metadata #
############################################################

# 1A. Orchestrator creates a collaboration

collab_task = driver.collaborations

collab_task.configure_logger(
    host="172.20.0.14", 
    port=9000, 
    sysmetrics_port=9100, 
    director_port=9200, 
    ttp_port=9300, 
    worker_port=9400, 
    ui_port=9000, 
    secure=False
)

collab_task.configure_mlops( 
    host="172.20.0.15", 
    port=5500, 
    ui_port=5500, 
    secure=False
)

collab_task.configure_mq( 
    host="172.20.0.16", 
    port=5672, 
    ui_port=15672, 
    secure=False
)

collab_task.create('test_collaboration')


# 1B. Orchestrator creates a project

driver.projects.create(
    collab_id="test_collaboration",
    project_id="test_project",
    action="classify",
    incentives={
        'tier_1': [],
        'tier_2': [],
    }
)


# 1C. Orchestrator creates an experiment

driver.experiments.create(
    collab_id="test_collaboration",
    project_id="test_project",
    expt_id="test_experiment",
     model=[
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
        {
            "activation": "softmax",
            "is_input": False,
            "l_type": "Linear",
            "structure": {
                "bias": True,
                "in_features": 4 * 28 * 28,
                "out_features": 3
            }
        }
    ]
)


# 1D. Orchestrator creates a run

driver.runs.create(
    collab_id="test_collaboration",
    project_id="test_project",
    expt_id="test_experiment",
    run_id="test_run",
    rounds=2, 
    epochs=1,
    base_lr=0.0005,
    max_lr=0.005,
    criterion="NLLLoss"


# 1E. Participants registers their servers' configurations

driver.participants.create(participant_id="worker_1")

driver.participants.create(participant_id="worker_2")


# 1E. Participants registers their role in a specific project

registration_task = driver.registrations

# Add and register worker_1 node
registration_task.add_node(
    host='172.17.0.2',
    port=8020,
    f_port=5000,
    log_msgs=True,
    verbose=True
)
registration_task.create(
    collab_id="test_collaboration",
    project_id="test_project",
    participant_id="worker_1",
    role="host"
)

registration_task = driver.registrations
registration_task.add_node(
    host='172.17.0.3',
    port=8020,
    f_port=5000,
    log_msgs=True,
    verbose=True
)
registration_task.create(
    collab_id="test_collaboration",
    project_id="test_project",
    participant_id="worker_2",
    role="guest"
)


# 1F. Participants registers their tags for a specific project

driver.tags.create(
    collab_id="test_collaboration",
    project_id="test_project",
    participant_id="worker_1",
    train=[["train"]],
    evaluate=[["evaluate"]]
)

driver.tags.create(
    collab_id="test_collaboration",
    project_id="test_project",
    participant_id="worker_2",
    train=[["train"]]
)


#######################################################
# Phase 2: TRAIN - Alignment, Training & Optimisation #
#######################################################

# 2A. Perform multiple feature alignment to dynamically configure datasets and models for cross-grid compatibility

driver.alignments.create(
    collab_id='test_collaboration',
    project_id="test_project",
    verbose=False,
    log_msg=False
)


# 2B. Trigger training across the federated grid

model_resp = driver.models.create(
    collab_id="test_collaboration",
    project_id="test_project",
    expt_id="test_experiment",
    run_id="test_run",
    log_msg=False,
    verbose=False
)


# 2C. Trigger hyperparameter optimisation across the grid


################################################
# Phase 3: EVALUATE - Validation & Predictions #
################################################

# 3A. Perform validation(s) of combination(s)

driver.validations.create(
    collab_id='test_collaboration',
    project_id="test_project",
    expt_id="test_experiment",
    run_id="test_run",
    log_msg=False,
    verbose=False
)


# 3B. Perform prediction(s) of combination(s)

driver.predictions.create(
    collab_id="test_collaboration",
    tags={"test_project": [["predict"]]},
    participant_id="worker_1",
    project_id="test_project",
    expt_id="test_experiment",
    run_id="test_run"
)

```

## Further Documentations
For now, documentations are still in progress. In the meantime, use python's `help()` function to find out existing parameters to each of the task classes. In general, each task class has up to 5 methods -  `.create()`, `.read_all`, `.read()`, `.update()`, `.delete()`. 

![Synergos Interface](./docs/images/synergos_driver_classes.png)*Interfacing components that make up the Synergos Driver package*

Alternatively, you may refer to the UML class diagram above for the list of functions supported for each component class.

In general, phase 1 operations (i.e. connection) have support for all methods, but phase 2 and 3 operations (i.e. training & evaluation) drop support for manual user updates or deletions of metadata entries within the grid, since all processes are dynamically generated by the system this point on.

