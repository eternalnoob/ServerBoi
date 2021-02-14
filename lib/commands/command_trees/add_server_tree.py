from lib.commands.commands_objects import CommandTree


class AddServerTree(CommandTree):
    """
    Conversation that goes
    P - add server
    B - Give name
    P - <Server Name>
    """

    def __init__(self):
        super().__init__()
        self.stage = {
            0: self.stage_name_get,
            1: self.stage_name_set,
            2: self.stage_game_set,
            3: self.stage_service_provider_set,
            4: self.stage_aws_account_set,
            5: self.stage_aws_region_set,
            6: self.stage_aws_instance_id_set,
            7: self.stage_confirmation,
            8: self.stage_correction_routing,
        }

    def move_to_next_step(self, next_stage):
        if self.correction:
            self.set_stage(6)
            self.stage_validation_get()
        else:
            next_stage()

    def stage_name_get(self, message=None):
        self.return_message = "What is the server's name?"
        self.iterate_stage()

    def stage_name_set(self, message):
        self.server_name = message.content
        self.move_to_next_step(self.stage_game_get)

    def stage_game_get(self):
        self.return_message = "What game is this for?"
        print(self.return_message)
        self.iterate_stage()

    def stage_game_set(self, message):
        self.game = message.content
        self.move_to_next_step(self.stage_service_provider_get)

    def stage_service_provider_get(self):
        self.return_message = "Which service provider? (Currently supported: aws)"
        self.iterate_stage()

    def stage_service_provider_set(self, message):
        valid_options = {"aws"}
        if message.content in valid_options:
            self.service_name = message.content
            self.move_to_next_step(self.stage_aws_account_get)
        else:
            self.return_message = f"{message.content} is not a valid option. Valid options: {list(valid_options)}"

    def stage_aws_account_get(self):
        self.return_message = "What is your AWS account number?"
        self.iterate_stage()

    def stage_aws_account_set(self, message):
        self.account_number = message.content
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

        if message.content in valid_regions:
            self.region_name = message.content
            self.move_to_next_step(self.stage_aws_instance_id_get)
        else:
            self.return_message = f"{message.content} is not a valid option. Valid options: {list(valid_regions)}"

    def stage_aws_instance_id_get(self):
        self.return_message = "What is the instance id? (Example: i-044e820ec4e8b0335)"
        self.iterate_stage()

    def stage_aws_instance_id_set(self, message):
        self.instance_id = message.content
        self.move_to_next_step(self.stage_validation_get)

    def stage_validation_get(self):
        self.correction = False
        self.return_message = f"""Validate the following is correct:

        Server Name: {self.server_name}
        Game: {self.game}
        Service Provider: {self.service_name}
        Account Number: {self.account_number}
        Region: {self.region_name}
        Instance ID: {self.instance_id}

Is this information correct? (y/n)
        """
        self.iterate_stage()

    def stage_confirmation(self, message):
        if message.content == "y":
            self.return_message = "Server added"
            self.lock_tree()
        elif message.content == "n":
            self.stage_correction()
        else:
            self.return_message = "Please respond y or n"

    def stage_correction(self):
        self.return_message = f"""Which field would you like to edit?

        1. Server Name (Currently {self.server_name})
        2. Game Name (Currently {self.game})
        3. Service Provider (Currently {self.service_name})
        4. Account Number (Currently {self.account_number})
        5. Region (Currently {self.region_name})
        6. Instance ID (Currently {self.instance_id})

Enter the number of the option you would wish to edit
        """

        self.iterate_stage()

    def stage_correction_routing(self, message):

        route_key = message.content

        valid_options = ["1", "2", "3", "4", "5", "6"]

        routing = {
            "1": {"function": self.stage_name_get, "stage": 0},
            "2": {"function": self.stage_game_get, "stage": 1},
            "3": {"function": self.stage_service_provider_get, "stage": 2},
            "4": {"function": self.stage_aws_account_get, "stage": 3},
            "5": {"function": self.stage_aws_region_get, "stage": 4},
            "6": {"function": self.stage_aws_instance_id_get, "stage": 5},
        }

        if message.content in valid_options:
            self.correction = True
            entry = routing[route_key]
            self.set_stage(entry["stage"])
            entry["function"]()

        else:
            self.return_message = f"Please select one of the following: {valid_options}"
