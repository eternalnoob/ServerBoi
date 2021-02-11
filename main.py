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

with open("config.json") as config_file:
    config = json.load(config_file)

admins = config["Admins"]
disallowed_channels = config["IgnoredChannels"]


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
        f"[Message Recieved] Message from {message.author.id} in {message.channel}: {message.content}"
    )

    if message.channel.id in (disallowed_channels):
        return

    if message.author == client.user:
        return

    message.content = message.content.lower()
    message_split = message.content.split(" ")
    command = message_split[0]

    if command in command_dict.keys():
        msg = command_dict[command].read_command(message, server_set, admins)
        msg.format(message)
        await message.channel.send(msg)
    else:
        msg = command_dict["fun"].read_command(message, server_set, admins)
        msg.format(message)
        await message.channel.send(msg)


if __name__ == "__main__":
    servers = config["Servers"]

    server_id = 0

    for server_entry in servers:
        server_object = create_server_object(server_id, server_entry)
        server_set[str(server_id)] = server_object
        server_id += 1

    command_dict = routing.get_command_dict()
    main()