import discord
from dotenv import load_dotenv
import asyncio
import os
import lib.server_management as server
import lib.message_routing as routing
from lib.commands.commands_objects import Interaction

# Load Discord token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Start Discord client
client = discord.Client()


# Main loop
def main():

    event_loop = asyncio.get_event_loop()
    try:
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

    if message.channel.id in (disallowed_channels):
        return

    if message.author == client.user:
        return

    conversation_key = f"{message.author.id}-{message.channel.id}"

    print(f"Conversation Key: {conversation_key}")

    if conversation_key in conversations:
        print("Existing conversation")
        print(
            f"Current tree stage: {conversations[conversation_key].command_tree.current_stage}"
        )
        msg = conversations[conversation_key].command_tree.read_input(message)
        if conversations[conversation_key].command_tree.locked:
            conversations.pop(conversation_key)
        msg.format(message)
        await message.channel.send(msg)

    else:
        print("Conversation doesnt exist. Checking if valid command")
        lowered_message = message.content.lower()
        message_split = lowered_message.split(" ")
        command = message_split[0]

        if lowered_message in command_tree_dict:
            print("Creating new conversation")
            command_tree = command_tree_dict[message.content]
            new_conversation = Interaction(
                message.author.id, message.channel.id, command_tree
            )
            conversations[conversation_key] = new_conversation
            msg = new_conversation.command_tree.read_input(message)
            msg.format(message)
            await message.channel.send(msg)
        elif command in command_dict:
            msg = command_dict[command].read_command(message, server_set, admins)
            msg.format(message)
            await message.channel.send(msg)
        else:
            msg = command_dict["fun"].read_command(message, server_set, admins)
            # Only send message if response comes back as str
            if isinstance(msg, str):
                msg.format(message)
                await message.channel.send(msg)


if __name__ == "__main__":
    config = server.get_config()

    admins = config["Admins"]
    disallowed_channels = config["IgnoredChannels"]
    conversations = {}

    servers = config["Servers"]

    server_set = server.create_server_objects(servers)

    command_dict = routing.get_command_dict()
    command_tree_dict = routing.get_command_tree_dict()
    main()