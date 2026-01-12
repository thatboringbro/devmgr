# devmgr

A Linux device control and audit tool designed to reduce endpoint attack surface by enabling,
disabling, and auditing hardware devices via kernel modules.

Built as a hands-on blue-team project to apply SOC and Linux hardening concepts beyond labs.

---

## Why this project exists

Modern Linux endpoints often expose unnecessary hardware such as webcams or Bluetooth adapters.
These devices increase the attack surface and can be abused by malware or unauthorized users.

`devmgr` was built as a blue-team focused tool to:
- Disable unused peripherals
- Verify device state
- Log actions for audit and investigation purposes

This project was created as part of my cybersecurity learning journey with a focus on SOC and
defensive operations.

---

## Features

- Enable or disable hardware devices via kernel modules
- Check device status (enabled / disabled)
- Root privilege enforcement
- Audit logging to `/var/log/devmgr.log`
- Simple, readable CLI output

---

## Supported devices (v1)

| Device     | Kernel module |
|-----------|---------------|
| Camera    | `uvcvideo`    |
| Bluetooth | `btusb`       |

---

## Usage

Make the script executable:

```bash
chmod +x devmgr.py
```

Run the tool:

```
sudo ./devmgr.py disable camera
sudo ./devmgr.py enable bluetooth
sudo ./devmgr.py status camera

```

## Contributions

Contributions, suggestions, and feedback are welcome.

For now, please reach out via X (Twitter):

https://x.com/thatboringbro

This project is part of my learning journey, and I’m happy to discuss ideas or improvements.
