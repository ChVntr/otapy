#!/usr/bin/python











# funções



def setores(lista, listname):
    if debugin and flags: print('SETORES\n'), time.sleep(dbfldrt)

    global onlyptw
    


    #listas:







    mallink = 'https://myanimelist.net/animelist/'
    proceed = True




    # assistindo
    if lista == 0:
        mallink2 = '?order=11&order2=-5&status=1'
        onlyptw = False
    
    # PTW em lançamento
    elif lista == 2:
        mallink2 = '?airing_status=1&order=-16&order2=-14'
        onlyptw = True
    
    # PTW ainda não lançado
    elif lista == 4:
        mallink2 = '?airing_status=3&order=-16&order2=-14'
        onlyptw = True
    
    # em espera
    elif lista == 1:
        mallink2 = '?order=12&order2=5&status=3'
        onlyptw = False

    # PTW
    elif lista == 3:
        mallink2 = '?airing_status=2&order=-16&order2=-15'
        onlyptw = True

    else:
        proceed = False



    if proceed:

        print(''.join(['BUSCANDO DA LISTA "', listname, '"...\n' ]))

        link = ''.join([mallink, usnm, mallink2])

        sopa = sopapranois(link)[0]

        opts = ('REPRODUZIR LISTA COMPLETA', 'ESCOLHER ANIME', 'VOLTAR')
        erabe = inqlist('', opts)

        if erabe == len(opts)-1:
            return

        while erabe == 0:
            ideep = proximo(sopa)
            if ideep == False: return
            id = ideep[0]
            ep = ideep[1]
            tl = processid(id)
            os.system('cls||clear')
            print('BUSCANDO ANIME:'.lower(), tl, '\nEPISÓDIO:'.lower(), ep, '')
            while provedores(tl, ep):
                ep = int(ep)+1
                ep = geteps(id, ep)
                if ep == False: break
            sopa = update(sopa)




        ogsopa = sopa


        idlist = list()
        epslist = list()
        entradas = 0
        while True:
            result = proximo(sopa)
            if result == False: break
            idlist.append(result[0])
            epslist.append(result[1])
            sopa = update(sopa)
            entradas+=1

        idlist = tuple(idlist)

        tllist = list()
        entradas2=0
        for id in idlist:
            sys.stdout.flush()
            tllist.append(processid(id))
            entradas2+=1
            tx = ''.join(['(', str(entradas2), '/', str(entradas), ') ENTRADAS ENCONTRADAS\r'.lower()])
            sys.stdout.write(tx)

        print('\n')
        tllist.append('VOLTAR')


        while True:

            
            choice = inqlist('SELECIONE O ANIME DESEJADO', tllist)
            if choice == len(tllist)-1:
                return

            varpika = 0
            while True:
                ep = geteps(idlist[choice], int(epslist[choice])+varpika)
                if ep == False:
                    break
                else:
                    provedores(tllist[choice], ep)
                varpika+=1
                       
def proximo(sopa):

    if debugin and flags: print('PROXIMO\n'), time.sleep(dbfldrt)

    animeid = (sopa[ sopa.find(';anime_id&quot;:')+16 : sopa.find(',&quot;anime_studios')])

    try:
        int(animeid)
    except:
        animeid = (sopa[sopa.find(',"anime_id":')+12 : sopa.find(',"anime_studios"')])
        try:
            int(animeid)
        except:
            return False

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
    nextep=str(ep)



    return str(animeid), nextep

def update(sopa):
    
    if debugin and flags: print('UPDATE\n'), time.sleep(dbfldrt)
    


    # checa se ainda tem coisa pra assistir
    # se não tiver manda de volra pros setores
    # se tiver tira o que já assistiu e manda de volta
    
    novasopa = sopa[int(sopa.find('anime_studios'))+5:]

    if novasopa.find('status":6') == -1 and novasopa.find('status&quot;:6') == -1:
        temptw = False
    else:
        temptw = True

    if (str(novasopa).find('"is_rewatching"')) == -1 and (str(novasopa).find(';is_rewatching&')) == -1:
        return ''

    elif onlyptw and temptw == False:
        return ''
    
    else:
        return novasopa

def animefire(tl, ep):  

    sv = 1


    #um monte de variavel pro bagulho funcionar

    tocou=False

    if afsearchep(tl, ep) == False:
        print('EPISODIO NÃO ENCONTRADO!'.lower())
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
                if tocou == True:
                    return True
                if tocou == 69: 
                    return False
                if tocou == False:
                    print('FALHA NA REPRODUÇÃO'.lower())



    print('EPISODIO NÃO ENCONTRADO!'.lower())
    return animefire2(tl, ep)

