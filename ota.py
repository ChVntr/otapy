#!/usr/bin/python











# funções



def setores():


    global onlyptw
    global loops
    loops+=1




    #listas:







    mallink = 'https://myanimelist.net/animelist/'





    # assistindo
    if loops == 0:
        print(
            '\nBUSCANDO LISTA "WATCHING"...'
        )
        mallink2 = '?order=11&order2=-5&status=1'
        onlyptw = False
    
    # PTW em lançamento
    elif loops == 1:
        print(
            '\nBUSCANDO LISTA "PLAN TO WATCH (AIRING)"...'
        )
        mallink2 = '?airing_status=1&order=-16&order2=14'
        onlyptw = True
    
    # PTW ainda não lançado
    elif loops == -3:
        print(
            '\nBUSCANDO LISTA "PLAN TO WATCH (NOT YET AIRED)"...'
        )
        mallink2 = '?airing_status=3&order=-14'
        onlyptw = False
    
    # em espera
    elif loops == -2:
        print(
            '\nBUSCANDO LISTA "ON HOLD"...'
        )
        mallink2 = '?order=12&order2=5&status=3'
        onlyptw = False

    # PTW
    elif loops == -4:
        print(
            '\nBUSCANDO LISTA "PLAN TO WATCH (FINISHED AIRING)"...'
        )
        mallink2 = '?airing_status=2&order=-16&order2=-15'
        onlyptw = True

    else:
        print('\n\n\nULTIMA LISTA ALCANÇADA\nREINICIANDO...\n\n\n')
        loops = -1
        setores()


    cnctvrf()
    page = requests.get(str(''.join([mallink, usnm, mallink2])))
    soup = BeautifulSoup(page.text, 'html.parser')
    sopa = str(soup.find('table', class_='list-table'))



    # se não tiver nenhum item PTW em lançamento passa pra proxima lista

    if onlyptw:
        if  sopa.find('"status":6') == -1 and sopa.find('&quot;status&quot;:6') == -1:
            setores()
    

    proximo(sopa)   

def proximo(sopa):

    # pegar o numero do proximo ep e o titulo
    # nessa ordem mesmo porque é assim que o ani-cli funciona
    # obs: CODIGO FEIO DA DESGRAÇA
    # por algum motivo desconhecido algumas listam tem sintase diferente

    if sopa.find('watched_episodes&quot;:') == -1:
        ep = str(int
              (sopa     [int(sopa.find('"num_watched_episodes":'))+23    :   int(sopa.find(',"created_at":'))]      )
              +1)

        titulo = str(sopa[
                int(sopa.find('"anime_title":"'))+15    :   int(sopa.find('","anime_title_eng":"'))])
        
    else:

        ep = str(
            int(sopa[
                int(sopa.find('watched_episodes&quot;:'))+23    :   int(sopa.find(',&quot;created_at'))])  +1)

        titulo = str(sopa[
                int(sopa.find('anime_title&quot;:&quot;'))+24    :   int(sopa.find('&quot;,&quot;anime_title_eng'))])



    # filtrar os characteres especiais do titulo
    
    titulo = titulo.replace('&quot;', '')
    titulo = titulo.replace('u2606', ' ')
    titulo = titulo.replace('u2605', ' ')
    titulo = titulo.replace('u00bd', ' ')
    titulo = titulo.replace('\\', '')
    titulo = titulo.replace('    ', ' ')
    titulo = titulo.replace('   ', ' ')
    titulo = titulo.replace('  ', ' ')
    tlpuro = titulo
    titulo = titulo.replace('3rd Season', '3')
    titulo = titulo.replace('3rd Season', '3')
    titulo = titulo.replace('2nd Season', '2')
    titulo = titulo.replace('Goumon', '')
    titulo = titulo.replace('(', '')
    titulo = titulo.replace(')', '')
    titulo = titulo.replace('"', '')
    titulo = titulo.replace('/', '')

    #print(tlpuro, ep)

    print(str(''.join(['\n\n\nBUSCANDO ANIME:\n', tlpuro, '\nEP:\n', ep, '\n\n'])))

    # juntar tudo em uma string

    info = ('ani-cli --skip -e ', str(ep), ' ', titulo)
    comando = str(''.join(info))


    # um monte de comando em bash

    # notificação show



    cnctvrf()
    if afonly == False:

        result = str(subprocess.run(comando, shell = True, executable="/bin/bash"))
        time.sleep(5)

        if result.find('returncode=1') != -1 and loops < 2:
            animefire(tlpuro, ep)
    else:
        animefire(tlpuro, ep)






    update(sopa)

