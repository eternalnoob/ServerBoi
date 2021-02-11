import lib.commands.fun as fun
import lib.commands.general_commands as general
import lib.commands.server_manage as server


class help_command(object):
    def __init__(self):

        self.commands = None

    def read_command(self, command):

        return general.help()


class list_command(object):
    def __init__(self):

        self.commands = None

    def read_command(self, command, server_objects):

        return general.list_servers(server_objects)


class server_command(object):
    def __init__(self):

        self.commands = None

    def read_command(self, command, server_objects):

        return server.server_manage(command, server_objects)


class fun_command(object):
    def __init__(self):

        self.commands = None

    def read_command(self, commands):

        self.commands = commands.content

        nou = ["no u", "nou", "n0 u", "no you", "noyou", "n o u", "n 0 u"]

        thank = ["thanks", "thx", "thank"]

        sorry = ["i'm sorry", "sorry", "my bad", "sorry"]

        if self.commands.startswith(tuple(nou)):

            return fun.nou(commands)

        elif any(string in self.commands for string in thank):

            return fun.thanks()

        elif any(string in self.commands for string in sorry):

            return fun.sorry()

        return


class hi_command(object):
    def __init__(self):

        self.commands = None

    def read_command(self, command):

        return general.hi()


def get_command_dict():
    command_dict = {
        "help": help_command(),
        "hi": hi_command(),
        "nou": fun_command(),
        "list": list_command(),
        "server": server_command(),
    }

    return command_dict