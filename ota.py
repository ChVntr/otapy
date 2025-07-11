run = True



#funções

def key_press(key):

    global tecla

    tecla = str(key)

    #if tecla == 'Key.enter': 
    #    prt('\033[1A')
        
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

def prt(string):

    if type(string) == tuple or type(string) == list:
        for item in string:
            prt(item)
    else:
        sys.stdout.write(str(string))

def getusername():

    global usnm
    validusername = False

    while validusername == False:
        usnm = input('\nUSERNAME DO MYANIMELIST: ')
        cnctvrf()
        response = str(requests.get(str(''.join(['https://myanimelist.net/profile/', usnm]))))
        if response.find('404') != -1:
            print(
                'USUARIO NÃO ENCONTRADO!'.lower()
            )
        else:
            validusername = True
            print('\n')

def apagar_linhas(n):

    sys.stdout.write(f"\033[{n}A")
    sys.stdout.write("\033[J")
    sys.stdout.write('\r')
    sys.stdout.write("\033[J")
    sys.stdout.flush()

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
    
    prt(f'anime: {id_ep_titulo[2]}\nep: {id_ep_titulo[1]}')

    classe = provedores(id_ep_titulo)
    midia_link = classe.ep_link

    if midia_link != False:
        subprocess.run(f'mpv {midia_link}', shell=True, capture_output=True)
    else: time.sleep(1)

    apagar_linhas(classe.linhas_apagar)
    
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





#classes

class menu():
    def __init__(self, lista_opts, n_linhas, uma_opt = None):
        self.cursor = 0
        self.opt_list = lista_opts
        self.n_linhas = n_linhas
        self.uma_opt = uma_opt

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

        mtp = 7

        opt_list = self.opt_list 

        for i in range(0, len(opt_list)):

            item = opt_list[i]

            tipo = type(item)

            if self.cursor == i: cor = colorama.Fore.BLUE
            else: cor = colorama.Fore.WHITE

            if tipo == tuple or tipo == list:

                prt(f'\n{cor}{item[0]}\t')

                for baboey in range(0, int(1/len(item[0])*mtp)):
                    #prt(int(1/len(item[0])*mtp))
                    prt('\t')

                for i2 in range(0, len(item[1])):

                    

                    item2 = item[1][i2]

                    if self.select[i] == i2: cor = colorama.Fore.BLUE
                    else: cor = colorama.Fore.WHITE

                    if len(item2) < 6: espaco = '\t\t'
                    else: espaco = '\t'


                    prt(f'{cor}|{item2}{espaco}')

            else:
                prt(f'\n{cor}{item}')

            prt(colorama.Fore.RESET)

        prt('\n')

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

        if cursor > len(opt_list)-1: cursor = len(opt_list)-1
        if cursor < 0: cursor = 0

        if cursor < len(select):
            if tecla == 'Key.right':
                select[cursor] += 1
                if len(opt_list[cursor][1]) == 2: select[cursor] += 1
                if select[cursor] > len(opt_list[cursor][1])-1: select[cursor] = len(opt_list[cursor][1])-1
                else: direct = True
            if tecla == 'Key.left':
                select[cursor] -= 1
                if select[cursor] < -1: direct = True
                if select[cursor] < 0: select[cursor] = 0
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

        apagar_linhas(self.n_linhas)

