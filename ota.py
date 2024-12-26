#!/usr/bin/python











# funções



def setores():
    if debugin: print('SETORES\n'), time.sleep(dbfldrt)

    global onlyptw
    global loops
    




    #listas:







    mallink = 'https://myanimelist.net/animelist/'
    proceed = True

    if debugin: 
        while True:
            try:
                loops = int(input('numero da lista: '))
                break
            except:
                ''



    # assistindo
    if loops == 0:
        print('BUSCANDO LISTA "WATCHING"...')
        mallink2 = '?order=11&order2=-5&status=1'
        onlyptw = False
    
    # PTW em lançamento
    elif loops == 1:
        print('BUSCANDO LISTA "PLAN TO WATCH (AIRING)"...')
        mallink2 = '?airing_status=1&order=-16&order2=14'
        onlyptw = True
    
    # PTW ainda não lançado
    elif loops == -3:
        print('BUSCANDO LISTA "PLAN TO WATCH (NOT YET AIRED)"...')
        mallink2 = '?airing_status=3&order=-14'
        onlyptw = False
    
    # em espera
    elif loops == 2:
        print('BUSCANDO LISTA "ON HOLD"...')
        mallink2 = '?order=12&order2=5&status=3'
        onlyptw = False

    # PTW
    elif loops == 3:
        print('BUSCANDO LISTA "PLAN TO WATCH (FINISHED AIRING)"...')
        mallink2 = '?airing_status=2&order=-16&order2=-15'
        onlyptw = True

    else:
        #print('ULTIMA LISTA ALCANÇADA\nREINICIANDO...\n\n\n')
        loops = 0
        proceed = False


    loops+=1

    

    print('')

    cnctvrf()

    if proceed:

        link = ''.join([mallink, usnm, mallink2])

        sopa = sopapranois(link)[0]


        # se não tiver nenhum item PTW em lançamento passa pra proxima lista

        if onlyptw:
            if  sopa.find('"status":6') == -1 and sopa.find('&quot;status&quot;:6') == -1:
                print('nao achei mais')
                ''
            else:
                proximo(sopa)
        else:
            proximo(sopa)           
    
def proximo(sopa):
    if debugin: print('PROXIMO\n'), time.sleep(dbfldrt)

    print('BUSCANDO ANIME:')

    # pegar o numero do proximo ep e o titulo
    # nessa ordem mesmo porque é assim que o ani-cli funciona
    # obs: CODIGO FEIO DA DESGRAÇA
    # por algum motivo desconhecido algumas listam tem sintase diferente
    #                      &quot;anime_id&quot;:
    animeid = (sopa[ sopa.find(';anime_id&quot;:')+16 : sopa.find(',&quot;anime_studios')])

    try:
        int(animeid)
    except:
        animeid = (sopa[sopa.find(',"anime_id":')+12 : sopa.find(',"anime_studios"')])
        try:
            int(animeid)
        except:
            print('\n\nOH SHIT\n"animeid" não retornou como integral')
            exit()


    link = ''.join(['https://myanimelist.net/anime/', animeid])
    tl_sopa = sopapranois(link)[1]
    #                          name="twitter:site"/><meta content='Himesama "Goumon" no Jikan desu' property="og:title"
    titulo = (tl_sopa[tl_sopa.find('"twitter:site"/><meta content=') +31 : tl_sopa.find('" property="og:title"')])
    if len(titulo) > 500: titulo = (tl_sopa[tl_sopa.find('"twitter:site"/><meta content=') +31 : tl_sopa.find(' property="og:title"')-1])



    print(titulo)

    if sopa.find('"num_watched_episodes":') != -1:
        
        findep = (int(sopa.find('"num_watched_episodes":'))+23, int(sopa.find(',"created_at":')))
        
    elif sopa.find(',&quot;num_watched_episodes&quot;:') != -1:

        findep = (int(sopa.find(',&quot;num_watched_episodes&quot;:'))+34, int(sopa.find(',&quot;created_at')))
        
    elif sopa.find('&quot;,&quot;anime_title_eng') != -1:

        findep = (int(sopa.find('"watched_episodes&quot;:'))+23, int(sopa.find(',&quot;created_at')))

    else:
        print('\n\nOH SHIT\ntitulo e ep não encontrados')
        exit()

    ep = int(sopa[findep[0] : (findep[1])])+1
    ep=str(ep)

    print(str(''.join(['EP:\n', ep, '\n\n'])))

    cnctvrf()

    provedores(titulo, ep)

    update(sopa)

