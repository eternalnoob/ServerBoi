def hi():

    return "Hi. Give me a command. You can say help to view available actions. If I don't respond to a message, you probably typed it wrong"


def help():

    msg = """
    Commands

    list | list all currently managed servers
    server <server_id> start | Starts server. Admin only.
    server <server_id> stop | Stops server. Admin only.
    server <server_id> reboot | Reboots server. Admin only.
    server <server_id> ip | Returns servers ip.
    server <server_id> info | Returns server info.

    """

    return msg


def list_servers(server_objects):
    msg = "Current managed servers: \n"

    for server in server_objects.values():
        msg += f"ID: {server.server_id} | Name: {server.server_name} | Game: {server.game} | IP: {server.public_ip}:{server.server_info['Port']} | Status: {server.server_manage('status')}\n"

    return msg