from lib.commands.commands_objects import CommandTree
from lib.server_management import add_server_to_config


class AddServerTree(CommandTree):
    """
    Command Tree to add a server to be tracked and managed by ServerBoi.

    Command will prompt user for various pieces of information to about this server they wish to add.

    TODO: Azure and GCP Support, Validate server information, give user IAM role template for cross account role.
    """

    def __init__(self):
        super().__init__()
        self.server = {
            "Name": "",
            "Game": "",
            "ServerInfo": {},
            "Service": "",
            "ServiceInfo": {},
            "Owner": "",
        }
        self.stage = {
            0: self.stage_name_get,
            1: self.stage_name_set,
            2: self.stage_game_set,
            3: self.stage_password_set,
            4: self.stage_port_set,
            5: self.stage_service_provider_set,
            6: self.stage_aws_account_set,
            7: self.stage_aws_region_set,
            8: self.stage_aws_instance_id_set,
            9: self.stage_confirmation,
            10: self.stage_correction_routing,
        }

    def move_to_next_step(self, next_stage):
        if self.correction:
            self.set_stage(8)
            self.stage_validation_get()
        else:
            next_stage()

    def stage_name_get(self, message=None):
        self.return_message = "What is the server's name?"
        self.iterate_stage()

    def stage_name_set(self, message):
        self.server["Name"] = message.content
        self.move_to_next_step(self.stage_game_get)

    def stage_game_get(self):
        self.return_message = "What game is this for?"
        print(self.return_message)
        self.iterate_stage()

    def stage_game_set(self, message):
        self.server["Game"] = message.content
        self.move_to_next_step(self.stage_password_get)

    def stage_password_get(self):
        self.return_message = "What is the server's password? If none, respond 'n'"
        self.iterate_stage()

    def stage_password_set(self, message):
        no_password_check = message.content.lower()
        if no_password_check != "n":
            self.server["ServerInfo"]["Password"] = message.content
        else:
            if self.server["ServerInfo"].get("Password", False):
                self.server["ServerInfo"].pop("Password")

        self.move_to_next_step(self.stage_port_get)

    def stage_port_get(self):
        self.return_message = (
            "What port is used to connect to the server? If none, respond 'n'"
        )
        self.iterate_stage()

    def stage_port_set(self, message):
        no_port_check = message.content.lower()
        if no_port_check != "n":
            self.server["ServerInfo"]["Port"] = message.content
        else:
            if self.server["ServerInfo"].get("Port", False):
                self.server["ServerInfo"].pop("Port")

        self.move_to_next_step(self.stage_service_provider_get)

    def stage_service_provider_get(self):
        self.return_message = "Which service provider? (Currently supported: aws)"
        self.iterate_stage()

    def stage_service_provider_set(self, message):
        valid_options = {"aws"}
        message_lowered = message.content.lower()
        if message_lowered in valid_options:
            self.server["Service"] = message_lowered
            self.move_to_next_step(self.stage_aws_account_get)
        else:
            self.return_message = f"{message.content} is not a valid option. Valid options: {list(valid_options)}"

    def stage_aws_account_get(self):
        self.return_message = "What is your AWS account number?"
        self.iterate_stage()

    def stage_aws_account_set(self, message):
        self.server["ServiceInfo"]["AccountId"] = message.content
        self.move_to_next_step(self.stage_aws_region_get)

    def stage_aws_region_get(self):
        self.return_message = "Which region is this instance hosted in?"
        self.iterate_stage()

    def stage_aws_region_set(self, message):
        valid_regions = {
            "us-east-1",
            "us-east-2",
            "us-west-1",
            "us-west-2",
            "eu-west-1",
            "eu-west-2",
            "eu-central-1",
            "ap-southeast-1",
            "ap-southeast-2",
            "ap-south-1",
            "ap-northeast-1",
            "ap-northeast-2",
            "sa-east-1",
        }

        if message.content.lower() in valid_regions:
            self.server["ServiceInfo"]["Region"] = message.content
            self.move_to_next_step(self.stage_aws_instance_id_get)
        else:
            self.return_message = f"{message.content} is not a valid option. Valid options: {list(valid_regions)}"

    def stage_aws_instance_id_get(self):
        self.return_message = "What is the instance id? (Example: i-044e820ec4e8b0335)"
        self.iterate_stage()

    def stage_aws_instance_id_set(self, message):
        self.server["ServiceInfo"]["InstanceId"] = message.content
        self.move_to_next_step(self.stage_validation_get)

    def stage_validation_get(self):
        self.correction = False
        self.return_message = f"""Validate the following is correct:

        Server Name: {self.server['Name']}
        Game: {self.server['Game']}
        Service Provider: {self.server['Service']}
        Password: {self.server['ServerInfo'].get('Password', "None")}
        Port: {self.server['ServerInfo'].get('Port', "None")}
        Account Number: {self.server['ServiceInfo']['AccountId']}
        Region: {self.server['ServiceInfo']['Region']}
        Instance ID: {self.server['ServiceInfo']['InstanceId']}

Is this information correct? (y/n)
        """
        self.iterate_stage()

    def stage_confirmation(self, message):
        response_check = message.content.lower()
        if response_check == "y":
            self.server["Owner"] = message.author.id
            self.return_message = "Server added"
            add_server_to_config(self.server)
            self.lock_tree()
        elif response_check == "n":
            self.stage_correction()
        else:
            self.return_message = "Please respond y or n"

    def stage_correction(self):
        self.return_message = f"""Which field would you like to edit?

        1. Name (Currently {self.server['Name']})
        2. Game (Currently {self.server['Game']})
        3. Password (Currently {self.server['ServerInfo'].get('Password', "None")})
        4. Port (Currently {self.server['ServerInfo'].get('Port', "None")})
        5. Service Provider (Currently {self.server['Service']})
        6. Account Number (Currently {self.server['ServiceInfo']['AccountId']})
        7. Region (Currently {self.server['ServiceInfo']['Region']})
        8. Instance ID (Currently {self.server['ServiceInfo']['InstanceId']})

Enter the number of the option you would wish to edit or enter 'q' to quit and cancel adding the server.
        """

        self.iterate_stage()

    def stage_correction_routing(self, message):

        route_key = message.content

        valid_options = ["1", "2", "3", "4", "5", "6", "7", "8"]

        routing = {
            "1": {"function": self.stage_name_get, "stage": 0},
            "2": {"function": self.stage_game_get, "stage": 1},
            "3": {"function": self.stage_password_get, "stage": 2},
            "4": {"function": self.stage_port_get, "stage": 3},
            "5": {"function": self.stage_service_provider_get, "stage": 4},
            "6": {"function": self.stage_aws_account_get, "stage": 5},
            "7": {"function": self.stage_aws_region_get, "stage": 6},
            "8": {"function": self.stage_aws_instance_id_get, "stage": 7},
        }

        if message.content in valid_options:
            self.correction = True
            entry = routing[route_key]
            self.set_stage(entry["stage"])
            entry["function"]()

        elif message.content.lower() == "q":
            self.return_message = "Quiting and canceling adding server."

        else:
            self.return_message = f"Please select one of the following: {valid_options}"
