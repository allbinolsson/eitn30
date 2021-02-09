import socket
from tuntap import TunTap

RCV_IP = "192.168.10.221"
MY_IP = "192.168.10.206"
UDP_PORT = 4000

if __name__ == "__main__":
    txSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rxSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rxSocket.bind((MY_IP, UDP_PORT))

    tun = TunTap(nic_type="Tun", nic_name="tun0")
    tun.config(ip="192.168.2.1", mask="255.255.255.0")

    while True:
        # buf = tun.read()
        # txSocket.sendto(buf, (RCV_IP, UDP_PORT))
        rcvd, addr = rxSocket.recvfrom(1024)
        print("Received: {}\tFrom address: {}".format(rcvd, addr))
        tun.write(rcvd)
    tun.close()