# Addressing Table

## VLANs and subnets

| VLAN | Name | Network | Virtual gateway (HSRP) | CORE1 / CORE2 | Addresses from |
|---|---|---|---|---|---|
| 10 | STAFF | 192.168.10.0/24 | 192.168.10.1 | .2 / .3 | DHCP (HQ-R1) |
| 20 | STUDENT | 192.168.20.0/24 | 192.168.20.1 | .2 / .3 | DHCP (HQ-R1) |
| 30 | GUEST | 192.168.30.0/24 | 192.168.30.1 | .2 / .3 | DHCP (HQ-R1) |
| 40 | SERVERS | 192.168.40.0/24 | 192.168.40.1 | .2 / .3 | Static: HQ-SRV .10 |
| 99 | MGMT | 192.168.99.0/24 | 192.168.99.1 | .2 / .3 | Static: ACC1 .11, ACC2 .12 |
| 110 | BR-STAFF | 192.168.110.0/24 | 192.168.110.1 (BR-R1) | | DHCP (BR-R1) |
| 130 | BR-GUEST | 192.168.130.0/24 | 192.168.130.1 (BR-R1) | | DHCP (BR-R1) |
| 199 | BR-MGMT | 192.168.199.0/24 | 192.168.199.1 (BR-R1) | | Static: BR-SW1 .2 |
| 999 | NATIVE-UNUSED | none | none | | Native and black-hole VLAN |

## Point-to-point links

| Link | Network | Addresses |
|---|---|---|
| HQ-R1 Gi0/0 to HQ-CORE1 Gi0/1 | 10.0.0.0/30 | R1 .1, CORE1 .2 |
| HQ-R1 Gi0/1 to HQ-CORE2 Gi0/1 | 10.0.0.4/30 | R1 .5, CORE2 .6 |
| HQ-R1 Gi0/2 to ISP Gi0/0 | 200.0.0.0/30 | R1 .1, ISP .2 |
| BR-R1 Gi0/1 to ISP Gi0/1 | 200.0.1.0/30 | BR-R1 .1, ISP .2 |
| ISP Gi0/2 to Internet-Server | 203.0.113.0/30 | ISP .1, server .2 |
| GRE tunnel HQ-R1 to BR-R1 | 10.255.255.0/30 | HQ-R1 .1, BR-R1 .2 |
| HQ-R1 Loopback0 | 10.255.0.1/32 | DHCP relay target |

## OSPF router IDs (process 1, area 0)

HQ-R1 1.1.1.1, HQ-CORE1 2.2.2.2, BR-R1 3.3.3.3, HQ-CORE2 4.4.4.4

## Cabling

| From | To | Purpose |
|---|---|---|
| HQ-R1 Gi0/0 | HQ-CORE1 Gi0/1 | Routed link |
| HQ-R1 Gi0/1 | HQ-CORE2 Gi0/1 | Routed link |
| HQ-R1 Gi0/2 | ISP Gi0/0 | HQ public link |
| BR-R1 Gi0/1 | ISP Gi0/1 | Branch public link |
| ISP Gi0/2 | Internet-Server Fa0 | Web server |
| HQ-CORE1 Fa0/1-2 | HQ-CORE2 Fa0/1-2 | EtherChannel Po12 |
| HQ-CORE1 Fa0/3 | HQ-ACC1 Fa0/1 | Uplink A |
| HQ-CORE2 Fa0/3 | HQ-ACC1 Fa0/2 | Uplink B |
| HQ-CORE1 Fa0/4 | HQ-ACC2 Fa0/1 | Uplink A |
| HQ-CORE2 Fa0/4 | HQ-ACC2 Fa0/2 | Uplink B |
| HQ-ACC1 Fa0/3, Fa0/4 | PC-Staff, PC-Student | VLAN 10, 20 |
| HQ-ACC2 Fa0/3, Fa0/4 | PC-Guest, HQ-SRV | VLAN 30, 40 |
| BR-R1 Gi0/0 | BR-SW1 Fa0/1 | Branch trunk |
| BR-SW1 Fa0/2, Fa0/3 | BR-PC-Staff, BR-PC-Guest | VLAN 110, 130 |
