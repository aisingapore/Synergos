#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
from typing import Dict, Union

# Libs


# Custom
from .base import BaseTask
from .endpoints import REGISTRATION_ENDPOINTS

##################
# Configurations #
##################


##############################################
# Registration task Class - RegistrationTask #
##############################################

class RegistrationTask(BaseTask):
    """ Interfacing class governing all registration-related interactions with 
        the remote Synergos grid

    Attributes:
        _type (str): Specifies the type of task
        address (str): Address where Synergos TTP is hosted at
        endpoints (str)): All endpoints governed by this task
    """

    def __init__(self, address: str):
        super().__init__(
            _type="registration", 
            address=address,
            endpoints=REGISTRATION_ENDPOINTS
        )
        self.__nodes = []

    ###########
    # Getters #
    ###########

    def count_nodes(self) -> int:
        """ Counts no. of nodes declared for a single participant

        Returns:
            No. of nodes declared (int)
        """
        return len(self.__nodes)


    def list_nodes(self) -> Dict[str, Union[str, int, bool]]:
        """ Lists all enqueued server nodes allocated for use in the federated
            cycle.

        Returns:
            All registered nodes (dict)
        """
        return {
            f"node_{idx}": self.__nodes[idx] 
            for idx in range(len(self.__nodes))
        }

    ###########
    # Setters #
    ###########

    def add_node(
        self, 
        host: str,
        port: int,
        f_port: int,
        log_msgs: bool = False,
        verbose: bool = False
    ):
        """ Enqueues a server node to be used for subsequent operations during
            the federated cycle. This is for compatibility between Synergos SME
            and Syncluster. Operation is idempotent (i.e. if server node 
            already exists, nothing happens)

        Args:
            host (str): Host IP of the participant's server
            port (int): Websocket port on which federated training resides
            f_port (int): Flask port on which REST-RPC orchestrations resides
            log_msgs (bool): Toggles if computation operations should be logged
            verbose (bool): Toggles verbosity of computation logging
        Returns:
            ID of registered node (dict)
        """
        node_info = {
            'host': host,
            'port': port,
            'f_port': f_port,
            'log_msgs': log_msgs,
            'verbose': verbose
        }
        if node_info not in self.__nodes:
            self.__nodes.append(node_info)
        
        node_id = f"node_{self.__nodes.index(node_info)}"
        return node_id


    def remove_node(self, node_id):
        """ Removes the node corresponding node ID, if it exists. This makes it
            unavailable for subsequent operations during the federated cycle.
            If specified node does not exist, return none. IDs will be
            re-computed and reassiged according to order of declaration

        Args:
            node_id (str): ID of the node to be removed
        Returns:
            Removed node configurations (dict)
        """
        try:
            node_idx = node_id.split('_')[-1]
            return self.__nodes.pop(node_idx)

        except Exception:
            raise RuntimeError("Invalid node ID specified!")


    ###########
    # Helpers #
    ###########

    def _generate_url(
        self, 
        collab_id: str = None,
        project_id: str = None, 
        participant_id: str = None
    ) -> str:
        """

        Args:
            collab_id (str): Identifier of collaboration
            project_id (str): Identifier of project
            participant_id (str): Identifier of participant
        Returns:
            Url (str)
        """
        REGISTRATION_ENDPOINT_MAPPINGS = {
            ('participant_id',): self.endpoints.PARTICIPANT_REGISTRATIONS,
            ('collab_id', 'participant_id'): self.endpoints.PARTICIPANT_COLLAB_REGISTRATIONS,
            ('collab_id',): self.endpoints.COLLABORATION_REGISTRATIONS,
            ('collab_id', 'project_id'): self.endpoints.PROJECT_REGISTRATIONS,
            ('collab_id', 'project_id', 'participant_id'): self.endpoints.REGISTRATION
        }

        input_keys = {
            'collab_id': collab_id, 
            'project_id': project_id, 
            'participant_id': participant_id
        }
        valid_keys = {k:v for k,v in input_keys.items() if v}
        for signature, endpoint_template in REGISTRATION_ENDPOINT_MAPPINGS.items():
            
            if set(signature) == set(valid_keys.keys()):
                return super()._generate_url(
                    endpoint=endpoint_template,
                    **valid_keys
                )

        # If no existing mapping found, declared keys are invalid!
        raise ValueError("Registrations have dependencies. Specify a valid key combination with at least 1 key!")

    ##################
    # Core functions #
    ##################

    def create(
        self,
        collab_id: str,
        project_id: str,
        participant_id: str, 
        role: str,
        **kwargs
    ):
        """ Creates a registration entry for the participant under a specific 
            project in the federated grid

        Args:
            collab_id (str): Identifier of collaboration
            project_id (str): Identifier of project
            participant_id (str): Identifier of participant
            role (str): Role of participant in the federated grid for this 
                particular project. Possible values are 
                1) 'guest'   - Participating to get an enhanced model
                2) 'host'    - Primarily contributing data only
                3) 'arbiter' - Trusted third party overseeing orchestration
            **kwargs
        Returns:
            
        """
        ###########################
        # Implementation Footnote #
        ###########################

        # [Cause]
        # To allow new node registration, nodes metadata needs to be declared &
        # assembled on the client's machine first, before sending it out to the
        # orchestrating node.

        # [Problems]
        # This results in possible state alignment issues. For example, after
        # a series of nodes have been submitted to the orchestrator, the client
        # has no way of removing nodes (they can update information about 
        # existing nodes (i.e. node_1) but cannot remove a node entirely). 

        # [Solution]
        # Instead of implementing custom state alignment code, simply remove 
        # any original registration data stored prior to current submission.
        # This way, the client can refresh their submissions by overriding
        # their previous nodes.
        
        # Delete any existing registrations (if applicable)
        retrieved_reg_resp = self.read(collab_id, project_id, participant_id)
        if retrieved_reg_resp.get('status') == 200:
            self.delete(collab_id, project_id, participant_id)

        registered_nodes = self.list_nodes()
        node_count = self.count_nodes()

        if node_count == 0:
            raise RuntimeError("No nodes detected! Please registered at least 1 node!")
        
        parameters = {
            'role': role, 
            'n_count': node_count, 
            **registered_nodes
        }

        # Clear the node cache
        self.__nodes.clear()

        return self._execute_operation(
            operation="post",
            url=self._generate_url(
                collab_id=collab_id,
                project_id=project_id, 
                participant_id=participant_id
            ),
            payload=parameters
        )

    
    def read_all(
        self, 
        collab_id: str = None,
        project_id: str = None, 
        participant_id: str = None
    ):
        """ Retrieves information/configurations of all registrations created in 
            the federated grid.
            
            Note:
            AT LEAST ONE KEY MUST BE SPECIFIED! 
            If only the project is specified, retrieve all registrations 
            involving said project. If only the participant is specified, 
            retrieve all registrations involving said participant.

        Args:
            collab_id (str): Identifier of collaboration
            project_id (str): Identifier of project
            participant_id (str): Identifier of participant
        Returns:

        """
        return self._execute_operation(
            operation="get",
            url=self._generate_url(
                collab_id=collab_id,
                project_id=project_id, 
                participant_id=participant_id
            ),
            payload=None
        )


    def read(self, collab_id: str, project_id: str, participant_id: str):
        """ Retrieves a single registration's information/configurations created
            in the federated grid

        Args:
            collab_id (str): Identifier of collaboration
            project_id (str): Identifier of project
            participant_id (str): Identifier of participant
        Returns:

        """
        return self._execute_operation(
            operation="get",
            url=self._generate_url(
                collab_id=collab_id,
                project_id=project_id, 
                participant_id=participant_id
            ),
            payload=None
        )
    
    
    def update(
        self, 
        collab_id: str,
        project_id: str, 
        participant_id: str, 
        **updates
    ):
        """ Updates a participant's information/configurations created in the 
            federated grid. 
            Note: 
            This is ONLY for updating EXISTING NODES already registered in the
            orchestrator (i.e. change attributes of node metadata). To apply
            inclusion or omission of nodes themselves, the client should 
            restart the submission process from scratch. The rationale is that
            one should only create a registration reccord when it is finalised.

        Args:
            collab_id (str): Identifier of collaboration
            project_id (str): Identifier of project
            participant_id (str): Identifier of participant
            **updates: Keyword pairs of parameters to be updated
        Returns:

        """
        return self._execute_operation(
            operation="put",
            url=self._generate_url(
                collab_id=collab_id,
                project_id=project_id, 
                participant_id=participant_id
            ),
            payload=updates
        )

    
    def delete(
        self, 
        collab_id: str,
        project_id: str, 
        participant_id: str
    ):
        """ Removes a participant's information/configurations previously created 
            from the federated grid

        Args:
            collab_id (str): Identifier of collaboration
            project_id (str): Identifier of project
            participant_id (str): Identifier of participant
        Returns:

        """
        return self._execute_operation(
            operation="delete",
            url=self._generate_url(
                collab_id=collab_id,
                project_id=project_id, 
                participant_id=participant_id
            ),
            payload=None
        )
    

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000
    address = f"http://{host}:{port}"

    from .collaborations import CollaborationTask
    from .projects import ProjectTask
    from .participants import ParticipantTask
    
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

    registrations = RegistrationTask(address)

    # Test registration creation
    registrations.add_node(
        host="111.111.111.111",
        port=5000,
        f_port=8020
    )
    create_response_1 = registrations.create(
        collab_id=collab_id,
        project_id=project_id,
        participant_id=participant_id_1,
        role='host'
    )
    print("Registration 1: Create response:", create_response_1)

    registrations.add_node(
        host="222.222.222.222",
        port=6000,
        f_port=9020
    )
    registrations.add_node(
        host="333.333.333.333",
        port=7000,
        f_port=10020
    )
    registrations.add_node(
        host="444.444.444.4444",
        port=8000,
        f_port=11020
    )
    create_response_2 = registrations.create(
        collab_id=collab_id,
        project_id=project_id,
        participant_id=participant_id_2,
        role='guest'
    )
    print("Registration 2: Create response:", create_response_2)   

    # Test registration retrieval bulk
    project_read_all_response = registrations.read_all(
        collab_id=collab_id,
        project_id=project_id
    )
    print("Project perspective - Read all response:", project_read_all_response)  

    participant_read_all_response_1 = registrations.read_all(
        participant_id=participant_id_1
    )
    print("Participant 1 perspective - Read all response:", participant_read_all_response_1) 

    participant_read_all_response_2 = registrations.read_all(
        participant_id=participant_id_2
    )
    print("Participant 2 perspective - Read all response:", participant_read_all_response_2) 

    # Test registration retrieval single
    single_read_response_1 = registrations.read(
        collab_id=collab_id,
        project_id=project_id,
        participant_id=participant_id_1
    )
    print("Registration 1: Read response:", single_read_response_1)

    single_read_response_2 = registrations.read(
        collab_id=collab_id,
        project_id=project_id,
        participant_id=participant_id_2
    )
    print("Registration 2: Read response:", single_read_response_2)

    # Test registration update
    update_response_1 = registrations.update(
        collab_id=collab_id,
        project_id=project_id,
        participant_id=participant_id_1, 
        role='arbiter'
    )
    print("Registration 1: Update response:", update_response_1)

    update_response_2 = registrations.update(
        collab_id=collab_id,
        project_id=project_id,
        participant_id=participant_id_2, 
        node_0={
            'host': "444.444.444.4444",
            'port': 9020,
            'f_port': 6000
        }
    )
    print("Registration 2: Update response:", update_response_2)

    # Test registration deletion
    delete_response_1 = registrations.delete(
        collab_id=collab_id,
        project_id=project_id,
        participant_id=participant_id_1
    )
    print("Registration 1: delete response:", delete_response_1)

    delete_response_2 = registrations.delete(
        collab_id=collab_id,
        project_id=project_id,
        participant_id=participant_id_2
    )
    print("Registration 2: delete response:", delete_response_2)

    print("Registrations left:", registrations.read_all(
        collab_id=collab_id,
        project_id=project_id
    )) 

    # Clean up
    collaborations.delete(collab_id=collab_id)