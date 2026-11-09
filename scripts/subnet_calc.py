# iface = host address with prefix
# iface.ip = host address no prefix
# iface.network = network address with prefix
# iface.network.network_address = network address no prefix
# iface.network.broadcast_address = broadcast address


import ipaddress

cidr = "192.168.1.16/28"
iface = ipaddress.ip_interface(cidr)
net = iface.network
all_hosts = list(net.hosts())
first_host = all_hosts[0]
last_host = all_hosts[-1]
pref = net.prefixlen
hosts_number = 2 ** (32 - pref) - 2

print(f"Address: {iface.ip}")
print(f"Network: {net.network_address}")
print(f"Broadcast: {net.broadcast_address}")
print(f"Mask: {net.netmask}")
print(f"Addresses number: {net.num_addresses}")
print(f"First usable host: {first_host}")
print(f"Last usable host: {last_host}")
print(f"Usable hosts: {hosts_number}")
print(f"Formula: {hosts_number}, library: {len(all_hosts)}, match: {hosts_number == len(all_hosts)}")
