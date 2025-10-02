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

def sopapranois(link, t = 4, load = None, redo = 0, redo_limite = 4, return_url = False):

    if debug: prt(f' {link}')

    if link == False or link == '': return False
    if redo > redo_limite: return False

    cnctvrf()

    try:
        page = requests.get(str(link), timeout=10)
    except Exception as e:
        cnctvrf()
        prt(f'\n{e} {redo+1}/{redo_limite+1}')
        retornar = sopapranois(link, t, load, redo+1, redo_limite)
        apagar_linhas(1)
        return retornar

    if return_url: return page.url

    soup = bs4.BeautifulSoup(page.text, 'html.parser')    

    if str(soup).find('<div id="captcha-container"></div>') != -1:
        if debug: prt(' captcha do inferno')
        if load != None:
            load.add()
        time.sleep(t)
        return sopapranois(link, t*2, load, redo, redo_limite)

    

    return str(soup)

def get_name_from_id(id):

    sopa = get_mal_sopa(id)

    titulo = texto_no_meio(sopa, '<h1 class="title-name h1_bold_none"><strong>', '</strong>')

    #print(titulo)
    #print(link)
    #exit()

    if titulo != False: titulo = titulo.replace('&amp;', '&')
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
            titulo = data[int(id)][:-1]
            titulo = titulo.replace('&amp;', '&')
            return titulo

        else:
            titulo = get_name_from_id(id)
            if titulo == False: return False
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

    titulo = get_name_from_file(id)

    cor = ''
    if int(id) in indisponiveis: cor = colorama.Fore.RED
    if int(id) in essamerdaehentai(): cor = colorama.Fore.LIGHTRED_EX

    sys.stdout.flush()
    prt(f'\nanime: {cor}{titulo}{colorama.Fore.RESET}\nep: {ep}')

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

        if menu1.select[0] == 7:
            #webbrowser.open(f'https://myanimelist.net/anime/{id}')
            pass

        return
    else: 
        if status != 1:
            if air_status != 3:
                if devmode and not debug and int(id) not in indisponiveis:
                    #prt('\a')
                    #webbrowser.open(f'https://myanimelist.net/anime/{id}')
                    pass
        time.sleep(1)
    
    apagar_linhas(classe.linhas_apagar+4)

def processtl(tl, mode=1):

    tl = tl.replace('Ü', 'U')
    tl = tl.replace("'", '')

    titulo = re.sub(r'[^a-zA-Z0-9]', ' ', tl) 

    while titulo.find('  ') != -1: titulo = titulo.replace('  ', ' ')    

    ntl = titulo
    
    if mode == 1:
        ntl = ntl.replace('Shinkakusha Kouho Senbatsu Shiken hen', '2nd season')
        ntl = ntl.replace('Kagaijugyou hen', '2nd season Kagaijugyou hen')
        ntl = ntl.replace('Azumanga Daiou The Animation', 'Azumanga Daioh')
        ntl = ntl.replace(' Meido ', ' maid ')
        ntl = ntl.replace('Dededede Destruction OVA', 'Dededede Destruction ONA')

        ntl = ntl.replace(' ', '-')

        while ntl.find('--') != -1: titulo = titulo.replace('--', '-')

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



    menu_eps = menu(lista_eps_menu)
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

def todososids():

    filename = f'{os.path.expanduser("~")}/otapy/TempInds'

    try:
        with open(filename, 'r') as f:
            f.close()
    except:
        with open(filename, 'w') as f:
            f.write('')
            f.close()

    id = indisponiveis[-1]
    lista = []
    while True:

        with open(filename, 'r') as f:
            data = list(f.readlines())
            f.close()

        apagar_linhas(99)
        id += 1

        print(f'{data}\n\n{id}')

        if id in indisponiveis: continue
        if id in essamerdaehentai(): continue
        
        tl = get_name_from_file(id)
        if tl == False: continue

        print(tl)

        result = provedores((id, 1, tl), mal_sopa=True, sleep=0)
        if result.indisp == True: 
            #prt('\a')
            #webbrowser.open(f'https://myanimelist.net/anime/{id}')
            lista.append(str(id) + ',')
            
            with open(filename, 'w') as f:
                f.write(list_to_string(lista))
                f.close()

