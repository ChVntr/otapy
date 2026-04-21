

def cnctvrf():

    try:
        #print('testamdo conexão')
        req = requests.get('https://myanimelist.net')
        sopa = str(bs4.BeautifulSoup(req.text, 'html.parser'))
        if sopa.find('500 Internal Server Error - MyAnimeList.net') == -1 and sopa != '':
            return False
        else: 
            nocom = True
            print(f'"{sopa[:300]}"')
    except Exception as e:
        nocom = True
        print(e)
        
    while nocom:
        print('FALHA DE CONExÃO!\nAGUARDANDO RESPOSTA DE "myanimelist.net"...'.lower())
        time.sleep(15)
        nocom = cnctvrf()

def sopapranois(link, return_url = False):

    print(link)

    if link == False or link == '': return False

    cnctvrf()

    try:
        page = requests.get(str(link), timeout=10)
    except requests.exceptions.RequestException as e:
        cnctvrf()
        print(e)
        if str(e).find('Invalid URL') != -1: return False
        return sopapranois(link)

    if return_url: return page.url

    soup = bs4.BeautifulSoup(page.text, 'html.parser')    

    if str(soup).find('<div id="captcha-container"></div>') != -1:
        if debug: prt(' captcha do inferno')
        return sopapranois(link)

    soup = str(soup)

    if soup == '': return False
    if soup.find('<title>404 Not Found') != -1: return False

    return soup

def prt(string, hold = False):

    if type(string) == tuple or type(string) == list:
        for item in string:
            prt(item)
    else:
        sys.stdout.write(str(string))

    if not hold: sys.stdout.flush()

def apagar_linhas(n):
    return
    if n < 1:
        sys.stdout.write('\r\033[J')
    else:
        sys.stdout.write(f"\033[{n}A \r\033[J")

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

def sopa_para_animes(sopa):

    sopa = sopa.replace('&quot;', '"')
    sopa = sopa.replace('\\/', '/')
    sopa = sopa.replace('\\"', '"')
    sopa = sopa[sopa.find('<table class="list-table"'):]

    frags_sopa = []

    while True:

        flags = find_all(sopa, '{"status"')

        if len(flags) < 1: 
            flags = find_all(sopa, '&quot;status&quot')

        if len(flags) < 1: 
            break

        if len(flags) < 2:
            frags_sopa.append(sopa[:sopa.find('">')])
            break

        frag = sopa[flags[0] : flags[1]]
        frags_sopa.append(frag)

        sopa = sopa[sopa.find(frag) + len(frag):]

    animes_lista = []

    for i in frags_sopa:
        anm = anime(i)
        animes_lista.append(anm)

    return animes_lista

def find_all(string, flag):
    
    og_str = string

    ocorrencias = []
    num = 0

    string = str(string)
    flag = str(flag)

    while string.find(flag) > -1:

        num += string.find(flag)
        ocorrencias.append(num)

        num += len(flag)

        string = og_str[num:]

    return ocorrencias


    avisei['text'] = ''

    usnm = usnm_box.get()

    response = str(requests.get(str(''.join(['https://myanimelist.net/profile/', usnm]))))
    if response.find('404') != -1: 
        avisei['text'] = 'Username invalido!'
        return False


    pass

def processtl(tl, mode=0):

    tl = tl.replace('Ü', 'U')
    tl = tl.replace("'", '')

    titulo = re.sub(r'[^a-zA-Z0-9]', ' ', tl) 

    while titulo.find('  ') != -1: titulo = titulo.replace('  ', ' ')    

    while titulo[-1] == ' ': titulo = titulo[:-1]
    while titulo[0] == ' ': titulo = titulo[1:]

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