def update(sopa):
    os.system('cls||clear')
    if debugin: print('UPDATE\n'), time.sleep(dbfldrt)
    


    # checa se ainda tem coisa pra assistir
    # se não tiver manda de volra pros setores
    # se tiver tira o que já assistiu e manda de volta
    
    novasopa = sopa[int(sopa.find('anime_studios'))+5:]

    if novasopa.find('status":6') == -1 and novasopa.find('status&quot;:6') == -1:
        temptw = False
    else:
        temptw = True

    if (str(novasopa).find('"is_rewatching"')) == -1 and (str(novasopa).find(';is_rewatching&')) == -1:
        ''

    elif onlyptw and temptw == False:
        ''
    
    else:
        proximo(novasopa)

def animefire(tl, ep):  

    sv = 1


    #um monte de variavel pro bagulho funcionar

    tocou=False

    if afsearchep(tl, ep) == False:
        print('\n\nEPISODIO NÃO ENCONTRADO!\n')
        return False


    notemplist = (
        'dandadan',
        'ranma-2024',
        )

    for title in notemplist:
        if tl == title:
            temp=False
            break
        else:
            temp=True


    result = (True, 0, 'none')
    while result[0]:

        result = afgetqual(tl, ep, result)
        eplink = result[2]

        if eplink != 'none':
            if eplink.find('/mp4_temp/') and temp == False:
                ''
            else:
                
                tocou = playmedia(eplink, result[3])
                if tocou:
                    return True
                else:
                    print('FALHA NA REPRODUÇÃO\n')

    print('\n\nEPISODIO NÃO ENCONTRADO!\n')
    return False

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

    while validusername == False and debugin == False:
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

    if debugin: usnm = 'gahvius'

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

def playmedia(link, filename=None):
    
    if filename == None: filename = 'ARQIUVO DE MEDIA'

    print(' '.join(['\nREPRODUZINDO:', filename, '\n']))

    if debugin: return True

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
    if debugin: print('PROVEDORES\n'), time.sleep(dbfldrt)

    global dubinfo

    epfound = False
    dubinfo = (False, False)




    dubsraw = (
        'one piece', 
        'dragon ball', 
        'one punch man', 
        'yu yu hakusho', 'yuy yyu hakusho',
        'saint seiya',
        'naruto',
    )

    dubs = list()
    for title in dubsraw:
        if (tl.lower()).find(title) != -1:
            dubs.append(tl)
    dubs = tuple(dubs)

    if tl in dubs:    
        dubinfo = (dubinfo[0], True)
    else:
        dubinfo = (dubinfo[0], False)

    if usnm.lower() == 'gahvius':
        dubinfo = (True, dubinfo[1])
        if dubinfo[1]: print('DUB = TRUE\n')
        

    titulo = re.sub(r'[^a-zA-Z0-9]', ' ', tl) 

    titulo = titulo.replace('      ', ' ')
    titulo = titulo.replace('     ', ' ')
    titulo = titulo.replace('    ', ' ')
    titulo = titulo.replace('   ', ' ')
    titulo = titulo.replace('  ', ' ')

    funcs = (afsearch, ani_cli)

    for func in funcs:
        epfound = func(titulo, ep)
        #if debugin: print('epfound =',epfound)
        if epfound: 
            break

    if debugin and epfound == False:
        nyaa(tl, ep)

    time.sleep(1)

def sopapranois(link):

    page = requests.get(str(link))
    soup = BeautifulSoup(page.text, 'html.parser')
    sopa = str(soup.find('table', class_='list-table'))

    return sopa, str(soup)

def verifyos():

    os = -1

    ptf = platform.platform()
    #print(ptf)

    if ptf.find('Emscripten') != -1:
        os = 0

    return os

def vaiumadub():

    print('')

    questions = [
        inquirer.List(
            "dub",
            message="BUSCAR POR EPISÓDIO DUBLADO?",
            choices=['SIM', 'NÃO'],
        ),
    ]

    dub = str(inquirer.prompt(questions))
    if dub == "{'dub': 'SIM'}":
        dub = True
    else:
        dub = False

    return dub

def streammagnet(link):
    
    print('\n\n', link, '\n')
    
    #exit()
    return True

