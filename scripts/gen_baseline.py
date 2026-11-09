"""Generate the login-hardening baseline for every device from one template.

Passwords come from environment variables, never from this file:
    LAB_ENABLE=... LAB_ADMIN=... python gen_baseline.py
Output goes to ./generated/<device>-baseline.txt
"""
import os
from pathlib import Path

SECRET = os.getenv('LAB_ENABLE', 'ChangeMe1')
ADMIN_PW = os.getenv('LAB_ADMIN', 'ChangeMe2')

# device name: last VTY line (routers 4, switches 15)
DEVICES = {
    'HQ-R1': 4, 'BR-R1': 4,
    'HQ-CORE1': 15, 'HQ-CORE2': 15,
    'HQ-ACC1': 15, 'HQ-ACC2': 15, 'BR-SW1': 15,
}

TEMPLATE = '''enable
configure terminal
enable secret {secret}
service password-encryption
ip domain-name campus.lab
username admin privilege 15 secret {admin}
access-list 10 permit 192.168.10.0 0.0.0.255
access-list 10 permit 192.168.110.0 0.0.0.255
line console 0
 login local
 exec-timeout 10 0
exit
line vty 0 {vty}
 login local
 transport input ssh
 access-class 10 in
 exec-timeout 10 0
end
'''

out = Path('generated')
out.mkdir(exist_ok=True)
for name, vty in DEVICES.items():
    text = TEMPLATE.format(secret=SECRET, admin=ADMIN_PW, vty=vty)
    (out / f'{name}-baseline.txt').write_text(text)
    print(f'[OK] {name}')