class anime():
    def __init__(self, sopa_frag):

        vari_nomes = ('anime_title', 'status', 'is_rewatching', 'num_watched_episodes', 'anime_airing_status', 'anime_id', 'anime_num_episodes')
        variaveis = []

        for i in vari_nomes:
            vari = texto_no_meio(sopa_frag, f'"{i}":', ',"')
            variaveis.append(vari)

        self.anime_title = variaveis[0][1:-1]
        self.status = int(variaveis[1])
        self.is_rewatching = int(variaveis[2])
        self.num_watched_episodes = int(variaveis[3])
        self.anime_airing_status = int(variaveis[4])
        self.anime_id = int(variaveis[5])
        self.anime_num_episodes = int(variaveis[6])

        if self.is_rewatching == 1: self.status = self.is_rewatching

        self.generos = []
        generos = texto_no_meio(sopa_frag, '"genres":[', ']')
        generos_flags = find_all(generos, '"name":"')
        for i in generos_flags:
            genero = generos[i+8:]
            genero = genero[:genero.find('"')]
            self.generos.append(genero)
        
        self.titulo = False
        
        self.sopas = []

    def ad_titulo(self, titulo):
        self.titulo = titulo

    def get_sopa(self, link):

        #print(link)       

        for i in self.sopas:
            if link == i[0]: return i[1]

        sopa = sopapranois(link)

        if sopa == False: return False
        
        self.sopas.append((link, sopa))
        
        if self.titulo == False:
            titulo = texto_no_meio(sopa, '<h1 class="title-name">', '</h1>')
            if titulo != False: self.ad_titulo(titulo)
            else:
                titulo = texto_no_meio(sopa, '<strong>', '</strong>')
                if titulo != False: self.ad_titulo(titulo)
        
        return sopa

    def get_eps_sopa(self, offset):

        link = f'https://myanimelist.net/anime/{self.anime_id}/blabla/episode?offset={offset}'
        sopa = self.get_sopa(link)
        return sopa



def veri_usnm():

    for i in mestres: i.destroy()

    load_label.configure(text='Carregando...')
    janela.update()

    cnctvrf()

    usnm = usn_entry.get()
    if bypass: usnm = 'gahvius'

    response = str(requests.get(f'https://myanimelist.net/profile/{usnm}'))
    if response.find('404') != -1: 
        load_label.configure(text='Username invalido!')
        janela.update()
        print('\a')
    else: 
        #butaum.destroy()
        janela.update()
        abrir_lista1()
        return
    janela.update()

def abrir_lista1():

    usnm = usn_entry.get()
    if bypass: usnm = 'gahvius'


    lista_link = f'https://myanimelist.net/animelist/{usnm}?'

    param = stts_var.get()
    stts_param = 0
    num = tabelaço[0].index(param)+1
    if num > 4: num+=1
    lista_link += f'status={num}&'
    stts_param = num

    air_param = 0
    param = air_var.get()
    if param == 'Todos': param = None
    if param != None:
        num = tabelaço[1].index(param)+1
        lista_link += f'airing_status={num}&'
        air_param = num

    for i in ((s1_var, chk1_var, 'order'), (s2_var, chk2_var, 'order2')):
        param = i[0].get()
        if param != None:
            num = tabelaço[2].index(param)+1
            asc = (1, 6, 8, 16, )

            if num > 6: num += 1
            if num > 9: num += 1
            
            #print(i[1].get())

            if num not in asc: num *= -1
            if i[1].get(): num *= -1
            
            lista_link += f'{i[2]}={num}&'

    sopa = sopapranois(lista_link)
    lista_animes = sopa_para_animes(sopa)
    lista_animes2 = []

    if air_param != 0 and stts_param != 0:
        for i in lista_animes:
            if stts_param == 7: lista_animes2.append(i)
            elif i.status == stts_param: lista_animes2.append(i)
    else: lista_animes2 = lista_animes

    load_label.configure(text='')

    abrir_lista2(lista_animes2)