def list_to_string(lista):

    if type(lista) != list and type(lista) != tuple: return lista

    string = ''

    for item in lista:
        string += str(list_to_string(item))
        string += ' '

    return string

def verificar_inds():

    filename = f'{os.path.expanduser("~")}/otapy/TempInds'

    try:
        with open(filename, 'r') as f:
            f.close()
    except:
        with open(filename, 'w') as f:
            f.write('')
            f.close()

    lista = []

    for id in indisponiveis:

        with open(filename, 'r') as f:
            data = list(f.readlines())
            f.close()

        if len(data) > 0:
            data[0] = data[0].replace('  ', ' ')
            if (' ' + data[0]).find(f' {id},') != -1: continue
            lista = data
                

        apagar_linhas(99)

        print(f'{data}\n\n{id}')

        tl = get_name_from_file(id)
        if tl == False: continue

        print(tl)

        result = provedores((id, 1, tl), mal_sopa=False, sleep=0)
        
        if result.ep_link == False: 
            #prt('\a')
            #webbrowser.open(f'https://myanimelist.net/anime/{id}')
            lista.append(str(id) + ',')
            
            with open(filename, 'w') as f:
                f.write(list_to_string(lista))
                f.close()
        else: 
            if result.ep_link != False: prt('\a')

def essamerdaehentai(id = None):

    filename = f'{os.path.expanduser("~")}/otapy/H'

    try:
        with open(filename, 'r') as f:
            f.close()
    except:
        with open(filename, 'w') as f:
            f.write(' ')
            f.close()

    with open(filename, 'r') as f:
        data = f.read()
        f.close()

    data = ' ' + data + ' '
    lista = []

    while True:

        while data.find('  ') != -1: data = data.replace('  ', ' ')

        if data == ' ': break

        bababeba = texto_no_meio(data, ' ', ' ', True, True)
        if bababeba == False: break

        data = ' ' + data.replace(bababeba, '') + ' '

        lista.append(int(bababeba))
        

    if id != None: lista.append(id)

    with open(filename, 'w') as f:
        f.write(list_to_string(sorted(lista)))
        f.close()

    return lista

def get_mal_sopa(id, page=1):

    global ram_info

    id = int(id)
    voltar = False
    existe = False

    for item in ram_info:
        if item[0] == id:
            existe = True
            voltar = item[page]
            break 
            
    if voltar != False: return voltar
    
    if not existe: ram_info.append([id, False, False, False, False, False])   
    
    num = 0
    for i in ram_info:
        if i[0] == id: break
        num += 1

    if page == 1:

        link = f'https://myanimelist.net/anime/{id}'
        sopa = sopapranois(link)

        ram_info[num][page] = sopa

        return sopa
    
    elif page == 2:

        link = f'https://myanimelist.net/anime/{id}/blablabla/episode?offset={offset}'
        sopa = sopapranois(link)

        ram_info[num][page] = sopa

        return sopa



#classes

