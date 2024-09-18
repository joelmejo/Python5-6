from scapy.all import *
from scapy.layers.http import HTTPRequest, HTTPResponse

iPkt = 0
def process_packet(pkt):
    global iPkt
    iPkt += 1
    print("-------------------")

    if not pkt.haslayer(IP):
        return
    
    ip_layer = "IP_SRC: " + pkt[IP].src + " IP_DST: " + pkt[IP].dst + " \nPROTOCOLLO: " + str(pkt[IP].proto) + " LUNGHEZZA: " + str(pkt[IP].len)
    print(ip_layer)

    if pkt[IP].proto == 6:
        tcp_ports = "SOURCE_PORT: " + str(pkt[IP].sport) + " DEST_PORT: " + str(pkt[IP].dport)
        print(tcp_ports)
        if pkt[IP].sport == 443 or pkt[IP].dport == 443:
            print("PKT HTTPS")
        elif pkt[IP].sport == 80 or pkt[IP].dport == 80:
            print("PKT HTTP")
    

sniff(iface="enp4s0",filter="tcp",prn=process_packet)
