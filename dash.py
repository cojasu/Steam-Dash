from winpcapy import WinPcapUtils
from binascii import hexlify
from steam import run

dash_macs = {
    "44:65:0d:65:48:8e" : "Campbells"
}

def is_arp(packet):
    eth_type1 = hexlify(packet[12])
    eth_type2 = hexlify(packet[13])
    return eth_type1 == '08' and eth_type2 == '06'

def who_has(packet):
    opcode1 = hexlify(packet[20])
    opcode2 = hexlify(packet[21])
    return opcode1 == '00' and opcode2 == '01'

def dash_button_press(mac):

    if mac in dash_macs:
        print("{0} button pressed".format(dash_macs[mac]))
    else:
        print("[{0}] unknown device".format(mac))

    if dash_macs[mac] == "Campbells":
        run()

def packet_callback(win_pcap, param, header, pkt_data):
    if not is_arp(pkt_data):
        return

    if not who_has(pkt_data):
        return

    # get IPs and MAC address
    ip_frame = pkt_data[14:]

    src_ip = ".".join([str(ord(b)) for b in ip_frame[0xe:0x12]])
    dst_ip = ".".join([str(ord(b)) for b in ip_frame[0x12:0x16]])
    src_mac = ":".join(hexlify(b) for b in ip_frame[0x8:0xe])

    if src_mac in dash_macs:
        dash_button_press(src_mac)

def main():
    WinPcapUtils.capture_on("*Ethernet*", packet_callback)

if __name__ == "__main__":
    main()