def nyaa(tl, ep):

    print('PROVEDOR: "nyaa.si"\n\n')

    result = False

    if int(ep) < 10:
        ep = ''.join(['0', ep])



    link = ''.join(['https://nyaa.si/?f=0&c=0_0&q=', (tl.replace(' ', '+')).lower(), '+', ep, '&s=seeders&o=desc'])
    if debugin: print(link)
    sopa = str(sopapranois(link)[1])



    trclasloc = sopa.find('<tr class="')
    if trclasloc != -1:
        temep = True
    else:
        temep = False


    achei = False
    while temep and achei == False:

        sopa = sopa[sopa.find('<tr class="'):]

        tlloc = (sopa.lower()).find(tl.lower())
        if tlloc != -1:

            eploc = sopa.find(''.join([' - ', ep, ' ']))
            diff = eploc - tlloc
            if eploc != -1 and diff < 200 and diff > -200:
                sopa = sopa[sopa.find(''.join([' - ', ep, ' '])):]
            else:
                temep = False
                
        else:
            temep = False

        if temep:
            if sopa.find('<a href="magnet:') != -1:
                magnet = sopa[sopa.find('<a href="magnet:') + 9 : sopa.find('"><i class="fa fa-fw fa-magnet"></i></a>')]
                achei = True

            if achei == False:
                if sopa.find('<tr class="') == -1:
                    temep = False

    if temep == False:
        achei = False
        print('EPISODIO NÃO ENCONTRADO!\n')

    if achei:
        result = streammagnet(magnet)



    return result

def afsearch(tl, ep):

    global dubinfo

    print('PROVEDOR: "animefire.plus"')


    ntl = tl

    ntl = ntl.replace('Shinkakusha Kouho Senbatsu Shiken-hen', '2nd season')
    ntl = ntl.replace('Kagaijugyou-hen', '2nd season Kagaijugyou-hen')
    ntl = ntl.replace('Azumanga Daiou The Animation', 'Azumanga Daioh')

    ntl = ntl.replace(' ', '-')

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

    if debugin: print(link)


    if animeexiste:

        deubom = False


        # verificar se tem dub
        link = ''.join(['https://animefire.plus/animes/', ntl, '-dublado-todos-os-episodios'])
        response = requests.get(url=link)

        try:
            if str(response) == '<Response [500]>':
                ''
            else:
                if dubinfo[0] == False:
                    dubinfo = (True, vaiumadub()) 
                if dubinfo[1]:
                    print('\nBUSCANDO EPISODIO DUBLADO!')
                    deubom = animefire(dubtl, ep)
        except:
            ''

        if deubom == False:
            print('\nBUSCANDO EPISODIO LEGENDADO!')
            deubom = animefire(ntl, ep)
    else:
        print('\nANIME NÃO ENCONTRADO!\n')
        deubom = False

    return deubom

def afsearchep(tl, ep):

    link = ''.join(['https://animefire.plus/download/', tl, '/', ep])

    sopa = (sopapranois(link))[1]

    if str(sopa).find('<h6 class="text-white quicksand300 mx-3">Download indisponível</h6>') != -1:
        return False
    else:
        return True

