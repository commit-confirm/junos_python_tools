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
  #POLICY_DST_ADD = POLICY['policy-information']['destination-addresses']['destination-address']
  #POLICY_DST_APP_ADD = POLICY['policy-information']['applications']['application']['application-term']
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
  POLICY_DST_ADD = POLICY['policy-information']['destination-addresses']['destination-address']
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
  POLICY_DST_APP_TERM = POLICY['policy-information']['applications']['application']
  if isinstance(POLICY_DST_APP_TERM, list):
    for item in POLICY_DST_APP_TERM:
      print(item['application-term']['protocol'], item['application-term']['destination-port-range']['low'],":",item['application-term']['destination-port-range']['high'], end =" ")
  if isinstance(POLICY_DST_APP_TERM, dict):
    if isinstance(POLICY_DST_APP_TERM['application-term'], list):
      for item in POLICY_DST_APP_TERM['application-term']:
        print(item['protocol'], item['destination-port-range']['low'],":",item['destination-port-range']['high'])
    if isinstance(POLICY_DST_APP_TERM['application-term'], dict):
      for item in POLICY_DST_APP_TERM:
        print(POLICY_DST_APP_TERM['application-term']['protocol'], POLICY_DST_APP_TERM['application-term']['destination-port-range']['low'],":",POLICY_DST_APP_TERM['application-term']['destination-port-range']['high'])
  print("\n")

# / Useful troubleshooting functions: 

def traverse(obj, prev_path = "obj", path_repr = "{}[{!r}]".format):
    if isinstance(obj,dict):
        it = obj.items()
    elif isinstance(obj,list):
        it = enumerate(obj)
    else:
        yield prev_path,obj
        return
    for k,v in it:
        for data in traverse(v, path_repr(prev_path,k), path_repr):
            yield data


#for path,value in traverse(POLICY_LIST[:9]):
#  print("{} = {}".format(path,value))

def LISTCHECK(d):
  if isinstance(d, dict): #check if it's a dict before using .iteritems()
    for k, v in d.iteritems():
      if isinstance(v, (list,dict)): #check for either list or dict
        print(v)
      else:
        print("Key :{0},  Value: {1}".format(k, v))
  elif isinstance(d, list): #allow for list input too
    item_list = []
    for item in d:
      print(item)

#test = POLICY_LIST[9]['policy-information']['applications']['application']
#LISTCHEC(test)
