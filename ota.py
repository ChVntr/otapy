#funções

def key_press(key):

    global tecla

    tecla = str(key)

    if tecla == 'Key.enter': 
        prt('\033[1A')
        
    return False

def texto_no_meio(texto, começo, fim, prsv_começo = None, prsv_final = None):

    loc1 = texto.find(começo) + len(começo)
    loc2 = loc1 + texto[loc1:].find(fim)

    if prsv_começo == True: loc1 -= len(começo)
    if prsv_final == True: loc2 += len(fim)

    for linha in (começo, fim):
        if texto.find(linha) == -1:
            return f'"{linha}" não encontrado'

    return texto[loc1:loc2]

def cnctvrf(url=None):

    try:
        requests.get('https://myanimelist.net')
        nocom=False
    except :
        nocom = True
        print('\n\nFALHA DE CONECÇÃO!\nAGUARDANDO RESPOSTA DE "myanimelist.net"...\n'.lower())

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

    global usnm
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

def apagar_linhas(n):

    sys.stdout.write(f"\033[{n}A \r\033[J")

def sopapranois(link, t = None):

    if t == None: t = 1

    cnctvrf()

    try:
        page = requests.get(str(link), timeout=5)
    except:
        cnctvrf()
        prt('   TIMEOUT!')
        return sopapranois(link)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')    

    if str(soup).find('<div id="captcha-container"></div>') != -1:
        time.sleep(t)
        return sopapranois(link, t*2)

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
                f.writelines(data)
                f.close()
    
    else: 
        while len(data) <= int(id):
            data.append('\n')
        with open(filename, 'w') as f:
            f.writelines(data)
            f.close()

    return get_name_from_file(id)

def play_ep(id_ep_titulo):
    

    sys.stdout.flush()
    prt(f'\nanime: {id_ep_titulo[2]}\nep: {id_ep_titulo[1]}')

    classe = provedores(id_ep_titulo)
    midia_link = classe.ep_link

    if midia_link != False:
        subprocess.run(f'mpv {midia_link}', shell=True, capture_output=True)
        apagar_linhas(classe.linhas_apagar+1)
    else: time.sleep(1)
    
    apagar_linhas(3)

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

