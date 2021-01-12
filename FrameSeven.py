#!/bin/python2
#coding: utf-8
##########################################################$
#			         Feito por Sayseven                   #
#   	FrameSeven: Ferramenta para auxilio de penstest   #
#		Use com sabedoria, não me responsabilizo por seus #
#       atos					                          #
#                                                         #  
##########################################################$
import socket
import optparse
import requests
import sys
import time
import struct
import os
import re
from bs4 import BeautifulSoup
import paramiko
import time



parser = optparse.OptionParser()
parser.add_option('-?', help="Caso ainda estiver com duvida use o -? help", dest="ajuda", action="store_true")
parser.add_option('-u', '--url', help='Lista diretorios no site', dest='site', metavar='site', action="store_true")
parser.add_option('-d', '--adm', help='Procura a pagina adm no site', dest='admin', metavar='admin', action="store_true")
parser.add_option('-l', help="Procurar todos os links dentro do site", dest="link", metavar='site',action="store_true")
parser.add_option('--sp', help='Scan de portas', dest='scan', metavar='site', action="store_true")
parser.add_option('--ssmtp', help='Enumerar smpt', dest='smtp', metavar='site',action="store_true")
parser.add_option('--bftp', help='Brutar fdp', dest='ftp', metavar='site usuario')
parser.add_option('--bssh', help='Brutar ssh', dest='ssh', metavar='site')

(options, args) = parser.parse_args()

class color():
	red = '\033[31m'
	blue_2 = '\33[36m'
	green = '\033[32m'
	blue = '\033[34m'
	yellow = '\033[33m'
	black = '\033[30m'
	white = '\033[37m'
	original = '\033[0;0m'
	reverse = '\033[2m'
	default = '\033[0m'


def help():
		os.system('clear')
		print(color.blue_2+ ''' 


				 (`-').-> (`-')  _         _  (`-') 
				 (OO )__  ( OO).-/  <-.    \-.(OO ) 
				,--. ,'-'(,------.,--. )   _.'    \ 
				|  | |  | |  .---'|  (`-')(_...--'' 
				|  `-'  |(|  '--. |  |OO )|  |_.' | 
				|  .-.  | |  .--'(|  '__ ||  .___.' 
				|  | |  | |  `---.|     |'|  |      
				`--' `--' `------'`-----' `--'  
							FrameSeven 1.0 Version 
		Usage: FrameSeven [options]
		Options:
			-h, --help		show this help message and exit
			-u  www.site.com, --url=www.google.com
							Lista diretorios no site
			-d	admin, --admin=admin
							Procura o admin
			-l				Procura links
			--sp			Scan de portas
			--ssmpt			Enumerar smtp
			--bftp			Brutar ftp
			--bssh			Brutar ssh			
				 ''')
		sys.exit(0)

def banner_portscan():
	print(color.red+'''
			88""Yb  dP"Yb  88""Yb 888888 .dP"Y8  dP""b8    db    88b 88 
			88__dP dP   Yb 88__dP   88   `Ybo." dP   `"   dPYb   88Yb88 
			88"""  Yb   dP 88"Yb    88   o.`Y8b Yb       dP__Yb  88 Y88 
			88      YbodP  88  Yb   88   8bodP'  YboodP dP""""Yb 88  Y8 
					FrameSeven 1.0 Version
			''')

