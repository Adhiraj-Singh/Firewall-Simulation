#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class final_topo(Topo):
  def build(self):
    #Floor 1 switch 1 hosts
    laptop = self.addHost("laptop", mac = "00:00:00:00:00:01", ip = "20.2.1.10/24", defaultRoute = "laptop-eth0")
    labmachine = self.addHost("labmachine", mac = "00:00:00:00:00:02", ip = "20.2.1.20/24", defaultRoute = "lab machine-eth0")
    # Floor 1 switch 2 hosts
    device1 = self.addHost("device1", mac = "00:00:00:00:00:03", ip = "20.2.1.30/24", defaultRoute = "device1-eth0")
    device2 = self.addHost("device2", mac = "00:00:00:00:00:04", ip = "20.2.1.40/24", defaultRoute = "device2-eth0")

    # Floor 2 switch 1 hosts
    host1 = self.addHost("host1", mac = "00:00:00:00:00:05", ip = "10.2.7.10/24", defaultRoute = "host1-eth0")
    host2 = self.addHost("host2", mac = "00:00:00:00:00:06", ip = "10.2.7.20/24", defaultRoute = "host2-eth0")

    # Trusted host, owned by department B employee - certified
    h_trust = self.addHost("h_trust", mac = "00:00:00:00:00:07", ip = "104.24.32.100/24", defaultRoute = "h_trust-eth0")

    # Untrusted host - potential hacker
    h_untrust = self.addHost("h_untrust", mac = "00:00:00:00:00:08", ip = "108.44.83.103/24", defaultRoute = "h_untrust-eth0")

    # Web server
    h_server = self.addHost("h_server", mac = "00:00:00:00:00:09", ip = "30.14.66/24", defaultRoute = "h_server-eth0")

    # Air-Gap hosts
    # !!!!!! YET TO ADD THESE
    client1 = self.addHost("client1", mac = "00:00:00:00:00:10", ip = "40.2.5.00/29", defaultRoute = "client1-eth0")
    client2 = self.addHost("client2", mac = "00:00:00:00:00:11", ip = "40.2.5.10/29", defaultRoute = "client2-eth0")
    client3 = self.addHost("client3", mac = "00:00:00:00:00:12", ip = "40.2.5.20/29", defaultRoute = "client3-eth0")
    client4 = self.addHost("client4", mac = "00:00:00:00:00:13", ip = "40.2.5.30/29", defaultRoute = "client4-eth0")
    client5 = self.addHost("client5", mac = "00:00:00:00:00:14", ip = "40.2.5.40/29", defaultRoute = "client5-eth0")
    client6 = self.addHost("client6", mac = "00:00:00:00:00:15", ip = "40.2.5.50/29", defaultRoute = "client6-eth0")
    client7 = self.addHost("client7", mac = "00:00:00:00:00:16", ip = "40.2.5.60/29", defaultRoute = "client7-eth0")
    client8 = self.addHost("client8", mac = "00:00:00:00:00:17", ip = "40.2.5.70/29", defaultRoute = "client8-eth0")



    # Creating switches
    # Floor 1
    s1 = self.addSwitch("s1")
    s2 = self.addSwitch("s2")
    # Floor 2
    s3 = self.addSwitch("s3")
    # Air gap floor
    s4 = self.addSwitch("s4")
    # Data center
    s5 = self.addSwitch("s5")
    # Core switch
    s6 = self.addSwitch("s6")

    # CONNECTING ALL THE DEVICES
    # Reversing order of port connections due to prev assignment formatting
    # Floor 1, switch 1
    self.addLink(laptop, s1, port1 = 0, port2 = 8)
    self.addLink(labmachine, s1, port1 = 0,  port2 = 9)
    # Floor 1, switch 2
    self.addLink(device1, s2, port1 = 0, port2 = 8)
    self.addLink(device2, s2, port1 = 0, port2 = 9)

    # Floor 2, switch 1
    self.addLink(host1, s3, port1 = 0, port2 = 8)
    self.addLink(host2, s3, port1 = 0, port2 = 9)

    # Air gapped floor switch 1
    self.addLink(client1,s4,port1 = 0, port2 = 1)
    self.addLink(client2,s4,port1 = 0, port2 = 2)
    self.addLink(client3,s4,port1 = 0, port2 = 4)
    self.addLink(client4,s4, port1 = 0, port2 = 5)
    self.addLink(client5,s4,port1 = 0, port2 = 6)
    self.addLink(client6,s4,port1 = 0, port2 = 7)
    self.addLink(client7,s4,port1 = 0, port2 = 8)
    self.addLink(client8,s4,port1 = 0, port2 = 9)

    # Data center to web server
    self.addLink(h_server, s5, port1 = 0, port2=8)
    

    

    # Connecting core switch to other switches / open hosts- ???? how many ports do we have access to? 
    # Floor 1 switch 1 to core
    
    self.addLink(s1, s6, port1 = 3, port2 =1)

    # Floor 1 switch 2 to core
    self.addLink(s2, s6, port1 =3, port2 = 2)

    # Floor 2 switch 1 to core
    self.addLink(s3, s6, port1 =3, port2 = 3)

    # Air gapped floor to core
    self.addLink(s4, s6, port1 = 3, port2 = 4)

    # Trusted host to core
    self.addLink(h_trust, s6, port1 = 0, port2 = 5)

    # Data center to core
    self.addLink(s5, s6, port1 = 2, port2 = 6)

    # Dont add untrusted yet, do we need ports if all traffic dropped from here?
    # Clarifications - Only certain type of traffic dropped, can be added normally

    # untrusted to Core
    self.addLink(h_untrust, s6, port1 =0, port2 = 7)

    #print "Delete me!"

def configure():
  topo = final_topo()
  net = Mininet(topo=topo, controller=RemoteController)
  net.start()

  CLI(net)
  
  net.stop()


if __name__ == '__main__':
  configure()
