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
from .endpoints import ALIGNMENT_ENDPOINTS

##################
# Configurations #
##################


########################################
# Alignment task Class - AlignmentTask #
########################################

class AlignmentTask(BaseTask):
    """ Interfacing class governing all alignment-related interactions with 
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
            _type="alignment", 
            address=address,
            endpoints=ALIGNMENT_ENDPOINTS
        )
        
    ###########
    # Helpers #
    ###########

    def _generate_url(self, collab_id: str, project_id: str) -> str:
        return super()._generate_url(
            endpoint=self.endpoints.ALIGNMENTS,
            collab_id=collab_id,
            project_id=project_id
        )

    ##################
    # Core functions #
    ##################

    def create(self, collab_id: str, project_id: str, **kwargs):
        """ Triggers multiple feature alignment for the participant under a 
            specific project in the federated grid

        Args:
            project_id (str): Identifier of project
            **kwargs
        Returns:
            
        """
        return self._execute_operation(
            operation="post",
            url=self._generate_url(collab_id=collab_id, project_id=project_id),
            payload=None
        )


    def read(self, collab_id: str, project_id: str):
        """ Retrieves a single set of tags' information/configurations created
            in the federated grid

        Args:
            project_id (str): Identifier of project
        Returns:

        """
        return self._execute_operation(
            operation="get",
            url=self._generate_url(collab_id=collab_id, project_id=project_id),
            payload=None
        )
    

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000
    address = f"http://{host}:{port}"

    from .collaborations import CollaborationTask
    from .projects import ProjectTask
    from .participants import ParticipantTask
    from .registrations import RegistrationTask
    from .tags import TagTask
    
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

    alignments = AlignmentTask(address)

    # Test alignment creation
    create_response = alignments.create(collab_id=collab_id, project_id=project_id)
    print("Alignments: Create response:", create_response)

    # Test alignment retrieval
    single_read_response = alignments.read(collab_id=collab_id, project_id=project_id)
    print("Alignments: Read response:", single_read_response)

    # Clean up
    collaborations.delete(collab_id=collab_id)