class menu():
    def __init__(self, lista_opts, uma_opt = None, offset = 0):
        self.cursor = 0
        self.opt_list = lista_opts
        self.n_linhas = len(find_all(list_to_string(opt_lista), '\n'))
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

            if self.cursor == i: 
                cor = colorama.Fore.BLUE
            else: cor = colorama.Fore.RESET

            if tipo == tuple or tipo == list:

                linha = str(item[0])
                
                if self.cursor == i:
                    for ii in listacomtodasascores:
                        linha = linha.replace(ii, '')
                
                prt(f'\n{cor}{linha}\t', True)

                for baboey in range(0, int(1/len(linha)*mtp)):
                    #prt(int(1/len(linha)*mtp))
                    prt('\t', True)

                for i2 in range(0, len(item[1])):

                    item2 = item[1][i2]

                    if self.select[i - self.offset] == i2: cor = colorama.Fore.BLUE
                    else: cor = colorama.Fore.RESET

                    if len(item2) < 6: espaco = '\t\t'
                    else: espaco = '\t'


                    prt(f'{cor}|{item2}{espaco}', True)

            else:
                linha = str(item)

                if self.cursor == i:
                    for ii in listacomtodasascores:
                        linha = linha.replace(ii, '')

                prt(f'\n{cor}{linha}', True)

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

    def __init__(self, lista, mal_sopa = True, sleep = 1):

        prt('\n\n', True)

        self.id = lista[0]
        self.ep = lista[1]
        self.titulo = lista[2]
        self.ep_link = False
        self.quero_dublado = 0
        self.yt_link = None
        self.linhas_apagar = 0
        self.sleep = sleep
        self.indisp = False

        

        subs_list = [
            (7791, 'k-on 2'),
        ]

        for item in subs_list:
            if item[0] == int(self.id):
                self.titulo = item[1]

        provs = (self.q1n, self.animesdigitalorg, self.animefire, self.animesonlinecc, self.animesgames, self.goyabu, self.animesorion, self.animezeira)

        #if debug: provs = (self.animezeira,)


        yt_list = [[11795, [[1, 'https://www.youtube.com/watch?v=dRBP1rpE5y8&t=1s']]], 
                    [58507, [[1, 'https://youtu.be/sHGcGkaYd38']]], 
                    [8939, [[1, 'https://youtu.be/GlxrJVdNyro']]],
                    [56213, [[1, 'https://www.youtube.com/watch?v=2zcZbIN3VPE'],
                            [2, 'https://www.youtube.com/watch?v=3VRuAhF1gLY'],
                            [3, 'https://www.youtube.com/watch?v=5n6K33W442w'],
                            [4, 'https://www.youtube.com/watch?v=Gv_lwgPAQsQ']]],
                    [30059, [[1, 'https://www.youtube.com/watch?v=mzGU_iUMBi8']]],
                    [47904, [[1, 'https://youtu.be/3RxlzJWWzdY'],
                             [2, 'https://youtu.be/fRsjv-JKyf8']]],
        ]

        for i in yt_list:

            if int(i[0]) == int(self.id):

                for i2 in i[1]:

                    if i2[0] == int(self.ep):

                        self.yt_link = i2[1]
                        
                        break
                break
        if self.yt_link != None:
            provs = (self.youtube,) + provs

        if devmode:

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
        if debug: self.quero_dublado = 1

        for prov in provs:

            if self.sleep > 0: time.sleep(self.sleep)
            apagar_linhas(self.linhas_apagar)
            self.linhas_apagar = 0
            prov()

            if self.ep_link != False: 
                break

        if int(self.id) in essamerdaehentai(): return

        if self.ep_link == False and int(self.ep) == 1:
            if mal_sopa:

                sopa = get_mal_sopa(self.id)

                available_at = texto_no_meio(sopa, '<h2>Available At', 'class="pb16"')
                genres = texto_no_meio(sopa, '>Genre', '</div>')
                air_status = texto_no_meio(sopa, '>Status:</span>', '</div>')

                flags = (
                    (genres, 'title="Hentai"'),
                    (air_status, 'Not yet aired'),
                )

                if available_at != False:
                    if available_at.find('https://www.youtube.com/watch?') != -1:
                        self.yt_link = texto_no_meio(available_at, 'https://www.youtube.com/watch?', '"', True)
                        if self.yt_link != False:
                            apagar_linhas(self.linhas_apagar)
                            self.youtube()
                            return
                        
                self.indisp = True

                for i in flags:
                    if i[0] != False:
                        if i[0].find(i[1]) != -1:
                            self.indisp = False

                            if i == flags[0]: essamerdaehentai(self.id)

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
        ep = self.ep
        aids = self.id

        # nomes especificos
        for bababoey in (1,):

            substituir = (
                ('Bishoujo Senshi Sailor Moon', 'sailor moon'),
                ('Shinseiki Evangelion', 'neon genesis evangelion'),
                ('yuu yuu hakusho', 'yu yu hakusho'), 
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
                (11491, 'Recorder to Randoseru'),
                (11617, 'highschool-dxd')
            )

            tl = self.titulo

            for item in substituir:
                tl = tl.lower().replace(item[0].lower(), item[1].lower())

            samelist = (
                (12729, 11617, 12),
            )

            for item in samelist:
                if int(self.id) == item[0]:
                    tl = get_name_from_file(item[1])
                    ep += item[2]
                    aids = item[1]
                    break

            for item in id_tl_list:
                if int(aids) == item[0]: 
                    tl = item[1]
                    break

            tl = processtl(tl)

            for item in substituir2:
                tl = tl.lower().replace(item[0].lower(), item[1].lower())


        titulo = tl

        if ep < 10:
            str_ep = f'0{str(ep)}'
        else: str_ep = str(ep)








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

                if ep_topo < ep:
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

                    page = int((int(ep_topo) - ep)/50)+1

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

            id_tl = (
                (31, 'neon-genesis-evangelion-death-rebirth'),
                (32, 'Neon Genesis Evangelion: The End of Evangelion'),
            )

            for item in id_tl:
                if int(self.id) == item[0]: 
                    tl = item[1]
                    break

            tl = processtl(tl)

            sd_list = (
                'ike-ina-chuu-takkyuubu',
                'serial-experiments-lain',
                'yuu-yuu-hakusho'
            )

            id_sd_list = (
                20,
            )

            bloquear = (
                (8, 0),
            )

            sd_perm = True
            for item in bloquear:

                if int(self.id) == item[0]:
                    if item[1] == 0: sd_perm = False
                    if item[1] == 1: hd_perm = False
                    if item[1] == 2: fhd_perm = False
                    break


        sub_link = f'https://animefire.plus/animes/{tl}-todos-os-episodios'
        dub_link = f'https://animefire.plus/animes/{tl}-dublado-todos-os-episodios'

        temp_links.append(dub_link)
        temp_links.append(sub_link)

        #print(f'\n{link_list}'), exit()

        for link in temp_links:

            if link == dub_link: versao = 'dublado'
            elif link == sub_link: versao = 'legendado'
            
            if True:

                sopa = sopapranois(link, redo_limite=0)

                if sopa == '' or sopa == False:
                    prt(f'\nanime {versao} não encontrado!')
                    self.linhas_apagar += 1
                    continue

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

                videolink = link

                if sopa == False:
                    prt(f'\nfalha ao reproduzir episodio {versao}!')
                    self.linhas_apagar += 1
                    continue

                sources = texto_no_meio(sopa, '"data":[', ']')
                sources = sources.replace('\\', '')

                sources_preserv = sources

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
                            
                if sources_preserv != '':
                    if sources_preserv.find('.googlevideo.') != -1:
                        link = videolink.replace('/video/', '/animes/')
                        sopa = sopapranois(link)
                        link = texto_no_meio(sopa, 'https://www.blogger.com/', '"', True)

                        if link != False:
                            if sopapranois(link).find('"errorContainer"') == -1:

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
        aids = int(self.id)
        ep = self.ep

        for item in substituir:
            tl = tl.lower().replace(item[0].lower(), item[1].lower())

        samelist = (
            (13055, 11499, 12),
            (16694, 11499, 14),
        )

        for item in samelist:
            if int(self.id) == item[0]:
                tl = get_name_from_file(item[1])
                ep += item[2]
                aids = item[1]
                break


        id_tl_list = (
            (530, 'sailor moon'),
        )

        for item in id_tl_list:
            if aids == item[0]: 
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
                if sopa.find(f'id="ep {ep}"') == -1:
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
                    
                    chunk = sopa[ : sopa.rfind(f'id="ep {ep}"')]
                    num = chunk.rfind('<li>')
                    link = sopa[num:num+200]
                    link = texto_no_meio(link, 'href="', '"')

                    sopa = sopapranois(link)

                    link = texto_no_meio(sopa, 'https://www.blogger.com/video', '"', True)

                    if link == False or sopapranois(link).find('"errorContainer"') != -1:
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
        ep = self.ep

        samelist = (
            (61322, 57592, 12),
        )

        for item in samelist:
            if int(self.id) == item[0]:
                tl = get_name_from_file(item[1])
                ep += item[2]

        subst_list = (
            (53065, 'Sono Bisque Doll wa Koi wo Suru 2'),
            (59095, 'Tensei shitara Dainana Ouji Datta node, Kimama ni Majutsu wo Kiwamemasu 2'),
        )

        for item in subst_list:
            if item[0] == int(self.id):
                tl = item[1]
                break

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

            if sopa == False or sopa.find('<title> 503 Service Unavailable') != -1:
                prt(f'\nprovedor indisponivel!')
                self.linhas_apagar += 1
                return

            if sopa.find('class="error404') != -1:
                prt(f'\nanime {versao} não encontrado!')
                self.linhas_apagar += 1
                continue

            if texto_no_meio(sopa, '<div class="data"', '</h1>').find('Dublado') != -1: versao = 'dublado'

            link = link.replace('/animes/', '/episodio/') + f'-episodio-{ep}'
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
                'drm.strp2p.site',
                'strp2p.com',
            )

            red_flags = (
                'File is no longer available',
                'Video not found!',
                'This content is no longer available.',
                '<title>Not Found</title>',
                '<title>403 Forbidden</title>',
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
                #for item in red_flags:
                #    if file_sopa.find(item) != -1: 
                #        ignorar = True
                #        break

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
                    
                    elif link.find('/antivirus3/')!= -1 or link.find('/antivirus2/')!= -1:
                        file = texto_no_meio(sopapranois(link), '"file": "', '?')

                        if file != False:

                            file_sopa = sopapranois(file)
                            deuruim = False
                            for item in red_flags:
                                if file_sopa.find(item) != -1:
                                    deuruim = True
                            if deuruim: continue

                            if devmode: webbrowser.open(link)

                    elif link.find('streamtape.com')!= -1:

                        if not debug: continue

                        file_sopa = sopapranois(link)
                        deuruim = False
                        for item in red_flags:
                            if file_sopa.find(item) != -1:
                                deuruim = True
                        if deuruim: continue

                        if devmode: webbrowser.open(link)

                    elif link.find('embedwish.com')!= -1:

                        file = link[ : link.find('?')]
                        file_sopa = sopapranois(file)
                        deuruim = False
                        for item in red_flags:
                            if file_sopa.find(item) != -1:
                                deuruim = True
                        if deuruim: continue

                        if devmode: webbrowser.open(link)
                        
                    elif link.find('/composite-google') != -1:

                        if debug: continue

                        filesopa = sopapranois(link)
                        file = texto_no_meio(filesopa, '"file": "', '?')

                        if file != False:

                            filesopa = sopapranois(file)

                            deuruim = False
                            for item in red_flags:
                                if filesopa.find(item) != -1:
                                    deuruim = True
                            if deuruim: continue

                            prt(f'\nreproduzindo episodio {versao}...')
                            self.linhas_apagar += 1

                            self.ep_link = file

                            return

                    elif link.find('.wixmp.com') != -1:
                        
                        if sopapranois(link) == 'Forbidden': continue
                        
                        if devmode: webbrowser.open(link)

                    else:
                        if debug:
                            print(f'\n\ncaiu no else\n\n{link}')
                            exit()
                        if devmode: webbrowser.open(link)

            prt(f'\nfalha ao reproduzir episodio {versao}!')
            self.linhas_apagar += 1
            
    def anime_existe(self, link, versao, n_flag):

        sopa = sopapranois(link)

        if sopa == False or sopa.find(n_flag) != -1:
            prt(f'\nanime {versao} não encontrado!')
            self.linhas_apagar += 1
            return False
        else: return True

    def ep_existe(self, link, versao, n_flag):

        sopa = sopapranois(link)

        if sopa == False or sopa.find(n_flag) != -1:
            prt(f'\nepisodio {versao} não encontrado!')
            self.linhas_apagar += 1
            return False
        else: return True

    def animesonlinecc(self):

        prt('provedor: animesonlinecc.to')

        tl = self.titulo
        aids = int(self.id)
        ep = self.ep
        tipo = 'episodio'

        # nomes especificos
        for bababoey in (1,):

            ova_list = (
                16694, 13055,
            )

            substituir = (
                (' season ', ' '),
                ('yuu yuu hakusho', 'yu yu hakusho'), 
            )
            for item in substituir:
                tl = tl.lower().replace(item[0], item[1])
        
            samelist = (
                (13055, 11499, 0),
                (16694, 11499, 2),
            )

            for item in samelist:
                if int(self.id) == item[0]:
                    tl = get_name_from_file(item[1])
                    ep += item[2]
                    aids = item[1]
                    break

            id_tl_list = (
                (530, 'sailor moon'),
            )

            for item in id_tl_list:
                if aids == item[0]: 
                    tl = item[1]
                    break
        
            if aids in ova_list: tipo = 'ova'

        tl = processtl(tl)
                
        link = f'https://animesonlinecc.to/episodio/{tl}-{tipo}-{ep}/'

        sopa = sopapranois(link, redo_limite=0)

        if sopa == False:
            prt('\nepisodio não encontrado!')
            self.linhas_apagar += 1

        else:

            if sopa.find('content="Página não encontrada') == -1:

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
        aids = int(self.id)
        ova = False

        ova_list = (
            (13055, 11499, (1, 2)),
            (16694, 11499, (3,)),
        )

        id_tl_list = (
            (530, 'sailor moon'),
        )

        for i in ova_list:
            if aids == i[0]:
                aids = i[1]
                ova = True
                ep = i[2][self.ep-1]
                tl = get_name_from_file(aids)

        for item in id_tl_list:
            if aids == item[0]: 
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

            if ova: flag = f'<h3>Ova {ep}</h3>'
            else: flag = f'dio {self.ep}</h3>'

            if sopa.find(flag) == -1:
                prt(f'\nepisodio {versao} não encontrado!')
                self.linhas_apagar += 1
                continue

            link = sopa[ : sopa.rfind(flag) ]
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

                if sopapranois(link).find('"errorContainer"') == -1:

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
                        webbrowser.open(link)

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
        aids = int(self.id)
        ep = self.ep



        id_tl_list = (
            (530, 'sailor moon'),
        )

        ova_list = (
            16694, 13055,
        )

        samelist = (
            (13055, 11499, 0),
            (16694, 11499, 2),
        )


        if aids in ova_list: ova = True
        else: ova = False

        for item in samelist:
            if int(self.id) == item[0]:
                tl = get_name_from_file(item[1])
                ep += item[2]
                aids = item[1]
                break

        for item in id_tl_list:
            if aids == item[0]: 
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

            if sopa.find(f'dio {ep}" href="') == -1:
                prt(f'\nepisodio {versao} não encontrado!')
                self.linhas_apagar += 1
                continue

            if ova:
                ova_eps = find_all(sopa, '<ul class="listaEP">')[1]
                sopa = sopa[ova_eps:]

            link = texto_no_meio(sopa, f'dio {ep}" href="', '"')
            sopa = sopapranois(link)

            link = texto_no_meio(sopa, 'data-video="', '"')
            sopa = sopapranois(link)

            link = texto_no_meio(sopa, '"file":"', '"')

            if link != False:

                link = link.replace('\\', '')

                if versao == 'dublado':
                    if self.quero_dublado == 0: self.escolher_dub()
                    if self.quero_dublado < 0: continue

                prt(f'\nreproduzindo episodio {versao}...')
                self.linhas_apagar += 1

                self.ep_link = link

                return
                
            prt(f'\nfalha ao reproduzir episodio {versao}!')
            self.linhas_apagar += 1

    def hinatasoul(self):

        prt('provedor: hinatasoul.com')

        tl = self.titulo

        tl = processtl(tl)

        links = (
            (f'https://www.hinatasoul.com/animes/{tl}-dublado', 'dublado'),
            (f'https://www.hinatasoul.com/animes/{tl}', 'legendado'),
        )

        for i in links:

            link = i[0]
            versao = i[1]

            sopa = sopapranois(link)

            if sopa.find('<title>403 Forbidden</title>') != -1:
                prt(f'\nanime {versao} não encontrado!')
                self.linhas_apagar += 1
                continue

            print('\n')
            print(sopa)
            exit()

        time.sleep(3)

    def akumanimes(self):

        prt('provedor: akumanimes.com')

        tl = self.titulo

    def animezeira(self):

        prt('provedor: animezeira.net')

        tl = self.titulo

        tl = processtl(tl)

        links = [
            [f'https://animezeira.net/{tl}-dublado/', f'https://animezeira.net/episodio/{tl}-dublado-episodio-{self.ep}/', 'dublado'],
            [f'https://animezeira.net/{tl}/', f'https://animezeira.net/episodio/{tl}-episodio-{self.ep}/', 'legendado'],
        ]

        for item in links:

            versao = item[2]
            ani_link = item[0]
            ep_link = item[1]

            sopa = sopapranois(ep_link)

            

            if sopa == False:
                prt(f'\nfalha ao reproduzir episodio {versao}!')
                self.linhas_apagar += 1
                continue

            if sopa.find('<title>Página não encontrada - Animezeira</title>') != -1:
                if self.sleep > 0:
                    sopa = sopapranois(ani_link)
                    if sopa != False:
                        if sopa.find('<title>Página não encontrada - Animezeira</title>') != -1:
                            prt(f'\nanime {versao} não encontrado!')
                            self.linhas_apagar += 1
                            continue
                
                prt(f'\nepisodio {versao} não encontrado!')
                self.linhas_apagar += 1
                continue

            link = texto_no_meio(sopa, '<div class="post-video">', '</video>')
            link = texto_no_meio(link, '<source src="', '"')

            link = sopapranois(link, return_url=True)

            if link == False:
                prt(f'\nfalha ao reproduzir episodio {versao}!')
                self.linhas_apagar += 1
                continue

            if sopapranois(link).find('"errorContainer"') == -1:

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
                

            prt(f'\nfalha ao reproduzir episodio {versao}!')
            self.linhas_apagar += 1

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
    player_off = False
    verificar_tudo = False
    indisp = False

    

    colorama.init()
    tecla = None

    
    if debug: usnm = 'gahvius'
    else: usnm = getusername()
    if usnm.lower() == 'gahvius': devmode = True

    if not devmode:
        debug = False
        player_off = False
        verificar_tudo = False

    run = True

    playerlist = ('mpv', '"H:/programas/mpv/mpv.exe"', 'vlc', '"C:/Program Files/VideoLAN/VLC/vlc.exe"')    



#listas 
for bababoey in (1,):

    opt_lista = [
        ['LISTA', ['todos', 'assistindo', 'completos', 'em espera', 'dropados', 'planejo assistir', 'lançamentos']], 
        ['STATUS', ['todos', 'em lançamento', 'terminados', 'não lançados']], 
        'ORDEM 1',
        'ORDEM 2', 
        '\nREPRODUZIR LISTA', 
        'ABRIR LISTA', 
        '\nSAIR' 
    ]

    if devmode: 
        opt_lista = [
            ['LISTA', ['todos', 'assistindo', 'completos', 'em espera', 'dropados', 'planejo assistir', 'lançamentos']], 
            ['STATUS', ['todos', 'em lançamento', 'terminados', 'não lançados']], 
            'ORDEM 1',
            'ORDEM 2', 
            '\nREPRODUZIR LISTA', 
            'ABRIR LISTA', 
            '\nVERIFICAR TODOS',
            'VERIFICAR INDISPONIVEIS',
            '\nSAIR',
        ]


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

    listacomtodasascores = (
        colorama.Fore.BLACK,
        colorama.Fore.BLUE,
        colorama.Fore.CYAN,
        colorama.Fore.LIGHTBLACK_EX,
        colorama.Fore.YELLOW,
        colorama.Fore.RED,
        colorama.Fore.WHITE,
        colorama.Fore.GREEN,
        colorama.Fore.LIGHTRED_EX,
        colorama.Fore.LIGHTBLUE_EX,
        colorama.Fore.LIGHTCYAN_EX,
        colorama.Fore.LIGHTGREEN_EX,
        colorama.Fore.LIGHTMAGENTA_EX,
    )




    indisponiveis = []

    ind_link = 'https://github.com/ChVntr/otapy/issues/2#issue-3332438286'
    ind_sopa = sopapranois(ind_link)

    indispo = texto_no_meio(ind_sopa, '"articleBody":"', '"')

    while True:

        if indispo == ' ' or indispo == '': break

        if indispo.find(',') == -1: 
            indisponiveis.append(int(indispo))
            break
        
        ind_id = indispo[ : indispo.find(',') ]
        indisponiveis.append(int(ind_id))

        indispo = indispo[ indispo.find(',')+1 : ]

    ram_info = []



#classes de menu
for bababoey in (1,):
    menu1 = menu(opt_lista)
    menu_ordem1 = menu(ordem_opt_list, True, 1)
    menu_ordem2 = menu(ordem_opt_list, True, 1)
    

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

    
    if menu1.select[0] > 5: menu1.select[1] = 0

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


            lista_proc = []
            t1 = False
            t2 = False

            

            if menu1.select[0] == 6:
                link1 = 'https://myanimelist.net/anime/season'
                link2 = f'https://myanimelist.net/animelist/{usnm}?order=14&status=7'

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
                    
                    #if devmode and not indisp and int(l_id) in indisponiveis: continue    
                    
                    if sopa_list.find(f'"anime_id":{l_id}') != -1 or sopa_list.find(f'anime_id&quot;:{l_id}') != -1:
                        continue

                    lista_proc.append((l_id, 0, 5, None))           
            elif menu1.select[0] == 7:

                player_off = True
                for id in sorted(indisponiveis):
                    load_lista.add()
                    rept = False
                    for item in lista_proc:
                        if item[0] == id:
                            rept = True
                            break
                    if rept: continue
                    lista_proc.append((id, 0, None, None))

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

                            #if devmode and not indisp and int(a_id) in indisponiveis: pass
                            #else: 
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

                    if int(item[0]) in indisponiveis:

                        tl = colorama.Fore.RED + tl

                    temp_list.append((item[0], item[1], tl, item[2], item[3]))



                lista_proc = temp_list

                lista_nomes = list(('VOLTAR\n',))

                for item in lista_proc:
                    lista_nomes.append(item[2])

                menu_nomes = menu(lista_nomes)

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

        elif opt_lista[menu1.cursor] == '\nVERIFICAR TODOS':
            todososids()

        elif opt_lista[menu1.cursor] == 'VERIFICAR INDISPONIVEIS':
            verificar_inds()

        prt('\a')                

                    

                    

                    
                    


