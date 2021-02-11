# ServerBoi

ServerBoi is a tool to allow users to interact with cloud resources via a Discord bot.

### How Commands are Structured

Commands are outlined in two places, `message_routing.py` and a corresponding file in the `commands` folder.

In `get_command_dict()` in `message_routing.py` contains a dict with the command's keyword being a key and the commands class being a value. This class should call functions outlined in a file within `commands` folder.

### Current Commands

* list | list all currently managed servers
* server <server_id> start | Starts server. Admin only.
* server <server_id> stop | Stops server. Admin only.
* server <server_id> reboot | Reboots server. Admin only.
* server <server_id> status | Returns servers status.
* server <server_id> ip | Returns servers ip.
* server <server_id> info | Returns server info.
