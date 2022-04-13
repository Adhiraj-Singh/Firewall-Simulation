# Simulation of a multi level office building FIREWALL which includes security air tight rooms, protocol restrictions, and packet switching based on a forwarding table

# CONTROLLER PIX FILE PURPOSE
# Regulates transmission of packets from source node to target node by checking protocol type, mac address, IP address of src and dst.
# Uses ope flow mod and networking python libraries

# SKELTON FILE PURPOSE
# Contains the topology required to connect the multi level network
# Uses mininet topology libary 
# Uses switches and switch ports to create final topology
# Each device has its own MAC address and IP address
