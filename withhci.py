import subprocess
import datetime

def process_scan_output(output):
	output = output.decode()
	lines = output.split("\n")
	if len(lines) <= 1:
		print("Found no devices")
		return []

	# cut the "scanning..." line
	lines = lines[1:]

	devices = []

	# process remaining lines, each containing a device
	for line in lines:
		line = line.split("\t")
		if len(line) == 3:
			devices.append((line[1], line[2]))

	return devices

def request_information(address):
	info = subprocess.Popen(["hcitool", "info", address], stdout=subprocess.PIPE)
	output, err = info.communicate()
	output = output.decode()
	index = output.find("\n")
	output = output[index+1:]
	return output

def scan():
	run_hcitool = subprocess.Popen(["hcitool", "scan"], stdout=subprocess.PIPE)
	scan_output, err = run_hcitool.communicate()
	return process_scan_output(scan_output)

logged_devices = set()

while True:
	devices = scan()
	for device in devices:
		if device[0] not in logged_devices:
			logged_devices.add(device[0])
			info = request_information(device[0])
			print(datetime.datetime.now())
			print(info)
			print()
