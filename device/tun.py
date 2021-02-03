from pytun import TunTapDevice

tun = TunTapDevice(name="tun_device")
print(tun.name)

tun.addr = "192.168.1.10"
tun.dstaddr = "192.168.1.11"
tun.netmask = "255.255.255.0"
tun.mtu = 1500

tun.up()
buf = tun.read(tun.mtu)
tun.write(buf)

tun.close()