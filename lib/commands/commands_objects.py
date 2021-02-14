import uuid


class CommandTree(object):
    def __init__(self):
        self.current_stage = 0
        self.locked = False
        self.correction = False
        self.stage = {}
        self.return_message = None

    def read_input(self, message):
        stage_function = self.stage[self.current_stage]
        stage_function(message)
        return self.return_message

    def iterate_stage(self):
        self.current_stage += 1

    def set_stage(self, stage):
        self.current_stage = stage

    def lock_tree(self):
        self.locked = True


class Interaction(object):
    def __init__(self, user_id, channel_id, command_tree):
        self.user_id = user_id
        self.channel_id = channel_id
        self.interaction_id = f"{uuid.UUID.hex}-{user_id}-{channel_id}"
        self.command_tree = command_tree()