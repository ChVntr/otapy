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
    elif loops == 2:
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

        link = ''.join([mallink, usnm, mallink2])

        sopa = sopapranois(link)

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

def animefire(tl, ep):  

    sv = 1


    #um monte de variavel pro bagulho funcionar

    tocou=False
    deubom=False
    brekaporra = False
    prevqual='none'
    num=1

    notemplist = (
        'dandadan',
        'ranma-2024',
        )

    sdlist = (
        'one-piece',
        'ike-ina-chuu-takkyuubu',
        'gintama',
        )

    for title in notemplist:
        if tl == title:
            temp=False
            break
        else:
            temp=True


    for title in sdlist:
        if tl == title:
            sd=True
            break
        else:
            sd=False

    if sd:
        qualidades = ('sd',)
        #qualidades = qualidades[:1]
    elif temp == False:
        qualidades = ('fhd', 'hd')
    else:
        qualidades = ('fhd', 'hd', 'temp')
    
    qualnum = len(qualidades)

    for qual in qualidades:

        if qual != prevqual:

            if qual == 'temp':
                print(''.join(['\n\nQUALIDADE:\n', str(num), '/', str(qualnum), ' (HD - LEGENDA TEMPORARIA)']))
            else:
                print(''.join(['\n\nQUALIDADE:\n', str(num), '/', str(qualnum), ' (', qual.upper(), ')']))

            sys.stdout.write('\n\nSERVIDOR:')
            prevqual = qual
            num+=1
            sv = 1

        for s1 in ('s2.', ''):
            s1=str(s1)

            for s2 in range (4):
                s2+=1
                s2=str(s2)

                if qual != 'temp':
                    link = ('https://', s1, 'lightspeedst.net/s', s2, '/mp4/', tl, '/', qual, '/', str(ep), '.mp4')
                else:
                    link = ('https://', s1, 'lightspeedst.net/s', s2, '/mp4_temp/', tl, '/', str(ep), '/720p.mp4')

                link = (''.join(link))

                #print(link)

                cnctvrf()
                sys.stdout.write(''.join(['\n', str(sv), '/8']))


                deubom=temstream(link)

                if deubom:
                    tocou = playmedia(link)
                    if tocou:
                        ''
                    else:
                        print('FALHA NA REPRODUÇÃO!')
                    break

                sv=sv+1
                    
            if deubom:
                break
        
        if tocou:
            break
    
    if tocou == False:
        print('\n\nEPISODIO NÃO ENCONTRADO!\n')

    return tocou

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
        qzq = future.result(timeout=12)
    except TimeoutError:
        finish = time.perf_counter()
        print(f' <Request TimeOut> {round(finish-start, 2)}s\n')
        qzq = False
    except:
        print('oh shit')
    
    executor.shutdown(wait=False)


    deubom = not qzq

    
    if deubom:
        print('\nCARREGANDO TRANSMISSÃO...')

    return deubom


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
        if response.find('Response [404]') == -1:
            sys.stdout.write(' <200>')
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
    
    players = ('mpv', 'vlc', 'mpv\\mpv.exe', 'C:\\Program Files\\VideoLAN\\VLC\\vlc.exe')

    
    for player in players:
        try:
            comando = ' '.join([player, link])
            result = subprocess.run(comando).returncode
            foi=True
            if int(result) == 0:
                return True
            else:
                return False
            break
        except:
            foi=False

    if foi == False:
        os.system('cls||clear')
        print('NENHUM REPRODUTOR DE VIDEO ENCONTRADO')
        exit()