def cnctvrf(url=None):

    try:
        requests.get('https://myanimelist.net')
        nocom=False
    except :
        nocom = True
        print('\nFALHA DE CONECÇÃO!\nAGUARDANDO RESPOSTA DE "myanimelist.net"...\n'.lower())

    while nocom:
        time.sleep(10)

        try:
            requests.get('https://myanimelist.net')
            nocom = False
        except:
            nocom = True

    if url != None:
        try:
            requests.get(url)
            return True
        except:
            return False

def getusername():
    os.system('cls||clear')
    
    global usnm
    validusername = False

    while validusername == False and debugin == False:
        usnm = input('USERNAME DO MYANIMELIST: ')
        cnctvrf()
        response = str(requests.get(str(''.join(['https://myanimelist.net/profile/', usnm]))))
        if response.find('404') != -1:
            print(
                'USUARIO NÃO ENCONTRADO\n\n'.lower()
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

    print(' '.join(['\nREPRODUZIR:'.lower(), filename, '\n']))

    if debugin: return True

    escolhas = list()

    try: 
        subprocess.run('mpv -clr')
        escolhas.append('MPV')
    except:
        try: 
            subprocess.run('mpv\\mpv.exe -clr')
            escolhas.append('MPV')
        except:
            ''
    
    escolhas.append('VLC')
    escolhas.append('VOLTAR')

    choice = inqlist('SELECIONE O REPRODUTOR DESEJADO', escolhas)

    mpv = ('mpv', 'mpv\\mpv.exe')
    vlc = ('vlc', 'C:\\Program Files\\VideoLAN\\VLC\\vlc.exe')
   
    players = list()
    if escolhas[choice] == 'MPV':
        for item in mpv:
            players.append(item)
    elif escolhas[choice] == 'VLC':
        for item in vlc:
            players.append(item)
    elif choice == len(escolhas)-1:
        return 69

    for player in players:
        cnctvrf()
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
        print('NENHUM REPRODUTOR DE VIDEO ENCONTRADO'.lower())
        exit()

def provedores(titulo, ep):
    
    if debugin and flags: print('PROVEDORES\n'), time.sleep(dbfldrt)
    
    print('\n')

    global dubinfo

    dubinfo = (False, False)




    for title in dubsraw:
        if (processtl(titulo, -1).lower()).find(title.lower()) != -1:
            dubs.append(titulo)

    if titulo in dubs:    
        dubinfo = (dubinfo[0], True)
    else:
        dubinfo = (dubinfo[0], False)

    if usnm.lower() == 'gahvius':
        dubinfo = (True, dubinfo[1])
        if dubinfo[1]: print('DUB = TRUE\n'.lower())
        




    funcs = (afsearch,)
    funcs = list(funcs)

    if not triedanicli:
        try:
            subprocess.run('ani-cli -V')
            funcs.append(ani_cli)
        except:
            print('ani-cli NÃO ENCCONTRADO/INSTALADO\n'.lower())
        triedanicli = True
        
    if debugin: 
        funcs.append(animesonlinecc)
        funcs.append(nyaa)

    epfound = False
    for func in funcs:
        if func == nyaa: epfound = func(titulo, ep)
        else: epfound = func(titulo, ep)
        print('')
        if epfound:
            os.system('cls||clear')
            break


    print('\n')

    
    
    return epfound

def sopapranois(link):

    cnctvrf()

    page = requests.get(str(link))
    soup = BeautifulSoup(page.text, 'html.parser')
    sopa = str(soup.find('table', class_='list-table'))

    return sopa, str(soup)

def verifyos():

    os = -1

    ptf = platform.platform()

    if ptf.find('Emscripten') != -1:
        os = 0

    return os

def vaiumadub():

    opts = ['SIM', 'NÃO']
    choice = inqlist('BUSCAR POR EPISÓDIO DUBLADO?', opts)

    if choice == 0:
        dub = True
    else:
        dub = False

    return dub

def streammagnet(link):
    
    print(link)
    time.sleep(3)

    return True

def nyaa(tl, ep):

    print('PROVEDOR: nyaa.si'.lower())

    result = False

    tl = tl.replace('½', '1/2')

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
        print('EPISODIO NÃO ENCONTRADO!'.lower())

    if achei:
        result = streammagnet(magnet)



    return result

def afsearch(tl, ep):

    global dubinfo

    print('PROVEDOR: animefire.plus'.lower())

    tl = tl.replace('Ü', 'ue')
    ntl = processtl(tl)

    dubtl = ''.join([ntl, '-dublado'])

    if ntl[-1] == '-':
        ntl = ntl[0 : (len(tl))-1]

    link = ''.join(['https://animefire.plus/animes/', ntl, '-todos-os-episodios'])

    if cnctvrf(link) == False:
        print('não foi possivel conectar ao provedor')
        return False


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
                if usnm.lower() == 'gahvius' and dubinfo[1]: 
                    print('dub NÃO ENCONTRADO!'.lower())
                    return False
            else:
                if dubinfo[0] == False:
                    dubinfo = (True, vaiumadub()) 
                if dubinfo[1]:
                    if debugin: print(link)
                    print('BUSCANDO EPISODIO DUBLADO...'.lower())
                    deubom = animefire(dubtl, ep)
                    if usnm.lower() == 'gahvius': return deubom
        except:
            ''

        if deubom == False:
            print('BUSCANDO EPISODIO LEGENDADO...'.lower())
            deubom = animefire(ntl, ep)
    else:
        print('ANIME NÃO ENCONTRADO!\n'.lower())
        return False

    return deubom

def afsearchep(tl, ep):

    link = ''.join(['https://animefire.plus/download/', tl, '/', ep])

    sopa = (sopapranois(link))[1]

    if str(sopa).find('<h6 class="text-white quicksand300 mx-3">Download indisponível</h6>') != -1 or sopa.find('não é possível fazer o download.') != -1:
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

    if eplink.find('lightspeedst.net') == -1: 
        #eplink = sopa[:sopa.find('&amp;title=[AnimeFire.plus]')]
        eplink = 'none'
    
    return (args[0], args[1], eplink, filename)

def ani_cli(tl, ep):

    print('PROVEDOR: "ani-cli"'.lower())

    tocou = False

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

def inqlist(string, opts, dft=None):


    newlist = list()
    for item in opts:
        newlist.append(str(item))
    opts = tuple(newlist)
        
    if dft != None: dft = str(dft)

    questions = [
        inquirer.List(
            "opções",
            message=string,
            choices=opts,
            default=dft,
        ),
    ]

    escolha = str(inquirer.prompt(questions))



    for opt in range(len(opts)):
        if escolha == ''.join(["{'opções': '", str(opts[opt]), "'}"]) or escolha == ''.join(["{'opções': ", '"', str(opts[opt]), '"}']):
            return opt
        
    print(escolha, '\nOH SHIT'), exit()
        
def selectlist():

    listnames = (
        'WATCHING',
        'ON HOLD',
        'PLAN TO WATCH (AIRING)',
        'PLAN TO WATCH (FINISHED AIRING)',
        'PLAN TO WATCH (NOT YET AIRED)',
        'VOLTAR',
        )    

    seleção = inqlist('SELECIONE A LISTA DESEJADA', listnames)

    if seleção == len(listnames)-1:
        getusername()
        return

    setores(seleção, listnames[seleção])

def processid(id):
    if debugin and flags: print('PROCESSANDO ID\n'), time.sleep(dbfldrt)


    link = ''.join(['https://myanimelist.net/anime/', id])
    tl_sopa = sopapranois(link)[1]

    to = 5
    while tl_sopa.find('<div id="captcha-container"></div>') != -1:
        print('...')
        time.sleep(to)
        tl_sopa = sopapranois(link)[1]
        to+=5

    titulo = (tl_sopa[tl_sopa.find('"twitter:site"/><meta content=') +31 : tl_sopa.find('" property="og:title"')])
    if len(titulo) > 500: titulo = (tl_sopa[tl_sopa.find('"twitter:site"/><meta content=') +31 : tl_sopa.find(' property="og:title"')-1])
    
    return titulo

def geteps(id, proximoep):
    if debugin: 
        if flags: print('GET EPS\n'), time.sleep(dbfldrt)

    print('carregando lista de episódios...')

    id=str(id)
    proximoep = int(proximoep)

    link = ''.join(['https://myanimelist.net/anime/', id, '/fuckyou/episode'])
    sopa = sopapranois(link)[1]
    ogsopa = sopa

    eps = getepslist(sopa)

    eonepiece = 99

    while len(eps) > eonepiece:

        link2 = ''.join([link, '?offset=', str(eonepiece+1)])
        sopa = sopapranois(link2)[1]

        if sopa.find('No episode information has been added to this title.') != -1: break

        maisep = getepslist(sopa)
        for ep in maisep: eps.append(ep)

        eonepiece +=100





    if proximoep > len(eps):
        for num in range(len(eps), proximoep):
            eps.append(num+1)

    eps.append('VOLTAR')

    print('')
    ep = inqlist('SELECIONE O EPISÓDIO DESEJADO', eps, eps[proximoep-1])
    if ep == len(eps)-1: return False
    


    return str(int(ep)+1)

def getepslist(sopa):

    lista1 = ('"episode-number nowrap" data-raw="', '">')

    eps = list()
    while sopa.find(lista1[0]) != -1:

        cord1 = sopa.find(lista1[0]) + len(lista1[0])
        cord2 = sopa[cord1:].find(lista1[1]) + cord1
        epnum = (sopa[cord1 : cord2])
        sopa = sopa[cord2:]

        try: int(epnum)
        except: print('OH SHIT'), exit()

        tx = ''.join(['/episode/', epnum, '">'])
        cord1 = sopa.find(tx) + len(tx)
        cord2 = sopa[cord1:].find('</a>') + cord1
        epname = sopa[cord1 : cord2]

        eps.append(' '.join([epnum, '-', epname]))

    return eps

def animefire2(tl, ep):

    link = ''.join(['https://animefire.plus/animes/', tl, '/', ep])
    sopa = sopapranois(link)[1]

    return False

def animesonlinecc(tl, ep):

    print('provedor: animesonlinecc.to')

    tl = processtl(tl)

    tl = tl.replace('yuu-yuu-hakusho', 'yu-yu-hakusho')

    link = ''.join(['https://animesonlinecc.to/anime/', tl, '/'])
    sopa = sopapranois(link)[1]

    if sopa.find('{"@id":null,"name":"Erro 404:') != -1:
        print('anime não encontrado!\n')
        return False

    link = ''.join(['https://animesonlinecc.to/episodio/', tl, '-episodio-', ep, '/'])
    sopa = sopapranois(link)[1]

    if sopa.find('{"@id":null,"name":"Erro 404:') != -1:
        print('episódio não encontrado!\n')
        return False

    if debugin:
        print(link)


    return False

def processtl(tl, mode=None):

    tl = tl.replace('Ü', 'U')

    titulo = re.sub(r'[^a-zA-Z0-9]', ' ', tl) 
    titulo = titulo.replace('      ', ' ')
    titulo = titulo.replace('     ', ' ')
    titulo = titulo.replace('    ', ' ')
    titulo = titulo.replace('   ', ' ')
    titulo = titulo.replace('  ', ' ')

    ntl = titulo
    
    if mode == None or mode == 0:
        ntl = ntl.replace('Shinkakusha Kouho Senbatsu Shiken-hen', '2nd season')
        ntl = ntl.replace('Kagaijugyou-hen', '2nd season Kagaijugyou-hen')
        ntl = ntl.replace('Azumanga Daiou The Animation', 'Azumanga Daioh')
        ntl = ntl.replace(' Meido ', ' maid ')
        ntl = ntl.replace('Dededede Destruction (OVA)', 'Dededede Destruction (ONA)')

        ntl = ntl.replace(' ', '-')

        ntl = ntl.lower() 

    return ntl






# importar os bgl tudo

print('IMPORTANDO EXTENSÕES...')


extotal = str(8)
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
        subprocess.run(''.join(['python -m pip install bs4']))
        import bs4
        from bs4 import BeautifulSoup
    exnow+=1

    print(''.join([str(exnow), '/', extotal]))
    try:
        import inquirer
    except:
        subprocess.run(''.join(['python -m pip install inquirer']))
        import inquirer
    exnow+=1

# subprocess.run('py -m pip install --upgrade pip')

















# loop que faz a parada funcionar


debugin = False
flags = False
dbfldrt = 0
dubs = list()
triedanicli = False

dubsraw = (
    'one piece', 
    'dragon ball', 
    'one punch man', 
    'yu yu hakusho', 
    'Yuu Yuu Hakusho',
    'saint seiya',
    'naruto',
    'sailor moon',
    'pokemon',
    'InuYasha',
)



getusername()

while True:
    os.system('cls||clear')
    if debugin and flags: print('LOOP START\n'), time.sleep(dbfldrt)
    selectlist()

exit()
