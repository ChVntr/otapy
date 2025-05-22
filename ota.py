#!/usr/bin/python











# funções



def setores(lista, listname):
    if debugin and flags: print('SETORES\n'), time.sleep(dbfldrt)

    global onlyptw
    global triedanicli
    triedanicli = 0


    #listas:







    mallink = 'https://myanimelist.net/animelist/'
    proceed = True




    # assistindo
    if lista == 0:
        mallink2 = '?order=11&order2=-5&status=1'
        onlyptw = False
    
    # PTW em lançamento
    elif lista == 2:
        mallink2 = '?airing_status=1&order=-16&order2=14'
        onlyptw = True
    
    # PTW ainda não lançado
    elif lista == 4:
        mallink2 = '?airing_status=3&order=-16&order2=14'
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

        if sopa.find('status":6') == -1 and sopa.find('status&quot;:6') == -1 and onlyptw:
            prt('lista vazia!')
            time.sleep(2)
            return False

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

            while provedores(tl, ep, id):
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
            sys.stdout.write('\r')
            entradas2+=1
            tx = ''.join(['(', str(entradas2), '/', str(entradas), ') ENTRADAS ENCONTRADAS'.lower()])
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
                    rslt = provedores(tllist[choice], ep, idlist[choice])
                if rslt: varpika+=1
                       
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

