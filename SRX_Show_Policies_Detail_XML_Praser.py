import os
import json
import xmltodict
import pprint
pp = pprint


#### Replace File Name ####
with open('sample.xml') as fd:
  doc = xmltodict.parse(fd.read())


POLICY_LIST = doc['rpc-reply']['multi-routing-engine-results']['multi-routing-engine-item']['security-policies']['security-context']['policies'][:]

POLICY_DETAILS = {
	}

for POLICY in POLICY_LIST[:]:
  #
  #Shortening XML Paths
  #
  POLICY_NAME = POLICY['policy-information']['policy-name']
  POLICY_ACTION = POLICY['policy-information']['policy-action']['action-type']
  POLICY_STATE = POLICY['policy-information']['policy-state']
  POLICY_SEQ = POLICY['policy-information']['policy-sequence-number']
  POLICY_SRC_ZONE = POLICY['policy-information']['context-information']['source-zone-name']
  POLICY_DST_ZONE = POLICY['policy-information']['context-information']['destination-zone-name']
  POLICY_SRC_ADD= POLICY['policy-information']['source-addresses']['source-address']
  POLICY_DST_ADD = POLICY['policy-information']['destination-addresses']['destination-address']
  POLICY_DST_APP_ADD = POLICY['policy-information']['applications']['application']['application-term']
  #
  #Printing Results
  #
  print("Policy Name: ", POLICY_NAME)
  print("Policy Action: ", POLICY_ACTION)
  print("Policy State: ", POLICY_STATE)
  print("Policy Seq: ", POLICY_SEQ)
  print("Policy SRC Zone: ", POLICY_SRC_ZONE)
  #
  #Checking if source addresses is a list and if so creating it
  #
  POLICY_SRC_ADDRESS_PREFIX_LIST = []
  if isinstance(POLICY_SRC_ADD, list):
    for ADDRESS_PREFIX in POLICY_SRC_ADD[:]:
      POLICY_SRC_ADDRESS_PREFIX_LIST.append(ADDRESS_PREFIX['prefixes']['address-prefix'])
    print("Policy Sources: ", POLICY_SRC_ADDRESS_PREFIX_LIST)
  elif not isinstance(POLICY_SRC_ADD, list):
    POLICY_SRC_ADDRESS_PREFIX_LIST.append(POLICY_SRC_ADD['prefixes']['address-prefix'])
    print("Policy Sources: ", POLICY_SRC_ADDRESS_PREFIX_LIST)
  #
  print("Policy Dst Zone: ", POLICY_DST_ZONE)
  #
  #Checking if destination addresses is a list and if so creating it
  #
  POLICY_DST_ADDRESS_PREFIX_LIST = []
  if isinstance(POLICY_DST_ADD, list):
    for ADDRESS_PREFIX in POLICY_DST_ADD[:]:
      POLICY_DST_ADDRESS_PREFIX_LIST.append(ADDRESS_PREFIX['prefixes']['address-prefix'])
    print("Policy Destinations: ", POLICY_DST_ADDRESS_PREFIX_LIST)
  elif not isinstance(POLICY_DST_ADD, list):
    POLICY_DST_ADDRESS_PREFIX_LIST.append(POLICY_DST_ADD['prefixes']['address-prefix'])
    print("Policy Destinations: ", POLICY_DST_ADDRESS_PREFIX_LIST)
  #
  #Checking destination ports and storing
  #  
  if isinstance(POLICY_DST_APP_ADD, list):
    for APP_SET in POLICY_DST_APP_ADD:
      PORTS = {
        "PROTO":APP_SET['protocol'],
        "LP":APP_SET['destination-port-range']['low'],
        "HP":APP_SET['destination-port-range']['high'],
        "PORT": 0
      }
      if PORTS['LP'] == PORTS['HP']:
        PORTS['PORT'] = PORTS['LP']
      elif PORTS['LP'] != PORTS['HP']:
        PORTS['PORT'] = PORTS['LP'],PORTS['HP']
      print(PORTS['PORT'], PORTS['PROTO'])
  elif not isinstance(POLICY_DST_APP_ADD, list):
    PORTS = {
      "PROTO":POLICY_DST_APP_ADD['protocol'],
      "LP":POLICY_DST_APP_ADD['destination-port-range']['low'],
      "HP":POLICY_DST_APP_ADD['destination-port-range']['high'],
      "PORT": 0
    }
    if PORTS['LP'] == PORTS['HP']:
      PORTS['PORT'] = PORTS['LP']
    elif PORTS['LP'] != PORTS['HP']:
      PORTS['PORT'] = PORTS['LP'],PORTS['HP']
    print(PORTS['PORT'], PORTS['PROTO'])
  print("\n")




#pp.pprint(POLICY['policy-information']['policy-name'])
