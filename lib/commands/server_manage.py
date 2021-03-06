def server_manage(message, server_objects):
    message_split = message.content.split(" ")
    command = message.content

    server = server_objects[str(message_split[1])]

    if "start" in command:
        server.server_manage("start")
        msg = (
            f"Server name is {server.server_name} and is started on {server.public_ip}"
        )
    elif "stop" in command:
        server.server_manage("stop")
        msg = "Server stopped"
    elif "reboot" in command:
        server.server_manage("reboot")
        msg = f"Server rebooted. New ip is {server.public_ip}"
    elif "status" in command:
        status = server.server_manage("status")
        msg = f"Server is currently {status}"
    elif "ip" in command:
        if server.public_ip == None:
            msg = f"Server is currently {server.server_manage('status')} and has no ip."
        else:
            msg = f"Server ip is {server.public_ip}:{server.server_info['Port']}"
    elif "info" in command:
        if server.server_manage("status") != "running":
            msg = "Server is currently off. Run server to see information"
        else:
            msg = f"Server name is {server.server_name} on ip {server.public_ip}:{server.server_info['Port']}."
    else:
        msg = "Command not recognized. Send me 'help' or learn to type"
    return msg