def update(sopa):


    # checa se ainda tem coisa pra assistir
    # se não tiver manda de volra pros setores
    # se tiver tira o que já assistiu e manda de volta

    novasopa = sopa[int(sopa.find('anime_title_eng'))+5:]



    if (str(novasopa).find('"is_rewatching"')) == -1 and (str(novasopa).find(';is_rewatching&')) == -1:
        setores()



    # aquele mesmo role de ver se o item em lançamento tá em PTW

    if onlyptw:
        if novasopa.find('status":6') == -1 and novasopa.find('status&quot;:6') == -1:
            setores()
    
    
    
    proximo(novasopa)

def animefire(titulo, ep):  

    print('PROVEDOR: animefire.plus')
    sv = 1

    titulo = titulo.replace('(', '')
    titulo = titulo.replace(')', '')
    titulo = titulo.replace('"', '')
    titulo = titulo.replace('/', '')

    tl = titulo

    #Shinkakusha Kouho Senbatsu Shiken-hen
    tl = tl.replace('Shinkakusha Kouho Senbatsu Shiken-hen', '2nd season')
    tl = tl.replace('Kagaijugyou-hen', '2nd season Kagaijugyou-hen')
    tl = tl.replace(';', '-')
    tl = tl.replace('.', '-')
    tl = tl.replace(' ', '-')
    tl = tl.replace(':', '-')
    tl = tl.replace(',', '')
    tl = tl.replace('!', '')
    tl = tl.replace('?', '')
    tl = tl.replace('---', '-')
    tl = tl.replace('--', '-')

    tl = tl.lower() 

    if tl[-1] == '-':
        tl = tl[0 : (len(tl))-1]

    #um monte de variavel pro bagulho funcionar

    deubom=False
    brekaporra = False
    prevqual='none'
    num=1

    if tl.find('dandadan') and tl.find('ranma') == -1:
        qualnum=3
        temp=True
    else:

        temp=False
        qualnum=2


    for qual in ('fhd', 'hd'):

        if qual != prevqual:
            print(''.join(['\n\nQUALIDADE:\n', str(num), '/', str(qualnum), ' (', qual.upper(), ')\n\nSERVIDOR:']))
            prevqual = qual
            num+=1
            sv = 1

        for s1 in ('s2.', 's1.', ''):
            s1=str(s1)

            for s2 in range (4):
                s2+=1
                s2=str(s2)

                link = ('https://', s1, 'lightspeedst.net/s', s2, '/mp4/', tl, '/', qual, '/', str(ep), '.mp4?type=video/mp4&title=[AnimeFire.plus]')

                link = (''.join(link))
                comando = ('mpv ', link, ' --window-maximized --title-bar=no')
                comando = (''.join(comando))

                #print(link)

                cnctvrf()
                sys.stdout.write(''.join(['\n', str(sv), '/12']))


                deubom=temstream(link)

                if deubom:
                    subprocess.run(comando, capture_output= True, shell = shll, executable=exctb)
                    brekaporra=True
                    break

                sv=sv+1
                    
            if brekaporra:
                break
        
        if brekaporra:
            break
    
    if brekaporra == False and temp == True:

        sv=1
        print('\n\nQUALIDADE:\n3/3 (HD - LEGENDA TEMPORARIA)\n\nSERVIDOR:')

        for s1 in ('s2.', 's1.', ''):
            s1=str(s1)

            for s2 in range (4):
                s2+=1
                s2=str(s2)

                link = ('https://', s1, 'lightspeedst.net/s', s2, '/mp4_temp/', tl, '/', str(ep), '/720p.mp4?type=video/mp4&title=[AnimeFire.plus]')

                link = (''.join(link))
                comando = ('mpv ', link, ' --window-maximized --title-bar=no')
                comando = (''.join(comando))

                cnctvrf()
                sys.stdout.write(''.join(['\n', str(sv), '/12']))

                deubom=temstream(link)

                if deubom:
                    subprocess.run(comando, capture_output= True, shell = shll, executable=exctb)
                    brekaporra=True
                    break

                sv=sv+1

            if brekaporra:
                break

    if sv == 13:
        print('\n\nEPISODIO NÃO ENCONTRADO!\n')

