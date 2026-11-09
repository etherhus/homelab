# Day 03 -> IPv4 subnet calculation, Python ipaddress module, basic subnet calculator

Date: 2026-11-09

## Target for today
Learn to calculate subnets by hand and verify results with a Python script

## What I achieved
- Calculated network address, broadcast, host range and mask for several subnets by hand (/24, /26, /27, /28)
- Wrote `scripts/subnet_calc.py` which analyses a subnet (network, broadcast, mask, host range and host count) using the `ipaddress` module, and verified it with my manual results

## What I learned

### IP Address
- IP address is used to identify a device in a network and lets routers deliver packets to it
- It consists of 32 bits and 4 octets (8 bits each)
- The prefix /N shows how many of the first bits belong to the network part, the remaining `32-N` bits are the host part. With `/24` the first three octets are the network, but with `/26` the boundary is inside the last octet
- Addresses in a subnet: `2^(32 - N)`. Usable hosts: `2^(32 - N) - 2`, because the first address is the network address and the last one is the broadcast address
- Subnet mask marks which bits of an address are the network part and which are the host part, device uses it to decide if destination is in its own subnet (send directly, ARP finds the MAC address) or outside it (send via the default gateway)
- Broadcast address is used to send data packets to every device on LAN network or subnet at the same time (one-to-all communication), its the last address in subnet

### Examples in practice
- `192.168.10.0/27` 
    - Mask: 24 + 3 network bits = `11111111.11111111.11111111.11100000` = `255.255.255.224`
    - Host bits: 5, so `2^5 = 32` addresses and `32 - 2 = 30` usable hosts
    - Block size: `256 - 224 = 32`; network: `0 // 32 = 0`, `0 * 32 = 0`, so `192.168.10.0`
    - Broadcast: `0 + 32 - 1 = 31`, so `192.168.10.31`
    - Usable hosts: `192.168.10.1 - 192.168.10.30`

- `10.0.5.77/26` 
    - Mask: 24 bits + 2 bits from host part = `11111111.11111111.11111111.11000000` = `255.255.255.192`
    - Block size: `256 - 192 = 64`; network: `77 // 64 = 1`, `1 * 64 = 64`, so `10.0.5.64`
    - Broadcast: `64 + 64 - 1 = 127`, so `10.0.5.127`
    - Usable hosts: `10.0.5.65 - 10.0.5.126` (62 hosts)

## Python script: `scripts/subnet_calc.py`

Takes an address with a prefix (currently set in the `cidr` variable) and prints: address, network address, broadcast, mask, number of addresses, first and last usable host and number of usable hosts

### How it works:
- `ipaddress.ip_interface(cidr)` returns an object holding the host address and the prefix
- `iface.ip` is the host address, `iface.network` is the network object
- `net.network_address`, `net.broadcast_address`, `net.netmask`, `net.num_addresses` and `net.hosts()` give the rest
- Usable hosts are calculated with my own formula `2 ** (32 - prefix) - 2` and can be compared with `len(list(net.hosts()))`

### Limitations and next step:
- The address is hardcoded and there is no input validation
- The formula doesn't work for `/31` and `/32`
- Next: read the address from the command line, handle errors, add a `--split` option

## Problems and solutions

- **Problem:** I calculated the broadcast of `10.0.5.64/26` as `10.0.5.128` and the host range up to `.127`
- **Diagnosis:** I forgot to subtract 1, so I got the start of the next subnet instead of the end of this one. The range had 65 addresses instead of 64
- **Solution:** broadcast = start of the next subnet - 1; checked the result with my script
- **Conclusion:** count the addresses in the range and compare with the block size
