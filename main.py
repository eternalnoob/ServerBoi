import discord
from dotenv import load_dotenv
import asyncio
import json
import os
import lib.message_routing as routing

# Load Discord token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Start Discord client
client = discord.Client()

config = load_config()
command_dict = routing.get_command_dict()


def load_config():
    with open("config.json") as config_file:
        config = json.load(config_file)
    return config


# Main loop
def main():

    event_loop = asyncio.get_event_loop()
    try:
        # event_loop.create_task(check_for_processes(processes_to_check))
        client.run(TOKEN)
        event_loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Stopping")
        event_loop.close()


@client.event
async def on_ready():
    print(f"[Bot Start] {client.user.name} has connected to Discord!")


@client.event
async def on_message(message):
    print(
        f"[Message Recieved] Message from {message.author} in {message.channel}: {message.content}"
    )

    disallowedChannels = [
        170364850256609280,
        666432608539901963,
        453802459379269633,
        278255133891100673,
        316003727506931713,
        585951696753131520,
        616679427979476994,
        711488008351645758,
        186263688603369473,
        698658837447704707,
    ]

    if message.channel.id in (disallowedChannels):
        return

    if message.author == client.user:
        return

    message.content = message.content.lower()
    command = message.content.split(" ")[0]

    if command in command_dict.keys():
        msg = command_dict[command].read_command(message)
        msg.format(message)
        await message.channel.send(msg)
    else:
        msg = command_dict["nou"].read_command(message)
        msg.format(message)
        await message.channel.send(msg)


if __name__ == "__main__":
    main()