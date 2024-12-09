#!/usr/bin/python











# funções



def setores():


    global onlyptw
    global loops
    




    #listas:







    mallink = 'https://myanimelist.net/animelist/'
    proceed = True




    # assistindo
    if loops == 0:
        print('BUSCANDO LISTA "WATCHING"...')
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
        print('ULTIMA LISTA ALCANÇADA\nREINICIANDO...\n\n\n')
        loops = 0
        proceed = False


    loops+=1

    print('')

    cnctvrf()

    if proceed:
        page = requests.get(str(''.join([mallink, usnm, mallink2])))
        soup = BeautifulSoup(page.text, 'html.parser')
        sopa = str(soup.find('table', class_='list-table'))



        # se não tiver nenhum item PTW em lançamento passa pra proxima lista

        if onlyptw:
            if  sopa.find('"status":6') == -1 and sopa.find('&quot;status&quot;:6') == -1:
                ''
            else:
                proximo(sopa)
        else:
            proximo(sopa)           
    
def proximo(sopa):


    # pegar o numero do proximo ep e o titulo
    # nessa ordem mesmo porque é assim que o ani-cli funciona
    # obs: CODIGO FEIO DA DESGRAÇA
    # por algum motivo desconhecido algumas listam tem sintase diferente

    if sopa.find('"num_watched_episodes":') != -1:
        
        findep = (int(sopa.find('"num_watched_episodes":'))+23, int(sopa.find(',"created_at":')))
        findtl = (int(sopa.find('"anime_title":"'))+15, int(sopa.find('","anime_title_eng":"')))
        
    elif sopa.find(',&quot;num_watched_episodes&quot;:') != -1:

        findep = (int(sopa.find(',&quot;num_watched_episodes&quot;:'))+34, int(sopa.find(',&quot;created_at')))
        findtl = (int(sopa.find('anime_title&quot;:&quot;'))+24, int(sopa.find('&quot;,&quot;anime_title_eng')))
        
    elif sopa.find('&quot;,&quot;anime_title_eng') != -1:

        findep = (int(sopa.find('"watched_episodes&quot;:'))+23, int(sopa.find(',&quot;created_at')))
        findtl = (int(sopa.find('anime_title&quot;:&quot;'))+24, int(sopa.find('&quot;,&quot;anime_title_eng')))

    else:
        print('oh shit')
    

    ep = int(sopa[findep[0] : (findep[1])])+1
    titulo = str(sopa[findtl[0] : findtl[1]])
    ep=str(ep)


    # filtrar os characteres especiais do titulo
    
    titulo = titulo.replace('&quot;', '')
    titulo = titulo.replace('u2606', ' ')
    titulo = titulo.replace('u2605', ' ')
    titulo = titulo.replace('u00bd', ' ')
    titulo = titulo.replace('\\', '')
    titulo = titulo.replace('    ', ' ')
    titulo = titulo.replace('   ', ' ')
    titulo = titulo.replace('  ', ' ')

    print(str(''.join(['BUSCANDO ANIME:\n', titulo, '\nEP:\n', ep, '\n\n'])))

    cnctvrf()

    provedores(titulo, ep)

    update(sopa)

def update(sopa):



    # checa se ainda tem coisa pra assistir
    # se não tiver manda de volra pros setores
    # se tiver tira o que já assistiu e manda de volta
    os.system('cls||clear')
    novasopa = sopa[int(sopa.find('anime_title_eng'))+5:]


    if (str(novasopa).find('"is_rewatching"')) == -1 and (str(novasopa).find(';is_rewatching&')) == -1:
        ''

    elif onlyptw:
        # aquele mesmo role de ver se o item em lançamento tá em PTW
        if novasopa.find('status":6') == -1 and novasopa.find('status&quot;:6') == -1:
            ''
    
    else:
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
            print(''.join(['\n\nQUALIDADE:\n', str(num), '/', str(qualnum), ' (', qual.upper(), ')']))
            sys.stdout.write('\n\nSERVIDOR:')
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

                #print(link)

                cnctvrf()
                sys.stdout.write(''.join(['\n', str(sv), '/12']))


                deubom=temstream(link)

                if deubom:
                    playmedia(link)
                    brekaporra=True
                    break

                sv=sv+1
                    
            if brekaporra:
                break
        
        if brekaporra:
            break
    
    if brekaporra == False and temp == True:

        sv=1
        print('\n\nQUALIDADE:\n3/3 (HD - LEGENDA TEMPORARIA)')
        sys.stdout.write('\n\nSERVIDOR:')

        for s1 in ('s2.', 's1.', ''):
            s1=str(s1)

            for s2 in range (4):
                s2+=1
                s2=str(s2)

                link = ('https://', s1, 'lightspeedst.net/s', s2, '/mp4_temp/', tl, '/', str(ep), '/720p.mp4?type=video/mp4&title=[AnimeFire.plus]')

                link = (''.join(link))

                cnctvrf()
                sys.stdout.write(''.join(['\n', str(sv), '/12']))

                deubom=temstream(link)

                if deubom:
                    playmedia(link)
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


    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    future = executor.submit(vaiounao, link)

    start = time.perf_counter()

    try:
        qzq = future.result(timeout=10)
    except TimeoutError:
        finish = time.perf_counter()
        print(f' <TimeOut> {round(finish-start, 2)}s\n')
        qzq = False
    except:
        print('oh shit')
    finally:
        executor.shutdown(wait=False)


    deubom = not qzq

    
    if deubom:
        print('CARREGANDO TRANSMISSÃO...')

    return deubom

