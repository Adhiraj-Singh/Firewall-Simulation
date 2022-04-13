# Final Skeleton


from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Final (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_final (self, packet, packet_in, port_on_switch, switch_id):
    

    # RULES
    # FLOOR 3 - NO LEAVING SUBNET
    # Untrusted host - NO ICMP TO FLOOR 1 or 2 or WEB SERVER
    # Untrusted host - NO IP to web server
    # Trusted host - NO ICMP to floor 1 OR WEB SERVER
    # Trusted host - NO TCP TO WEB SERVER
    # FLOOR 1 <----> FLOOR - NO ICMP IN BETWEEN EITHER WAY

    # First we determine if incoming traffic is ip or no, if not, flood the packet out


    # Should check ip traffic first
    tcpTrue = packet.find("tcp")
    ipTrue = packet.find("ipv4")
    icmpTrue = packet.find("icmp")
    

    # checking ig ip traffic
    if (ipTrue is not None):
      # checking switch id 
      # FLOOR 1 SWITCH 1 - REGULAR FILTERED TRAFFIC - NO RESTRICT - 2 hosts
      if(switch_id ==1):
        # now check which port it was received on
        # no icmp allowed between dep A and dep B, AKA floor and floor 2 - let core worry about that
        if (port_on_switch == 8):
          # if packet from laptop
          if(ipTrue.dstip == "20.2.1.20"):
            self.accept(packet,packet_in,9) # send to lab machine
          else:
            # send to core
            self.accept(packet, packet_in, 3)
        elif (port_on_switch ==9):
          # if input from lab machine, send to laptop or the core switch
          if(ipTrue.dstip == "20.2.1.10"):
            self.accept(packet,packet_in, 8)
          else:
            #send to core
            self.accept(packet,packet_in,3)
        elif(port_on_switch ==3):
          # this means info has been passed from the core switch 
          # now check if information going to valid addresses, otherwise drop the packet
          if(ipTrue.dstip == "20.2.1.10"):
            self.accept(packet, packet_in, 8) # send to laptop
          elif(ipTrue.dstip == "20.2.1.20"):
            self.accept(packet, packet_in, 9)
          else:
            # dropping the packet
            self.drop(packet, packet_in)
        # not doing any action for unknown port, no errors expected
      
      # FLOOR 1 - SWITCH 2 - REGULAR TRAFFIC - NO RESTRICT - 2 Hosts
      if (switch_id ==2):
        if (port_on_switch == 8):
          # if packet from device 1
          if(ipTrue.dstip == "20.2.1.40"):
            self.accept(packet,packet_in,9) # send to device 2
          else:
            # send to core
            self.accept(packet, packet_in, 3)
        elif (port_on_switch ==9):
          # if input from device 2, send to device 1or the core switch
          if(ipTrue.dstip == "20.2.1.30"):
            self.accept(packet,packet_in, 8)
          else:
            #send to core
            self.accept(packet,packet_in,3)
        elif(port_on_switch ==3): # checking if received FROM core
          # this means info has been passed from the core switch 
          # now check if information going to valid addresses, otherwise drop the packet
          if(ipTrue.dstip == "20.2.1.30"):
            self.accept(packet, packet_in, 8) # send to device1
          elif(ipTrue.dstip == "20.2.1.40"):
            self.accept(packet, packet_in, 9) # send to device 2
          else:
            # dropping the packet
            self.drop(packet, packet_in)

      # FLOOR 2 - SWITCH 1 - REGULAR TRAFFIC - Save restrictons for core logic??
      if(switch_id == 3):
        if (port_on_switch == 8):
          # if packet from host 1
          if(ipTrue.dstip == "10.2.7.20"):
            self.accept(packet,packet_in,9) # send to host 2
          else:
            # send to core
            self.accept(packet, packet_in, 3)
        elif (port_on_switch ==9):
          # if input from host 2, send to host 2 or the core switch
          if(ipTrue.dstip == "10.2.7.10"):
            self.accept(packet,packet_in, 8)
          else:
            #send to core
            self.accept(packet,packet_in,3)
        elif(port_on_switch ==3): # if coming from core
          # this means info has been passed from the core switch 
          # now check if information going to valid addresses, otherwise drop the packet
          if(ipTrue.dstip == "10.2.7.10"):
            self.accept(packet, packet_in, 8) # send to host 1
          elif(ipTrue.dstip == "10.2.7.20"):
            self.accept(packet, packet_in, 9) # send to host 2
          else:
            # dropping the packet
            self.drop(packet, packet_in)
      
      # AIR TIGHT FLOOR - ONLY INTERNAL COMMUNICATION ALLOWED
      # Check and compare with all IP addresses, if none match, drop the packet 
      # Check if src is internal , otherwise drop packet
      # check dstip, if valid, send, otherwise drop
      if(switch_id == 4):
        if(ipTrue.srcip == "40.2.5.00" or ipTrue.srcip == "40.2.5.10" or ipTrue.srcip == "40.2.5.20" or ipTrue.srcip == "40.2.5.30" or ipTrue.srcip == "40.2.5.40" or ipTrue.srcip == "40.2.5.50" or ipTrue.srcip == "40.2.5.60" or ipTrue.srcip == "40.2.5.70"):
          if(ipTrue.dstip == "40.2.5.00"):
            self.accept(packet,packet_in, 1)
          elif(ipTrue.dstip == "40.2.5.10"):
            self.accept(packet,packet_in,2)
          elif(ipTrue.dstip == "40.2.5.20"):
            self.accept(packet,packet_in,4)
          elif(ipTrue.dstip == "40.2.5.30"):
            self.accept(packet,packet_in,5)
          elif(ipTrue.dstip == "40.2.5.40"):
            self.accept(packet,packet_in,6)
          elif(ipTrue.dstip == "40.2.5.50"):
            self.accept(packet,packet_in,7)
          elif(ipTrue.dstip == "40.2.5.60"):
            self.accept(packet,packet_in,8)
          elif(ipTrue.dstip == "40.2.5.70"):
            self.accept(packet,packet_in,9)
          else:
            self.drop(packet,packet_in)
      
      # DATA CENTER - ONE HOST - WEB SERVER - NO RESTRICT
      if(switch_id == 5):
        if(port_on_switch == 8):
          self.accept(packet,packet_in,2)
        elif(port_on_switch == 2):
          if(ipTrue.dstip == "30.1.4.66"):
            self.accept(packet,packet,8)
          else:
            self.drop(packet,packet_in)
        else:
          self.drop(packet,packet_in)
      
      # CORE SWITCH - WILL IMPLEMENT RULES HERE - 
      if(switch_id == 6):

        # checking for icmp packet - larger set of rules for ICMP so first, then check for tcp and rest
        if(icmpTrue is not None):
          # go through every port
          # floor 1 switch 1 incoming
          if(port_on_switch == 1):
            if (ipTrue.dstip == "10.2.7.10" or ipTrue.dstip == "10.2.7.20"):
              self.drop(packet,packet_in)
            elif(ipTrue.dstip == "20.2.1.30" or ipTrue.dstip == "20.2.1.40" ):
              self.accept(packet,packet_in,2)
            elif(ipTrue.dstip == "104.24.32.100"):
              self.accept(packet,packet_in,5)
            elif(ipTrue.dstip == "108.44.83.103"):
              self.accept(packet,packet_in,7)
            elif(ipTrue.dstip == "30.1.4.66"):
              self.accept(packet, packet_in,6)
          
          # incoming from floor 1 switch 2
          if(port_on_switch == 2):
            if (ipTrue.dstip == "10.2.7.10" or ipTrue.dstip == "10.2.7.20"):
              self.drop(packet,packet_in)
            elif(ipTrue.dstip == "20.2.1.10" or ipTrue.dstip == "20.2.1.20" ):
              self.accept(packet,packet_in,1)
            elif(ipTrue.dstip == "104.24.32.100"):
              self.accept(packet,packet_in,5)
            elif(ipTrue.dstip == "108.44.83.103"):
              self.accept(packet,packet_in,7)
            elif(ipTrue.dstip == "30.1.4.66"):
              self.accept(packet, packet_in,6)
          
          # incoming from floor 2 switch 1
          if(port_on_switch == 3):
            if (ipTrue.dstip == "20.2.1.10" or ipTrue.dstip == "20.2.1.20" or ipTrue.dstip == "20.2.1.30" or ipTrue.dstip == "20.2.1.40"):
              self.drop(packet,packet_in)
            elif(ipTrue.dstip == "104.24.32.100"):
              self.accept(packet,packet_in,5)
            elif(ipTrue.dstip == "108.44.83.103"):
              self.accept(packet,packet_in,7)
            elif(ipTrue.dstip == "30.1.4.66"):
              self.accept(packet, packet_in,6)
          
          # incoming from trusted host
          if(port_on_switch == 5):
            # CHECKING IF TCP RULES NEED TO BE APPLIED
            if(tcpTrue is None):
              if(ipTrue.dstip == "20.2.1.10" or ipTrue.dstip == "20.2.1.20" or ipTrue.dstip == "20.2.1.30" or ipTrue.dstip == "20.2.1.40" or ipTrue.dstip == "30.1.4.66"):
                self.drop(packet, packet_in)
              elif(ipTrue.dstip == "108.44.83.103"):
                self.accept(packet,packet_in,7)
              elif(ipTrue.dstip == "10.2.7.10" or ipTrue.dstip == "10.2.7.20"):
                self.accept(packet,packet_in,3)
            else:
              if(ipTrue.dstip == "30.1.4.66"):
                self.drop(packet,packet_in)
              elif(ipTrue.dstip == "20.2.1.10" or ipTrue.dstip == "20.2.1.20"):
                self.accept(packet, packet_in, 1)
              elif(ipTrue.dstip == "20.2.1.30" or ipTrue.dstip == "20.2.1.40"):
                self.accept(packet,packet_in,2)
              elif(ipTrue.dstip == "108.44.83.103"):
                self.accept(packet,packet_in, 7)
              elif(ipTrue.dstip == "10.2.7.10" or ipTrue.dstip == "10.2.7.20"):
                self.accept(packet,packet_in, 3)
          
          # incoming from untrusted host 
          if(port_on_switch == 7):
            if(ipTrue.dstip == "20.2.1.10" or ipTrue.dstip == "20.2.1.20" or ipTrue.dstip == "20.2.1.30"  or ipTrue.dstip == "20.2.1.40" or ipTrue.dstip == "10.2.7.10" or ipTrue.dstip == "10.2.7.20" or ipTrue.dstip == "30.1.4.66"):
              self.drop(packet,packet_in)
            elif(ipTrue.dstip == "104.24.32.100"):
              self.accept(packet,packet_in, 5)
          
          # incoming from data center
          if(port_on_switch == 6):
            if(ipTrue.dstip == "20.2.1.10" or ipTrue.dstip == "20.2.1.20"):
              self.accept(packet,packet_in,1)
            elif(ipTrue.dstip == "20.2.1.30" or ipTrue.dstip == "20.2.1.40"):
              self.accept(packet,packet_in,2)
            elif(ipTrue.dstip == "104.24.32.100"):
              self.accept(packet,packet_in,5)
            elif(ipTrue.dstip == "108.44.83.103"):
              self.accept(packet,packet_in,7)
            elif(ipTrue.dstip == "10.2.7.10" or ipTrue.dstip == "10.2.7.20"):
              self.accept(packet,packet_in,3)
        # in case it is not icmp traffic, any other ip traffic dropped if from untrusted to web server

        elif(ipTrue.srcip == "108.44.83.103" and ipTrue.dstip == "30.1.4.66"):
          self.drop(packet,packet_in)
        # drop if tcp coming from host to web server
        elif(ipTrue.srcip == "104.24.32.100" and ipTrue.dstip == "30.1.4.66" and (tcpTrue is not None)):
          self.drop(packet,packet_in)
        # do i need to code all over again for other traffic???
        else:
          self.accept(packet,packet_in, of.OFPP_FLOOD)
    else:
      self.accept(packet,packet_in,of.OFPP_FLOOD)


    #print "Example code."

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.port, event.dpid)
  
  def accept(self, packet, packet_in, output_port):
    # seperate function to create a new open flow entry and send out packet
    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)
    # Time out defined in assignment pdf
    msg.idle_timeout = 30
    msg.hard_timeout = 30
    msg.buffer_id = packet_in.buffer_id
    #send message out, first define the port action
    msg.actions.append(of.ofp_action_output(port = output_port))
    msg.data = packet_in
    self.connection.send(msg)
  
  # creating seperate drop function
  def drop(self,packet, packet_in):
    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)
    msg.idle_timeout = 30
    msg.hard_timeout = 30

    msg.buffer_id = packet_in.buffer_id
    self.connection.send(msg)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
