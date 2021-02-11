import discord
from dotenv import load_dotenv
import asyncio
import json
import os
import lib.message_routing as routing
import lib.service_classes as services

# Load Discord token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Start Discord client
client = discord.Client()

server_set = {}


def load_config():
    with open("config.json") as config_file:
        config = json.load(config_file)
    return config


def create_server_object(server_id, server):
    if server["Service"] == "aws":
        server = services.aws_server(server_id, **server)
    elif server["Service"] == "gcp":
        server = services.gcp_server(server_id, **server)
    elif server["Service"] == "azure":
        server = services.azure_server(server_id, **server)

    return server


# Main loops
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
    message_split = message.content.split(" ")
    command = message_split[0]

    if command in command_dict.keys():
        msg = command_dict[command].read_command(message_split, server_set)
        msg.format(message)
        await message.channel.send(msg)
    else:
        msg = command_dict["nou"].read_command(message)
        msg.format(message)
        await message.channel.send(msg)


if __name__ == "__main__":
    config = load_config()
    servers = config["Servers"]

    server_id = 0

    for server_entry in servers:
        print(server_entry)
        server_object = create_server_object(server_id, server_entry)
        server_set[str(server_id)] = server_object
        server_id += 1

    command_dict = routing.get_command_dict()
    main()