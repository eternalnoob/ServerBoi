import boto3
import json
import os
import time
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import requests
from pathlib import Path
from requests.auth import HTTPDigestAuth
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient


class server_object(object):
    def __init__(self, server_id, Game, Name, ServerInfo, Service, ServiceInfo):

        self.server_id = server_id

        self.game = Game

        self.server_name = Name

        self.server_info = ServerInfo

        self.service = Service

        self.service_info = ServerInfo


class aws_server(server_object):
    def __init__(self, server_id, Game, Name, ServerInfo, Service, ServiceInfo):

        super().__init__(server_id, Game, Name, ServerInfo, Service, ServiceInfo)

        self.instance_id = ServiceInfo["InstanceId"]

        self.region = ServiceInfo["Region"]

        self.account_id = ServiceInfo["AccountId"]

        self.get_server_instance_object()

    def get_server_instance_object(self):

        sts_client = boto3.client("sts")

        assumed_role_object = sts_client.assume_role(
            RoleArn=f"arn:aws:iam::{self.account_id}:role/ServerBoiRole",
            RoleSessionName="ServerBoiSession",
        )

        credentials = assumed_role_object["Credentials"]

        ec2 = boto3.resource(
            "ec2",
            region_name=self.region,
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretAccessKey"],
            aws_session_token=credentials["SessionToken"],
        )

        self.instance = ec2.Instance(self.instance_id)

        self.public_ip = self.instance.public_ip_address

    def __repr__(self):

        return f"{self.instance_id}"

    def server_manage(self, action):

        if action == "start":

            self.instance.start()

            self.state = self.server_manage("status")  # pending

            while self.instance.state == "pending":

                time.sleep(1)

        if action == "stop":

            self.instance.stop()

            while self.instance.state == "stopping":

                time.sleep(1)

        if action == "reboot":

            self.instance.reboot()

            while self.instance.state == "rebooting":

                time.sleep(1)

            self.refresh_public_ip()

        if action == "status":

            return self.instance.state["Name"]

    def refresh_public_ip(self):

        self.public_ip = self.instance.public_ip_address


class gcp_server(server_object):
    def __init__(self, server_id, Game, Name, ServerInfo, Service, ServiceInfo):

        super().__init__(server_id, Game, Name, ServerInfo, Service, ServiceInfo)

        self.project = ServiceInfo["Project"]

        self.instance_name = ServiceInfo["InstanceName"]

        self.zone = ServiceInfo["Zone"]

        self.service_client = self.google_request_client()

        self.public_ip = self.refresh_public_ip()

    def __repr__(self):

        return f"{self.instance_name}"

    def google_request_client(self):

        credentials = GoogleCredentials.get_application_default()

        return discovery.build("compute", "v1", credentials=credentials)

    def server_manage(self, command):

        if command == "start":

            request = self.service_client.instances().start(
                project=self.project, zone=self.zone, instance=self.instance_name
            )

            response = request.execute()

            while response["status"] != "RUNNING":

                request = self.service_client.instances().get(
                    project=self.project, zone=self.zone, instance=self.instance_name
                )

                response = request.execute()

                time.sleep(1)

            self.refresh_public_ip()

        elif command == "stop":

            request = self.service_client.instances().stop(
                project=self.project, zone=self.zone, instance=self.instance_name
            )

        elif command == "status":

            request = self.service_client.instances().get(
                project=self.project, zone=self.zone, instance=self.instance_name
            )

        response = request.execute()

        return response["status"].lower()

    def refresh_public_ip(self):

        request = self.service_client.instances().get(
            project=self.project, zone=self.zone, instance=self.instance_name
        )

        response = request.execute()

        try:

            nat_ip = response["networkInterfaces"][0]["accessConfigs"][0]["natIP"]

            return nat_ip

        except:

            return None


class azure_server(server_object):
    def __init__(self, server_id, Game, Name, ServerInfo, Service, ServiceInfo):

        super().__init__(server_id, Game, Name, ServerInfo, Service, ServiceInfo)

        self.subscription_id = ServiceInfo["SubscriptionId"]

        self.vm_name = ServiceInfo["VmName"]

        self.location = ServiceInfo["Location"]

        self.group_name = ServiceInfo["GroupName"]

        self.credentials = self.azure_credentials()

        self.compute_client = ComputeManagementClient(
            self.credentials, self.subscription_id
        )

        self.network_client = NetworkManagementClient(
            self.credentials, self.subscription_id
        )

        self.get_public_ip_name()

        self.refresh_public_ip()

    def __repr__(self):

        return f"{self.vm_name}"

    @staticmethod
    def azure_credentials():

        credentials = ServicePrincipalCredentials(
            client_id="288e1135-fea8-488a-ba71-f71f84a229e6",
            secret=".la2WpgER.Rxe_-exgi_8Lm4OU.dKI9P30",
            tenant="84bd82a8-13a5-4f9e-b5af-66c05512e76c",
        )

        return credentials

    def instance_view(self):

        return self.compute_client.virtual_machines.get(
            self.group_name, self.vm_name, expand="instanceView"
        )

    def server_manage(self, command):

        if command == "start":

            self.compute_client.virtual_machines.start(self.group_name, self.vm_name)

            while self.server_manage("status") != "PowerState/running":

                time.sleep(1)

            self.refresh_public_ip()

        elif command == "stop":

            self.compute_client.virtual_machines.power_off(
                self.group_name, self.vm_name
            )

            while self.server_manage("status") != "PowerState/stopped":

                time.sleep(1)

        elif command == "reboot":

            self.compute_client.virtual_machines.restart(self.group_name, self.vm_name)

        elif command == "status":

            instance_view = self.instance_view()

            return instance_view.instance_view.statuses[1].code

    def get_public_ip_name(self):

        instance_view = self.instance_view()

        for item in instance_view.network_profile.network_interfaces:

            nicName = item.id.split("/")[8]

        nic = self.network_client.network_interfaces.get(self.group_name, nicName)

        for item in nic.ip_configurations:

            self.public_ip_name = item.public_ip_address.id.split("/")[8]

    def refresh_public_ip(self):

        ip_query = self.network_client.public_ip_addresses.get(
            self.group_name, self.public_ip_name
        )

        self.public_ip = ip_query.ip_address