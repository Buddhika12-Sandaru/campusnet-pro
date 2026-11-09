# Device configs

One file per device: `HQ-R1.txt`, `HQ-CORE1.txt`, `HQ-CORE2.txt`, `HQ-ACC1.txt`, `HQ-ACC2.txt`, `BR-R1.txt`, `BR-SW1.txt`, `ISP.txt`.

## How to export

1. Open the device CLI and run `show running-config`.
2. Press the spacebar until the whole config is shown, then copy it.
3. Save it as a `.txt` file named after the device, in a folder called `configs_raw/` (not committed).
4. Clean the secrets:

   ```
   python scripts/sanitize_configs.py configs_raw configs
   ```

5. Open every file in `configs/` and check that no password, key or secret is left.

Passwords and keys are shown as `<lab-secret>`.
