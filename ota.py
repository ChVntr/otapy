#funções

def key_press(key):

    global tecla

    tecla = str(key)

    if tecla == 'Key.enter': 
        prt('\033[1A')
        
    return False

def texto_no_meio(texto, começo, fim, prsv_começo = None, prsv_final = None):

    for i in [texto, começo, fim]:
        if type(i) != str:
            return False

    loc1 = texto.find(começo) + len(começo)
    loc2 = loc1 + texto[loc1:].find(fim)

    if prsv_começo == True: loc1 -= len(começo)
    if prsv_final == True: loc2 += len(fim)

    for linha in (começo, fim):
        if texto.find(linha) == -1:
            return False
            

    return texto[loc1:loc2]

def cnctvrf(url=None):

    try:
        requests.get('https://myanimelist.net')
        nocom=False
    except :
        nocom = True
        print('\n\nFALHA DE CONExÃO!\nAGUARDANDO RESPOSTA DE "myanimelist.net"...\n'.lower())

    while nocom:
        time.sleep(10)

        try:
            requests.get('https://myanimelist.net')
            nocom = False
            apagar_linhas(5)
        except:
            nocom = True

    if url != None:
        try:
            requests.get(url)
            return True
        except:
            return False

def prt(string, hold = False):

    if type(string) == tuple or type(string) == list:
        for item in string:
            prt(item)
    else:
        sys.stdout.write(str(string))

    if not hold: sys.stdout.flush()

def getusername():

    validusername = False
    linhas = 2

    while validusername == False:
        usnm = input('\nUSERNAME DO MYANIMELIST: ')
        cnctvrf()
        response = str(requests.get(str(''.join(['https://myanimelist.net/profile/', usnm]))))
        if response.find('404') != -1:
            prt('USUARIO NÃO ENCONTRADO!\n'.lower())
            linhas+=3
        else:
            validusername = True
            apagar_linhas(linhas)

    return usnm

def apagar_linhas(n):

    if n < 1:
        sys.stdout.write('\r\033[J')
    else:
        sys.stdout.write(f"\033[{n}A \r\033[J")

def sopapranois(link, t = 4, load = None):

    if debug: prt(f' {link}')

    if link == False or link == '': return False

    cnctvrf()

    try:
        page = requests.get(str(link), timeout=10)
    except Exception as e:
        cnctvrf()
        prt(f'\n{e}')
        retornar = sopapranois(link, t, load)
        apagar_linhas(1)
        return retornar

    soup = bs4.BeautifulSoup(page.text, 'html.parser')    

    if str(soup).find('<div id="captcha-container"></div>') != -1:
        if debug: prt(' captcha do inferno')
        if load != None:
            load.add()
        time.sleep(t)
        return sopapranois(link, t*2, load)

    return str(soup)

def get_name_from_id(id):

    link = f'https://myanimelist.net/anime/{id}'

    sopa = sopapranois(link)

    titulo = texto_no_meio(sopa, '<h1 class="title-name h1_bold_none"><strong>', '</strong>')

    #print(titulo)
    #print(link)
    #exit()

    return titulo

def get_name_from_file(id):

    filename = f'{os.path.expanduser("~")}/otapy/MalIDToTitle'



    try:
        with open(filename, 'r') as f:
            data = f.readlines()
            f.close()
    except:
        with open(filename, 'w') as f:
            f.write('')
            f.close()
        return get_name_from_file(id)





    if len(data) > int(id):

        if data[int(id)] != '' and data[int(id)] != '\n':
            return data[int(id)][:-1]

        else:
            titulo = get_name_from_id(id)
            data[int(id)] = titulo+'\n'
            with open(filename, 'w') as f:
                try: f.writelines(data)
                except:
                    f.close()

                    titulo = processtl(titulo, 0)
                    data[int(id)] = titulo+'\n'
                    
                    with open(filename, 'w') as f:                    
                        f.writelines(data)
                f.close()
    
    else: 
        while len(data) <= int(id):
            data.append('\n')
        with open(filename, 'w') as f:
            f.writelines(data)
            f.close()

    return get_name_from_file(id)

def play_ep(id, ep, status = None, air_status = None):
    
    if debug: apagar_linhas(99)
    if devmode:
        if int(status) == 2: ep = 1 

    titulo = get_name_from_file(id)

    sys.stdout.flush()
    prt(f'\nanime: {titulo}\nep: {ep}')

    classe = provedores((id, ep, titulo))
    midia_link = classe.ep_link

    if midia_link != False:

        tocou = False

        if not player_off:
            for player in playerlist:

                op = subprocess.run(f'{player} {midia_link}', shell=True, capture_output=True)
                if op.returncode == 0: 
                    tocou = True
                    break
        else: tocou = True

        if not tocou:
            prt('\nNENHUM REPRODUTOR DE VIDEO ENCONTRADO!\n')
            exit()

        apagar_linhas(classe.linhas_apagar+4)
        if devmode and not player_off: 
            if debug: return
            play_ep(id, ep+1, status)
        elif not player_off: get_eps(id, ep)
        return
    else: 
        if status != 1:
            if air_status != 3:
                if devmode and not debug:
                    prt('\a')
                    webbrowser.open(f'https://myanimelist.net/anime/{id}')
        time.sleep(1)
    
    apagar_linhas(classe.linhas_apagar+4)

def processtl(tl, mode=1):

    tl = tl.replace('Ü', 'U')

    titulo = re.sub(r'[^a-zA-Z0-9]', ' ', tl) 
    titulo = titulo.replace('      ', ' ')
    titulo = titulo.replace('     ', ' ')
    titulo = titulo.replace('    ', ' ')
    titulo = titulo.replace('   ', ' ')
    titulo = titulo.replace('  ', ' ')

    ntl = titulo
    
    if mode == 1:
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