def banner_diretorio():
	print(color.yellow+''' 
		    .=-.-.               ,----.  ,--.--------.   _,.---._                 .=-.-.  _,.---._     
         _,..---._  /==/_ /.-.,.---.   ,-.--` , \/==/,  -   , -\,-.' , -  `.   .-.,.---.  /==/_ /,-.' , -  `.   
       /==/,   -  \|==|, |/==/  `   \ |==|-  _.-`\==\.-.  - ,-./==/_,  ,  - \ /==/  `   \|==|, |/==/_,  ,  - \  
       |==|   _   _\==|  |==|-, .=., ||==|   `.-. `--`\==\- \ |==|   .=.     |==|-, .=., |==|  |==|   .=.     | 
       |==|  .=.   |==|- |==|   '='  /==/_ ,    /      \==\_ \|==|_ : ;=:  - |==|   '='  /==|- |==|_ : ;=:  - | 
       |==|,|   | -|==| ,|==|- ,   .'|==|    .-'       |==|- ||==| , '='     |==|- ,   .'|==| ,|==| , '='     | 
       |==|  '='   /==|- |==|_  . ,'.|==|_  ,`-._      |==|, | \==\ -    ,_ /|==|_  . ,'.|==|- |\==\ -    ,_ /  
       |==|-,   _`//==/. /==/  /\ ,  )==/ ,     /      /==/ -/  '.='. -   .' /==/  /\ ,  )==/. / '.='. -   .'   
       `-.`.____.' `--`-``--`-`--`--'`--`-----``       `--`--`    `--`--''   `--`-`--`--'`--`-`    `--`--''     
					                   FrameSeven 1.0 Version
		''')


def banner_admin():
	print(color.red+''' 
 	....###....########..##.....##.####.##....##
	...##.##...##.....##.###...###..##..###...##
	..##...##..##.....##.####.####..##..####..##
	.##.....##.##.....##.##.###.##..##..##.##.##
	.#########.##.....##.##.....##..##..##..####
	.##.....##.##.....##.##.....##..##..##...###
	.##.....##.########..##.....##.####.##....##
			FrameSeven 1.0 Version
	''')


def banner_smtp():
	print(color.white+''' 
	      ::::::::    :::   ::: ::::::::::: ::::::::: 
    	   :+:    :+:  :+:+: :+:+:    :+:     :+:    :+: 
   	   +:+        +:+ +:+:+ +:+   +:+     +:+    +:+  
  	  +#++:++#++ +#+  +:+  +#+   +#+     +#++:++#+    
        	+#+ +#+       +#+   +#+     +#+           
	#+#    #+# #+#       #+#   #+#     #+#            
	########  ###       ###   ###     ###   
			FrameSeven 1.0 Version
	''')

def banner_link():
	print(color.blue_2+ ''' 
		__       __  .__   __.  __  ___      _______.
		|  |     |  | |  \ |  | |  |/  /     /       |
		|  |     |  | |   \|  | |  '  /     |   (----`
		|  |     |  | |  . `  | |    <       \   \    
		|  `----.|  | |  |\   | |  .  \  .----)   |   
		|_______||__| |__| \__| |__|\__\ |_______/    
				FrameSeven 1.0 Version
   ''')


def banner_ftp():
	print(color.blue+'''
	
	 ▄▀▀▀█▄    ▄▀▀▀█▀▀▄  ▄▀▀▄▀▀▀▄ 
	█  ▄▀  ▀▄ █    █  ▐ █   █   █ 
	▐ █▄▄▄▄   ▐   █     ▐  █▀▀▀▀  
 	 █    ▐      █         █      
 	 █         ▄▀        ▄▀       
	█         █         █         
	▐         ▐         ▐         
		FrameSeven 1.0 Version
	
	''')


def banner_ssh():
	print(color.white+'''

             *     ,MMM8&&&.            *
                  MMMM88&&&&&    .
                 MMMM88&&&&&&&
     *           MMM88&&&&&&&&
                 MMM88&&&&&&&&
                 'MMM88&&&&&&'
                   'MMM8&&&'      *    _
          |\___/|                      \\
         =) ^Y^ (=   |\_/|              ||    '
          \  ^  /    )a a '._.-""""-.  //
           )=*=(    =\T_= /    ~  ~  \//
          /     \     `"`\   ~   / ~  /
          |     |         |~   \ |  ~/
         /| | | |\         \  ~/- \ ~\
         
  jgs_/\_//_// __//\_/\_/\_((_|\((_//\_/\_/\_
  |  |  |  | \_) |  |  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
                   ___     FrameSeven 1.0 Version
                   `MM       
                    MM       
    ____     ____   MM  __   
   6MMMMb\  6MMMMb\ MM 6MMb  
  MM'    ` MM'    ` MMM9 `Mb 
  YM.      YM.      MM'   MM 
   YMMMMb   YMMMMb  MM    MM 
       `Mb      `Mb MM    MM 
  L    ,MM L    ,MM MM    MM 
  MYMMMM9  MYMMMM9 _MM_  _MM_
                           
                           
                           
	''')