def verifyos():

    # verificar OS

    osname = platform.platform()

    if osname.find('Windows') != -1:    
        osv = 1
        
    elif osname.find('Android') != -1: 
        osv = 2

    elif osname.find('Linux') != -1: 
        osv = 3

    noplayer = False

    try:
        subprocess.run('mpv -V')
        player = 'mpv'

    except:
        try:
            subprocess.run('vlc -V')
            player = 'vlc'

        except:

            if osv == 1:
                try:
                    subprocess.run('mpv\\mpv.exe -V')
                    player = 'mpv\\mpv.exe'
                except:
                    noplayer = True

            else:
                noplayer = True

    if noplayer:
        os.system('cls||clear')
        print('REPRODUTOR DE VIDEO NÃO ENCONTRADO')
        exit()



    return osv, player

def getusername():

    global usnm

    validusername = False

    while validusername == False:
        usnm = input('USERNAME DO MYANIMELIST: ')
        cnctvrf()
        response = str(requests.get(str(''.join(['https://myanimelist.net/profile/', usnm]))))
        if response.find('404') != -1:
            print(
                'USUARIO NÃO ENCONTRADO\n\n'
            )
        else:
            validusername = True
            print('\n')

def vaiounao(link):

    start = time.perf_counter()


    try:
        response = str(requests.get(url=link, timeout=6))
        finish = time.perf_counter()
        #print(response)
        if response.find('Response [404]') == -1:
            qzq=False
        else:
            sys.stdout.write(' <404>')
            qzq=True
    except requests.exceptions.ConnectionError:
        finish = time.perf_counter()
        qzq=True
        sys.stdout.write(' <Connection Error>')
    except requests.exceptions.Timeout:
        finish = time.perf_counter()
        qzq=True
        sys.stdout.write(' <Connection TimeOut>')

    except:
        finish = time.perf_counter()
        qzq=True
        sys.stdout.write(' <Erro Desconhecido>')


    sys.stdout.write(f' {round(finish-start, 2)}s')

    return qzq

def playmedia(link):

    argmt=verifyos()

    comando=' '.join([argmt[1], link])
    
    subprocess.run(comando)
    
def provedores(tl, ep):

    epfound = False

    try:
        subprocess.run('ani-cli -V')
        anicli=True
    except:
        anicli=False

    if anicli:

        titulo = tl

        titulo = titulo.replace('3rd Season', '3')
        titulo = titulo.replace('3rd Season', '3')
        titulo = titulo.replace('2nd Season', '2')
        titulo = titulo.replace('Goumon', '')
        titulo = titulo.replace('(', '')
        titulo = titulo.replace(')', '')
        titulo = titulo.replace('"', '')
        titulo = titulo.replace('/', '')


        info = ('ani-cli --skip -e ', str(ep), ' ', titulo)
        comando = str(''.join(info))


        print('PROVEDOR: ani-cli\n')
        
        result = str(subprocess.run(comando, shell = True, executable="/bin/bash"))
        time.sleep(5)

        if result.find('returncode=1') == -1:
            epfound = True

    if epfound == False:
        animefire(tl, ep)








# importar os bgl tudo

print('IMPORTANDO EXTENSÕES...')


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

print(''.join([str(8), '/', extotal]))
import os

try:
    print(''.join([str(9), '/', extotal]))
    import concurrent.futures
    from concurrent.futures import ThreadPoolExecutor, TimeoutError
except:
    cnctvrf()
    subprocess.run(''.join(['python -m pip install concurrent.futures']))
    import concurrent.futures
    from concurrent.futures import ThreadPoolExecutor, TimeoutError

print('')

# subprocess.run('py -m pip install --upgrade pip')

os.system('cls||clear')
















# loop que faz a parada funcionar




getusername()

loops=0


setproctitle.setproctitle('anipy_prcs')

while True:
    setores()

exit()