def get_eps(id, atual, cursor = None, offset = 0, stat = None, air_status = None):
    prt('\n')

    load_ep = load('carregando episodios')

    lista_eps_menu = list()
    lista_eps_menu.append('VOLTAR\n')
    lista_eps_menu.append('PAGINA ANTERIOR')
    lista_eps_menu.append('PROXIMA PAGINA\n')

    atual = int(atual)+2

    offset = (int(atual/25) * 25) + (offset * 25)
    if offset < 0: offset = 0

    link = f'https://myanimelist.net/anime/{id}/blablabla/episode?offset={offset}'
    sopa = sopapranois(link)

    tx = 'class="episode-number nowrap"'
    #sopa = sopa[sopa.find(tx) + len(tx) : ]

    ep_num = offset
    while len(lista_eps_menu) < 28:
        
        if sopa.find(tx) == -1: break
        sopa = sopa[sopa.find(tx) + len(tx) : ]
        
        load_ep.add()

        ep_num = int(texto_no_meio(sopa, '">', '</td>'))
        ep_name = texto_no_meio(sopa, f'/episode/{ep_num}">', '</a>')
        lista_eps_menu.append(f'{ep_num} - {ep_name}')
        

    while len(lista_eps_menu) < 28:

        ep_num+=1
        lista_eps_menu.append(ep_num)

        load_ep.add()



    menu_eps = menu(lista_eps_menu, 2)
    if cursor != None:
        menu_eps.cursor = cursor
    else: menu_eps.cursor = atual-offset+1


    apagar_linhas(1)

    while True:

        menu_eps.update()
        menu_eps.input()

        ep = offset + menu_eps.cursor - 2

        if tecla == 'Key.enter':

            if menu_eps.cursor == 0: return False

            elif menu_eps.cursor == 1:
                if offset > 0:
                    return get_eps(id, atual, menu_eps.cursor, -1)
                

            elif menu_eps.cursor == 2:
                return get_eps(id, atual, menu_eps.cursor, +1)

            else: 
                play_ep(id, ep, stat, air_status)
                return

            

    
    


    #prt(f'\n\n{ep_num} - {ep_name}\n')

def find_all(string, flag):
    
    return [x.start() for x in re.finditer(flag, string)]











#classes

class menu():
    def __init__(self, lista_opts, n_linhas = 0, uma_opt = None, offset = 0):
        self.cursor = 0
        self.opt_list = lista_opts
        self.n_linhas = n_linhas
        self.uma_opt = uma_opt
        self.offset = offset
        self.n_printed = 1 + self.n_linhas

        select = list()
        for item in lista_opts:
            if type(item) == tuple or type(item) == list:
                if uma_opt == True:
                    select.append(-1)
                else:
                    select.append(0)

        self.select = select
        self.ciclos = 0

        prt('\a')

    def update(self):

        #if self.ciclos > 0:
        #    prt('\033[10A \033[J')

        correcao = False

        mtp = 7

        opt_list = self.opt_list 

        n = 15
        for i in range(0, len(opt_list)):

            if len(opt_list) > (n+1)*2:
                if i > self.cursor + n and i > (n+1)*2: 
                    break
                if i < self.cursor - n - 2 and i < len(opt_list) - (n+1)*2 -1:
                    correcao = True
                    continue            

            item = opt_list[i]

            tipo = type(item)

            if self.cursor == i: cor = colorama.Fore.BLUE
            else: cor = colorama.Fore.WHITE

            if tipo == tuple or tipo == list:

                prt(f'\n{cor}{item[0]}\t', True)

                for baboey in range(0, int(1/len(item[0])*mtp)):
                    #prt(int(1/len(item[0])*mtp))
                    prt('\t', True)

                for i2 in range(0, len(item[1])):

                    item2 = item[1][i2]

                    if self.select[i - self.offset] == i2: cor = colorama.Fore.BLUE
                    else: cor = colorama.Fore.WHITE

                    if len(item2) < 6: espaco = '\t\t'
                    else: espaco = '\t'


                    prt(f'{cor}|{item2}{espaco}', True)

            else:
                prt(f'\n{cor}{item}', True)

            prt(colorama.Fore.RESET)

            self.n_printed += 1
            
        prt('\n')
        if correcao: prt('\n')

    def input(self):

        self.ciclos += 1
        direct = False

        cursor = self.cursor
        select = list(self.select)
        opt_list = self.opt_list 

        with pynput.keyboard.Listener(on_press=key_press) as Listener:
            Listener.join()

        if tecla == 'Key.down': cursor += 1 
        elif tecla == 'Key.up': cursor -= 1

        if cursor > len(opt_list)-1: cursor = 0
        if cursor < 0: cursor = len(opt_list)-1

        if cursor < len(select):
            val = cursor - self.offset
            if tecla == 'Key.right':
                select[val] += 1
                if len(opt_list[val][1]) == 2: select[val] += 1
                if select[val] > len(opt_list[val][1])-1: select[val] = len(opt_list[val][1])-1
                else: direct = True
            if tecla == 'Key.left':
                select[val] -= 1
                if select[val] < -1: direct = True
                if select[val] < 0: select[val] = 0
                else: direct = True
            
            

        

        
        if self.uma_opt == True and direct:
            change_found = False
            for n in range(0, len(select)):
            
                if select[n] != self.select[n] and not change_found:
                    self.select[n] = select[n]
                    change_found = True
                else:
                    self.select[n] = -1
        else: self.select = select

        self.cursor = cursor

        apagar_linhas(self.n_printed)
        self.n_printed = 1 + self.n_linhas

