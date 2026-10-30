# Day 1 -> Linux VM, SSH, Network Basics

Date: 2026-10-30

## Target for today
Set up Ubuntu Server and establish connection through SSH

## What I achieved
- Installed Ubuntu Server 26.04.1 LTS in VirtualBox 
    (2 GB RAM, 2 CPUs, disk 20 GB VDI)
- Configured NAT with port forwarding 127.0.0.1:2222 -> 22
- Established SSH connection through PowerShell
- Made a snapshot after installation

## What I learned

### NAT (Network Addeess Translation) and Bridged connection difference

**NAT** 
- hides virtual machine from other devices in the same network 
- it behaves as a router
- network traffic goes through the host
- it has a private subnet 
- higher safety (isolation)

**Bridged**
- has direct access to the LAN
- is visible to other devices in LAN network
- behaves as a separate device
- gets IP from the same DHCP server
- exposed to LAN network

### SSH access to the VM (NAT + port forwarding)

- VM uses NAT so its address (10.0.2.15) is private and not directly reachable from the host
- Port forwarding rule maps host `127.0.0.1:2222` -> guest `:22` (SSH)
- 127.0.0.1 (loopback) means only this computer can use the rule, other devices from my network cannot
- Port 22 on the guest is the standard SSH port, port 2222 is arbitrary
- Connecting with: `ssh -p 2222 user@127.0.0.1`

### Testing connectivity vs DNS (ping 8.8.8.8 vs ping google.com)

- `ping 8.8.8.8` checks Internet connection, if it fails the problem is in connection itself (not DNS) 
- `ping google.com` also checks network connection AND proper DNS service, if 8.8.8.8 works but google.com doesn't, the problem is DNS
- Before sending any packet, the IP address of 'google.com' must be known, and thats what DNS server does - translates domain names to IP address

## Commands

- `ip a` shows interfaces and IP addresses
- `ss -tlnp` shows ports with listening services
- `systemctl status ssh` SSH service state
- `ping -c 4 <address>` sends 4 ICMP packets

## Problems and solutions

- **Problem:** `Connection closed by 127.0.0.1 port 2222` in first connection with `ssh -p 2222 user@127.0.0.1`
- **Diagnosis:** 
    - checked SSH service in VM with `systemctl status ssh`
    - confirmed the server listens on port 22 with `sudo ss -tlnp | grep :22`
    - tested local connection in VM `ssh user@localhost`
- **Solution:** the next connection from the host worked, probably SSH server was not ready on first try after installation (cause not confirmed)
- **Conclusion** first check the service locally in VM then the whole path through port forwarding