def afgetqual(tl, ep, args):

    wtf = False
    args = (args[0], args[1]+1, args[2])

    link = ''.join(['https://animefire.plus/download/', tl, '/', ep])
    sopa = str((sopapranois(link))[1])
    ogsopa = sopa
    

    if sopa.find(';opacity: 0.3;">F-HD</span>') == -1 and args[1] == 1:
        if sopa.find('(F-HD)" href="') == -1:
            wtf= True
        else:
            sopa = sopa[sopa.find('(F-HD)" href="') + 14 : ]
    elif sopa.find(';opacity: 0.3;">HD</span>') == -1 and args[1] == 2:
        if sopa.find('(HD)" href="') == -1:
            wtf= True
        else:
            sopa = sopa[sopa.find('(HD)" href="') + 12 : ]
    elif sopa.find(';opacity: 0.3;">SD</span>') == -1 and args[1] == 3:
        if sopa.find('(SD)" href="') == -1:
            wtf= True
        else:
            sopa = sopa[sopa.find('(SD)" href="') + 12 : ]
    else:
        if args[1] == 4:
            return (False, args[1], 'none')
        else:
            return (True, args[1], 'none')

    eplink = sopa[:sopa.find('.mp4?type')+4]
    filename = sopa[sopa.find('[AnimeFire.plus] ')+17 : sopa.find('" style="cursor')]

    if wtf:

        sopa = ogsopa

        if args[1] == 1:
            sopa = sopa[sopa.find('<a (f-hd)'):]
            qual = '(F-HD)'            
        if args[1] == 2:
            sopa = sopa[sopa.find('<a (hd)'):]
            qual = '(HD)' 
        if args[1] == 3:
            sopa = sopa[sopa.find('<a (sd)'):]       
            qual = '(SD)'      

        eplink = sopa[sopa.find('download="')+10 : sopa.find('.mp4?type')+4]
        filename = ' '.join([tl.replace('-', ' '), '- Episódio', ep, qual])
            
    if eplink.find('/mp4_temp/') != -1:
        filename = filename.replace('(HD)', '(HD - LEGENDA TEMPORÁRIA)')

    return (args[0], args[1], eplink, filename)


    global symbs

    if procedimento == 0:

        while tx.find('\\u') != -1:
            fsymbcode = tx[tx.find('\\u')+1 : tx.find('\\u')+6]
            symbcode = fsymbcode[1:]

            try:
                int(symbcode[:1])
            except:
                break
            
            link = ''.join(['https://www.htmlsymbols.xyz/unicode/U+', symbcode.upper()])
            sopa = sopapranois(link)[1]
            symb = sopa[sopa.find('<title>')+7 : sopa.find('<title>')+8]
            
            symbsl = list(symbs)
            symbsl.append(symb)
            symbs = tuple(symbsl)
            tx = tx.replace(fsymbcode, symb)

    elif procedimento == 1:
        for symb in symbs:
            tx = tx.replace(symb, ' ')

    else:
        return tx


    tx = tx.replace('&quot;', '')
    tx = tx.replace('\\', '')

    tx = tx.replace('    ', ' ')
    tx = tx.replace('   ', ' ')
    tx = tx.replace('  ', ' ')
    
    return tx

def ani_cli(tl, ep):

    print('PROVEDOR: "ani-cli"')

    tocou = False

    try:
        subprocess.run('ani-cli -V')
    except:
        print('(PROVEDOR NÃO ENCCONTRADO/INSTALADO)\n\n')
        return False


    titulo = tl

    titulo = titulo.replace('3rd Season', '3')
    titulo = titulo.replace('3rd Season', '3')
    titulo = titulo.replace('2nd Season', '2')
    titulo = titulo.replace('Goumon', '')

    info = ('ani-cli --skip -e ', str(ep), ' ', titulo)
    comando = str(''.join(info))
    
    result = str(subprocess.run(comando, shell = True, executable="/bin/bash"))

    if result.find('returncode=1') == -1:
        tocou = True

    return tocou








# importar os bgl tudo

print('IMPORTANDO EXTENSÕES...')


extotal = str(9)
exnow = 1

print(''.join([str(exnow), '/', extotal]))
import subprocess, sys
exnow+=1

print(''.join([str(exnow), '/', extotal]))
import platform
exnow+=1

print(''.join([str(exnow), '/', extotal]))
import time
exnow+=1

print(''.join([str(exnow), '/', extotal]))
import os
exnow+=1

print(''.join([str(exnow), '/', extotal]))
import re
exnow+=1

sisop = verifyos()
#print(sisop)

if sisop != 0:

    print(''.join([str(exnow), '/', extotal]))
    try:
        import requests
    except:
        subprocess.run(''.join(['python -m pip install requests']))
        import requests
    exnow+=1

    print(''.join([str(exnow), '/', extotal]))
    try:
        import bs4
        from bs4 import BeautifulSoup
    except:
        cnctvrf()
        subprocess.run(''.join(['python -m pip install bs4']))
        import bs4
        from bs4 import BeautifulSoup
    exnow+=1

    print(''.join([str(exnow), '/', extotal]))
    try:
        import concurrent.futures
        from concurrent.futures import ThreadPoolExecutor, TimeoutError
    except:
        cnctvrf()
        subprocess.run(''.join(['python -m pip install concurrent.futures']))
        import concurrent.futures
        from concurrent.futures import ThreadPoolExecutor, TimeoutError
    exnow+=1

    print(''.join([str(exnow), '/', extotal]))
    try:
        import inquirer
    except:
        subprocess.run(''.join(['python -m pip install inquirer']))
        import inquirer
    exnow+=1

print('')

# subprocess.run('py -m pip install --upgrade pip')
os.system('cls||clear')
















# loop que faz a parada funcionar


debugin = False
dbfldrt = 0

getusername()

loops=0

while True:
    if debugin: print('LOOP START\n'), time.sleep(dbfldrt)
    setores()

exit()