def abrir_lista2(lista):

    lista_frame_r = []

    frame_master2 = tkinter.Frame(frame_master_master)
    mestres.append(frame_master2)

    frame_master3 = tkinter.Frame(frame_master_master)
    #frame_master3.pack()

    dub_chk = tkinter.Checkbutton(frame_master3, variable=dub_chk_var, text='Dublado')
    dub_chk.pack(side='left')

    sub_chk = tkinter.Checkbutton(frame_master3, variable=sub_chk_var, text='Legendado')
    sub_chk.pack()
    
    mestres.append(frame_master3)
    frame_master3.pack(after=frame_master1, side='bottom')
    frame_master2.pack(fill='both', expand=True, side='right', )
    

    if len(lista) < 1: 
        tkinter.Label(frame_master2, text='Lista vazia ¯\\_(ツ)_/¯').pack(anchor='center')
        return

    frame_l = tkinter.Frame(frame_master2)
    frame_l.pack(fill='both', expand=True, side='left')

    canvas_l = tkinter.Canvas(frame_l)
    canvas_l.pack(side='left', fill='both', expand=True)

    scroll_anime = tkinter.Scrollbar(frame_l, command=canvas_l.yview)
    scroll_anime.pack(side='right', fill='y')
    canvas_l.configure(yscrollcommand=scroll_anime.set)

    frame_ani_but = tkinter.Frame(canvas_l)
    frame_ani_but.bind(
        "<Configure>",
        lambda e: canvas_l.configure(scrollregion=canvas_l.bbox("all"))
)
    canvas_l.create_window((0, 0), window=frame_ani_but, anchor="nw")

    for i in range(len(lista)):
        tkinter.Button(frame_ani_but, text=lista[i].anime_title, command=lambda i=i: abrir_anime(lista[i])).pack(anchor='w', padx=4, pady=2)
    
    

    print('\a')

        

    def abrir_anime(ani):

        print(ani.anime_title)

        for i in lista_frame_r: 
            i.destroy()
        frame_r = tkinter.Frame(frame_master2)
        frame_r.pack(fill='both', expand=True, side='right', anchor='e')
        lista_frame_r.clear()
        lista_frame_r.append(frame_r)


        def pegar_os_eps():
            frame_load = tkinter.Frame(frame_r)
            frame_load.pack()

            load_label = tkinter.Label(frame_load, text='Carregando episodios...')
            load_label.pack()

            janela.update()

            offset = ani.num_watched_episodes - 50
            if offset < 0: offset = 0

            sopa_eps = ani.get_eps_sopa(offset)
            sopa_eps = texto_no_meio(sopa_eps, '<tr class="episode-list-data">', '</table>', prsv_começo=True)

            finais = (0,) + tuple(find_all(sopa_eps, '</td></tr>'))

            eps_lista = []
            if sopa_eps != False:
                for i in range(len(finais)-1):
                    chunk = sopa_eps[finais[i]:finais[i+1]]
                    epnum = int(texto_no_meio(chunk, '<td class="episode-number nowrap" data-raw="', '">'))
                    ep_nome = texto_no_meio(chunk, f'/episode/{epnum}">', '</a>')
                    
                    eps_lista.append((epnum, ep_nome))

            total_eps = ani.anime_num_episodes
            if total_eps < 1: total_eps = ani.num_watched_episodes + 12

            while len(eps_lista) < total_eps:

                if len(eps_lista) < 1:
                    eps_lista.append((1, ''))
                    
                eps_lista.append((eps_lista[-1][0]+1, ''))

                if eps_lista[0][0] != 1:
                    eps_lista.insert(0, (eps_lista[0][0]-1, ''))
                    
                    

            frame_load.destroy()
            return eps_lista

        def ant_ep():

            primeiro_ep = eps_lista[0][0]

            offset = primeiro_ep - 50
            if offset < 0: offset = 0

            sopa_eps = ani.get_eps_sopa(offset)
            sopa_eps = texto_no_meio(sopa_eps, '<tr class="episode-list-data">', '</table>', prsv_começo=True)

            finais = (0,) + tuple(find_all(sopa_eps, '</td></tr>'))

            prv_eps_lista = []
            if sopa_eps != False:
                for i in range(len(finais)-1):
                    chunk = sopa_eps[finais[i]:finais[i+1]]
                    epnum = int(texto_no_meio(chunk, '<td class="episode-number nowrap" data-raw="', '">'))
                    ep_nome = texto_no_meio(chunk, f'/episode/{epnum}">', '</a>')
                    
                    if epnum < eps_lista[0][0]: prv_eps_lista.append((epnum, ep_nome))

            prv_eps_lista.reverse()

            for i in prv_eps_lista:
                eps_lista.insert(0,i)

            for i in ep_butoes: i.destroy()
            ep_butoes.clear()

            ult_botao = prv_bt
            for i in range(len(eps_lista)):
                bt = tkinter.Button(frame_eps_but, text=f'{eps_lista[i][0]} - {eps_lista[i][1]}', command=lambda i=i: rep_ep(ani, eps_lista[i][0]))
                if eps_lista[i][0] <= ani.num_watched_episodes: bt.config(fg='grey')
                bt.pack(anchor='w', padx=4, pady=2, after=ult_botao)
                ult_botao = bt
                ep_butoes.append(bt)

            n_bts = len(ep_butoes) + 2

            if eps_lista[0][0] == 1: 
                n_bts -= 1
                prv_bt.destroy()

            canvas_r.update_idletasks()
            frac = (ani.num_watched_episodes - primeiro_ep) / n_bts
            canvas_r.yview_moveto(frac * 0.96)

            janela.update()

        def prox_ep():

            offset = eps_lista[-1][0]

            sopa_eps = ani.get_eps_sopa(offset)
            sopa_eps = texto_no_meio(sopa_eps, '<tr class="episode-list-data">', '</table>', prsv_começo=True)

            finais = (0,) + tuple(find_all(sopa_eps, '</td></tr>'))

            prv_eps_lista = []
            if sopa_eps != False:
                for i in range(len(finais)-1):
                    chunk = sopa_eps[finais[i]:finais[i+1]]
                    epnum = int(texto_no_meio(chunk, '<td class="episode-number nowrap" data-raw="', '">'))
                    ep_nome = texto_no_meio(chunk, f'/episode/{epnum}">', '</a>')
                    
                    if epnum > eps_lista[-1][0]: prv_eps_lista.append((epnum, ep_nome))


            while len(prv_eps_lista) < 50:

                if len(prv_eps_lista) < 1:
                    prv_eps_lista.append((eps_lista[-1][0]+1, ''))
                    
                prv_eps_lista.append((prv_eps_lista[-1][0]+1, ''))
                    
            #prv_eps_lista.reverse()

            for i in prv_eps_lista:
                eps_lista.append(i)

            for i in ep_butoes: i.destroy()
            ep_butoes.clear()

            for i in range(len(eps_lista)):
                bt = tkinter.Button(frame_eps_but, text=f'{eps_lista[i][0]} - {eps_lista[i][1]}', command=lambda i=i: rep_ep(ani, eps_lista[i][0]))
                if eps_lista[i][0] <= ani.num_watched_episodes: bt.config(fg='grey')

                bt.pack(anchor='w', padx=4, pady=2, before=nxt_bt)
                ep_butoes.append(bt)

            janela.update()


        eps_lista = pegar_os_eps()

        tl_tx = tkinter.Label(frame_r, text=ani.titulo)
        tl_tx.pack()

        tkinter.Checkbutton(frame_r, text=('Reproduzir sem pausas'), variable=sempausa_chk_var).pack(side='top', anchor='w', pady=10)

        canvas_r = tkinter.Canvas(frame_r)
        canvas_r.pack(side='left', fill='both', expand=True)

        scroll_eps = tkinter.Scrollbar(frame_r, command=canvas_r.yview)
        scroll_eps.pack(side='right', fill='y')
        canvas_r.configure(yscrollcommand=scroll_eps.set)

        frame_eps_but = tkinter.Frame(canvas_r)
        frame_eps_but.bind("<Configure>", lambda e: canvas_r.configure(scrollregion=canvas_r.bbox("all")))
        
        canvas_r.create_window((0, 0), window=frame_eps_but, anchor="nw")

        n_bts = eps_lista[-1][0] - eps_lista[0][0]

        if eps_lista[0][0] != 1:
            prv_bt = tkinter.Button(frame_eps_but, text='Carregar eps anteriores', command= ant_ep)
            prv_bt.pack(anchor='w', padx=4, pady=10)
            n_bts += 1

        ep_butoes = []
        for i in range(len(eps_lista)):
            bt = tkinter.Button(frame_eps_but, text=f'{eps_lista[i][0]} - {eps_lista[i][1]}', command=lambda i=i: rep_ep(ani, eps_lista[i][0]))
            if eps_lista[i][0] <= ani.num_watched_episodes: bt.config(fg='grey')
            bt.pack(anchor='w', padx=4, pady=2)
            ep_butoes.append(bt)

        nxt_bt = tkinter.Button(frame_eps_but, text='Carregar mais eps', command=prox_ep)
        nxt_bt.pack(anchor='w', padx=4, pady=10)
        n_bts += 1

        canvas_r.update_idletasks()
        frac = (ani.num_watched_episodes - eps_lista[0][0]) / n_bts
        canvas_r.yview_moveto(frac * 0.9)
        
        def rep_ep(ani, ep):

            if ani.titulo == False: ani.get_sopa(f'https://myanimelist.net/anime/{ani.anime_id}')

            print(ani.titulo, ep)

            def animesdigitalorg(dub=False):

                
                tl = ani.titulo
                str_ep = str(ep)
                if len(str_ep) < 2: str_ep = f'0{str_ep}'
                
                tl_dif = ((392, 'Yu Yu Hakusho'),
                        )

                for i in tl_dif:
                    if ani.anime_id == i[0]:
                        tl = i[1]
                        break

                link = f'https://animesdigital.org/search/{processtl(tl).replace(' ', '+')}'
                sopa = sopapranois(link)

                if dub: tl += ' Dublado'
                if sopa.find(f'title="Assistir {tl} Online em HD"') != -1:

                    link = sopa[:sopa.find(f'title="Assistir {tl} Online em HD"')]
                    link = link[link.rfind('href="'):]
                    link = texto_no_meio(link, '"', '"')
                    
                    sopa = sopapranois(link)
                    link = sopa[:sopa.find('property="og:url"')]
                    link = link[link.rfind('https://animesdigital.org/anime/'):-2]

                    if sopa != False and sopa.find('<div class="msg404">') == -1:

                        tl_in_sopa = texto_no_meio(sopa, '<title>', '</title>')
                        if tl_in_sopa.find('Dublado') != -1: db = True
                        else: db = False
                        
                        if db == dub:
                        
                            ep_topo = texto_no_meio(sopa, '<div class="title_anime">', '</div>', prsv_final=True)
                            ep_topo = texto_no_meio(ep_topo, 'Episódio ', '</div>')
                        
                            deubom = False
                            try:
                                ep_topo = int(ep_topo)
                                if ep_topo >= ep: deubom = True
                            except:
                                pass

                            if deubom:

                                if sopa.find(f'Episódio {str_ep}</div>') == -1:

                                    ep_topo = texto_no_meio(sopa, '<div class="title_anime">', '</div>', prsv_final=True)
                                    ep_topo = texto_no_meio(ep_topo, 'Episódio ', '</div>')

                                    page = int((int(ep_topo) - ep)/50)+1

                                    link = f'{link}/page/{page}/'
                                    sopa = sopapranois(link)

                                    if sopa.find(f'Episódio {str_ep}</div>') == -1: deubom = False

                                if deubom:

                                    link = sopa[:sopa.rfind(f'Episódio {str_ep}</div>')]
                                    link = link[link.rfind('https://animesdigital.org/video/'):]
                                    link = link[:link.find('"')]
                                    sopa = sopapranois(link)

                                    ep_links = []
                                    while sopa.find('class="metaframe rptss no-lazy"') != -1:
                                        ep_link = texto_no_meio(sopa, 'class="metaframe rptss no-lazy"', '>')
                                        ep_link = texto_no_meio(ep_link, 'https', '"', True)

                                        ep_links.append(ep_link.replace('&amp;', '&'))
                                        sopa = sopa[sopa.find(ep_link):]
                                    
                                    ep_links2 = []
                                    for i in ep_links:
                                        sopa = sopapranois(i)

                                        if sopa.find('<title>Animes Online - Assistir Animes Online Grátis</title>') != -1: continue

                                        if sopa.find('var player = jwplayer') != -1:
                                            link = texto_no_meio(i, 'https://cdn-', 'index.m3u8', True, True)
                                            ep_links2.append(link)
                                            continue
                                            link = texto_no_meio(sopa, "file: '", "'")
                                            if link != False: 
                                                ep_links2.append(link)
                                                continue
                                        
                                        print('sopinha diferenciada')

                                    for a in ep_links2:
                                        foi = rep_ep2(a)
                                        if foi: return True

                return False

            def animefire(dub=False):

                tl = ani.titulo
                #tl = processtl(tl)
                #tl = tl.replace(' ', '-').lower()

                sopa = sopapranois(f'https://animefire.io/pesquisar/{processtl(tl).replace(' ', '-').lower()}')

                if sopa != False:

                    if dub: tl += ' (Dublado)'
                    print(tl)

                    if sopa.find(tl) != -1:

                        link = sopa[:sopa.find(f'<h3 class="animeTitle">{tl}</h3>')]
                        link = link[link.rfind('https://animefire.io/animes/'):]
                        #print(link)
                        res_tl = texto_no_meio(link, '/animes/', '-todos-os-episodios"')

                        if res_tl != False:

                            link = f'https://animefire.io/video/{res_tl}/{ep}'
                            sopa = sopapranois(link)

                            if sopa!= False:

                                sopa = sopa.replace('\\', '')

                                srcs = find_all(sopa, '"src":"')
                                #print(srcs)

                                links = []
                                for i in srcs:
                                    
                                    link = texto_no_meio(sopa[i:], ':"', '"')
                                    if link != False: 
                                        if link.find('/mp4_temp/') == -1: links.append(link)
                                        else: print('é temp')

                                link = links.reverse()

                                for i in links:
                                    print(i)
                                    res = rep_ep2(i)
                                    if res == True: return True

                return False

            def topanimes(dub=False):
                
                tl = ani.titulo

                #tl = tl.replace('rd Season', '')
                tl_dif = ((55825, 'Jigokuraku 2'),
                        (60058, '[Oshi no Ko] 3'),
                        (62568, 'Dr. Stone: Science Future'),
                        )
                
                ep_dif_list = ((62568, 24),
                        )

                for i in tl_dif:
                    if ani.anime_id == i[0]:
                        tl = i[1]
                        break

                ep_dif = 0
                for i in ep_dif_list:
                    if ani.anime_id == i[0]:
                        ep_dif = i[1]
                        break

                link = f'https://topanimes.net/?s={processtl(tl).replace(' ', '+')}'
                sopa = sopapranois(link)

                flags = find_all(sopa, '<div class="result-item">')

                link = False

                if dub: tl += ' Dublado'
                for i in flags:
                    chunk = sopa[i:sopa[i:].find('</div>')+i]
                    res_title = texto_no_meio(chunk, '<img alt="', '"')
                    if res_title == tl: link = texto_no_meio(chunk, 'href="', '"')

                if link != False:

                    tl_url = texto_no_meio(link, '/animes/', '/')
                    link = f'https://topanimes.net/episodio/{tl_url}-episodio-{ep+ep_dif}/'

                    sopa = sopapranois(link)

                    flags = find_all(sopa, 'id="source-player-')

                    links = []

                    putaria = (
                        ('%2F', '/'),
                        ('%3A', ':'),
                        ('%3F', '?'),
                        ('%3D', '='),
                        ('&amp;', '&'),
                        ('%23', '#'),
                        ('%26', '&'),
                    )

                    ignorar = ('/filemoon.sx/', 
                            '/png.strp2p.com/', 
                            '/f-cdn/', 
                            '/streamingverde.com/',
                            )
                    
                    ignorar2 = ('<h1>Erro: Vídeo não encontrado.</h1>',
                                )

                    for i in flags:

                        chunk = sopa[i:sopa[i:].find('</iframe>')+i]
                        if chunk.find('"source-player-trailer"') != -1: continue
                        link = texto_no_meio(chunk, 'src="', '"')
                        if link != False:

                            for i in putaria:
                                link = link.replace(i[0], i[1])

                            links.append(link)

                    for i in links:

                        nope = False
                        for i2 in ignorar:
                            if i.find(i2) != -1: 
                                nope = True
                                break
                        if nope: continue

                        link = i

                        if link.find('/aviso/?url=') != -1:
                            link = texto_no_meio(link, '?url=', '&')
                            if link == False: continue

                        sopa = sopapranois(link)

                        if sopa != False:

                            nope = False
                            for i2 in ignorar2:
                                if sopa.find(i2) != -1: 
                                    nope = True
                                    break
                            if nope: continue

                            if sopa.find('.m3u8') != -1:
                                link = sopa[:sopa.rfind('.m3u8')+5]
                                link = link[link.rfind('https:'):]
                                foi = rep_ep2(link)
                                if foi: return True

                            if sopa.find('.mp4') != -1:
                                link = sopa[:sopa.rfind('.mp4')+4]
                                link = link[link.rfind('https:'):]
                                if link.find('/media.discordapp.net/') == -1:
                                    foi = rep_ep2(link)
                                    if foi: return True



                        print('sopinha interessante')

                return False

            provedores = (topanimes, animesdigitalorg, animefire)
            #provedores = (topanimes,)

            dub_var = []
            if dub_chk_var.get(): dub_var.append(True)
            if sub_chk_var.get(): dub_var.append(False)
            
            for i in dub_var:
                for i2 in provedores:
                    foi = i2(i)
                    if foi: break
                if foi: break

            if sempausa_chk_var.get():
                if foi: rep_ep(ani, ep+1)
                else: 
                    pos_in_lista = 0
                    for anime in lista:
                        if anime == ani: break
                        pos_in_lista += 1
                    if pos_in_lista+1 < len(lista):
                        abrir_anime(lista[pos_in_lista+1])
                        rep_ep(lista[pos_in_lista+1], lista[pos_in_lista+1].num_watched_episodes+1)


