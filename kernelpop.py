import sys
from src.kernelpop import kernelpop
from constants import color_print, USAGE_STRING

# hacky rebind of input so we can use existing input() code for python2 and python3
try:
	input = raw_input
except NameError:
	pass


def main():

	# parse out whether we want a digestible output (json, xml)
	digest_type = None
	if "--digest" in sys.argv:
		if "json" in sys.argv:
			print("[*] outputting results in json digestible format")
			digest_type = "json"
		elif "xml" in sys.argv:
			print("[*] sorry, only json digestible output is supported at the moment (--digest json)")
			exit(0)

	if len(sys.argv) < 2:
		kernelpop()
	elif "-e" in sys.argv[1:3] and len(sys.argv) > 2:
		kernelpop(mode="exploit", exploit=sys.argv[2], digest=digest_type)
	elif "-i" in sys.argv[1:3] or "-u" in sys.argv[1:3]:
		color_print("[*] please note, vulnerability detection is not as accurate by uname alone", color="yellow")
		color_print("\tconsider running locally on the machine to be tested to get a more accurate reading", color="yellow")
		if "-i" in sys.argv[1:3]:
			uname = input("Please enter uname: ")
			if "darwin" in str(uname).lower():
				color_print("[!] macs require additional input", color="yellow")
				osx_ver = input("[*] Please enter the OSX `ProductVersion`. It is found in 2nd line of output of `sw_vers` command: ")
				if len(str(osx_ver).split(".")) != 3:
					color_print("[-] OSX version input is not correct (Major.Minor.Release i.e 10.9.5)", color="red")
					exit(1)
				kernelpop(mode="input", uname=uname, osx_ver=osx_ver, digest=digest_type)
			else:
				kernelpop(mode="input", uname=uname, digest=digest_type)
		else:
			# support for command line input of uname with '-u' flag
			if "darwin" in str(uname).lower():
				color_print("[!] cannot enumerate mac from uname alone...please use interactive-mode (-i)", color="red")
				exit(1)
			uname = " ".join(sys.argv[2:])
			color_print("[*] processing uname: {}".format(uname), color="yellow")
			kernelpop(mode="input", uname=uname, digest=digest_type)
	# if only --digest <option> is passed
	elif "--digest" in sys.argv[1:3]:
		kernelpop(digest=digest_type)
	else:
		color_print("[!] please format your arguments properly", color="yellow")
		color_print(USAGE_STRING)
		color_print("[-] closing ...", color="red")


if __name__ == "__main__":
	main()