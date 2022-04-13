# Simulation of a multi level office building FIREWALL which includes security air tight rooms, protocol restrictions, and packet switching based on a forwarding table
# TOPOLOGY DESCRIPTION - 
  # Floor 1 - host1 host 2
  # Floor 2 - host 1 host 2
  # Singular Trusted host
  # Singular Untrusted host
  # Web server
  # Air-Gapped Hosts - Calculating IP addresses using IP address using subnet mask size 29

# CONTROLLER POX FILE PURPOSE
# Regulates transmission of packets from source node to target node by checking protocol type, mac address, IP address of src and dst.
# Uses open flow mod and networking python libraries

# SKELTON FILE PURPOSE
# Contains the topology required to connect the multi level network
# Uses mininet topology libary 
# Uses switches and switch ports to create final topology
# Each device has its own MAC address and IP address

# RUNNING SIMULATION
# open Ubuntu Terminal
# start mininet - "sudo mn"
# Run python files using linux command line pytoon3 "file name 1" "file name 2"
# check topology physical connections using - "dump"
# Run primary test for checking correct packet dropping using "pingall" can take a while to run
# Test HTTP protocol regulation using - "wget"