def rep_ep2(file_link):

    print(file_link)

    #return False

    filename = f'{os.path.expanduser("~")}/otapy/anitemp.mp4'
    with open(filename, 'w') as f:

        #print('iniciando download do ep')
        down_st = time.perf_counter()

        #f.write(requests.get(file_link).content)
        f.write(file_link)
        #print(f'download terminado em {time.perf_counter() - down_st}s')
        f.close()

        subp = subprocess.run(filename, shell=True, stdout=True)
        os.remove(filename)

        if subp.returncode != 0: return False
        return True



#imports
import requests
import subprocess
import sys
import bs4
import os
import time
import re
import webbrowser
import tkinter
import flet

run = True
sopas = []
debug = False
save_existe = False
bypass = False
mestres = []

#tabelas
tabelaço = (('Assistindo', 'Completos', 'Em Espera', 'Droppados', 'Planejo Assistir', 'Todos'),
            
            ('Em Exibição', 'Exibido', 'Não Exibido', 'Todos'),
            
            ('Titulo',
             'Finish Date',
             'Start Date',
             'Score',
             'Ultimo Update',
             'Tipo',
            
             'Avaliação',
             'Valor de Rewatch',
            
             'Prioridade',
             'Eps Assistidos',
             'Armazenamento',
             'Air Start Date',
             'Air End Date',
             'Status',
             'MAL Score',
             'Dif de Score.',
             'Popularidade'),
)