def cnctvrf():

    try:
        requests.get('https://myanimelist.net')
        nocom=False
    except:
        nocom = True
        print('\n\n\nFALHA DE CONECÇÃO!\nAGUARDANDO RESPOSTA DE "myanimelist.net"...')

    while nocom:
        time.sleep(10)

        try:
            response = str(requests.get('https://myanimelist.net'))
            nocom = False
            #print('com net')
        except:
            nocom = True
            #print('FAZ O L')

def temstream(link):

    start = time.perf_counter()

    try:
        response = str(requests.get(url=link))
        finish = time.perf_counter()
        #print(response)
        if response.find('Response [404]') == -1:
            qzq=False
        else:
            sys.stdout.write(' <404>')
            qzq=True
    except requests.exceptions.ConnectTimeout:
        finish = time.perf_counter()
        qzq=True
        print(f' <TimeOut>')
    except:
        finish = time.perf_counter()
        qzq=True
        sys.stdout.write(' <Failed Request>')

    deubom = not qzq

    sys.stdout.write(f' {round(finish-start, 2)}s')
    
    if deubom:
        print('\nCARREGANDO TRANSMISSÃO...')

    return deubom

def verifyos():

    # verificar OS

    global exctb
    global shll

    osname = platform.platform()

    if osname.find('Windows') != -1:    
        osv = 1
        shll=False
        exctb = 'mpv\\mpv.exe'

    elif osname.find('Android') != -1: 
        osv = 2

    elif osname.find('Linux') != -1: 

        osv = 3
        exctb = '/bin/bash'
        shll = True

    return osv

def getusername():

    global usnm

    validusername = False

    while validusername == False:
        usnm = input('\nUSERNAME DO MYANIMELIST: ')
        cnctvrf()
        response = str(requests.get(str(''.join(['https://myanimelist.net/profile/', usnm]))))
        if response.find('404') != -1:
            print(
                'USUARIO NÃO ENCONTRADO'
            )
        else:
            validusername = True













# importar os bgl tudo

print(
    'IMPORTANDO EXTENSÕES...'
)


extotal = str(9)

print(''.join([str(1), '/', extotal]))
import subprocess, sys

print(''.join([str(2), '/', extotal]))
import platform

print(''.join([str(3), '/', extotal]))
from datetime import datetime

print(''.join([str(4), '/', extotal]))
import time

try:
    print(''.join([str(5), '/', extotal]))
    import requests
except:
    subprocess.run(''.join(['python -m pip install requests']))
    import requests

try:
    print(''.join([str(6), '/', extotal]))
    import bs4
    from bs4 import BeautifulSoup
except:
    cnctvrf()
    subprocess.run(''.join(['python -m pip install bs4']))
    import bs4
    from bs4 import BeautifulSoup

try:
    print(''.join([str(7), '/', extotal]))
    import setproctitle
except:
    cnctvrf()
    subprocess.run(''.join(['python -m pip install setproctitle']))
    import setproctitle

print(''.join([str(8), '/', extotal, '\n']))
import os

print(''.join([str(9), '/', extotal, '\n']))
import signal

subprocess.run('py -m pip install --upgrade pip')






if verifyos() == 1:
    print(
        '\nVERIFICANDO VERSÃO DO MPV...\n' 
    )

    upfile = open('mpv\\updater.bat', 'r')
    lastline = (upfile.readlines()[-1])
    print(lastline)
    if str(lastline) == 'timeout 5':
        print('timeout = true')
    upfile.close()
    
    subprocess.run('mpv\\updater.bat')
    os.system('cls||clear')








# definir as variaveis

anicli = False

if verifyos() == 1 or anicli == False:
    afonly = True

onlyptw = False
loops = -1
acabou = 3

validusername = False











# loop que faz a parada funcionar




getusername()

while loops != acabou:
    
    setproctitle.setproctitle('anipy_prcs')
    setores()

exit()
