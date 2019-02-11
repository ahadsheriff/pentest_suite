"""
    Simple port scanner using netcat 
"""

import sys
import getopt
import subprocess
import re

def main():
	host = input("Enter a host ip address: ")
	start = input("Enter a start port:")
	end = input("Enter an end port: ")

	scanner(host, start, end)

def scanner(host, start, end):

	# store netcat port scanning command
	cmd = 'nc -zp 9090 ' + host + ' ' + start + '-' + end + ' -v'
	print("SCANNING...")

	# write output to a txt file
	with open("./outfile.txt", "wb", 0) as out:
		subprocess.run([cmd], stdout=out, check=True, shell=True)

main()