cabecalho = {'User-agent': 'Windows 7', 'Referer': 'https://google.com/', 'CP_IPcountry': 'USA',
             'Origin': 'http://google.com/'}

meus_cookies = {'Ultima-visita': '20-11-2020'}


if os.environ['USER'] != "root":
	print("Você precisa ser root!!\n")
	sys.exit(0)

if options.ajuda:
    os.system('clear')
    help()

if len(args) == 0:
	help()
else:
	alvo = args[0]

if options.site: # -u 
	os.system('clear')
	banner_diretorio()
	convert = ('http://' + alvo + '/') #www.site.com
	robots = (convert + 'robots.txt')
	results2 = []
	robotscheck = requests.get(robots)
	texto = requests.get(convert,
						 headers=cabecalho,
						 cookies=meus_cookies)
	print('Começou: '+ time.strftime("%X %x %Z\n"))
	ipresult = socket.gethostbyaddr(alvo)
	print('IP do alvo: '+ str(ipresult) +'\n')
	lista = open("wordlist/diretorios.txt", "r")
	for item in lista:
		try:
			listas = item.strip()
			scan = (convert+listas)
			scan1 = requests.get(scan,
							 	headers=cabecalho,
								cookies=meus_cookies)
			if scan1.status_code == 200:
				print(color.red+"[+] RESP: 200: "+ scan)
				results2.append(scan)
		except:
			print('')
	else:
		print('')

	texto = None

	if robotscheck.status_code == 200:
		print(color.yellow+"[+] Verificando o robots.txt")
		time.sleep(2)
		print('')
		texto = robotscheck.text
		print(color.blue_2+texto)
	else:
		print('')
	textoresult = open('diretorios.txt', 'w')
	for dire in results2:
		dire2 = dire+"\n"
		textoresult.write(str(dire2))
	print('Foram encontados:' +str(len(results2)) + 'diretorios online')
	print('Foi criado um arquivo .txt chamado diretorios.txt :D')
	print('Finalizou'+ time.strftime("%X %x %Z"))


if options.admin:
	banner_admin()
	convert1 = ('http://'+ alvo + '/')
	print('Começou '+ time.strftime("%X %x %Z\n"))
	texto1 = requests.get(convert1)
	admin = []
	ipresult = socket.gethostbyname(alvo)
	print("IP do alvo " + str(ipresult) + '\n')
	lista1 = open("wordlist/adm.txt", "r")
	time.sleep(1)
	for administrador in lista1:
		try:
			adm = administrador.strip()
			scan2 = (convert1+adm)
			scan3 = requests.get(scan2,
								headers=cabecalho,
								cookies=meus_cookies)
			if scan3.status_code == 200:
				print(color.red+scan2+ " >>>>> [+]Admin encontrado[+] :D")
				admin.append(scan2)
		except:
			print('')
	textoresult2 = open("adminresult.txt", "w")
	for resul in admin:
		resul2 = resul+"\n"
		textoresult2.write(str(resul2))
	print("Foram encontrados: "+ str(len(admin)) + "diretorios ADM online")
	print("Foi criado um arquivo .txt chamado adminresult.txt :)")
	print("Finalizou"+ time.strftime("%X %x %Z"))
else:
	print('')