class provedores():

    def __init__(self, lista):

        prt('\n\n', True)

        self.id = lista[0]
        self.ep = lista[1]
        self.titulo = lista[2]
        self.ep_link = False
        self.quero_dublado = 0
        self.yt_link = None
        self.linhas_apagar = 0

        subs_list = [
            (7791, 'k-on 2'),
        ]

        for item in subs_list:
            if item[0] == int(self.id):
                self.titulo = item[1]

        provs = (self.animesdigitalorg, self.q1n, self.animefire, self.animesonlinecc, self.animesgames, self.goyabu)
        if debug: provs = [self.q1n,]

        yt_list = [[11795, [[1, 'https://www.youtube.com/watch?v=dRBP1rpE5y8&t=1s']]], 
                    [58507, [[1, 'https://youtu.be/sHGcGkaYd38']]], 
                    [8939, [[1, 'https://youtu.be/GlxrJVdNyro']]],
                    [56213, [[1, 'https://www.youtube.com/watch?v=2zcZbIN3VPE'],
                            [2, 'https://www.youtube.com/watch?v=3VRuAhF1gLY'],
                            [3, 'https://www.youtube.com/watch?v=5n6K33W442w'],
                            [4, 'https://www.youtube.com/watch?v=Gv_lwgPAQsQ']]],
                    [30059, [[1, 'https://www.youtube.com/watch?v=mzGU_iUMBi8']]],]

        for i in yt_list:

            if int(i[0]) == int(self.id):

                for i2 in i[1]:

                    if i2[0] == int(self.ep):

                        self.yt_link = i2[1]
                        
                        break
                break
        if self.yt_link != None:
            provs = (self.youtube,) + provs

        if usnm.lower() == 'gahvius':

            dub_plis = (
                'one piece', 
                'dragon ball', 
                'one punch man', 
                'yu yu hakusho', 
                'Yuu Yuu Hakusho',
                'Yuu☆Yuu☆Hakusho',
                'saint seiya',
                'naruto',
                'sailor moon',
                'InuYasha',
                'gokudolls',)

            self.quero_dublado = -1

            for item in dub_plis:

                if self.titulo.lower().find(item.lower()) != -1:
                    self.quero_dublado = 2
                    break

        for prov in provs:

            time.sleep(1)
            apagar_linhas(self.linhas_apagar)
            self.linhas_apagar = 0
            prov()

            if self.ep_link != False: 
                break

    def escolher_dub(self):
        prt('\n\nepisodio dublado encontrado!\nreproduzir?\n')
        escolha = menu(('SIM', 'NAO'))

        while True:
            
            escolha.update()
            escolha.input()

            if tecla == 'Key.enter':
                break
        
        apagar_linhas(3)
        prt('\033[1A')
        
        if escolha.cursor == 0: self.quero_dublado = 1
        elif escolha.cursor == 1: self.quero_dublado = -1

    def animesdigitalorg(self):

        prt('provedor: animesdigital.org')

        temp_links = list()


        # nomes especificos
        for bababoey in (1,):

            ova_list = (
                'Fullmetal Alchemist: Brotherhood Specials'
            )

            substituir = (
                ('Bishoujo Senshi Sailor Moon', 'sailor moon'),
            )

            substituir2 = (
                ('ranma-2024', 'ranma-½-2024'),
            )

            id_tl_list = (
                (59095, 'Tensei shitara Dainana Ouji 2'),
                (58567, 'solo leveling ii'),
                (5114, 'fullmetal-abb001'),
                (392, 'Yu Yu Hakusho'),
                (61322,'dr stone science future 2'),
                (1254, 'os cavaleiros do zodiaco'),
            )


            tl = self.titulo
            for item in id_tl_list:
                if int(self.id) == item[0]: 
                    tl = item[1]
                    break


            if tl in ova_list: ova = True



            for item in substituir:
                tl = tl.lower().replace(item[0].lower(), item[1].lower())

            tl = processtl(tl)

            for item in substituir2:
                tl = tl.lower().replace(item[0].lower(), item[1].lower())


        titulo = tl

        if self.ep < 10:
            str_ep = f'0{str(self.ep)}'
        else: str_ep = str(self.ep)








        sub_link = f'https://animesdigital.org/anime/a/{titulo}'
        dub_link = sub_link + '-dublado'
        
        

        temp_links.append(dub_link)
        temp_links.append(sub_link)


        link_list = list(temp_links)


        for link in link_list:

            if link == sub_link: versao = 'legendado'
            if link == dub_link: versao = 'dublado'

            sopa = sopapranois(link)

            if sopa.find('<div class="msg404">') != -1:
                prt(f'\nanime {versao} não encontrado!')
                self.linhas_apagar += 1
                continue

            tl_in_sopa = texto_no_meio(sopa, '<title>', '</title>')
            if tl_in_sopa.find('Dublado') != -1: versao = 'dublado'
            
            ep_topo = texto_no_meio(sopa, '<div class="title_anime">', '</div>', prsv_final=True)
            ep_topo = texto_no_meio(ep_topo, 'Episódio ', '</div>')
            
            try:
                ep_topo = int(ep_topo)

                if ep_topo < self.ep:
                    prt(f'\nepisodio {versao} não encontrado!')
                    self.linhas_apagar += 1
                    continue

            except:
                prt(f'\n falha ao buscar episodio {versao}!')
                self.linhas_apagar += 1
                continue
                
            if sopa != False:

                if sopa.find(f'Episódio {str_ep}</div>') == -1:

                    ep_topo = texto_no_meio(sopa, '<div class="title_anime">', '</div>', prsv_final=True)
                    ep_topo = texto_no_meio(ep_topo, 'Episódio ', '</div>')

                    page = int((int(ep_topo) - self.ep)/50)+1

                    link = f'{link}/page/{page}/'
                    sopa = sopapranois(link)

                sopa = sopa[:sopa.find(f'Episódio {str_ep}</div>')]
                sopa = sopa[sopa.rfind('https://animesdigital.org/video/a/'):]
                link = sopa[:sopa.find('"')]

                sopa = sopapranois(link)
                if sopa == False:
                    prt(f'\nfalha ao reproduzir episodio!')
                    self.linhas_apagar += 1
                else:
                    link = texto_no_meio(sopa, 'https://api.anivideo.net/', '"', prsv_começo=True)
                    link = texto_no_meio(link, 'https://cdn-', '&amp;nocache', True)

                    if link != False:

                        if self.quero_dublado > 1:
                            if versao != 'dublado': continue
                        if self.quero_dublado < 0:
                            if versao != 'legendado': continue

                        if versao == 'dublado':
                            if self.quero_dublado == 0: self.escolher_dub()
                            
                        if versao == 'legendado' or self.quero_dublado > 0:
                            self.ep_link = link

                            prt(f'\nreproduzindo episodio {versao}...')
                            self.linhas_apagar += 1
                            
                            return

    def animefire(self):

        prt('provedor: animefire.plus')

        temp_links = list()
        sd_perm = False


        # nomes especificos
        for bababoey in (1,):

            substituir = (
                ('Ü', 'ue'),
                ('Takkyuu-bu', 'takkyuubu'),
                ('½', '1/2'),
                ('daidaidaidaidaisuki', 'dai-dai-dai-dai-daisuki'),
                ('nd season', ''),
                ('rd season', ''),
                ('th season', ''),
            )

            tl = self.titulo

            for item in substituir:
                tl = tl.lower().replace(item[0].lower(), item[1].lower())             

            tl = processtl(tl)

            sd_list = (
                'ike-ina-chuu-takkyuubu',
                'serial-experiments-lain',
                'yuu-yuu-hakusho'
            )

            if tl in sd_list: sd_perm = True


        sub_link = f'https://animefire.plus/animes/{tl}-todos-os-episodios'
        dub_link = f'https://animefire.plus/animes/{tl}-dublado-todos-os-episodios'

        temp_links.append(dub_link)
        temp_links.append(sub_link)

        #print(f'\n{link_list}'), exit()

        for link in temp_links:

            if link == dub_link: versao = 'dublado'
            elif link == sub_link: versao = 'legendado'
            
            sopa = sopapranois(link)

            if sopa == '':
                prt(f'\nanime {versao} não encontrado!')
                self.linhas_apagar += 1
            else:

                if versao == 'dublado': link = f'https://animefire.plus/video/{tl}-dublado/{self.ep}'
                else: link = f'https://animefire.plus/video/{tl}/{self.ep}'

                if self.ep_existe(link, versao, '"status":"500"'):

                    if self.quero_dublado > 1:
                        if versao != 'dublado': continue
                    if self.quero_dublado < 0:
                        if versao != 'legendado': continue

                    sd_src = False
                    hd_src = False
                    fhd_src = False

                    sopa = sopapranois(link)

                    sources = texto_no_meio(sopa, '"data":[', ']')
                    sources = sources.replace('\\', '')

                    while True:

                        if sources.find('"src":') == -1: break

                        src = texto_no_meio(sources, '"src":"', '"')

                        if src.find('/sd/') != -1: sd_src = src
                        elif src.find('/hd/') != -1: hd_src = src
                        elif src.find('/fhd/') != -1: fhd_src = src

                        sources = sources[ sources.find('}')+1 : ]

                        
                    src_list = [fhd_src, hd_src, sd_src]

                    for link in src_list:

                        if link != False:

                            if link != sd_src or sd_perm:

                                if versao == 'dublado':
                                    if self.quero_dublado == 0: self.escolher_dub()
                                    
                                if versao == 'legendado' or self.quero_dublado > 0:

                                    self.ep_link = link

                                    prt(f'\nreproduzindo episodio {versao}...')
                                    self.linhas_apagar += 1
                                    return
                                

                    prt(f'\nfalha ao reproduzir episodio {versao}!')
                    self.linhas_apagar += 1
                    continue

                else: continue

    def goyabu(self):

        prt('provedor: goyabu.to')

        substituir = (
            ('Tensei shitara Dainana Ouji Datta node, Kimama ni Majutsu wo Kiwamemasu', 'tensei shitara dainana ouji'),
            ('season 2', '2'),
            ('2nd season', '2'),
            ('part 2', '2'),
        )

        tl = self.titulo

        for item in substituir:
            tl = tl.lower().replace(item[0].lower(), item[1].lower())

        id_tl_list = (
            (530, 'sailor moon'),
        )

        for item in id_tl_list:
            if int(self.id) == item[0]: 
                tl = item[1]
                break
        

        tl = processtl(tl)

        sub_link = f'https://goyabu.to/anime/{tl}'
        dub_link = f'{sub_link}-dublado'

        links = list()
        links.append(dub_link)
        links.append(sub_link)

        for link in links:

            if link == dub_link: versao = 'dublado'
            elif link == sub_link: versao = 'legendado'

            sopa = sopapranois(link)

            if sopa.find('<title>404 Not Found</title>') != -1:
                prt(f'\nanime {versao} não encontrado!')
                self.linhas_apagar += 1
            else:
                if sopa.find(f'id="ep {self.ep}"') == -1:
                    prt(f'\nepisodio {versao} não encontrado!')
                    self.linhas_apagar += 1
                else:

                    if self.quero_dublado > 1:
                        if versao != 'dublado': continue
                    if self.quero_dublado < 0:
                        if versao != 'legendado': continue

                    if versao == 'dublado':
                        if self.quero_dublado == 0: self.escolher_dub()
                        if self.quero_dublado < 0: continue
                    
                    chunk = sopa[ : sopa.rfind(f'id="ep {self.ep}"')]
                    num = chunk.rfind('<li>')
                    link = sopa[num:num+200]
                    link = texto_no_meio(link, 'href="', '"')

                    sopa = sopapranois(link)

                    link = texto_no_meio(sopa, 'https://www.blogger.com/video', '"', True)

                    if sopapranois(link).find('"errorContainer"') != -1:
                        prt(f'\nfalha ao reproduzir episodio {versao}!')
                        self.linhas_apagar += 1
                        continue

                    prt(f'\nreproduzindo episodio {versao}...')
                    self.linhas_apagar += 1

                    self.ep_link = link

                    return

    def youtube(self):

        prt('provedor: youtube.com')

        prt('\nreproduzindo episodio...')
        self.linhas_apagar += 1

        self.ep_link = self.yt_link

    def q1n(self):
        
        prt('provedor: q1n.net')

        tl = self.titulo

        tl = processtl(tl)

        sub_link = f'https://q1n.net/animes/{tl}'
        dub_link = f'{sub_link}-dublado'

        links = [
            [dub_link, 'dublado'],
            [sub_link, 'legendado'],
        ]

        for item in links:

            link = item[0]
            versao = item[1]

            sopa = sopapranois(link)

            if sopa.find('class="error404') != -1:
                prt(f'\nanime {versao} não encontrado!')
                self.linhas_apagar += 1
                continue

            if texto_no_meio(sopa, '<div class="data"', '</h1>').find('Dublado') != -1: versao = 'dublado'

            link = link.replace('/animes/', '/episodio/') + f'-episodio-{self.ep}'
            ep_link = link
            sopa = sopapranois(link)

            if sopa.find('class="error404') != -1:
                prt(f'\nepisodio {versao} não encontrado!')
                self.linhas_apagar += 1
                continue

            trns_sopa = texto_no_meio(sopa, 'playcontainer', '<span id="playernotice"')

            trns_links = []

            ignore_list = (
                '/off/',
                'disneycdn.net',
                'filemoon.sx',
                'vgembed.com',
                'mixdrop.ag',
                'rogeriobetin.com',
                '/jwplayer/',
                'upns.ink',
                'short.icu',
            )

            red_flags = (
                'File is no longer available',
                'Video not found!',
                'This content is no longer available.',
            )

            while True:

                ignorar = False

                if trns_sopa.find('speed-src="') == -1: break

                trns = texto_no_meio(trns_sopa, 'speed-src="', '"')
                og_trns = trns

                for item in ignore_list:
                    if trns.find(item) != -1: 
                        ignorar = True
                        break
                if ignorar:
                    trns_sopa = trns_sopa[ trns_sopa.find(og_trns) : ]
                    continue

                if trns.find('?url=') != -1:
                    trns = trns[ trns.find('?url=')+5 : ]
                    trns = trns.replace('%2F', '/')
                    trns = trns.replace('%3A', ':')
                    trns = trns.replace('%3F', '?')
                    trns = trns.replace('%3D', '=')
                    trns = trns.replace('%23', '#')

                #file_sopa = sopapranois(trns)

                for item in red_flags:
                    break
                    if file_sopa.find(item) != -1: 
                        ignorar = True
                        break
                if ignorar:
                    trns_sopa = trns_sopa[ trns_sopa.find(og_trns) : ]
                    continue

                trns_links.append(trns)

                trns_sopa = trns_sopa[ trns_sopa.find(og_trns) : ]

            if len(trns_links) > 0:

                if self.quero_dublado > 1:
                    if versao != 'dublado': continue
                if self.quero_dublado < 0:
                    if versao != 'legendado': continue

                if versao == 'dublado':
                    if self.quero_dublado == 0: self.escolher_dub()
                    if self.quero_dublado < 0: continue

                for link in trns_links:
                    
                    if link.find('/csst.online/') != -1:
                        if debug: continue
                        for q in ('4k', 1080, 720):

                            file_sopa = sopapranois(link)
                            file_sopa = file_sopa[ file_sopa.find('var player') : ]

                            file = texto_no_meio(file_sopa, f'[{q}p]', '.mp4', prsv_final=True)

                            if file != False:

                                prt(f'\nreproduzindo episodio {versao}...')
                                self.linhas_apagar += 1

                                self.ep_link = file

                                return
                    elif link.find('https://cdn-')!= -1:
                        if debug: continue
                        file = texto_no_meio(link, 'https://cdn-', '.m3u8', True, True)

                        if file != False:

                            prt(f'\nreproduzindo episodio {versao}...')
                            self.linhas_apagar += 1

                            self.ep_link = file

                            return
                    elif link.find('blogger.com')!= -1:
                        if debug: continue
                        file = link[ : link.find('&amp')]
                        if sopapranois(file).find('"errorContainer"') != -1: continue

                        prt(f'\nreproduzindo episodio {versao}...')
                        self.linhas_apagar += 1

                        self.ep_link = file

                        return
                    elif link.find('/antivirus3/')!= -1:
                        if not debug: continue
                        file = texto_no_meio(sopapranois(link), '"file": "', '?')

                        if file != False:

                            file_sopa = sopapranois(file)
                            deuruim = False
                            for item in red_flags:
                                if file_sopa.find(item) != -1:
                                    deuruim = True
                            if deuruim: continue

                            prt(f'\nreproduzindo episodio {versao}...')
                            self.linhas_apagar += 1

                            self.ep_link = file

                            return
                    elif link.find('streamtape.com')!= -1:

                        if not debug: continue

                        file_sopa = sopapranois(link)
                        deuruim = False
                        for item in red_flags:
                            if file_sopa.find(item) != -1:
                                deuruim = True
                        if deuruim: continue

                        exit()
                    elif link.find('embedwish.com')!= -1:

                        if not debug: continue


                        file = link[ : link.find('?')]
                        file_sopa = sopapranois(file)
                        deuruim = False
                        for item in red_flags:
                            if file_sopa.find(item) != -1:
                                deuruim = True
                        if deuruim: continue

                        exit()

                    else:
                        if debug:
                            print('\n')
                            print(link)
                            exit()
                        elif devmode: webbrowser.open(f'view-source:{link}')

            prt(f'\nfalha ao reproduzir episodio {versao}!')
            self.linhas_apagar += 1
            
    def anime_existe(self, link, versao, n_flag):

        sopa = sopapranois(link)

        if sopa.find(n_flag) != -1:
            prt(f'\nanime {versao} não encontrado!')
            self.linhas_apagar += 1
            return False
        else: return True

    def ep_existe(self, link, versao, n_flag):

        sopa = sopapranois(link)

        if sopa.find(n_flag) != -1:
            prt(f'\nepisodio {versao} não encontrado!')
            self.linhas_apagar += 1
            return False
        else: return True

    def animesonlinecc(self):

        prt('provedor: animesonlinecc.to')

        tl = self.titulo
        # nomes especificos
        for bababoey in (1,):
            substituir = (
                (' season ', ' '),
            )
            for item in substituir:
                tl = tl.lower().replace(item[0], item[1])
        
            id_tl_list = (
                (530, 'sailor moon'),
            )

            for item in id_tl_list:
                if int(self.id) == item[0]: 
                    tl = item[1]
                    break
        
        tl = processtl(tl)

        link = f'https://animesonlinecc.to/episodio/{tl}-episodio-1/'

        if sopapranois(link).find('content="Página não encontrada') != -1:
            prt('\nanime não encontrado!')
            self.linhas_apagar += 1
        else:
            link = f'https://animesonlinecc.to/episodio/{tl}-episodio-{self.ep}/'

            if sopapranois(link).find('content="Página não encontrada') == -1:

                sopa = sopapranois(link)

                opts = texto_no_meio(sopa, '<ul class="options">', '</ul>')

                opt_list = list()
                while True:

                    if opts.find('<a class="options"') == -1: break

                    opt_list.append(texto_no_meio(opts, '</b> ', ' </a>').lower())

                    opts = opts[ opts.find('</li>')+5 : ]

                prioridade = ['dublado', 'fhd', 'fullhd', 'hd', 'legendado']
                if self.quero_dublado > 1: prioridade = ['dublado',] 

                if usnm.lower() == 'gahvius':
                    for item in opt_list:
                        if item not in prioridade:
                            print(f'\n\n{item}\n\n'), exit()

                for item in prioridade:
                    if item not in opt_list:
                        prioridade.remove(item)

                if len(prioridade) > 0:

                    if 'dublado' in prioridade:
                        if self.quero_dublado == 0: self.escolher_dub()
                        if self.quero_dublado < 0: prioridade.remove('dublado')

                    for i in prioridade:
                        n=0
                        for i2 in opt_list:
                            n+=1
                            if i2 == i:
                
                                link = texto_no_meio(sopa, f'id="option-{n}">', '</div>')
                                link = texto_no_meio(link, 'src="', '"')

                                if link == False: continue

                                if link.find('.blogger.com') != -1:
                                    if sopapranois(link).find('"errorContainer"') != -1: 
                                        continue

                                if link.find('.blogger.com') == -1 and link.find('.wixstatic.') == -1:
                                    if usnm.lower() == 'gahvius':
                                        print(f'\n\n{link}\n\n'), exit() 
                                    continue

                                prt(f'\nreproduzindo episodio {i}...')
                                self.linhas_apagar += 1

                                self.ep_link = link
                                return


                prt(f'\nfalha ao reproduzir episodio!')
                self.linhas_apagar += 1
                
            else: 

                prt('\nepisodio não encontrado!')
                self.linhas_apagar += 1

    def animesbr(self):
        prt('provedor: animesbr.tv')
        self.linhas_apagar += 1

        tl = self.titulo
        tl = processtl(tl)

        link = f'https://animesbr.tv/animes/{tl}/'
        sopa = sopapranois(link)

        if sopa.find('class="error404') == -1:

            link = f'https://animesbr.tv/episodios/{tl}-episodio-{self.ep}/'
            sopa = sopapranois(link)

            if sopa.find('class="error404') == -1:

                opts = texto_no_meio(sopa, 'id="playeroptions', '</div>', True, True)

                print(f'\n\n{opts}\n\n')
                exit()




           
           
            prt('\nepisodio não encontrado!')
            self.linhas_apagar += 1
            return

        prt('\nanime não encontrado!')
        self.linhas_apagar += 1
        return

    def gdrive(self):
        
        return
        prt('provedor: GDrive')

        link = 'https://drive.google.com/drive/u/0/folders/1OMlwFLqTlwn6kjVAuCqB7katIxxyt0_4'
        sopa = sopapranois(link)

        if sopa.find(self.titulo) == -1:
            prt('\nanime não encontrado!')
            self.linhas_apagar += 1
            return
        else:            

            sopa = sopa[: sopa.find(self.titulo)+len(self.titulo)]
            sopa = sopa[find_all(sopa, ',')[-40] :]

            folder_id = texto_no_meio(sopa, '"', '"')

            link = f'https://drive.google.com/drive/folders/{folder_id}?usp=drive_link'
            sopa = sopapranois(link)

            

            print(f'\n{sopa.find('1X0PCv72dsBXdADTe0EKt-Gigk-demS3O')}\n{sopa.find('01.mp4')}'), exit()

    def animesgames(self):

        prt('provedor: animesgames.cc')

        tl = self.titulo

        id_tl_list = (
            (530, 'sailor moon'),
        )

        for item in id_tl_list:
            if int(self.id) == item[0]: 
                tl = item[1]
                break

        tl = processtl(tl)

        links = (
            (f'https://animesgames.cc/animes/{tl}-dublado-todos-os-episodios', 'dublado'),
            (f'https://animesgames.cc/animes/{tl}-todos-os-episodios', 'legendado'),
        )

        for item in links:

            link = item[0]
            versao = item[1]

            sopa = sopapranois(link)

            if texto_no_meio(sopa, '<title>', '</title>').find('Dublado') != -1: versao = 'dublado'

            if sopa.find('<title>Nada Encontrado') != -1:
                prt(f'\nanime {versao} não encontrado!')
                self.linhas_apagar += 1
                continue

            if sopa.find(f'dio {self.ep}</h3>') == -1:
                prt(f'\nepisodio {versao} não encontrado!')
                self.linhas_apagar += 1
                continue

            link = sopa[ : sopa.rfind(f'dio {self.ep}</h3>') ]
            link = link[link.rfind('https://animesgames.cc/video/') : ]
            link = link[ : link.find('">')]
            eplink = link

            sopa = sopapranois(link)

            link = sopa[ : sopa.find('"video_src"')]
            link = link[link.rfind('<link') : ]
            link = texto_no_meio(link, '"', '"')

            if link.find('.blogspot.com') != -1:

                sopa = sopapranois(link)

                link = texto_no_meio(sopa, 'https://www.blogger.com/video', '"', True)

                if sopapranois(link).find('"errorContainer"') != -1:
                    prt(f'\nfalha ao reproduzir episodio {versao}!')
                    self.linhas_apagar += 1

                if versao == 'dublado':
                    if self.quero_dublado == 0: self.escolher_dub()
                    if self.quero_dublado < 0: continue

                if self.quero_dublado > 1:
                    if versao != 'dublado': continue
                if self.quero_dublado < 0:
                    if versao != 'legendado': continue

                prt(f'\nreproduzindo episodio {versao}...')
                self.linhas_apagar += 1

                self.ep_link = link

                return
            else:
                if devmode:
                    if link.find('ns565646.ip') == -1:
                        webbrowser.open(eplink)

            prt(f'\nfalha ao reproduzir episodio {versao}!')
            self.linhas_apagar += 1
                
    def animeson000010(self):

        prt('provedor: animeson000010.blogspot.com')
        self.linhas_apagar += 1

        tl = self.titulo

        id_tl_list = (
            (530, 'sailor moon'),
        )

        for item in id_tl_list:
            if int(self.id) == item[0]: 
                tl = item[1]
                break

        tl = processtl(tl)

    def animesorion(self):

        prt('provedor: animesorionvip.net')

        tl = self.titulo

        id_tl_list = (
            (530, 'sailor moon'),
        )

        for item in id_tl_list:
            if int(self.id) == item[0]: 
                tl = item[1]
                break

        tl = processtl(tl)

        links = [
            [f'https://animesorionvip.net/animes/{tl}-dublado-todos-os-episodios', 'dublado'],
            [f'https://animesorionvip.net/animes/{tl}-todos-os-episodios', 'legendado'],
        ]

        for item in links:

            link = item[0]
            versao = item[1]

            sopa = sopapranois(link)

            if sopa.find('<title>') == -1:
                prt(f'\nanime {versao} não encontrado!')
                self.linhas_apagar += 1
                continue
        
            if texto_no_meio(sopa, '<title>', '</title>').find('Dublado') != -1: versao = 'dublado'
            #if versao != 'dublado' and self.quero_dublado > 1: continue

            if sopa.find(f'dio {self.ep}" href="') == -1:
                prt(f'\nepisodio {versao} não encontrado!')
                self.linhas_apagar += 1
                continue

            link = texto_no_meio(sopa, f'dio {self.ep}" href="', '"')
            sopa = sopapranois(link)

            link = texto_no_meio(sopa, 'data-video="', '"')
            sopa = sopapranois(link)

            print('\n')
            print(sopa)
            exit()

