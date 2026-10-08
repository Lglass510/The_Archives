# Linux Notes

Ubuntu Server (Linux1) and Rocky Linux (reaper1) from The Keep.

## Network state

```bash
ip addr                     # interfaces and addresses
ip route                    # routing table
ip route get 172.16.10.10   # which route a packet would take
ip neigh                    # ARP / neighbor table
resolvectl status           # DNS servers in use
```

Reading a route: `172.16.10.0/24 dev eth0 proto kernel scope link src 172.16.10.30` means the subnet is directly connected on `eth0`, the kernel created the route, and `.30` is the source address.

## Netplan (Ubuntu)

```yaml
network:
  version: 2
  ethernets:
    eth0:
      addresses: [172.16.10.30/24]
      routes:
        - to: default
          via: 172.16.10.1
      nameservers:
        addresses: [172.16.10.10]
```

```bash
sudo netplan get
sudo netplan generate
sudo netplan try      # rolls back automatically if you don't confirm
sudo chmod 600 /etc/netplan/*.yaml   # clears the permissions warning
```

Use spaces, never tabs. "Inconsistent indentation" and "did not find expected" are both indentation errors.

## SSH

```sshconfig
Host rocky-linux
    HostName reaper1
    User <username>
    IdentityFile ~/.ssh/<key>
```

Domain account from Linux to a Windows DC (quotes keep the backslash):

```bash
ssh 'GLASSLAB\\Administrator'@<dc1-ip>
```

- Use keys with a passphrase. Keep keys out of every repository.
- Never expose a domain controller's SSH to the internet.
- Connection refused: is the host up, is `sshd` running, is the port open in the firewall?
- Permission denied: right username, public key installed for that account, client using the right key?
