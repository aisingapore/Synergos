from synergos import Driver

host = "localhost"
port = 5000

# Initiate Driver
driver = Driver(host=host, port=port)

############################################################
# Phase 1: CONNECT - Submitting TTP & Participant metadata #
############################################################

# 1A. TTP controller creates a project

driver.projects.create(
    project_id="test_project",
    action="classify",
    incentives={
        'tier_1': [],
        'tier_2': [],
        'tier_3': []
    }
)


# 1B. TTP controller creates an experiment

driver.experiments.create(
    project_id="test_project",
    expt_id="test_experiment",
    model = [
        # Input: N, C, Height, Width [N, 1, dimension, dimension]
        {
            "activation": "relu",
            "is_input": True,
            "l_type": "Conv2d",
            "structure": {
                "in_channels": 1, 
                "out_channels": 4, # [N, 4, 32, 32]
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
                "in_features": 4 * 32 * 32,
                "out_features": 1
            }
        }
    ]
)


# 1C. TTP controller creates a run

driver.runs.create(
    project_id="test_project",
    expt_id="test_experiment",
    run_id="test_run",
    rounds=2, 
    epochs=1,
    base_lr=0.0005,
    max_lr=0.005,
    criterion="L1Loss"
)


# 1D. Participants registers their servers' configurations

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


# 1E. Participants registers their role in a specific project

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

# 1F. Participants registers their tags for a specific project

driver.tags.create(
    project_id="test_project",
    participant_id="test_participant_1",
    train=[["train"]],
    evaluate=[["evaluate"]],
    predict = [["predict"]]
)

driver.tags.create(
    project_id="test_project",
    participant_id="test_participant_2",
    train=[["train"]],
    evaluate=[["evaluate"]],
    predict=[["predict"]]
)


#######################################################
# Phase 2: TRAIN - Alignment, Training & Optimisation #
#######################################################

# 2A. Perform multiple feature alignment to dynamically configure datasets and models for cross-grid compatibility

driver.alignments.create(project_id="test_project")


# 2B. Trigger training across the federated grid

model_resp = driver.models.create(
    project_id="test_project",
    expt_id="test_experiment",
    run_id="test_run"
)


# 2C. Trigger hyperparameter optimisation across the grid


################################################
# Phase 3: EVALUATE - Validation & Predictions #
################################################

# 3A. Perform validation(s) of combination(s)

driver.validations.create(
    project_id="test_project",
    expt_id="test_experiment",
    run_id="test_run"
)


# 3B. Perform prediction(s) of combination(s)

driver.predictions.create(
    tags={"test_project": [["predict"]]},
    participant_id="test_participant_1",
    project_id="test_project",
    expt_id="test_experiment",
    run_id="test_run"
)