class load():

    def __init__(self, linha):

        self.pontos = 0
        self.linha = linha
        prt(self.linha)

    def add(self):

        self.pontos += 1
        if self.pontos > 3:
            self.pontos = 0
            prt('\r\033[J', True)
            prt(self.linha) 
        else:
            prt('.')







#imports
import requests
import colorama
import subprocess
import sys
import pynput
import bs4
import os
import time
import re
import webbrowser



#init
for bababoey in (1,):

    os.makedirs(f'{os.path.expanduser("~")}/otapy/', exist_ok=True)

    debug = False
    devmode = False
    player_off = True

    

    colorama.init()
    tecla = None

    
    if debug: usnm = 'gahvius'
    else: usnm = getusername()
    if usnm.lower() == 'gahvius': devmode = True

    if not devmode:
        debug = False
        player_off = False

    run = True

    playerlist = ('mpv', '"H:/programas/mpv/mpv.exe"', 'vlc', '"C:/Program Files/VideoLAN/VLC/vlc.exe"')    



#listas 
for bababoey in (1,):

    opt_lista = (
        ('LISTA', ('todos', 'assistindo', 'completos', 'em espera', 'dropados', 'planejo assistir', 'lançamentos')), 
        ('STATUS', ('todos', 'em lançamento', 'terminados', 'não lançados')), 
        'ORDEM 1',
        'ORDEM 2', 
        '\nREPRODUZIR LISTA', 
        'ABRIR LISTA', 
        '\nSAIR' 
    )

    ordem_opt_list = (
        'TITLE',
        'END DATE',
        'START DATE',
        'SCORE',
        'LAST UPDATED',
        'TYPE',
        
        'RATING',
        'REWATCH VALUE',
        
        'PRIORITY',
        'WATCHED EPS',
        'STATUS',
        'AIR START DATE',
        'STORAGE',
        'STATUS',
        'MAL SCORE',
        'SCORE DIFF.',
        'POPULARITY'
    )

    outra_lista = list()
    outra_lista.append('VOLTAR\n')
    for item in ordem_opt_list:
        outra_lista.append((item, ('Asc', 'Desc')))
    ordem_opt_list = outra_lista

    indisponiveis = (
        17387, 23189, 23187, 10742, 23191,
        23181, 1254, 523, 530, 2465, 2154,
        30, 268, 650, 1462, 31, 1575, 1689,
        32, 437, 245, 1593, 659, 2759, 8626,
        53047, 908, 849, 1210, 2904, 5177,
        5667, 5667, 7017, 6421, 7902, 6862,
        6956, 7593, 7785, 9203, 8408, 8795,
        9062, 10067, 8857, 9289, 10119, 9515,
        10805, 10521, 11491, 11285, 11499,
        13055, 13161, 13469, 13093, 12729,
        14227, 14199, 13759, 16001, 14189,
        16694, 15775, 16417, 24181, 17397,
        16397, 16934, 16592, 17074, 20159,
        19221, 18397, 20021, 18139, 20931,
        20767, 35773, 20899, 21863, 24475, 
        21881, 24227, 28149, 27899, 23199, 
        31181, 31621, 33142, 31952, 33094, 
        34102, 35823, 35466, 36456, 37991,
        35868, 39652, 38680, 56949, 40513,
        39710, 40052, 47904, 44942, 48548,
        52015, 51773, 49834, 49835, 52198,
        53850, 53851, 50587, 54959, 57603,
        55813, 55357, 59493, 53747, 54857,
        59571, 59419, 54740, 61160, 60534,
        55514, 59833, 53512, 60326,
    )




