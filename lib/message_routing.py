import commands.fun as fun
import commands.general_commands as general


class help_command(object):
    def __init__(self):

        self.commands = None

    def read_command(self, command):

        return general.help()


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
    }

    return command_dict