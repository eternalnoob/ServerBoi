import lib.commands.fun as fun
import lib.commands.general_commands as general
import lib.commands.server_manage as server


class help_command(object):
    def __init__(self):

        self.commands = None

    def read_command(self, command, server_objects, admins):

        return general.help()


class list_command(object):
    def __init__(self):

        self.commands = None

    def read_command(self, command, server_objects, admins):

        return general.list_servers(server_objects)


class server_command(object):
    def __init__(self):

        self.commands = None

    def read_command(self, message, server_objects, admins):
        command = message.content.split(" ")[2]
        admin_commands = {"start", "stop", "reboot"}

        if command in admin_commands:
            if message.author.id in admins:
                server.server_manage(message, server_objects)
            else:
                return "This command can only be ran by admins"

        return server.server_manage(message, server_objects)


class fun_command(object):
    def __init__(self):

        self.commands = None

    def read_command(self, commands, server_objects, admins):

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

    def read_command(self, command, server_objects, admins):

        return general.hi()


def get_command_dict():
    command_dict = {
        "help": help_command(),
        "hi": hi_command(),
        "fun": fun_command(),
        "list": list_command(),
        "server": server_command(),
    }

    return command_dict