class provedores():
    def __init__(self, lista):

        prt('\n\n')

        self.linhas_apagar = 2

        self.id = lista[0]
        self.ep = lista[1]
        self.titulo = lista[2]
        self.ep_link = False
        self.quero_dublado = 1


        self.animesdigitalorg()
        if self.ep_link != False: return

    def animesdigitalorg(self):

        prt('provedor: animesdigital.org')
        self.linhas_apagar += 1

        temp_links = list()

        titulo = processtl(self.titulo)
        if self.ep < 10:
            str_ep = f'0{str(self.ep)}'
        else: str_ep = str(self.ep)








        sub_link = f'https://animesdigital.org/anime/a/{titulo}'
        
        if self.quero_dublado > 0:
            dub_link = sub_link + '-dublado'
            temp_links.append(dub_link)

        temp_links.append(sub_link)


        link_list = list(temp_links)


        for link in temp_links:

            if link == sub_link: versao = 'legendado'
            if link == dub_link: versao = 'dublado'

            sopa = sopapranois(link)

            if sopa.find('<div class="msg404">') != -1:
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
            if link == dub_link: versao = 'dublado'

            sopa = sopapranois(link)



            if sopa.find(f'Episódio {str_ep}</div>') == -1:
                print('\nessa merda tá em outra pagina')
                exit()




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
    debug = False

    colorama.init()
    tecla = None

    usnm = 'gahvius'



#listas 
for bababoey in (1,):

    opt_lista = (
        ('LISTA', ('todos', 'assistindo', 'completos', 'em espera', 'dropados', 'planejo assistir')), 
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
        'STORAGE',
        'AIR START DATE',
        'AIR END DATE',
        'STATUS',
        'MAL SCORE',
        'SCORE DIFF.',
        'POPULARITY'
    )

    outra_lista = list()
    for item in ordem_opt_list:
        outra_lista.append((item, ('Asc', 'Desc')))
    ordem_opt_list = outra_lista
    ordem_opt_list.append('\nVOLTAR')



#classes de menu
for bababoey in (1,):
    menu1 = menu(opt_lista, 10)
    menu_ordem1 = menu(ordem_opt_list, 20, True)
    menu_ordem2 = menu(ordem_opt_list, 20, True)

    lista_menus = list((menu1, menu_ordem1, menu_ordem2))

    filename = f'{os.path.expanduser("~")}/otapy/LastList'

    try:
        with open(filename, 'r') as f:
            data = list(f.readlines())
            f.close()

        for i in range(0, 2):
            for i2 in range(0, len(lista_menus[i].select)-1):
                lista_menus[i].select[i2] = int(data[i][i2])-1


    except:
        with open(filename, 'w') as f:
            f.write('')
            f.close()





while run:

    if not run: 
        break



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


        if menu1.cursor == 6:
            run = False
            break
        
        elif menu1.cursor == 2:
            while True:

                menu_ordem1.update()
                menu_ordem1.input()
                
                if tecla == 'Key.enter':
                    if menu_ordem1.cursor == 17:
                        break

        elif menu1.cursor == 3:
            while True:

                menu_ordem2.update()
                menu_ordem2.input()
                
                if tecla == 'Key.enter':
                    if menu_ordem2.cursor == 17:
                        break

        elif menu1.cursor == 4 or menu1.cursor == 5:

            lista_proc = list()
            t1 = False
            t2 = False

            prt((
            '\n', 
            'carregando lista...'
            ))
            sys.stdout.flush()
            
            sopa = sopapranois(lista_link)
            sopa = texto_no_meio(sopa, '<table class="list-table"', '<tr class="list-table-header">')
            




            if sopa.find('{"status":') != -1:

                referencia = '{"status":'
                id_flag = '"anime_id":'
                w_eps_flag = '"num_watched_episodes":'

                print('t2')

            elif sopa.find('&quot;status') != -1: 

                referencia = '&quot;status'
                id_flag = 'anime_id&quot;:'
                w_eps_flag = 'num_watched_episodes&quot;:'

                print('t1')


            sopa = sopa[sopa.find(referencia) + len(referencia):]
            
            while True:
                
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

            apagar_linhas(1)

            if menu1.cursor == 5:
                temp_list = list()
                for item in lista_proc:
                    
                    tl = get_name_from_file(item[0])

                    temp_list.append((item[0], item[1], tl))
                lista_proc = temp_list

            elif menu1.cursor == 4:

                for item in lista_proc:

                    lista = list(item)

                    lista[1] = int(item[1])+1

                    lista.append(get_name_from_file(item[0]))

                    play_ep(lista)

                    

                    

                    

                    
                    


