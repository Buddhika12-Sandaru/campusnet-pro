# Role-Based Access Policy

Access is enforced with extended ACLs on the VLAN interfaces of both cores (identical on CORE1 and CORE2, because either can be the active gateway) and on the branch router.

| Role | VLAN | ACL | Allowed | Blocked |
|---|---|---|---|---|
| Staff | 10 | none | Everything | Nothing |
| Student | 20 | STUDENT_IN | Own gateway, DHCP, DNS and HTTP to HQ-SRV, replies to Staff, Internet | Other inside networks, branch, router and switch addresses |
| Guest | 30 | GUEST_IN | Own gateway, DHCP, DNS to HQ-SRV, replies to Staff, Internet | All inside networks including the web page on HQ-SRV |
| Servers | 40 | SERVERS_IN | DNS replies, TCP established, echo-reply, Internet | Starting connections to inside networks |
| Branch Guest | 130 | BR_GUEST_IN | Own gateway, DNS to HQ-SRV, replies to branch Staff, Internet | All other inside networks |

## Why the ACLs contain return-traffic rules

Extended ACLs are stateless. When Staff pings or opens a session to a student PC, the reply passes the Student ACL in the opposite direction and would be dropped by the `deny` line. Each ACL therefore allows only replies (`echo-reply`, `tcp ... established`) towards Staff. Students cannot start connections to Staff.

## Why DHCP has its own line

`permit udp any eq 68 any eq 67` lets DHCP renewals reach the DHCP server on the edge router. Without it, the `deny` for 10.0.0.0/8 would block renewals.

## Edge ACL (HQ-R1 and BR-R1, public interface, inbound)

Allows GRE, ESP and ISAKMP from the peer site, replies to our own traffic (`echo-reply`, `tcp established`), drops private and loopback source addresses (anti-spoofing), and logs everything else.