opts_menu1 = ('MAL username', 
              'Status', 
              'Status de lançamento', 
              'Primeiro sort', 
              'Segundo sort')




os.makedirs(f'{os.path.expanduser("~")}/otapy/', exist_ok=True)


janela = tkinter.Tk()
#janela.geometry('1280x720')
janela.title('OtaPy 3')

frame_master_master = tkinter.Frame(janela)
frame_master_master.pack(fill='both', expand=True, anchor='nw') 
frame_master_l = tkinter.Frame(frame_master_master)
frame_master_l.pack(side='left', anchor='n')
frame_master1 = tkinter.Frame(frame_master_l)
frame_menu1 = tkinter.Frame(frame_master1)




c1_list = []
c2_list = []

usn_entry = tkinter.Entry(frame_menu1)
c1_list.append(usn_entry)

stts_var = tkinter.StringVar()
stts_drop = tkinter.OptionMenu(frame_menu1, stts_var, *tabelaço[0])
c1_list.append(stts_drop)

air_var = tkinter.StringVar()
air_drop = tkinter.OptionMenu(frame_menu1, air_var, *tabelaço[1])
c1_list.append(air_drop)

s1_var = tkinter.StringVar()
s1_drop = tkinter.OptionMenu(frame_menu1, s1_var, *tabelaço[2])
c1_list.append(s1_drop)

