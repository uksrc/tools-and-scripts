#!/usr/bin/env python3

import subprocess
import re
import json

def get_lease_ids():
    result = subprocess.run(
        ["openstack", "reservation", "lease", "list"],
        capture_output=True, text=True
    )
    lines = result.stdout.splitlines()
    ids = []
    for line in lines:
        match = re.match(r"\|\s*([0-9a-f\-]{36})\s*\|", line)
        if match:
            ids.append(match.group(1))
    return ids

def get_lease_show_output(lease_id):
    result = subprocess.run(
        ["openstack", "reservation", "lease", "show", lease_id, "-f", "shell"],
        capture_output=True, text=True
    )
    return result.stdout

def parse_shell_output(shell_output):
    # Parse key="value" pairs into a dict, handling multi-line values
    result = {}
    key = None
    value_lines = []
    for line in shell_output.splitlines():
        match = re.match(r'^(\w+)="(.*)', line)
        if match:
            if key is not None:
                # Save the previous key-value
                result[key] = "\n".join(value_lines).rstrip('"')
            key, first_value = match.groups()
            value_lines = [first_value]
            # If this line ends with an unescaped quote, it's a single-line value
            if first_value.endswith('"') and not first_value.endswith('\\"'):
                result[key] = first_value[:-1]
                key = None
                value_lines = []
        else:
            # Continuation of a multi-line value
            if key is not None:
                value_lines.append(line)
    if key is not None:
        result[key] = "\n".join(value_lines).rstrip('"')
    return result

def extract_reservations(reservations_raw):
    # Unescape the string (replace \" with ")
    unescaped = reservations_raw.replace('\\"', '"')
    # Find all JSON objects in the string (handles multiple reservations)
    reservation_objs = re.findall(r'\{.*?\}(?=(?:\s*\{)|$)', unescaped, re.DOTALL)
    reservations = []
    for obj in reservation_objs:
        try:
            reservations.append(json.loads(obj))
        except Exception as e:
            print(f"Error parsing reservation: {e}")
    return reservations

def main():
    lease_ids = get_lease_ids()
    for lease_id in lease_ids:
        output = get_lease_show_output(lease_id)
        data = parse_shell_output(output)
        print(f"Lease name: {data.get('name')}")
        reservations_raw = data.get("reservations", "")
        reservations = extract_reservations(reservations_raw)
        for reservation in reservations:
            # Ensure amount is always an int
            amount = reservation.get("amount")
            try:
                amount = int(amount)
            except Exception:
                amount = amount  # fallback, just in case
            print(f"  reservation amount: {amount}")
            resource_properties_raw = reservation.get("resource_properties", "")
            try:
                # Unescape and parse the resource_properties JSON string
                resource_properties = json.loads(resource_properties_raw)
                rp_name = resource_properties.get("name")
                print(f"  resource_properties name: {rp_name}")
            except Exception as e:
                print(f"    Error parsing resource_properties: {e}")

if __name__ == "__main__":
    main()