import random


def nou(commands):

    number = random.randint(1, 101)

    if number == 69:

        msg = "Fuck you"

    elif number in range(1, 10):

        msg = ("No u, {}").format(commands.author.name)

    elif number in range(11, 21):

        msg = "No u buddy"

    elif number == 42:

        msg = "Nerd"

    elif number in range(22, 33):

        msg = ("No, fuk u {}").format(commands.author.name)

    elif number == 80:

        msg = "Wow, you're right. I've never though about it that way before"

    elif number == 81:

        msg = "Yeah u rite"

    else:

        msg = "No u"

    return msg


def thanks():

    np = ["Np", "No prob", "Gotchu"]

    number = random.randint(0, 2)

    return np[number]


def sorry():

    app = [
        "Don't appologize it shows weakness",
        "Its okay just don't let it happen again",
        "Good",
    ]

    number = random.randint(0, 2)

    return app[number]