s2_var = tkinter.StringVar()
s2_drop = tkinter.OptionMenu(frame_menu1, s2_var, *tabelaço[2])
c1_list.append(s2_drop)

chk1_var = tkinter.BooleanVar()
chk1 = tkinter.Checkbutton(frame_menu1, variable=chk1_var, text='Decrescente')
c2_list.append(chk1)

chk2_var = tkinter.BooleanVar()
chk2 = tkinter.Checkbutton(frame_menu1, variable=chk2_var, text='Decrescente')
c2_list.append(chk2)

frame = tkinter.Frame(frame_master1)
frame2 = tkinter.Frame(frame_master1)

butaum = tkinter.Button(frame, text='Abrir lista', command=(veri_usnm))

load_label = tkinter.Label(frame, text='')

if not save_existe:
    stts_var.set(tabelaço[0][5])
    air_var.set(tabelaço[1][3])
    s1_var.set(tabelaço[2][13])
    s2_var.set(tabelaço[2][0])
    chk1_var.set(False)
    chk2_var.set(False)

n_row = 0
for i in opts_menu1:
    tkinter.Label(frame_menu1, text=i).grid(row=n_row, column=0)
    n_row+=1

n_row = 0
for i in c1_list: 
    i.grid(row=n_row, column=1)
    n_row+=1

n_row = 3
for i in c2_list: 
    i.grid(row=n_row, column=2)
    n_row+=1

frame_menu1.pack(anchor='n', fill='both')
frame.pack()
frame2.pack()
butaum.pack(pady=(20, 0))
load_label.pack(pady=(20, 0))

frame_master1.pack(anchor='nw', padx=(0,20))

dub_chk_var = tkinter.BooleanVar()
dub_chk_var.set(False)
sub_chk_var = tkinter.BooleanVar()
sub_chk_var.set(True)
sempausa_chk_var = tkinter.BooleanVar()
sempausa_chk_var.set(False)






if bypass:
    veri_usnm()


#ex_anime = sopa_para_animes(sopapranois('https://myanimelist.net/animelist/Gahvius?order=5&status=7'))[0]
#rep_ep(ex_anime, 5)
#exit()


janela.mainloop()