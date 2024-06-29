#!/usr/bin/env python

# To Run: on command line, enter: python3 mac_changer.py -i eth0 -m 00:11:22:33:44:55
# change eth0 to wan0 or other.
# change mac_address to whatever you want.

import subprocess
import optparse
import re


def get_args():
    # Create an OptionParser object to handle command-line arguments
    parser = optparse.OptionParser()
    # Add an option for the interface, storing its value in the 'interface' attribute
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address.")
    # Add an option for the new MAC address, storing its value in the 'new_mac' attribute
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address.")
    # Parse the command-line arguments and store them in 'options' and 'arguments'
    (options, arguments) = parser.parse_args()
    # Check if an interface was specified
    if not options.interface:
        # If not, display an error message and exit
        parser.error("[-] Please specify an interface, use --help for more info.")
    # Check if a new MAC address was specified
    elif not options.new_mac:
        # If not, display an error message and exit
        parser.error("[-] Please specify a new mac address, use --help for more info.")
    # If all required options were specified, return the 'options' object
    return options


def get_curr_mac(interface):
    # Use subprocess to run the 'ifconfig' command with the specified interface
    # and capture the output
    ifconfig_results = subprocess.check_output(["ifconfig", interface])
    # Use regular expression to search for the MAC address in the output
    # The pattern matches 6 pairs of hexadecimal digits separated by colons
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_results))
    
    # If a MAC address was found, return it
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        # If not, print an error message
        print("[-] Could not read MAC address.")


def change_mac(interface, new_mac):
    # Print a message indicating that the MAC address is being changed
    print("[+] Changing MAC Address for " + interface + " to: " + str(new_mac))
    # Use subprocess to run the 'ifconfig' command to:
    # 1. Bring the interface down
    subprocess.call(["ifconfig", interface, "down"])
    # 2. Set the new MAC address
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    # 3. Bring the interface back up
    subprocess.call(["ifconfig", interface, "up"])

# Get the command-line arguments using the get_args function
options = get_args()

# Get the current MAC address of the specified interface
curr_mac = get_curr_mac(options.interface)
# Print the current MAC address
print("Current MAC address is: " + str(curr_mac))

# Change the MAC address using the change_mac function
change_mac(options.interface, options.new_mac)

# Get the new current MAC address (after the change)
curr_mac = get_curr_mac(options.interface)
# Check if the MAC address was successfully changed
if curr_mac == options.new_mac:
    # If it was changed, print a success message
    print("[+] MAC address was successfully changed to: " + str(curr_mac))
else:
    # If not, print an error message
    print("[-] MAC address was not changed.")
