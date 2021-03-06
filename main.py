#!/usr/bin/python
import sys
import argparse
import PyPDF2
import bruteforcer
import signal
import string

def main(argv):
	signal.signal(signal.SIGINT, lambda x,y: sys.exit(0)) # Ctrl+c
	argParser = argparse.ArgumentParser()
	methodGroup = argParser.add_mutually_exclusive_group(required=True)
	argParser.add_argument("pdf", help="Designate a pdf file")
	methodGroup.add_argument("-w", help="Use a wordlist")
	methodGroup.add_argument("-b", help="Bruteforce every possible password",
		action="store_true")
	argParser.add_argument("-l", help="Chose character lists for -b argument")
	argParser.add_argument("-c", help="Designate custom character set")
	argParser.add_argument("-max", help="Chose maximum length of password",
		type=int)
	argParser.add_argument("-min", help="Chose minimum length of password",
		type=int, default=1)
	args = argParser.parse_args()
	print(args)
	try:
		print("[*] Opening PDF...")
		pdfReader = PyPDF2.PdfFileReader(open(args.pdf, 'rb'))
		if pdfReader.isEncrypted == False:
			print("[!] Operation failed: the PDF is not encrypted.")
			exit()
		else:
			print("[*] PDF is encrypted, continuing...")
			try:
				guesser = bruteforcer.Guesser()
				guesserMinLength = 1
				guesserMaxLength = 0
				if args.min or args.max:
					print("[*] Setting length requirements: "+str(args.min)+
					"-"+str(args.max) + " characters")
					guesserMaxLength = args.max
					guesserMinLength = args.min
				if args.w:
					print("[*] Opening wordlist...")
					wordList = open(args.w, 'rbU')
					guesser.bruteWordlist(wordList, pdfReader, guesserMinLength,
						guesserMaxLength)
				elif args.b:
					if not args.max:
						print("[!] Opearation failed: -b argument requires "+
							"-max argument.")
						return
					print("[*] Compiling lists...")
					selectedLists = []
					if args.l:
						if "l" in args.l:
							selectedLists.extend(string.ascii_lowercase)
						if "u" in args.l:
							selectedLists.extend(string.ascii_uppercase)
						if "s" in args.l:
							selectedLists.extend(string.punctuation)
						if "d" in args.l:
							selectedLists.extend(string.digits)
						if "w" in args.l:
							selectedLists.extend(" ")
					elif not args.l:
						if args.c:
							selectedLists.extend(args.c)
						else:
							selectedLists.extend(string.ascii_lowercase)
							selectedLists.extend(string.ascii_uppercase)
							selectedLists.extend(string.punctuation)
							selectedLists.extend(string.digits)
							selectedLists.extend(" ")
					guesser.bruteRandom(selectedLists, pdfReader,
						guesserMinLength, guesserMaxLength)

			except IOError:
				print("There was an IO error")
	except IOError:
		print("There was an IO error. Is the file name correct?")

if __name__ == "__main__":
	main(sys.argv)
