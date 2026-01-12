#!/usr/bin/env python3

import sys
import os
import subprocess
import logging
import pwd
from datetime import datetime


DEVICE_MAP = {
    "camera": "uvcvideo",
    "bluetooth": "btusb"
}

LOG_FILE = "/var/log/devmgr.log"

def setup_logging():
    try:
        logging.basicConfig(
            filename=LOG_FILE,
            level=logging.INFO,
            format="%(asctime)s | user=%(user)s | %(message)s",
        )
    except Exception:
        pass


def log_event(message):
    try:
        uid = os.geteuid()
        user = pwd.getpwuid(uid).pw_name
        logging.info(message, extra={"user": user})
    except Exception:
        pass



def require_root():
    if os.geteuid() != 0:
        print("[!] This tool must be run as root.")
        log_event("execution failed | reason=not root")
        sys.exit(1)


def usage():
    print("Usage: devmgr <enable|disable|status> <device>")
    print("Supported devices:", ", ".join(DEVICE_MAP.keys()))
    log_event("execution failed | reason=invalid usage")
    sys.exit(1)


def disable_module(module, device):
    try:
        print(f"[*] Disabling module: {module}")
        subprocess.run(
            ["modprobe", "-r", module],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"[+] {module} disabled successfully.")
        log_event(f"action=disable | device={device} | result=success")

    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to disable {module}.")
        log_event(
            f"action=disable | device={device} | result=failure | error={e.stderr.strip()}"
        )


def enable_module(module, device):
    try:
        print(f"[*] Enabling module: {module}")
        subprocess.run(
            ["modprobe", module],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"[+] {module} enabled successfully.")
        log_event(f"action=enable | device={device} | result=success")

    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to enable {module}.")
        log_event(
            f"action=enable | device={device} | result=failure | error={e.stderr.strip()}"
        )


def module_status(module, device):
    try:
        result = subprocess.run(
            ["lsmod"],
            check=True,
            capture_output=True,
            text=True
        )

        if module in result.stdout:
            print(f"[+] {module} status: ENABLED")
            log_event(f"action=status | device={device} | state=enabled")
        else:
            print(f"[-] {module} status: DISABLED")
            log_event(f"action=status | device={device} | state=disabled")

    except subprocess.CalledProcessError:
        print("[!] Failed to determine module status.")
        log_event(f"action=status | device={device} | result=failure")



def main():
    print("Welcome to the device manager tool!")
    print("Author: redacted")
    print("Twitter(X): @thatboringbro\n")

    setup_logging()
    log_event("tool started")

    require_root()

    if len(sys.argv) != 3:
        usage()

    action = sys.argv[1].lower()
    device = sys.argv[2].lower()

    if device not in DEVICE_MAP:
        print(f"[!] Device not supported: {device}")
        log_event(f"execution failed | unsupported device={device}")
        usage()

    module = DEVICE_MAP[device]

    print(f"[*] Requested action: {action}")
    print(f"[*] Target device: {device} ({module})\n")

    if action == "disable":
        disable_module(module, device)
    elif action == "enable":
        enable_module(module, device)
    elif action == "status":
        module_status(module, device)
    else:
        print("[!] Invalid action.")
        usage()


if __name__ == "__main__":
    main()