def animefire(tl, ep, part2):  

    global afpart2

    #um monte de variavel pro bagulho funcionar

    tocou=False

    if afsearchep(tl, ep) == False:
        print('\nEPISODIO NÃO ENCONTRADO!'.lower())
        afpart2 = False
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

        prt('.')

        result = afgetqual(tl, ep, result, part2)
        eplink = result[2]

        if eplink != 'none':
            if eplink.find('/mp4_temp/') and temp == False:
                ''
            else:
                prt('\n')
                tocou = playmedia(eplink, result[3])
                if tocou == True:
                    return True
                if tocou == 69: 
                    return False

    if temp:
        if part2:
            result = animefire2(tl, ep)
            if result == True: return True

    prt('\nfalha ao reproduzir episódio!\n')
    return False

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
    print('V1.0.7.12\n')
    
    global usnm
    validusername = False

    while validusername == False and debugin == False:
        usnm = input('USERNAME DO MYANIMELIST: ')
        cnctvrf()
        response = str(requests.get(str(''.join(['https://myanimelist.net/profile/', usnm]))))
        if response.find('404') != -1:
            print(
                'USUARIO NÃO ENCONTRADO\n'.lower()
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

    escolhas = list()
    
    vlcbanlist = (
        'https://www.blogger.com/video',
        'animesorionvip.net/player',
    )

    mpvbanlist = (
        '#EXT-X-PLAYLIST-TYPE:VOD',
        #'mywallpaper-4k-image',
    )

    vlcban = False
    mpvban = False

    for item in vlcbanlist:
        if link.find(item) != -1: vlcban = True
    for item in mpvbanlist:
        if link.find(item) != -1: mpvban = True

    if not mpvban:
        try: 
            spcs('mpv -clr')
            escolhas.append('MPV')
        except:
            try: 
                spcs('mpv\\mpv.exe -clr')
                escolhas.append('MPV')
            except:
                ''

    if not vlcban:
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
        return False

    for player in players:
        cnctvrf()
        try:
            comando = ' '.join([player, link])
            result = spcs(comando)
            foi=True
            if int(result.returncode) == 0:
                return True
            else:
                print('FALHA NA REPRODUÇÃO'.lower())
                return False
            break
        except:
            foi=False

    if foi == False:
        os.system('cls||clear')
        print('NENHUM REPRODUTOR DE VIDEO ENCONTRADO'.lower())
        exit()

def provedores(titulo, ep, id=None):
    global triedanicli
    global afpart2
    afpart2 = True
    
    if debugin and flags: print('PROVEDORES\n'), time.sleep(dbfldrt)
    
    print('\n')

    global dubinfo

    dubinfo = (False, False, False)



    for title in dubsraw:
        if (processtl(titulo, -1).lower()).find(title.lower()) != -1:
            dubinfo = (dubinfo[0], True, dubinfo[2])

    if usnm.lower() == 'gahvius':
        dubinfo = (True, dubinfo[1], dubinfo[2])
        if dubinfo[1]:
            dubinfo = (True, True, True)
            print('DUB = TRUE\n'.lower())


    funcs = (animesdigitalorg, afsearch, goyabu)
    funcs = list(funcs)
    

    if triedanicli == 0:
        try:
            spcs('ani-cli -V')
            triedanicli = 1
        except:
            print('ani-cli NÃO ENCCONTRADO/INSTALADO\n'.lower())
            triedanicli = 2
    
    if triedanicli == 1 and not dubinfo[2]:
        funcs.append(ani_cli)

    funcs2 = (q1n, animesonlinecc, animesorion, afsearch2)
    for item in funcs2:
        funcs.append(item)

    epfound = False
    for func in funcs:
        if func == nyaa: epfound = func(titulo, ep)
        else: epfound = func(titulo, ep)
        print('')
        if epfound:
            os.system('cls||clear')
            break
        if debugin: exit()

    if id != None and not epfound:
        if idtoyt(id, ep):
            return True
        var = 0
        for item in id_ep_link:
            if item[0] == int(id):
                for eps in item:
                    if type(eps) == list:
                        if eps[0] == int(ep):
                            for link in eps[1]:
                                if yt_especifico(link):
                                    return True


    print('\n')

    
    
    return epfound

def sopapranois(link):

    cnctvrf()

    try:
        page = requests.get(str(link), timeout=5)
    except:
        cnctvrf()
        return (False, '')
    soup = BeautifulSoup(page.text, 'html.parser')
    sopa = str(soup.find('table', class_='list-table'))

    return sopa, str(soup)

def verifyos():

    os = -1

    ptf = platform.platform()

    if ptf.find('Emscripten') != -1:
        os = 0

    if ptf.find('Linux') != -1:
        os = 1

    if ptf.find('android') != -1:
        os = 2


    #print(ptf)

    return os

def vaiumadub():
    global dubinfo

    opts = ['SIM', 'NÃO']
    choice = inqlist('BUSCAR POR EPISÓDIO DUBLADO?', opts)

    if choice == 0:
        dubinfo = (True, True, False)
    else:
        dubinfo = (True, False, False)

def streammagnet(link):
    
    print(link)
    time.sleep(3)

    return False

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

def afsearch(tl, ep, part2=None):

    global afpart2

    print('PROVEDOR: animefire.plus'.lower())

    if part2 == None: part2 = False

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
                if dubinfo[2]: 
                    print('dub NÃO ENCONTRADO!'.lower())
                    return False
            else:
                if dubinfo[0] == False:
                    vaiumadub() 
                if dubinfo[1]:
                    if debugin: print(link)
                    prt('BUSCANDO EPISODIO DUBLADO...'.lower())
                    deubom = animefire(dubtl, ep, part2)
                    if usnm.lower() == 'gahvius': return deubom
        except:
            ''

        if deubom == False:
            prt('BUSCANDO EPISODIO LEGENDADO...'.lower())
            deubom = animefire(ntl, ep, part2)
    else:
        print('ANIME NÃO ENCONTRADO!'.lower())
        afpart2 = False
        return False

    return deubom

def afsearchep(tl, ep):

    link = ''.join(['https://animefire.plus/download/', tl, '/', ep])

    sopa = (sopapranois(link))[1]

    if str(sopa).find('<h6 class="text-white quicksand300 mx-3">Download indisponível</h6>') != -1 or sopa.find('não é possível fazer o download.') != -1:
        return False
    else:
        return True

def afgetqual(tl, ep, args, part2):

    wtf = False
    args = (args[0], args[1]+1, args[2])


    link = ''.join(['https://animefire.plus/download/', tl, '/', ep])
    sopa = str((sopapranois(link))[1])
    ogsopa = sopa


    if not part2 and sopa.find(';opacity: 0.3;">F-HD</span>') == -1 and args[1] == 1:
        if sopa.find('(F-HD)" href="') == -1:
            wtf= True
        else:
            sopa = sopa[sopa.find('(F-HD)" href="') + 14 : ]
    elif sopa.find(';opacity: 0.3;">HD</span>') == -1 and args[1] == 2:
        if sopa.find('(HD)" href="') == -1:
            wtf= True
        else:
            sopa = sopa[sopa.find('(HD)" href="') + 12 : ]
    elif part2 and sopa.find(';opacity: 0.3;">SD</span>') == -1 and args[1] == 3:
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
        if not part2:
            return (False, args[1], 'none')
        filename = ' '.join([filename, '(LEGENDA TEMPORÁRIA)'])

    if eplink.find('lightspeedst.net') == -1: 
        #eplink = sopa[:sopa.find('&amp;title=[AnimeFire.plus]')]
        eplink = 'none'
    
    return (args[0], args[1], eplink, filename)

def ani_cli(tl, ep):

    print('PROVEDOR: ani-cli'.lower())
    
    tocou = False

    titulo = tl

    titulo = titulo.replace('3rd Season', '3')
    titulo = titulo.replace('3rd Season', '3')
    titulo = titulo.replace('2nd Season', '2')
    titulo = titulo.replace('Goumon', '')

    info = ('ani-cli -e', ep, titulo, '&')
    comando = str(' '.join(info))
    result = str(spcs(comando))
    

    if result.find('No results found!') != -1:
        prt('anime não encontrado!\n')
        return False
    if result.find('Episode not released!') != -1:
        prt('episódio não encontrado!\n')
        return False
    if result.find('Links Fetched') != -1:
        return True
    if result.find(': rofi:') != -1:
        prt('provedor indisponivel!\n')
        return False

    return False

def inqlist(string, opts, dft=None):

    prt('\a')

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

    filename = 'MalIDToTitle'

    try:
        with open(filename, 'r') as f:
            ''
    except:
        with open(filename, 'w') as f:
            f.write('')

    with open(filename, 'r') as f:
        data = f.readlines()
    
    podeir = False
    try:
        tlfromfile = data[int(id)]
        podeir = True
    except:
            for t in range(len(data), int(id)+1):
                data.append('\n')
            if debugin: print('')
        
    if podeir and tlfromfile != '' and tlfromfile != ' ' and tlfromfile != '\n':
        #if debugin: print('\ncu seco')
        tl = tlfromfile[:-1]
        tl = tl.replace('&amp;', '&')
        return tl

    link = ''.join(['https://myanimelist.net/anime/', id])
    tl_sopa = sopapranois(link)[1]

    to = 5
    if tl_sopa.find('<div id="captcha-container"></div>') != -1:
        prt('..')
        while tl_sopa.find('<div id="captcha-container"></div>') != -1:
            prt('.')
            time.sleep(to)
            tl_sopa = sopapranois(link)[1]
            to+=5

    titulo = (tl_sopa[tl_sopa.find('"twitter:site"/><meta content=') +31 : tl_sopa.find('" property="og:title"')])
    if len(titulo) > 500: titulo = (tl_sopa[tl_sopa.find('"twitter:site"/><meta content=') +31 : tl_sopa.find(' property="og:title"')-1])
    
    
    try:
        data[int(id)] = ''.join([titulo, '\n'])
        with open(filename, 'w') as f:
            f.writelines(data)
    except:
        data[int(id)] = '\n'
        with open(filename, 'w') as f:
            f.writelines(data)

    if debugin: print('\n\n', id, data[int(id)])

    return titulo

def geteps(id, proximoep):
    if debugin: 
        if flags: print('GET EPS\n'), time.sleep(dbfldrt)

    sys.stdout.write('carregando lista de episódios...'), sys.stdout.flush()
    

    id=str(id)
    proximoep = int(proximoep)

    link = ''.join(['https://myanimelist.net/anime/', id, '/fuckyou/episode'])
    sopa = sopapranois(link)[1]
    ogsopa = sopa

    eps = getepslist(sopa)

    eonepiece = 99

    while len(eps) > eonepiece:

        sys.stdout.write('.'), sys.stdout.flush()

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
        epname = epname.replace('&amp;', '&')

        eps.append(' '.join([epnum, '-', epname]))

    return eps

def animefire2(tl, ep):

    link = ''.join(['https://animefire.plus/animes/', tl, '/', str(ep)])
    sopa = sopapranois(link)[1]
    if debugin: print(link)

    if sopa.find('https://www.blogger.com/video') == -1:
        if debugin: print('naotem')
        return False

    if debugin: print('tem')

    kw = 'src="https://www.blogger.com/video'
    loc = sopa.find(kw)+5
    loc2 = loc + sopa[loc:].find('" style="')
    if debugin: print(loc, loc2)
    link = sopa[loc : loc2]
    if debugin: prt(link)


    if sopapranois(link)[1].find('<div class="errorMessage">') != -1:
        return False
    
    prt('\n')
    return playmedia(link, filename=' '.join([tl, 'Episódio', ep]))

def animesonlinecc(tl, ep):

    print('provedor: animesonlinecc.to')

    fnm = ''.join([tl, ' - Episódio ', ep])

    if tl == 'Bishoujo Senshi Sailor Moon': tl = 'sailor moon'
    tl = tl.replace('½', '1/2')
    tl = processtl(tl)
    tl = tl.replace('yuu-yuu-hakusho', 'yu-yu-hakusho')
    tl = tl.replace('-daidaidaidaidaisuki-', '-dai-dai-dai-dai-daisuki-')
    tl = tl.replace('2nd-season', '2')
    tl = tl.replace('3rd-season', '3')

    link = ''.join(['https://animesonlinecc.to/episodio/', tl, '-episodio-', ep, '/'])
    sopa = sopapranois(link)[1]
    if debugin: print(link)

    if sopa.find('https://www.blogger.com/video') == -1:
        print('anime/episódio não encontrado!')
        return False





    temdub = False
    temsub = False
    dubop = None

    if sopa.find('</b> Dublado </a>') != -1: 
        temdub = True
        loc = sopa.find('"> <b class="icon-play_arrow"></b> Dublado </a>')
        dubop = sopa[loc-1:loc]

        linkloc1 = ''.join(['id="option-', dubop])
        linkloc2 = sopa.find(linkloc1)
        loc = linkloc2 + sopa[linkloc2:].find('https://www.blogger.com/video')

        linkdub = sopa[loc : sopa[loc:].find('"')+loc]
        fnmdub = ''.join([fnm, ' (Dublado)'])
        if debugin: print(link)
    else:
        if dubinfo[2]:
            print('dub NÃO ENCONTRADO!'.lower())
            return False

    if sopa.find('</b> Legendado </a>') != -1: 
        temsub = True
        loc = sopa.find('"> <b class="icon-play_arrow"></b> Legendado </a>')
        dubop = sopa[loc-1:loc]

        linkloc1 = ''.join(['id="option-', dubop])
        linkloc2 = sopa.find(linkloc1)
        loc = linkloc2 + sopa[linkloc2:].find('https://www.blogger.com/video')

        linksub = sopa[loc : sopa[loc:].find('"')+loc]
        fnmsub = ''.join([fnm, ' (Legendado)'])
        if debugin: print(link)


    if debugin: print(temsub, temdub)

    if temdub and temsub:
        if dubinfo[0] == False:
            vaiumadub()
            temdub = dubinfo[1]

    while temdub:
        print('BUSCANDO EPISODIO DUBLADO...'.lower())
        if sopapranois(linkdub)[1].find('<div class="errorMessage">') != -1:
            print('episódio não encontrado!')
            break
        result = playmedia(linkdub, filename=fnmdub)
        if result == True: return True
        break
    while temsub:
        print('BUSCANDO EPISODIO Legendado...'.lower())
        if debugin: print(linksub)
        if sopapranois(linksub)[1].find('<div class="errorMessage">') != -1:
            print('episódio não encontrado!')
            break
        result = playmedia(linksub, filename=fnmsub)
        if result == True: return True
        break



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
        ntl = ntl.replace('Shinkakusha Kouho Senbatsu Shiken hen', '2nd season')
        ntl = ntl.replace('Kagaijugyou hen', '2nd season Kagaijugyou hen')
        ntl = ntl.replace('Azumanga Daiou The Animation', 'Azumanga Daioh')
        ntl = ntl.replace(' Meido ', ' maid ')
        ntl = ntl.replace('Dededede Destruction OVA', 'Dededede Destruction ONA')

        ntl = ntl.replace(' ', '-')

        while ntl[-1] == '-':
            ntl = ntl[:-1]

        ntl = ntl.lower() 

    return ntl

def animesdigitalorg(tl, ep):
    print('provedor: animesdigital.org')

    temdub=False
    edub=False
    ova = False

    ogtl = tl

    if tl.lower().find('one punch man') != -1:
        print('ANIME NÃO ENCONTRADO!'.lower())
        return False
    
    if int(ep) < 10: ep = ''.join(['0', ep])

    if tl.find('Fullmetal Alchemist: Brotherhood') != -1:
        if tl == 'Fullmetal Alchemist: Brotherhood Specials': 
            ova = True
        tl = 'fullmetal-abb001'
        
    if tl == 'Ore dake Level Up na Ken Season 2: Arise from the Shadow': tl = 'solo leveling ii'
    if tl == 'Bishoujo Senshi Sailor Moon': tl = 'sailor moon'
    tl = processtl(tl)
    tl = tl.replace('yuu-yuu-hakusho', 'yu-yu-hakusho')
    tl = tl.replace('ranma-2024', 'ranma-½-2024')


    sublink = ''.join(['https://animesdigital.org/anime/a/', tl])
    link = sublink
    dublink = ''.join([link, '-dublado'])
    if debugin: print(link)
    sopa = sopapranois(link)[1]

    if sopa.find('<div class="msg404">') != -1:
        print('ANIME NÃO ENCONTRADO!'.lower())
        return False
    links = (sublink,)
    if debugin: print(sublink)

    if sopa[sopa.find('<title>') : sopa.find('</title>')].find('Dublado') != -1:
        edub=True
    else:
        if sopapranois(dublink)[1].find('<div class="msg404">') == -1:
            if debugin: print(dublink)
            temdub=True

    if dubinfo[2]:
        if not edub and not temdub:
            print('dub NÃO ENCONTRADO!'.lower())
            return False
        

    if temdub:
        if not dubinfo[0]:
            vaiumadub()
        if dubinfo[1]:
            links = (dublink, sublink)



    
    if ova == True: tx = 'Ova '
    else: tx = 'Episódio '
    eploc = tx + str(ep) + '"'
    if debugin: print(eploc)

    for link in links:
        defbreak = False

        sopa = sopapranois(link)[1]
        if debugin: print(link)

        if link == dublink or edub: prt('buscando episódio dublado...')
        else: prt('buscando episódio legendado...')

        page = 1

        varalha = False
        while sopa.find(eploc) == -1:
            varalha = True
            if sopa.find('<div class="item_ep b_flex">') == -1:
                prt('\nepisódio não encontrado!\n')
                defbreak = True
                break
            fep = texto_no_meio(sopa, '<div class="item_ep b_flex">', '<div class="date"')
            fep = texto_no_meio(fep, 'Episódio ', '"')
            if debugin: print(fep)
            try:
                fep = int(fep)
            except:
                prt('\nprovedor indisponivel!\n')
                return False
            if fep < int(ep):
                prt('\nepisódio não encontrado!\n')
                defbreak = True
                break
            page+=1
            linkus = ''.join([link, '/page/', str(page)])
            if debugin: print(linkus)
            prt('.')
            sopa = sopapranois(linkus)[1]
        

        if defbreak == False:
            print('')
            if varalha: link = linkus

            tx = '<div class="item_ep b_flex">'
            enquanto = True
            while enquanto:
                if sopa.find(tx) == -1: break
                sopa = sopa[sopa.find(tx)+len(tx):]
                if sopa.find(eploc) == -1:
                    if debugin: print(link, 'sem eploc')
                    enquanto = False
                    break
                link = texto_no_meio(sopa, 'https://animesdigital.org/video/a/', '"', True)            
            
            sopa = sopapranois(link)[1]
            if debugin: print(link)

            fnm = texto_no_meio(sopa, '<title>', '</title>')
            if debugin: print(fnm)

            loc = sopa.find('https://api.anivideo.net')
            if loc == -1:
                print('falha ao reproduzir episódio!')
                if debugin: print('SEU MERDA')
                defbreak = True
            if not defbreak:
                link = texto_no_meio(sopa, 'https://api.anivideo.net', '"', True)
                if debugin: print(link)

                sopa = sopapranois(link)[1]
                link = texto_no_meio(sopa, "https://cdn-s", "'", True)
                if debugin: print(link)

                if playmedia(link, fnm) == True:
                    return True


    return False

def animesorion(tl, ep):
    print('provedor: animesorionvip.net')

    if tl == 'Bishoujo Senshi Sailor Moon': tl = 'sailor moon'
    tl = processtl(tl)
    tl = tl.replace('yuu-yuu-hakusho', 'yu-yu-hakusho')

    link = ''.join(['https://animesorionvip.net/animes/', tl, '-todos-os-episodios'])
    if debugin: print(link)
    sopa = sopapranois(link)[1]

    tx = 'https://animesorionvip.net/video/'
    if sopa.find(tx) == -1:
        print('ANIME NÃO ENCONTRADO!'.lower())
        return False

    if sopa.find(''.join(['Episódio ', ep])) == -1:
        print('episódio não encontrado!')
        return False

    tempsopa = sopa
    while True:
        if tempsopa.find(tx) == -1:
            print('episódio não encontrado!')
            return False
        loc = tempsopa.find(tx)
        tempsopa = tempsopa[loc : loc + tempsopa[loc:].find('">')]
        if tempsopa.find(''.join(['Episódio ', ep])) == -1:
            tempsopa = sopa[sopa.find(tempsopa)+5:]
        else: 
            break
        

    if debugin: print(tempsopa)
    tx = 'title="'
    fnm = tempsopa[tempsopa.find(tx)+len(tx) : ]
    link = tempsopa[:tempsopa.find('"')]

    sopa = sopapranois(link)[1]
    loc = sopa.find('https://animesorionvip.net/player')
    link = sopa[loc : loc + sopa[loc:].find('=&')]

    if dubinfo[2]:
        if fnm.lower().find('dublado') == -1:
            print('dub NÃO ENCONTRADO!'.lower())
            return False

    return playmedia(link, fnm)

def q1n(tl, ep):

    print('provedor: q1n.net')

    tl = processtl(tl)

    titulos = list()

    link = ''.join(['https://q1n.net/a/', tl])
    if debugin: print(link)
    sopa = sopapranois(link)[1]

    if sopa.find('<body class="error404">') != -1:
        print('anime não encontrado!')
        return False

    dubtl = ''
    link = ''.join(['https://q1n.net/a/', tl, '-Dublado'])
    sopa = sopapranois(link)[1]
    if sopa.find('<body class="error404">') == -1:
        if debugin: print(link)
        if dubinfo[0] == False:
            vaiumadub()
        if dubinfo[1]:
            dubtl = ''.join([tl, '-dublado'])
            titulos.append(dubtl)
    else: 
        if dubinfo[2]:
            print('dub não encontrado')
            return False

    if dubinfo[2] == False: titulos.append(tl)

    for tl in titulos:

        if tl == dubtl: print('buscando episódio dublado...')
        else: print('buscando episódio legendado...')

        link = ''.join(['https://q1n.net/e/', tl, '-episodio-', ep])
        if debugin: print(link)
        sopa = sopapranois(link)[1]

        tx = '"VideoObject","name": "'
        loc1 = sopa.find(tx) + len(tx)
        fnm = sopa[loc1 : ]
        fnm = fnm[ : fnm.find('"')]

        if sopa.find('<body class="error404">') != -1:
            print('episódio não encontrado!')
            break

        if sopa.find("https://q1n.net/ao/?id=") != -1:
            link = sopa[sopa.find('https://q1n.net/ao/?id=') : ]
            link = link[ : link.find('"')]
            sopa2 = sopapranois(link)[1]
            if debugin: print(link)
            if sopa2.find('secvideo') != -1:
                if usnm.lower() == 'gahvius':
                    print(link, '\nEITA POHA\a'), time.sleep(99999), exit()
            else:
                if debugin == 1231:
                    sopa2 = sopapranois(link)[1]
                    link = sopa2[sopa2.find('https://api.q9x.in/') :]
                    link = link[: link.find('"')]
                    print(link, sopapranois(link)[1]), exit()

        if sopa.find("https://www.blogger.com/video.g") != -1:
            link = sopa[sopa.find('https://www.blogger.com/video.g') : ]
            link = link[ : link.find(';')]
            if debugin: print(link)
            if playmedia(link, fnm) == True:
                return True


        print('falha ao reproduzir episódio!')


    return False
    
def prt(string):

    if type(string) == tuple or type(string) == list:
        for item in string:
            prt(item)
            #prt(' ')
    else:
        string = str(string)
        sys.stdout.write(string)
        sys.stdout.flush()

def spcs(comando):

    volta = None
    if verifyos() == 1:
        volta = subprocess.run(comando, capture_output=True, shell=True)
    elif verifyos() == -1:
        volta = subprocess.run(comando)
    elif verifyos() == 2:
        volta = subprocess.run(comando, shell=True)

    return volta

def idtoyt(id, ep):

    link = ''.join(['https://myanimelist.net/anime/', id])
    sopa = sopapranois(link)[1]
    sopa = sopa[sopa.find('<div class="external_links">') : ]
    sopa = sopa[ : sopa.find('<div class="clearfix')]

    if sopa.find('https://www.youtube.com/watch') != -1:

        link = sopa[sopa.find('https://www.youtube.com/watch') : ]
        link = link[ : link.find('"')]
        link = link.replace('&amp;', '&')
        
        return yt_especifico(link)
        
    return False

def yt_especifico(link):

    print('provedor: youtube.com')

    tx = '"title":{"simpleText":"'
    titulo = sopapranois(link)[1]
    titulo = titulo[titulo.find(tx)+len(tx) : ]
    titulo = titulo[ : titulo.find('"},"description"')]
    titulo = titulo.replace('\\', '')
    return playmedia(link, titulo)
        
    return False

def goyabu(tl, ep):
    
    prt('provedor: goyabu.to\n')

    tl = processtl(tl)

    link = ''.join(['https://goyabu.to/anime/', tl])
    sopa = sopapranois(link)[1]
    dubsopa = sopapranois(''.join([link, '-dublado']))[1]

    vrs = list()

    if dubsopa.find('<title>404 Not Found</title>') == -1:
        vrs.append(dubsopa)
    else:
        if dubinfo[2]:
            print('dub NÃO ENCONTRADO!'.lower())
            return False

    if sopa.find('<title>404 Not Found</title>') == -1:
        vrs.append(sopa)
    
    if len(vrs) == 0:
        prt('anime não encontrado!\n')

    if len(vrs) > 1:
        if not dubinfo[0]:
            prt('\n')
            vaiumadub()
        if not dubinfo[1]:
            vrs = (sopa,)

    for sopa in vrs:
        
        if sopa == dubsopa:
            prt('buscando episódio dublado...\n')
        else:
            prt('buscando episódio legendado...\n')

        if sopa.find(''.join(['id="ep ', ep, '"'])) == -1:
            prt('episódio não enontrado!\n')

        else:

            int_point = ''.join(['id="ep ', ep, '">'])
            file_name = sopa[sopa.find(int_point) + len(int_point) : ]
            file_name = file_name[ : file_name.find('</a>')]

            int_point = sopa.find(int_point)
            link = sopa[(sopa[:int_point].rfind('https://goyabu.to/')):]
            link = link[ : link.find('"')]

            sopa = sopapranois(link)[1]

            link = sopa[sopa.find('https://www.blogger.com/video'):]
            link = link[ : link.find('"')]

            if playmedia(link, file_name): return True

    return False

def afsearch2(tl, ep):
    if not afpart2: return False
    return afsearch(tl, ep, part2=True)

def texto_no_meio(texto, começo, fim, prsv_começo = None):

    loc1 = texto.find(começo)
    loc2 = loc1 + texto[loc1:].find(fim)

    if prsv_começo != True: loc1 += len(começo)

    return texto[loc1:loc2]





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

if sisop != 0:

    print(''.join([str(exnow), '/', extotal]))
    try:
        import requests
    except:
        spcs(''.join(['python -m pip install requests']))
        import requests
    exnow+=1

    print(''.join([str(exnow), '/', extotal]))
    try:
        import bs4
        from bs4 import BeautifulSoup
    except:
        spcs(''.join(['python -m pip install bs4']))
        import bs4
        from bs4 import BeautifulSoup
    exnow+=1

    print(''.join([str(exnow), '/', extotal]))
    try:
        import inquirer
    except:
        spcs(''.join(['python -m pip install inquirer']))
        import inquirer
    exnow+=1

# subprocess.run('py -m pip install --upgrade pip')

















# loop que faz a parada funcionar


debugin = False
flags = False
dbfldrt = 0
dubs = list()

dubsraw = (
    'one piece', 
    'dragon ball', 
    'one punch man', 
    'yu yu hakusho', 
    'Yuu Yuu Hakusho',
    'saint seiya',
    'naruto',
    'sailor moon',
    'InuYasha',
    'gokudolls',
)

id_ep_link = [[11795, [1, ['https://www.youtube.com/watch?v=dRBP1rpE5y8&t=1s']]], 
            [58507, [1, ['https://youtu.be/sHGcGkaYd38']]], 
            [8939, [1, ['https://youtu.be/GlxrJVdNyro']]],
            [56213, [1, ['https://www.youtube.com/watch?v=2zcZbIN3VPE']],
                    [2, ['https://www.youtube.com/watch?v=3VRuAhF1gLY']],
                    [3, ['https://www.youtube.com/watch?v=5n6K33W442w']],
                    [4, ['https://www.youtube.com/watch?v=Gv_lwgPAQsQ']]],
            [30059, [1, ['https://www.youtube.com/watch?v=mzGU_iUMBi8']]],
            ]




getusername()

while True:
    os.system('cls||clear')
    if debugin and flags: print('LOOP START\n'), time.sleep(dbfldrt)
    selectlist()

exit()
