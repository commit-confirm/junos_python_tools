import requests
import json
from pprint import pprint
import urllib3
import urllib

urllib3.disable_warnings()


# Get Libre IP address for later API calls
input_ip = input("Please insert the Librenms API IP address: ")
# Get auth token and format as dict for later api calls
input_token = input("Please insert your X-Auth token: ")
headers["X-Auth-Token"] = input_token

# Define auth header and do get request
req = requests.get(
    "https://{}:443//api/v0/devices".format(input_ip), headers=headers, verify=False
)

# Take request and load as json/dict
jreq = json.loads(req.text)


device_list = []


def junos_check(jreq=jreq):
    """
    Function to form a list of Junos/Juniper devices
    """
    for device in jreq["devices"]:
        if device["os"] == "junos":
            device_list.append(device["hostname"])
        else:
            continue


junos_check()

device_ports = {}
device = {}


def get_ports(device_list=device_list):
    """
    Get a list of ports for each device
    """
    for device in device_list:
        port_req = requests.get(
            "https://{}:443//api/v0/devices/{}/ports".format(input_ip, device),
            headers=headers,
            verify=False,
        )
        preq = json.loads(port_req.text)

        item_list = []
        for item in preq["ports"]:
            """
            This loop is to creat a nested list within the device_ports 
            dict using the device name as the key and interfaces as values
            """
            item_list.append(item["ifName"])
            device_ports[device] = item_list


get_ports()


def get_port_stats(device_ports=device_ports):
    """
    Creat a final nested dict structure containing a device, its ports and the stats for each port
    """
    final_device = dict()
    for device, ports in device_ports.items():
        if device == "test-device":
            final_ports = dict()
            for port in ports:
                final_port_stats = dict()
                testr = requests.get(
                    "https://{}:443//api/v0/devices/{}/ports/{}".format(
                        input_ip, device, urllib.parse.quote(port, safe="")
                    ),
                    headers=headers,
                    verify=False,
                )
                testreq2 = json.loads(testr.text)

                final_port_stats["ifName"] = testreq2["port"]["ifName"]
                final_port_stats["port_id"] = testreq2["port"]["port_id"]
                final_port_stats["ifDescr"] = testreq2["port"]["ifDescr"]
                final_port_stats["ifSpeed"] = testreq2["port"]["ifSpeed"]
                final_port_stats["ifOperStatus"] = testreq2["port"]["ifOperStatus"]
                final_port_stats["ifAdminStatus"] = testreq2["port"]["ifAdminStatus"]

                # Hand nested dict to upper dict
                final_ports[port] = final_port_stats
            final_device[device] = final_ports
        else:
            continue
    return final_device


stats = get_port_stats()
pprint(stats)
