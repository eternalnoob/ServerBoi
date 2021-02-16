import json
import lib.service_classes as services


def get_config():
    with open("config.json") as config_file:
        config = json.load(config_file)
    return config


def add_server_to_config(server):
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    servers = config["Servers"]

    servers.append(server)

    with open("config.json", "w") as config_file:

        config_file.write(json.dumps(config))


def remove_server_from_config(server):
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    servers = config["Servers"]

    servers.remove(server)

    with open("config.json", "w") as config_file:

        config_file.write(json.dumps(config))


def create_server_object(server_id, server):
    if server["Service"] == "aws":
        server = services.aws_server(server_id, **server)
    elif server["Service"] == "gcp":
        server = services.gcp_server(server_id, **server)
    elif server["Service"] == "azure":
        server = services.azure_server(server_id, **server)

    return server


def create_server_objects(servers):
    server_set = {}

    server_id = 0

    for server_entry in servers:
        server_object = create_server_object(server_id, server_entry)
        server_set[str(server_id)] = server_object
        server_id += 1

    return server_set