def provedores(tl, ep):

    epfound = False

    print('PROVEDOR: "ani-cli"')

    try:
        subprocess.run('ani-cli -V')
        anicli=True
    except:
        anicli=False
        print('(PROVEDOR NÃO ENCCONTRADO/INSTALADO)\n\n')

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

    # animefire
    if epfound == False:

        print('PROVEDOR: "animefire.plus"')


        ntl = tl

        ntl = ntl.replace('(', '')
        ntl = ntl.replace(')', '')
        ntl = ntl.replace('"', '')
        ntl = ntl.replace('/', '')

        ntl = ntl.replace('Shinkakusha Kouho Senbatsu Shiken-hen', '2nd season')
        ntl = ntl.replace('Kagaijugyou-hen', '2nd season Kagaijugyou-hen')
        ntl = ntl.replace(';', '-')
        ntl = ntl.replace('.', '-')
        ntl = ntl.replace(' ', '-')
        ntl = ntl.replace(':', '-')
        ntl = ntl.replace(',', '')
        ntl = ntl.replace('!', '')
        ntl = ntl.replace('?', '')
        ntl = ntl.replace('---', '-')
        ntl = ntl.replace('--', '-')

        ntl = ntl.lower() 
        dubtl = ''.join([ntl, '-dublado'])

        if ntl[-1] == '-':
            ntl = ntl[0 : (len(tl))-1]

        link = ''.join(['https://animefire.plus/animes/', ntl, '-todos-os-episodios'])
        response = requests.get(url=link)
        
        try:
            if str(response) == '<Response [500]>':
                animeexiste = False
            else:
                animeexiste = True
        except:
            animeexiste = False




        if animeexiste:

            deubom = False

            # verificar se tem dub
            link = ''.join(['https://animefire.plus/animes/', ntl, '-dublado-todos-os-episodios'])
            response = requests.get(url=link)

            try:
                if str(response) == '<Response [500]>':
                    temdub = False
                else:
                    temdub = True
            except:
                temdub = False
            
            while temdub:

                dubs = ('one-piece',)

                if usnm.lower() == 'gahvius':
                    if ntl in dubs:    
                        dub = 's'
                        temdub = False
                    else:
                        dub = 'n'

                else:
                    dub = input('\nDUB ENCONTRADO!\nPROCURAR POR EPISÓDIOS DUBLADOS? (s,n): ').lower()

                if dub == 's':            
                    print('\nBUSCANDO EPISODIO DUBLADO!')  
                    deubom = animefire(dubtl, ep)
                    temdub = False
                elif dub == 'n':
                    temdub = False
                else:
                    print('COMANDO INVALIDO!')

                



            if deubom == False:
                print('\nBUSCANDO EPISODIO LEGENDADO!')
                animefire(ntl, ep)
        else:
            print('\nANIME NÃO ENCONTRADO!\n')
            time.sleep(1)

def sopapranois(link):

    page = requests.get(str(link))
    soup = BeautifulSoup(page.text, 'html.parser')
    sopa = str(soup.find('table', class_='list-table'))

    return sopa

def verifyos():

    os = -1

    ptf = platform.platform()
    #print(ptf)

    if ptf.find('Emscripten') != -1:
        os = 0

    return os









# importar os bgl tudo

print('IMPORTANDO EXTENSÕES...')


extotal = str(8)

print(''.join([str(1), '/', extotal]))
import subprocess, sys

print(''.join([str(2), '/', extotal]))
import platform

print(''.join([str(3), '/', extotal]))
from datetime import datetime

print(''.join([str(4), '/', extotal]))
import time

print(''.join([str(5), '/', extotal]))
import os

sisop = verifyos()
#print(sisop)

if sisop != 0:

    try:
        print(''.join([str(6), '/', extotal]))
        import requests
    except:
        subprocess.run(''.join(['python -m pip install requests']))
        import requests

    try:
        print(''.join([str(7), '/', extotal]))
        import bs4
        from bs4 import BeautifulSoup
    except:
        cnctvrf()
        subprocess.run(''.join(['python -m pip install bs4']))
        import bs4
        from bs4 import BeautifulSoup

    try:
        print(''.join([str(8), '/', extotal]))
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

while True:
    setores()

exit()