#classes de menu
for bababoey in (1,):
    menu1 = menu(opt_lista, 2)
    menu_ordem1 = menu(ordem_opt_list, 1, True, 1)
    menu_ordem2 = menu(ordem_opt_list, 1, True, 1)
    

    lista_menus = list((menu1, menu_ordem1, menu_ordem2))

    filename = f'{os.path.expanduser("~")}/otapy/LastList'

    try:
        with open(filename, 'r') as f:
            data = list(f.readlines())
            f.close()

        for i in range(0, len(lista_menus)):
            for i2 in range(0, len(lista_menus[i].select)):
                lista_menus[i].select[i2] = int(data[i][i2])-1



    except:
        with open(filename, 'w') as f:
            f.write('')
            f.close()



#this is where the fun begins
while run:

    if not run: break

    menu1.update()
    menu1.input()



    #montando o link da lista
    for bababoey in (1,):
        if menu1.select[0] == 0: status = 7
        elif menu1.select[0] == 5: status = 6
        else: status = menu1.select[0]

        if menu1.select[1] == 0: air_status = ''
        else: air_status = f'airing_status={menu1.select[1]}&'

        ordens = list()
        for lista in (menu_ordem1.select, menu_ordem2.select):
            for n in range(0, len(lista)):
                if lista[n] > -1:
                    num = n+1
                    
                    if num > 6: num+=1
                    if num > 9: num+=1

                    if num > 10: num *= -1

                    if lista[n] == 1: num = num*-1
                    ordens.append(num)
                    break

        if len(ordens) > 0: ordem1 = f'order={ordens[0]}&'
        else: ordem1 = ''
        
        if len(ordens) > 1: ordem2 = f'order2={ordens[1]}&'
        else: ordem2 = ''

        lista_link = f'https://myanimelist.net/animelist/{usnm}?{air_status}{ordem1}{ordem2}status={status}'




    if tecla == 'Key.enter':

        data = list()
        data2 = list()



        for item in lista_menus:
            data.append(item.select)

        for i in data:
            linha = ''
            for i2 in i:
                linha += str(i2+1)
            data2.append(linha+'\n')

        with open(filename, 'w') as f:
            f.writelines(data2)
            f.close()




        if menu1.cursor == len(menu1.opt_list)-1:
            run = False
            quit()
            exit()
            break

        elif menu1.cursor == 2:
            while True:

                menu_ordem1.update()
                menu_ordem1.input()
                
                if tecla == 'Key.enter':
                    if menu_ordem1.cursor == 0:
                        break

        elif menu1.cursor == 3:
            while True:

                menu_ordem2.update()
                menu_ordem2.input()
                
                if tecla == 'Key.enter':
                    if menu_ordem2.cursor == 0:
                        break

        elif menu1.cursor == 4 or menu1.cursor == 5:

            prt('\n')
            load_lista = load('carregando lista')


            lista_proc = list()
            t1 = False
            t2 = False

            

            if menu1.select[0] == 6:
                link1 = 'https://myanimelist.net/anime/season'
                link2 = f'https://myanimelist.net/animelist/{usnm}?airing_status=1'

                sopa = sopapranois(link1, load=load_lista)
                sopa_list = sopapranois(link2, load=load_lista)

                sopa_list = texto_no_meio(sopa_list, '<table class="list-table"', '<tr class="list-table-header">')

                tx = '<div class="title">'

                skip_list = (
                    'season',
                    'part',
                )

                load_lista.linha = 'coletando IDs'
                while True:
                    
                    if sopa.find(tx) == -1: break
                    sopa = sopa[ sopa.find(tx)+len(tx) : ]

                    load_lista.add()
                    
                    if texto_no_meio(sopa, '<div class="genres js-genre"', '</div>').find('/anime/genre/12/') != -1: continue

                    sinop = texto_no_meio(sopa, '<p class="preline">', '</p')
                    if texto_no_meio(sinop, ' ', ' ') in skip_list: continue
                    if sinop[ : sinop.find(' ')] == 'Sequel': continue

                    titulo = texto_no_meio(sopa, '', '</a>')

                    if titulo[ find_all(titulo, ' ')[-2] : find_all(titulo, ' ')[-1] ][1:].lower() in skip_list: continue
                    if titulo[find_all(titulo, ' ')[-1] :][1:].lower() == 'season': continue

                    l_id = texto_no_meio(sopa, '/anime/', '/')
                    
                    if sopa_list.find(f'"anime_id":{l_id}') != -1 or sopa_list.find(f'anime_id&quot;:{l_id}') != -1:
                        continue

                    lista_proc.append((l_id, 0, 5))           
            else:

                lista_link = lista_link.replace('airing_status=2&', '')

                sopa = sopapranois(lista_link, load=load_lista)
                sopa = texto_no_meio(sopa, '<table class="list-table"', '<tr class="list-table-header">')
            

                if sopa.find('{"status":') != -1:

                    referencia = '{"status":'
                    id_flag = '"anime_id":'
                    w_eps_flag = '"num_watched_episodes":'

                elif sopa.find('&quot;status') != -1: 

                    referencia = '&quot;status'
                    id_flag = 'anime_id&quot;:'
                    w_eps_flag = 'num_watched_episodes&quot;:'



                sopa = sopa[sopa.find(referencia) + len(referencia):]
                
                load_lista.linha = 'coletando IDs'
                while True:

                    load_lista.add()

                    status = int(sopa[sopa.find(',')-1])
                    is_rewatch = int(texto_no_meio(sopa, 'is_rewatching&quot;:', ','))

                    if is_rewatch == 1: status = 1
                    
                    if menu1.select[0] == 5: status-=1

                    if menu1.select[0] == 0 or status == menu1.select[0]:
                        
                        air_status = sopa[sopa.find('airing_status'):]
                        air_status = int(air_status[air_status.find(',')-1])
                        
                        if menu1.select[1] == 0 or menu1.select[1] == air_status:

                            a_id = texto_no_meio(sopa, id_flag, ',')
                            w_eps = texto_no_meio(sopa, w_eps_flag, ',')

                            try: 
                                int(a_id)
                                int(w_eps)
                            except: 
                                print(a_id)
                                print(w_eps)
                                exit()

                            lista_proc.append((a_id, w_eps, status, air_status))


                    if sopa.find(referencia) == -1: 
                            if len(lista_proc) == 0: print(lista_proc)
                            break

                    sopa = sopa[sopa.find(referencia) + len(referencia):] 

            if menu1.cursor == 5:





                temp_list = list()

                load_lista.linha = 'coletando titulos'
                for item in lista_proc:
                    
                    load_lista.add()

                    tl = get_name_from_file(item[0])

                    temp_list.append((item[0], item[1], tl, item[2], item[3]))



                lista_proc = temp_list

                lista_nomes = list(('VOLTAR\n',))

                for item in lista_proc:
                    lista_nomes.append(item[2])

                menu_nomes = menu(lista_nomes, 1)

                apagar_linhas(1)

                while True:
                    
                    menu_nomes.update()
                    menu_nomes.input()

                    if tecla == 'Key.enter':
                        
                        if menu_nomes.cursor == 0: break
                        else:
                            anime = lista_proc[menu_nomes.cursor-1]
                            get_eps(anime[0], anime[1], stat=anime[3], air_status=anime[4])
                            


            elif menu1.cursor == 4:

                apagar_linhas(1)

                
                for item in lista_proc:

                    lista = list(item)

                    lista[1] = int(item[1])+1

                    

                    #lista.append(get_name_from_file(item[0]))

                    play_ep(lista[0], lista[1], lista[2], lista[3])

                #apagar_linhas(3)

                    

                    

                    

                    
                    