if options.scan:
	banner_portscan()
	time.sleep(2)
	ports = range(21, 8080)
	sitescan = alvo
	portas_abertas = []
	ipresult = socket.gethostbyname(sitescan)
	print("IP do alvo: " + str(ipresult) + "\n")
	for porta in ports:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(0.5)
		try:
			conexao = s.connect_ex((sitescan, porta))
		except:
			print("Problema com socket do portscan\n")
		if conexao == 0:
			print("[+] Porta Aberta [+]" + (str(porta)))
			portas_abertas.append(str(porta))
		elif conexao == 11:
			print("[-] Porta Filtrada [-] " + (str(porta)))
			portas_abertas.append(str(porta))
	portaresult = open("portaresult.txt", "w")
	for port in portas_abertas:
		port2 = port+"\n"
		portaresult.write(str(port2))
	print("Foram encontradas " + str(len(portas_abertas)) + " portas no alvo")
	print("Foi criado um arquivo .txt chamado portaresult.txt :)")
	print("Finalizou "+ time.strftime("%X %x %Z"))

if options.smtp:
	banner_smtp()
	lista_smtp = open("wordlist/rockyou.txt", "r")
	adm_smtp = []
	ipresult = socket.gethostbyname(alvo)
	print("IP do alvo: " + ipresult +"\n")
	time.sleep(1)
	for linha in lista_smtp:
		linhas = linha.strip()
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			s.connect((alvo, 25))
		except:
			print("Problema com socket smtp\n")
			break	
		s.recv(1024)
		s.send("VRFY "+linhas)
		resp = s.recv(1024)
		if re.search('252', resp):
			print("[+] Usuario encontrado [+]"+ resp.strip('252 2.0.0'))
			adm_smtp.append(str(resp.strip('252 2.0.0')))

	smtpresult = open("smtplist.txt", "w")
	for smtp_adm in adm_smtp:
		smtp_adm2 = smtp_adm+"\n"
		smtpresult.write(str(smtp_adm2))
	print("Foram encontrados: "+ str(len(adm_smtp)) + "usarios online")
	print("Foi criado um arquivo .txt chamado smtplist.txt :D")
	print("Finalizou" + time.strftime("%X %x %Z"))

if options.link:
	banner_link()
	convert2 = ("http://" + alvo + "/")
	req = requests.get(convert2,
					   headers=cabecalho,
					   cookies=meus_cookies)
	html = req.text
	soup = BeautifulSoup(html, 'html.parser')
	links = soup.find_all('a')
	cont = 0
	for linkzin in links:
		cont += 1
		print(color.blue_2+"======================"+str(cont)+ "======================")
		print(linkzin.get("href"))
	print(color.blue_2+"====================== TERMINOU ======================")
	print("Foram encontrados: "+ str((cont)) + "Links")
	result_links = open("result_links", "w")
	for linkzin in links:
		linkzin2 = linkzin.get("href")+"\n"
		result_links.write(str(linkzin2))
	print("Foi criado um arquivo .txt chamado ResulLinks.txt :D")
	print("Finalizou " + time.strftime("%X %x %Z"))

if options.ftp:
	banner_ftp()
	username = options.ftp
	lista_ftp =  open("wordlist/rockyou.txt", "r")
	for linha in lista_ftp:
		listas = linha.strip()
		print("Testando com %s:%s"%(username, listas))
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			s.connect((alvo, 21))
		except:
			print("Problema com socket ftp")
			sys.exit(1)
		s.recv(1024)
		s.send("USER"+username+"\r\n")
		s.recv(1024)
		s.send("PASS"+listas+"\r\n")
		result = s.recv(1024)

		if(re.search("230", result)):
			print("[+]===> PASS FOUND: %s <===[+] :) " + linhas)
			break

if options.ssh:
	banner_ssh()
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	lista_ssh = open("wordlist/rockyou.txt", "r")
	for linha in lista_ssh:
		linhas = linha.strip()
		time.sleep(3)
		try:
			ssh.connect(alvo, username=options.ssh, password=linhas)
		except:
			paramiko.AuthenticationException
			print("[-] Acesso Negado [-] " + linhas)
		else:
			print("[+] Senha Encontrada [+] " + linhas)
			break


