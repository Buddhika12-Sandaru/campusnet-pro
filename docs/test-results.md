# Test Plan and Results

Tick a row only when its screenshot is in `screenshots/`. Screenshot names are listed so the table links to the proof.

| # | From | Action | Expected | Proves | Evidence | Done |
|---|---|---|---|---|---|---|
| 1 | PC-Staff | `ipconfig` | 192.168.10.x, gateway .10.1, DNS 192.168.40.10 | DHCP relay through HSRP | test01_dhcp_staff.png | [ ] |
| 2 | PC-Staff | `ping 192.168.40.10` | Replies | Staff reaches servers | test02_staff_server.png | [ ] |
| 3 | PC-Staff | ping Student PC | Replies | Echo-reply rule | test03_staff_student.png | [ ] |
| 4 | PC-Student | ping Staff PC | Blocked | Student ACL | test04_student_staff_blocked.png | [ ] |
| 5 | PC-Student | `ping 192.168.40.10` | Blocked | Only DNS and web allowed | test05_student_server_blocked.png | [ ] |
| 6 | PC-Student | Browser http://192.168.40.10 | Page opens | TCP 80 allowed | test06_student_web.png | [ ] |
| 7 | PC-Guest | Browser http://192.168.40.10 | Blocked | Guest isolation | test07_guest_web_blocked.png | [ ] |
| 8 | PC-Guest | Browser www.example.com | Page opens | DNS, NAT, Internet for guests | test08_guest_internet.png | [ ] |
| 9 | PC-Student | `ping 203.0.113.2` | Replies | NAT overload | test09_student_internet.png | [ ] |
| 10 | HQ-SRV | `ping 192.168.10.11` | Blocked | Servers ACL | test10_server_blocked.png | [ ] |
| 11 | HQ-R1 | `show ip nat translations` | Entries listed | NAT table | test11_nat.png | [ ] |
| 12 | PC-Staff | ping BR-PC-Staff | Replies | GRE tunnel and OSPF | test12_staff_branch.png | [ ] |
| 13 | PC-Staff | `tracert` BR-PC-Staff | 192.168.10.1, 10.0.0.1, 10.255.255.2, PC | Traffic uses the tunnel | test13_tracert_tunnel.png | [ ] |
| 14 | BR-PC-Guest | `ping 192.168.40.10` | Blocked | Branch guest ACL | test14_brguest_blocked.png | [ ] |
| 15 | BR-PC-Guest | Browser www.example.com | Page opens | DNS over tunnel, branch NAT | test15_brguest_internet.png | [ ] |
| 16 | BR-PC-Staff | ping BR-PC-Guest | Replies | Branch echo-reply rule | test16_branch_staff_guest.png | [ ] |
| 17 | PC-Staff | `ssh -l admin 10.0.0.1`, then `telnet 10.0.0.1` | SSH login, Telnet refused | SSH on, Telnet off | test17_ssh_telnet.png | [ ] |
| 18 | PC-Student | `ssh -l admin 10.0.0.1` | Fails | VTY ACL and Student ACL | test18_student_ssh_blocked.png | [ ] |
| 19 | HQ-R1 | `show ip ospf neighbor` | 3 neighbours FULL | OSPF | test19_ospf_neighbors.png | [ ] |
| 20 | HQ-R1 | `show ip ospf interface gi0/0` | Message-digest authentication | OSPF authentication | test20_ospf_auth.png | [ ] |
| 21 | HQ-CORE1/2 | `show standby brief` | CORE1 Active, CORE2 Standby | HSRP | test21_hsrp.png | [ ] |
| 22 | HQ-ACC1 | `show spanning-tree vlan 10` | One Root FWD, one Altn BLK | Rapid-PVST+ | test22_stp.png | [ ] |
| 23 | HQ-CORE1 | `show etherchannel summary` | Po12(SU) | LACP | test23_etherchannel.png | [ ] |
| 24 | HQ-R1 | `show crypto isakmp sa` | QM_IDLE | IPsec up | test24_ipsec.png | [ ] |