def get_eps(id, atual, cursor = None, offset = 0):
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

            else: return ep

            

    
    


    #prt(f'\n\n{ep_num} - {ep_name}\n')











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

        provs = (self.animesdigitalorg, self.animefire, self.goyabu)
        #provs = (self.goyabu,)

        for prov in provs:

            self.linhas_apagar = 0
            prov()
            if self.ep_link != False: break
            time.sleep(1)
            apagar_linhas(self.linhas_apagar)

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
                ('one punch man', 'null'),
                ('Fullmetal Alchemist: Brotherhood', 'fullmetal-abb001'),
                ('Fullmetal Alchemist: Brotherhood Specials', 'fullmetal-abb001'),
                ('Ore dake Level Up na Ken Season 2: Arise from the Shadow', 'solo leveling ii'),
                ('Bishoujo Senshi Sailor Moon', 'sailor moon'),
                ('part 2', '2'),
            )

            substituir2 = (
                ('yuu-yuu-hakusho', 'yu-yu-hakusho'),
                ('ranma-2024', 'ranma-½-2024'),
            )



            tl = self.titulo



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
        
        

        if self.quero_dublado > -1: temp_links.append(dub_link)
        temp_links.append(sub_link)


        link_list = list(temp_links)


        for link in temp_links:

            if link == sub_link: versao = 'legendado'
            if link == dub_link: versao = 'dublado'

            sopa = sopapranois(link)

            if sopa.find('<div class="msg404">') != -1:
                if versao == 'legendado' or self.quero_dublado > 0: 
                    prt(f'\nanime {versao} não encontrado!')
                    self.linhas_apagar += 1
                link_list.remove(link)
            else:
                
                ep_topo = texto_no_meio(sopa, '<div class="title_anime">', '</div>', prsv_final=True)
                ep_topo = texto_no_meio(ep_topo, 'Episódio ', '</div>')
                
                try:
                    ep_topo = int(ep_topo)

                    if ep_topo < self.ep:
                        prt(f'\nepisodio {versao} não encontrado!')
                        self.linhas_apagar += 1
                        link_list.remove(link)

                except:
                    prt(f'\n falha ao buscar episodio {versao}!')
                    self.linhas_apagar += 1
                    link_list.remove(link)
 
                
        if len(link_list) < 1: 
            return


        for link in link_list:

            if link == sub_link: versao = 'legendado'
            elif link == dub_link: 
                versao = 'dublado'
                if self.quero_dublado == 0: self.escolher_dub()
                if self.quero_dublado < 0: continue

            sopa = sopapranois(link)



            if sopa.find(f'Episódio {str_ep}</div>') == -1:
                prt('\nessa merda tá em outra pagina')
                self.linhas_apagar += 1
                return




            sopa = sopa[:sopa.find(f'Episódio {str_ep}</div>')]
            sopa = sopa[sopa.rfind('https://animesdigital.org/video/a/'):]
            link = sopa[:sopa.find('"')]



            sopa = sopapranois(link)
            link = texto_no_meio(sopa, 'https://api.anivideo.net/', '"', prsv_começo=True)
            link = texto_no_meio(link, 'https://cdn-', '&amp;nocache', True)

            

            prt(f'\nreproduzindo episodio {versao}...')
            self.linhas_apagar += 1
            

            break

        


        self.ep_link = link

    def animefire(self):

        prt('provedor: animefire.plus')

        temp_links = list()


        # nomes especificos
        for bababoey in (1,):

            substituir = (
                ('Ü', 'ue'),

            )

            tl = self.titulo

            for item in substituir:
                tl = tl.lower().replace(item[0].lower(), item[1].lower())             

            tl = processtl(tl)


        sub_link = f'https://animefire.plus/animes/{tl}-todos-os-episodios'
        dub_link = f'https://animefire.plus/animes/{tl}-dublado-todos-os-episodios'

        if self.quero_dublado >= 0: temp_links.append(dub_link)
        temp_links.append(sub_link)
        link_list = list(temp_links)

        for link in temp_links:

            if link == dub_link: versao = 'dublado'
            elif link == sub_link: versao = 'legendado'
            

            sopa = sopapranois(link)

            if sopa == '':
                if versao == 'legendado' or self.quero_dublado > 0:
                    prt(f'\nanime {versao} não encontrado!')
                    self.linhas_apagar += 1
            else:

                if versao == 'dublado': link = f'https://animefire.plus/download/{tl}-dublado/{self.ep}'
                else: link = f'https://animefire.plus/download/{tl}/{self.ep}'

                sopa = sopapranois(link)

                if sopa.find('">Download indisponível</h6>') != -1:
                    if versao == 'legendado' or self.quero_dublado > 0:
                        prt(f'\nepisodio {versao} não encontrado!')
                        self.linhas_apagar += 1
                else:

                    link = sopa[sopa.rfind('download='):]
                    link = texto_no_meio(link, '"', '"')

                    

                    if link[-4:] == '(SD)' or link.find('mp4_temp') != -1:
                        if versao == 'legendado' or self.quero_dublado > 0:
                            prt(f'\nepisodio {versao} em alta qualidade não encontrado!')
                            self.linhas_apagar += 1
                    else:

                        if link.find('googlevideo.com/') != -1:
                            if versao == 'legendado' or self.quero_dublado > 0:
                                prt(f'\nepisodio {versao} não encontrado!')
                                self.linhas_apagar += 1
                        else:

                            if versao == 'dublado':
                                if self.quero_dublado == 0: self.escolher_dub()
                                if self.quero_dublado < 0: continue

                            self.ep_link = f'{texto_no_meio(link, 'http', 'mp4&amp', True)}{tl}-{self.ep}-{versao}'

                            prt(f'\nreproduzindo episodio {versao}...')
                            self.linhas_apagar += 1
                            return

    def goyabu(self):

        prt('provedor: goyabu.to')
        self.linhas_apagar+=1

        substituir = (
            ('Tensei shitara Dainana Ouji Datta node, Kimama ni Majutsu wo Kiwamemasu', 'tensei shitara dainana ouji'),
            ('season 2', '2'),
            ('2nd season', '2'),
            ('part 2', '2'),
        )

        tl = self.titulo

        for item in substituir:
            tl = tl.lower().replace(item[0].lower(), item[1].lower())

        tl = processtl(tl)

        sub_link = f'https://goyabu.to/anime/{tl}'
        dub_link = f'{sub_link}-dublado'

        links = list()
        if self.quero_dublado > -1: links.append(dub_link)
        links.append(sub_link)

        for link in links:

            if link == dub_link: versao = 'dublado'
            elif link == sub_link: versao = 'legendado'

            sopa = sopapranois(link)

            if sopa.find('<title>404 Not Found</title>') != -1:
                if versao == 'legendado' or self.quero_dublado > 0:
                    prt(f'\nanime {versao} não encontrado!')
                    self.linhas_apagar += 1
            else:
                if sopa.find(f'id="ep {self.ep}"') == -1:
                    if versao == 'legendado' or self.quero_dublado > 0:
                        prt(f'\nepisodio {versao} não encontrado!')
                        self.linhas_apagar += 1
                else:

                    if versao == 'dublado':
                        if self.quero_dublado == 0: self.escolher_dub()
                        if self.quero_dublado < 0: continue
                    
                    chunk = sopa[ : sopa.rfind(f'id="ep {self.ep}"')]
                    num = chunk.rfind('<li>')
                    link = sopa[num:num+200]
                    link = texto_no_meio(link, 'href="', '"')

                    sopa = sopapranois(link)

                    link = texto_no_meio(sopa, 'https://www.blogger.com/video', '"', True)

                    prt(f'\nreproduzindo episodio {versao}...')
                    self.linhas_apagar += 1

                    self.ep_link = link

                    return

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





