#!/usr/bin/env python
#
# Python Version: 2.7
#
# Test VPC subnet creation in all available zones 
# Used for older AWS accounts with both ec2-classic and default-VPC options
#

# Must be the first line
from __future__ import print_function

import boto.vpc
import boto.ec2
import sys, getopt

# Dummy varibles
#
VPC_CIDR =  '10.10.0.0/16'
SUBNETS = ( '10.10.0.0/24',  '10.10.1.0/24',  '10.10.2.0/24',
            '10.10.3.0/24',  '10.10.4.0/24',  '10.10.5.0/24' )

def usage():
  """ Usage Statement """

  print("""

  Test VPC subnet creation in all availabe zones

  vpc-subnet-test.py -p <profile>

  """)
  exit(1)

def get_args():
  """ Check the arguments """

  argv = sys.argv[1:]
  profile = ''

  try:
    opts, args = getopt.getopt(argv,'hp:',['profile='])
  except getopt.GetoptError:
    usage()

  for opt, arg in opts:
    if opt in ('-p', '--profile'):  profile = arg
    elif opt == '-h':               usage()

  if profile == '' or len(sys.argv) != 3:
    usage()

  return profile

def get_regions():
  """ Build a region list """

  reg_list = []
  for reg in boto.vpc.regions():
    if reg.name == 'us-gov-west-1' or reg.name == 'cn-north-1':
      continue
    reg_list.append(reg.name)

  return reg_list

regions = get_regions()
profile = get_args()
reg_total = len(regions)
reg_no = 0

print("Testing VPC subnet creation in all availabe zones..\n")
while reg_total > 0:
  # Test each region
  #
  reg_name = regions[reg_no]
  myregion = boto.ec2.get_region(region_name=reg_name)

  try:
    conn = boto.vpc.VPCConnection(profile_name=profile, region=myregion)
  except boto.provider.ProfileNotFoundError as e:
    print(e.message)
    exit(1)
  else:
    print("Region:", reg_name)

  # Create a test VPC
  #
  try:
    test_vpc = conn.create_vpc(VPC_CIDR, instance_tenancy='default')
  except boto.exception.EC2ResponseError as e:
    print(e.message, "\n")
    reg_no += 1; reg_total -= 1
    continue

  # Get all available zones
  #
  all_azs = conn.get_all_zones()
  az_total = len(all_azs)

  sub_list = [ ]
  sub_total = 0
  az_no = 0

  # Test each AZ by attempting to create a subnet
  #
  while az_no < az_total:
    az_name = str(all_azs[az_no])
    az_name = az_name[5:]
    print("Attempting", az_name, end = "")

    try:
      sub = conn.create_subnet(test_vpc.id, SUBNETS[sub_total], availability_zone=az_name)
    except boto.exception.EC2ResponseError as e:
      print(" ..failed!")
      print(e.message, "\n")
      az_no += 1
    else:
      print(" ..success!")
      sub_list.append(sub.id)
      sub_total += 1; az_no += 1

  # Clean up the mess
  #
  print("\nCleaning up", end = "")
  while sub_total != 0:
    sub_total -= 1
    conn.delete_subnet(sub_list[sub_total])

  conn.delete_vpc(test_vpc.id)
  print(" ..done!\n")

  reg_no += 1; reg_total -= 1
#
print("Testing complete.")
