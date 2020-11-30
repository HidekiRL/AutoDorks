#!usr/bin/python
# -*- coding: utf-8 -*-

###################################################################
#Script Name	:AutoDorks
#Python v       :Python 3
#Copyright      :2020, AutoDorks
#Version        :1.0.0
#Description	:Execute the main google dorks against a target selected by the attacker,
#		 generating a final report with the information garthered.
#Author       	:Hideki
#Email         	:Baniamundaray@gmail.com
###################################################################

import os, readline, time, progressbar, requests, subprocess
from itertools import cycle
from progress.bar import Bar
# pip install pyfiglet
import pyfiglet
# pip install clint
from clint.textui import colored
from bs4 import BeautifulSoup

result = pyfiglet.figlet_format("AutoDorks", font = "slant")
print(colored.white(result))
print(colored.green("                    Hideki®"))
print(colored.green("---------------------------------------------------\n"))

Directory = subprocess.check_output("pwd", shell=True).strip().decode('utf-8')

#Functions
def googleSearch(query,download,extension):
	URL_MAIN = 'https://www.google.com/search'
	HEADER = {'User-agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
	PAYLOAD= {'q' : query, 'start' : 0, 'num': num_search}
	RESPONSE = requests.get(URL_MAIN, params = PAYLOAD, headers = HEADER)
	if (RESPONSE.status_code == 429):
		print(colored.red("[!]Status Code 429 Too Many Request."))
		time.sleep(1)
		print(colored.green("[*]Loading proxy list..."))
		print(colored.green("[*]Starting..."))
		for i in range(1,len(proxy_list)):
			proxy = next(proxy_pool)
			try:
				print(colored.green("[+]Proxy : ")+proxy)
				RESPONSE = requests.get(URL_MAIN, params = PAYLOAD, headers = HEADER, proxies={"http": proxy, "https":proxy})
				if(RESPONSE.status_code == 200):
					print(colored.green("[+]Proxy found!"))
					break
			except:
				print(colored.red("[!]Connection error, Switching proxy..."))
				continue
	SOUP = BeautifulSoup(RESPONSE.content, features="lxml")
	LINKS = SOUP.findAll(class_='rc')
	bar = progressbar.ProgressBar(maxval=len(LINKS), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
	bar.start()
	PROGRESS_BAR=0
	for link in LINKS:
		bar.update(PROGRESS_BAR+1)
		print(colored.white('\nGetting urls: %s\n'%link.a.get('href')[:50]), end="")
		report.write(str(PROGRESS_BAR+1)+". "+str(link.a.get('href'))+"\n")
		if (download == True and confirmation_download.lower() == "yes"):
			os.system("wget "+str(link.a.get('href'))+" -P "+path+"/file_dork_scan/"+extension)
		PROGRESS_BAR = PROGRESS_BAR+1
		time.sleep(0.3)
		if (PROGRESS_BAR != len(LINKS)):
			print ("\033[A                             \033[A")
			print ("\033[A                             \033[A")

def get_names(names):
	name = ""
	aux_name = ""
	name_len = len(target.split())
	if(name_len == 1):
		names.write(target+"\n")
		names.close()
	else:
		names.write(target+"\n")
		name = target.replace(" ",".")
		names.write(name+"\n")
		name  = target.replace(" ", "-")
		names.write(name+"\n")
		name = target.replace(" ", "_")
		names.write(name+"\n")
		for i in range (1,name_len):
			name = target.split()[0]+" "+target.split()[i]
			names.write(name+"\n")
			aux_name = name.replace(" ",".")
			names.write(aux_name+"\n")
			aux_name = name.replace(" ","-")
			names.write(aux_name+"\n")
			aux_name = name.replace(" ","_")
			names.write(aux_name+"\n")
		name = target.split()[0]
		for i in range(1,name_len):
			name = name + target.split()[i][0].upper()
		names.write(name+"\n")
		name = target.split()[0]
		for i in range(1,name_len):
			name = name + "."+target.split()[i][0].upper()
		names.write(name+"\n")
		names.close()
#Info
path = ""
target = input(colored.white("Type the full name of the target:\n"))
if(len(target) == 0):
	print(colored.red("[!] Error, please introduce a name"))
	os.system("python3 dorks.py")

confirmation_download = input(colored.white("Do you want to download files if there are any? (Yes/No)\n"))
if (confirmation_download.lower() == "yes"):
	path = input(colored.white("Type the full path where you want to save the files\n"))
	print(colored.white("Do you want to proceed with"),target,colored.white("as target and"),path,colored.white("as path for saving the files? (Yes/No)"))
	confirmation = input(colored.white("\r"))

	if(confirmation.lower() == "no"):
 	       os.system("python3 dorks.py")
	elif(confirmation.lower() == "yes"):
		print("")
	else :
		print(colored.red("[!] Error, restarting the script..."))
		os.system("python3 dorks.py")

elif (confirmation_download.lower() == "no"):
	print(colored.white("Do you want to proceed with"),target,colored.yellow("as target?"))
	confirmation = input(colored.white("(Yes/No)"))

	if(confirmation.lower() == "no"):
        	os.system("python3 dorks.py")
	elif(confirmation.lower() == "yes"):
		print("")
	else:
		print(colored.red("[!] Error, restarting the script..."))
		os.system("python3 dorks.py")
else:
	print(colored.red("[!] Error, restarting the script..."))
	os.system("python3 dorks.py")
num_search_input = input(colored.white("Enter the max number of results you want per google dork\n"))
try:
	num_search = int(num_search_input)
except:
	print(colored.red("[!]Error, please introduce a number"))
	os.system("python3 dorks.py")


print("\n------------------------------------------------------")
print("|                      "+colored.blue("G")+colored.red("o")+colored.yellow("o")+colored.blue("g")+colored.green("l")+colored.red("e")+"                        |")
print("------------------------------------------------------\n")

#Attack
report = open('report.txt','w')
names_w = open('names.txt','w')
get_names(names_w)
names = open('names.txt','r')
proxies = open('HTTP-proxies.txt', 'r')
dorks = open('dorks.txt', 'r')
extensions = open('extensions.txt', 'r')
proxy_list = []

report.write("GOOGLE DORKS REPORT\n")
report.write("Target:"+target+"\n\n")


for proxy in proxies:
	proxy_list.append(proxy.rstrip("\n"))

proxy_pool = cycle(proxy_list)

for name in names:
	print("\n------------------------------------------------------\r")
	print(colored.yellow("Target: "+name.rstrip("\n")))
	print("------------------------------------------------------")
	dorks = open('dorks.txt', 'r')
	extensions = open('extensions.txt', 'r')
	for dork in dorks:
		report.write("\nTop "+str(num_search)+" results with dork --> "+dork.rstrip("\n")+'"'+name.rstrip("\n")+'"\n\n')
		if(dork.rstrip("\n") == "ext:"):
			for ext in extensions:
				report.write("\n[Files with extension: "+ext.upper().rstrip("\n")+"]"+"\n\n")
				query = dork.rstrip("\n")+ext.rstrip("\n")+' 	"'+name.rstrip("\n")+'"'
				print("\nCurrent dork --> ["+dork.rstrip("\n")+ext.rstrip("\n")+' "'+name.rstrip("\n")+'"]')
				googleSearch(query,True,ext)
		else:
			query = dork.rstrip("\n")+'"'+name.rstrip("\n")+'"'
			print("\nCurrent dork --> ["+dork.rstrip("\n")+'"'+name.rstrip("\n")+'"]')
			googleSearch(query,False,0)

print("\n<-------------------------------------------------------------------------->")
print(colored.green("\n[+]Done!"))
print(colored.green("[+]Making report.txt..."))
print(colored.green("[+]PATH "+Directory+"/report.txt"))