#init
for bababoey in (1,):

    os.makedirs(f'{os.path.expanduser("~")}/otapy/', exist_ok=True)

    debug = False

    colorama.init()
    tecla = None

    #usnm = getusername()
    usnm = 'gahvius'

    run = True



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

        if debug: prt(('\033[11B', lista_link, '\033[11A'))



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

                sopa = sopapranois(link1)
                sopa_list = sopapranois(link2)

                sopa_list = texto_no_meio(sopa_list, '<table class="list-table"', '<tr class="list-table-header">')

                tx = '<div class="title">'

                skip_list = (
                    'nd season',
                    'rd season',
                    'th season',
                    ' season ',
                    ' part ',
                )

                load_lista.linha = 'coletando IDs'
                while True:
                    
                    if sopa.find(tx) == -1: break
                    sopa = sopa[ sopa.find(tx)+len(tx) : ]

                    load_lista.add()
                    
                    if texto_no_meio(sopa, '<div class="js-anime', '<div class="js-anime').find('/anime/genre/12/') != -1: continue

                    titulo = texto_no_meio(sopa, '', '</a>')

                    tem = False
                    for item in skip_list:
                        if titulo.lower().find(item.lower()) != -1: tem = True
                    if tem: continue

                    l_id = texto_no_meio(sopa, '/anime/', '/')
                    
                    if sopa_list.find(f'"anime_id":{l_id}') != -1 or sopa_list.find(f'anime_id&quot;:{l_id}') != -1:
                        continue

                    lista_proc.append((l_id, 0))           
            else:

                sopa = sopapranois(lista_link)
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

                            lista_proc.append((a_id, w_eps))


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

                    temp_list.append((item[0], item[1], tl))



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
                            ep = get_eps(anime[0], anime[1])

                            if ep != False: play_ep((anime[0], ep, anime[2]))

            elif menu1.cursor == 4:

                apagar_linhas(0)

                
                for item in lista_proc:

                    lista = list(item)

                    lista[1] = int(item[1])+1

                    

                    lista.append(get_name_from_file(item[0]))

                    play_ep(lista)

                #apagar_linhas(3)

                    

                    

                    

                    
                    


