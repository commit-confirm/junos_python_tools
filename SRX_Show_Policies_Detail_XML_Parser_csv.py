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
  print(POLICY_NAME, end ="| ")
  print(POLICY_ACTION, end ="| ")
  print(POLICY_STATE, end ="| ")
  print(POLICY_SEQ, end ="| ")
  print(POLICY_SRC_ZONE, end ="| ")
  print(POLICY_DST_ZONE, end ="| ")
  #
  #Checking if source addresses is a list and if so creating it
  #
  POLICY_SRC_ADDRESS_PREFIX_LIST = []
  if isinstance(POLICY_SRC_ADD, list):
    for ADDRESS_PREFIX in POLICY_SRC_ADD[:]:
      POLICY_SRC_ADDRESS_PREFIX_LIST.append(ADDRESS_PREFIX['prefixes']['address-prefix'])
    print(POLICY_SRC_ADDRESS_PREFIX_LIST, end ="| ")
  elif not isinstance(POLICY_SRC_ADD, list):
    POLICY_SRC_ADDRESS_PREFIX_LIST.append(POLICY_SRC_ADD['prefixes']['address-prefix'])
    print(POLICY_SRC_ADDRESS_PREFIX_LIST, end ="| ")
  #
  #
  #Checking if destination addresses is a list and if so creating it
  #
  POLICY_DST_ADD = POLICY['policy-information']['destination-addresses']['destination-address']
  POLICY_DST_ADDRESS_PREFIX_LIST = []
  if isinstance(POLICY_DST_ADD, list):
    for ADDRESS_PREFIX in POLICY_DST_ADD[:]:
      POLICY_DST_ADDRESS_PREFIX_LIST.append(ADDRESS_PREFIX['prefixes']['address-prefix'])
    print(POLICY_DST_ADDRESS_PREFIX_LIST, end ="| ")
  elif not isinstance(POLICY_DST_ADD, list):
    POLICY_DST_ADDRESS_PREFIX_LIST.append(POLICY_DST_ADD['prefixes']['address-prefix'])
    print(POLICY_DST_ADDRESS_PREFIX_LIST, end ="| ")
  #
  #Checking destination ports and storing
  #  
  POLICY_DST_APP_TERM = POLICY['policy-information']['applications']['application']
  if isinstance(POLICY_DST_APP_TERM, list):
    for item in POLICY_DST_APP_TERM:
      if isinstance(item['application-term'], list):
        for item in item['application-term']:
          print(item['protocol'], item['destination-port-range']['low'],":",item['destination-port-range']['high'], end =" ")
      else:
        print(item['application-term']['protocol'], item['application-term']['destination-port-range']['low'],":",item['application-term']['destination-port-range']['high'], end =" ")
  print("\n") 


POLICY_DST_ADD = POLICY['policy-information']['destination-addresses']['destination-address']







def myprint(d):
  if isinstance(d,dict): #check if it's a dict before using .iteritems()
    for k, v in d.iteritems():
      if isinstance(v, (list,dict)): #check for either list or dict
        #myprint(v)
        print("test1")
      else:
        #print("Key :{0},  Value: {1}".format(k, v))
        print("test2")
  elif isinstance(d,list): #allow for list input too
    for item in d:
      for proto in item['application-term']:
        print(proto['protocol'])


    for item in d:
      if isinstance(item, list):
        for k, v in d.iteritems():
          print("test4")
      elif isinstance(item, dict):
        for k, v in item:
          type(v)
        #print(item['application-term'])
        #print(item['application-term'][0])
      #print(item['application-term'])
      #print("test3")


#pp.pprint(POLICY['policy-information']['policy-name'])