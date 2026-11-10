# Problem Log

Real problems found while testing, with the evidence and the fix.

## 1. ACLs existed but were not applied

- **Symptom:** a Student PC could ping the Staff PC and the server; a Guest PC could open the internal web page. Both should be blocked.
- **What I checked:** `show access-lists` on HQ-CORE1 listed STUDENT_IN, GUEST_IN and SERVERS_IN, but none showed match counters.
- **Cause:** the ACLs were defined, but the `ip access-group ... in` lines on the VLAN interfaces were missing.
- **Fix:** applied the ACLs on VLAN 20, 30 and 40 on both cores. Verified with `show ip interface vlan 20` (inbound ACL listed) and retested; the blocked tests then failed as expected while Internet access still worked.
- **Lesson:** an ACL does nothing until it is bound to an interface and direction. Match counters are the fastest proof.

## 2. OSPF did not form over the GRE tunnel

- **Symptom:** ping to the branch returned "Destination host unreachable" from the ISP address; tracert left through the ISP instead of the tunnel. `show ip ospf neighbor` on HQ-R1 showed two neighbours, not three.
- **What I checked:** Tunnel0 was up/up, and IPsec showed `QM_IDLE`, so the tunnel and encryption were fine. The tunnel interface showed packets in but none out, which meant HQ-R1 was not sending OSPF hellos. HQ-CORE1 had no routes for the branch networks.
- **Cause:** the tunnel interface was still passive in OSPF. The command `no passive-interface tunnel 0` was rejected by this Packet Tracer version.
- **Fix:** removed `passive-interface default` and made only the loopback and the public interface passive instead. The same on BR-R1. Neighbours reached FULL and the branch tests passed.
- **Lesson:** when a tunnel is up but routing is missing, check the routing protocol on the tunnel, not the tunnel itself. Simulator syntax can differ from real IOS, so keep a workaround that does not depend on the interface name.

## 3. Edge ACL on the wrong device

- **Symptom:** `show access-lists OUTSIDE_IN` printed nothing on HQ-R1, while the list appeared on HQ-CORE1.
- **Cause:** the edge ACL block was pasted on a core switch. Its last line was also not the intended `deny ip any any log`.
- **Fix:** removed it from the core, applied it on the public interface of HQ-R1 and BR-R1, and made the last line `deny ip any any log`. Re-tested the tunnel afterwards.
- **Lesson:** filter on the device and interface where the traffic actually enters, and retest the critical path (the tunnel) after any edge filtering.

## 4. Locked out by credentials

- **Symptom:** device login rejected after hardening.
- **Cause:** after hardening, the console and VTY lines use `login local`, so a username and password are required. Earlier projects used different values.
- **Fix:** recorded the lab credentials in a private note (not in the repository) and reset one device with the `username` and `enable secret` commands.
- **Lesson:** write credentials down before enabling `login local` and `login block-for`, and keep an unhardened backup file.

## 5. OSPF key not supported on the tunnel interface

- Symptom: `ip ospf message-digest-key` was rejected on Tunnel0.
- Cause: this Packet Tracer version does not support the command on tunnel interfaces.
- Decision: kept MD5 authentication on the internal routed links and relied on IPsec
  (ESP with AES-256) to protect the tunnel, including the OSPF packets inside it.
- Lesson: when a feature is missing in a simulator, say so, and check what else already
  protects the same traffic.