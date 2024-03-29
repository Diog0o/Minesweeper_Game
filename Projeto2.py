#2.1.1

def cria_gerador (b,s):
    """
    int x int → gerador
    Recebe um inteiro b correspondente ao número de bits
    do gerador e um inteiro positivo s correspondente à seed ou estado inicial,
    e devolve o gerador correspondente
    """
    if (type(b) != int or (b != 32 and b!= 64) or type(s)!= int or s<=0):
        raise ValueError("cria_gerador: argumentos invalidos")
    if b == 32:
        if s > (2**32) -1:
            raise ValueError("cria_gerador: argumentos invalidos")
    if b == 64:
        if s > (2**64) -1:
            raise ValueError("cria_gerador: argumentos invalidos")
    return {"dimensao":b , "seed":s , "estado": s}

def cria_copia_gerador (g):
    """
    gerador → gerador
    Recebe um gerador e devolve uma cópia nova do gerador.
    """
    return {"dimensao": g["dimensao"], "seed": g["seed"],\
         "estado": g["estado"]}

def obtem_estado (g):
    """
    gerador → int
    Devolve o estado atual do gerador g sem o alterar.
    """
    return g["estado"]

def define_estado (g,s):
    """
    gerador x int → int
    Define o novo valor do estado do gerador g como sendo s,
    e devolve s.
    """
    g["estado"] = s
    return s

def atualiza_estado (g):
    """
    gerador → int
    Atualiza o estado do gerador g de acordo com o algoritmo
    xorshift de geração de números pseudoaleatórios, e devolve-o
    """
    if (g["dimensao"] == 32):
        s = g["estado"]
        s ^= ( s << 13 ) & 0xFFFFFFFF
        s ^= ( s >> 17 ) & 0xFFFFFFFF
        s ^= ( s << 5 ) & 0xFFFFFFFF
        g["estado"] = s
    else:
        s = g["estado"]
        s ^= ( s << 13 ) & 0xFFFFFFFFFFFFFFFF
        s ^= ( s >> 7 ) & 0xFFFFFFFFFFFFFFFF
        s ^= ( s << 17 ) & 0xFFFFFFFFFFFFFFFF
        g["estado"] = s
    return s

def eh_gerador (arg):
    """
    universal → booleano
    Devolve True caso o seu argumento seja um TAD gerador e
    False caso contrário
    """
    if type(arg) != dict or "dimensao" not in arg or\
         "seed" not in arg or "estado" not in arg:
        return False
    if arg["dimensao"] != 32 and arg["dimensao"] != 64:
        return False
    if type(arg["seed"]) != int or arg["seed"] < 0 \
    or type(arg["estado"]) != int or arg["estado"] < 0:
        return False
    return True

def geradores_iguais (g1,g2):
    """
    gerador x gerador → booleano
    Devolve True apenas se g1 e g2 são geradores e são
    iguais
    """
    if (eh_gerador(g1) and eh_gerador (g2)):
        if g1["dimensao"] == g2["dimensao"] and g1["seed"] == g2["seed"]\
             and g1["estado"] == g2["estado"]:
            return True
    return False

def gerador_para_str(g):
    """
    gerador → str
    Devolve a cadeia de carateres que representa o seu argumento
    da forma, como por exemplo "xorshift32(s=1)"
    """
    return "xorshift" + str(g["dimensao"]) + "(s=" +  str(g["estado"]) +")"



def gera_numero_aleatorio (g,n):
    """
    gerador x int → int
    Atualiza o estado do gerador g e devolve um número
    aleatório no intervalo [1, n] obtido a partir do novo estado s.

    """
    atualiza_estado(g)
    return 1 + obtem_estado(g) % n
    
def gera_carater_aleatorio (g,c):
    """
    gerador x str → str
    Atualiza o estado do gerador g e devolve um caráter
    aleatório no intervalo entre "A" e o caráter maiúsculo c.
    """
    atualiza_estado(g)
    l = ord(c) - ord("A") + 1
    return chr( ord("A") + obtem_estado(g) % l)





#2.1.2

def cria_coordenada (col,lin):
    """
    str x int → coordenada
    Recebe os valores correspondentes à coluna col e
    linha lin e devolve a coordenada correspondente. Verifica os argumentos 
    """
    if type(col) != str or type(lin) != int or len(col) != 1 \
        or lin>99 or lin <1 or ord(col) < ord("A") or ord(col)> ord("Z") :
        raise ValueError("cria_coordenada: argumentos invalidos")
    else:
        return (col,lin)


def obtem_coluna(c):
    """ 
    coordenada → str
    Devolve a coluna col da coordenada c.
    """
    return c[0]
    
def obtem_linha(c):
    """
    coordenada → int
    Devolve a linha lin da coordenada c.
    """
    return c[1]


def eh_coordenada(arg):
    """
    universal → booleano
    Devolve True caso o seu argumento seja um TAD coordenada e 
    False caso contrário.
    """
    if type(arg) != tuple or len(arg) != 2:
        return False
    if  type(arg[0])!=str or len(arg[0]) != 1 \
         or ord(arg[0]) < ord("A") or ord(arg[0])> ord("Z")\
             or type(arg[1]) != int or int(arg[1])>99 or (arg[1])<1 :
        return False
    return True

def coordenadas_iguais (c1,c2):
    """
    coordenada x coordenada → booleano
    Devolve True apenas se c1 e c2 são coordenadas e
    são iguais.
    """
    if not eh_coordenada(c1) or not eh_coordenada(c2):
        return False
    if obtem_coluna(c1) == obtem_coluna(c2) and\
         obtem_linha(c1) == obtem_linha(c2):
        return True
    return False

def coordenada_para_str(c):
    """
    coordenada → str
    Devolve a cadeia de carateres que representa o seu
    argumento, como no exemplo A01.
    """
    if obtem_linha(c) >= 10:
        return obtem_coluna(c) + str(obtem_linha(c))
    else:
        return obtem_coluna(c) + "0" + str(obtem_linha(c))

def str_para_coordenada(s):
    """
    str → coordenada
    Devolve a coordenada reapresentada pelo seu argumento.
    """
    if s[1] == 0:
        return cria_coordenada(s[0], int(s[2]))
    else:
        return cria_coordenada(s[0],int(s[1:]))


def obtem_coordenadas_vizinhas (c):
    """
    coordenada → tuplo
    devolve um tuplo com as coordenadas vizinhas à coordenada c, começando 
    pela coordenada na diagonal acima-esquerda de c e seguindo no sentido 
    horário.
    """
    res=()
    coluna = obtem_coluna(c)
    linha =obtem_linha(c)
    c1=(chr(ord(coluna)-1), linha - 1)
    c8=(chr(ord(coluna)-1), linha)
    c7=(chr(ord(coluna)-1), linha + 1)
    c6=(coluna, linha + 1)
    c5=(chr(ord(coluna)+1), linha +1)
    c4=(chr(ord(coluna)+1), linha)
    c3=(chr(ord(coluna)+1), linha-1)
    c2=(coluna, linha -1)
    res_provisorio=(c1,c2,c3,c4,c5,c6,c7,c8)
    for i in res_provisorio:
        if ord(i[0]) >= ord("A") and ord(i[0]) <= ord("Z")\
             and i[1] <=99 and i[1] >=1:
            res= res + (cria_coordenada(i[0],i[1]),)
    return res

def obtem_coordenada_aleatoria(c,g):
    """
    coordenada x gerador → coordenada
    Recebe uma coordenada c e um TAD gerador g, e devolve uma coordenada
    gerada aleatoriamente. c define a maior coluna e maior linha possíveis.
    """
    coluna_aleatoria = gera_carater_aleatorio(g, obtem_coluna(c))
    linha_aleatoria = gera_numero_aleatorio(g, obtem_linha(c))
    return cria_coordenada(coluna_aleatoria,linha_aleatoria)



# 2.1.3

def cria_parcela ():
    """
    {} → parcela
    Devolve uma parcela tapada sem mina escondida.
    """
    return {"estado": "tapada", "mina": "nao"}

def cria_copia_parcela (p):
    """
    parcela → parcela
    Recebe uma parcela p e devolve uma nova cópia da parcela.
    """
    return {"estado": p["estado"], "mina": p["mina"]}

def limpa_parcela (p):
    """
    parcela → parcela
    Modifica destrutivamente a parcela p modificando o seu estado para limpa,
    e devolve a própria parcela.
    """
    p["estado"] = "limpa"
    return p

def marca_parcela (p):
    """
    parcela → parcela
    Modifica destrutivamente a parcela p modificando o seu estado para marcada
    com uma bandeira, e devolve a própria parcela.
    """
    p["estado"] = "marcada"
    return p

def desmarca_parcela (p):
    """
    parcela → parcela
    Modifica destrutivamente a parcela p modificando o seu estado para tapada, 
    e devolve a própria parcela.
    """
    p["estado"] = "tapada"
    return p

def esconde_mina (p):
    """
    parcela → parcela
    Modifica destrutivamente a parcela p escondendo uma mina na parcela, 
    e devolve a própria parcela.
    """
    p["mina"] = "sim"
    return p

def eh_parcela (arg):
    """
    universal → booleano
    Devolve True caso o seu argumento seja um TAD parcela e
    False caso contrário
    """
    if type(arg) != dict or "estado" not in arg or "mina" not in arg:
        return False
    if (arg["estado"] != "tapada" and arg["estado"] != "limpa" \
        and arg["estado"] != "marcada" ) or (arg["mina"] != "sim" \
            and arg["mina"] != "nao"):
        return False
    return True

def eh_parcela_tapada (p):
    """
    parcela → booleano
    Devolve True caso a parcela p se encontre tapada e False caso contrário.
    """
    if (eh_parcela(p)):
        if (p["estado"] == "tapada"):
            return True
    return False

def eh_parcela_marcada (p):
    """
    parcela → booleano
    Devolve True caso a parcela p se encontre marcada com uma bandeira e False
    caso contrário.
    """
    if (eh_parcela(p)):
        if (p["estado"] == "marcada"):
            return True
    return False

def eh_parcela_limpa (p):
    """
    parcela → booleano
    Devolve True caso a parcela p se encontre limpa e False
    caso contrário.
    """
    if (eh_parcela(p)):
        if (p["estado"] == "limpa"):
            return True
    return False

def eh_parcela_minada (p):
    """
    parcela → booleano
    Devolve True caso a parcela p esconda uma mina e False caso contrário.
    """
    if (eh_parcela(p)):
        if (p["mina"] == "sim"):
            return True
    return False

def parcelas_iguais(p1,p2):
    """
    parcela x parcela → booleano
    Devolve True apenas se p1 e p2 são parcelas e são iguais.
    """
    if (eh_parcela(p1) and eh_parcela(p2)):
        if (p1["estado"] == p2["estado"] and p1["mina"] == p2["mina"]):
            return True
    return False

def parcela_para_str (p):
    """
    parcela → str
    Devolve a cadeia de caracteres que representa a parcela
    em função do seu estado: parcelas tapadas ("#"), parcelas marcadas ("@"),
    parcelas limpas sem mina ("?") e parcelas limpas com mina ("X").
    """
    if p["estado"] == "tapada":
        return "#"
    if p["estado"] == "marcada":
        return "@"
    if p["estado"] == "limpa" and p["mina"] == "nao":
        return "?"
    else:
        return "X"

def alterna_bandeira(p):
    """
    parcela → booleano
    Recebe uma parcela p e modifica-a destrutivamente da seguinte
    forma: desmarca se estiver marcada e marca se estiver tapada,
    devolvendo True.
    Em qualquer outro caso, não modifica a parcela e devolve False.
    """
    if eh_parcela_marcada(p):
        desmarca_parcela(p)
        return True
    if eh_parcela_tapada(p):
        marca_parcela(p)
        return True
    return False


#2.1.4

def cria_campo (c,l):
    """
    str x int → campo
    Recebe uma cadeia de carateres e um inteiro correspondentes
    à última coluna e à última linha de um campo de minas, e devolve o campo
    do tamanho pretendido formado por parcelas tapadas sem minas.
    Verifica argumentos.
    """
    if type(c) != str or type(l) != int or len(c) != 1 \
        or ord(c) < ord("A") or ord(c)> ord("Z") or l>99 or l<1:
        raise ValueError("cria_campo: argumentos invalidos")     
    try:        
        res={}
        for j in range (1,l +1):
            for i in range (ord("A"), ord(c) +1):  
                coordenada= cria_coordenada(chr(i),j)
                res[coordenada] = cria_parcela()
        return res
    except:
        raise ValueError("cria_campo: argumentos invalidos")

def cria_copia_campo(m):
    """
    campo → campo
    Recebe um campo e devolve uma nova cópia do campo.
    """
    res={}
    for coordenadas in m:
        res[coordenadas] = cria_copia_parcela(m.get(coordenadas))
    return res


def obtem_ultima_coluna(m):
    """
    campo → str
    Devolve a cadeia de caracteres que corresponde à última coluna do 
    campo de minas.
    """
    lista = list(m.keys())
    return obtem_coluna(lista[-1])

def obtem_ultima_linha(m):
    """
    campo → int
    Devolve o valor inteiro que corresponde à última linha do campo de minas.
    """
    lista = list(m.keys())
    return obtem_linha(lista[-1])

def obtem_parcela(m,c):
    """
    campo x coordenada → parcela
    Devolve a parcela do campo m que se encontra na coordenada c.
    """
    return m.get(c)


def obtem_coordenadas (m,s):
    """
    campo x str → tuplo
    Devolve o tuplo formado pelas coordenadas ordenadas dependendo do valor
    de s: "limpas" para as parcelas limpas, "tapadas" para
    as parcelas tapadas, "marcadas" para as parcelas marcadas, e "minadas"
    para as parcelas que escondem minas.
    """
    res=()
    if s == "tapadas":
        for i in m:
            if eh_parcela_tapada(obtem_parcela(m,i)):
                res= res + (i,)
    if s == "limpas":
        for i in m:
            if eh_parcela_limpa(obtem_parcela(m,i)):
                res= res + (i,)
    if s == "marcadas":
        for i in m:
            if eh_parcela_marcada(obtem_parcela(m,i)):
                res= res + (i,)
    if s == "minadas":
        for i in m:
            if eh_parcela_minada(obtem_parcela(m,i)):
                res= res + (i,)
    return res


def obtem_numero_minas_vizinhas (m,c):
    """
    campo x coordenada → int
    Devolve o número de parcelas vizinhas da parcela na coordenada c 
    que escondem uma mina.
    """
    coord_vizinhas = obtem_coordenadas_vizinhas(c)
    res= 0
    for i in coord_vizinhas:
        if eh_parcela_minada(obtem_parcela(m,i)):
            res= res +1
    return res


def eh_campo (arg):
    """
    universal → booleano
    Devolve True caso o seu argumento seja um TAD campo e False caso contrário.
    """
    if type(arg) != dict or len(arg) == 0:
        return False
    for i in arg:
        if (not eh_coordenada(i)):
            return False
        if (not eh_parcela(obtem_parcela(arg,i))):
            return False
    return True


def eh_coordenada_do_campo(m,c):
    """
    campo x coordenada → booleano
    Devolve True se c é uma coordenada válida dentro do campo m.
    """
    col_max = obtem_ultima_coluna(m)
    lin_max = obtem_ultima_linha(m)
    if  ord(obtem_coluna(c)) < ord("A") or ord(obtem_coluna(c)) > ord(col_max)\
         or (obtem_linha(c)) < 1 or (obtem_linha(c)) > lin_max:
        return False
    return True


def campos_iguais(m1,m2):
    """
    campo x campo → booleano
    Devolve True apenas se m1 e m2 forem campos e forem iguais.
    """
    if not eh_campo(m1) or not eh_campo(m2):
        return False
    if len(m1) != len(m2):
        return False
    coordenadas_m1 = list(m1.keys())
    coordenadas_m2 = list(m2.keys())
    for i in range (len(coordenadas_m1)):
        if not coordenadas_iguais(coordenadas_m1[i],coordenadas_m2[i]):
            return False
        if not parcelas_iguais(obtem_parcela(m1, coordenadas_m1[i]),\
             obtem_parcela(m2, coordenadas_m2[i])):
            return False
    return True



def campo_para_str (m):
    """
    campo → str
    Devolve uma cadeia de caracteres que representa o campo de minas.
    """
    res="   "
    col_max= obtem_ultima_coluna(m)
    lin_max= obtem_ultima_linha(m)
    tamanho_coluna = ord(col_max) - ord("A") +1
    lista_coordenadas = list(m.keys())
    for i in range(ord("A"), ord(col_max) +1):
        res= res + chr(i)
    res= res + "\n  +"
    for j in range(tamanho_coluna):
        res= res + "-"
    res= res + "+\n"
    contador =-1
    for ii in range (1,lin_max +1):
        contador = contador +1 
        if ii >= 10:
            res= res + str(ii) + "|"
        else:
            res= res + "0" + str(ii) + "|"
        for jj in range(contador * tamanho_coluna,\
             contador*tamanho_coluna + tamanho_coluna): 
            if parcela_para_str(obtem_parcela(m,lista_coordenadas[jj])) == "?":
                if obtem_numero_minas_vizinhas(m,lista_coordenadas[jj]) == 0:
                    res= res + " "
                else:
                    res= res + str(obtem_numero_minas_vizinhas(m,\
                        lista_coordenadas[jj]))
            else:
                res = res + parcela_para_str(obtem_parcela(m,\
                    lista_coordenadas[jj]))
        res= res + "|\n"
    res= res + "  +"
    for j in range(tamanho_coluna):
        res= res + "-"
    res= res + "+"
    return res


def coloca_minas (m,c,g,n):
    """
    campo x coordenada x gerador x int → campo
    Modifica destrutivamente o campo m escondendo n minas em parcelas 
    dentro do campo.
    """
    coord_vizinha_aux = obtem_coordenadas_vizinhas(c)
    coord_vizinhas=[coordenada_para_str(c)]
    coord_final = cria_coordenada(obtem_ultima_coluna(m),obtem_ultima_linha(m))
    for i in coord_vizinha_aux:
        coord_vizinhas=coord_vizinhas + [coordenada_para_str(i)]
    minas_colocadas =[]
    while len(minas_colocadas) < n:
        c_aux = obtem_coordenada_aleatoria(coord_final,g)
        if coordenada_para_str(c_aux) not in coord_vizinhas \
            and coordenada_para_str(c_aux) not in minas_colocadas:
            minas_colocadas= minas_colocadas +[coordenada_para_str(c_aux)]
            esconde_mina(obtem_parcela(m,c_aux))
    return m

def limpa_campo(m,c):
    """
    campo x coordenada → campo
    Modifica destrutivamente o campo limpando a parcela na coordenada c, 
    devolvendo-o. Se não houver nenhuma mina vizinha escondida, limpa
    iterativamente todas as parcelas vizinhas tapadas.
    """
    if eh_parcela_minada(obtem_parcela(m,c)):
        limpa_parcela(obtem_parcela(m,c))
    else:
        limpa_parcela(obtem_parcela(m,c))
        coord_analisar=[]
        if (obtem_numero_minas_vizinhas(m,c)) == 0:
            coord_analisar =[c]
        while len(coord_analisar) != 0:
            coord_vizinhas=obtem_coordenadas_vizinhas(coord_analisar[0])
            coord_vizinhas_tapadas =[]
            del coord_analisar[0]
            for j in coord_vizinhas:
                if eh_parcela_tapada(obtem_parcela(m,j)) \
                    and not eh_parcela_minada(obtem_parcela(m,j)):
                    coord_vizinhas_tapadas= coord_vizinhas_tapadas + [j]
            for l in coord_vizinhas_tapadas:
                if obtem_numero_minas_vizinhas(m,l) == 0 \
                    and eh_parcela_tapada(obtem_parcela(m,l)):
                    coord_analisar = coord_analisar + [l]
            for k in coord_vizinhas_tapadas:
                limpa_parcela(obtem_parcela(m,k))
    return m


def jogo_ganho (m):
    """
    campo → booleano
    recebe um campo do jogo das minas e devolve True se todas as parcelas
    sem minas se encontram limpas, ou False caso contrário
    """
    coord_limpas= obtem_coordenadas(m,"limpas")
    num_coord_sem_minas = ((1 + ord(obtem_ultima_coluna(m))- ord("A")) \
        * obtem_ultima_linha(m)) - len(obtem_coordenadas(m,"minadas"))
    if len(coord_limpas) != num_coord_sem_minas:
        return False
    else:
        for i in coord_limpas:
            if eh_parcela_minada(obtem_parcela(m,i)):
                return False
    return True
    

def turno_jogador(m):
    """
    campo → booleano
    Recebe um campo de minas e oferece ao jogador a opção de escolher uma 
    ação e uma coordenada. A função modifica destrutivamente o campo de 
    acordo com ação escolhida, devolvendo False caso o jogador tenha limpo
    uma parcela que continha uma mina, ou True caso contrário.
    """
    M_ou_L = (input("Escolha uma ação, [L]impar ou [M]arcar:"))
    while M_ou_L != "M" and M_ou_L != "L":
        M_ou_L = (input("Escolha uma ação, [L]impar ou [M]arcar:"))
    coordenada_str= (input("Escolha uma coordenada:"))
    while  len(coordenada_str) != 3 or ord(coordenada_str[0])  < 65 \
        or ord(coordenada_str[0]) > 90 or ord(coordenada_str[1]) < 48 \
            or ord(coordenada_str[1]) >57 or ord(coordenada_str[2]) < 48\
                 or ord(coordenada_str[2]) >57 or \
                    not eh_coordenada_do_campo(m,cria_coordenada\
                        (coordenada_str[0],int(coordenada_str[1:]))):
        coordenada_str= (input("Escolha uma coordenada:"))
    coordenada= str_para_coordenada(coordenada_str)
    if M_ou_L == "M":
        alterna_bandeira(obtem_parcela(m,coordenada))
        return True
    else:
        limpa_campo(m,coordenada)
        if eh_parcela_minada(obtem_parcela(m,coordenada)):
            return False
        return True


def minas (c,l,n,d,s):
    """
    str x int x int x int x int → booleano
    A função recebe uma cadeia de carateres e 4 valores inteiros 
    correspondentes, respetivamente, a: última coluna c; última linha l; 
    número de parcelas com minas n; dimensão do gerador de números d; e estado
    inicial ou seed s para a geração de números aleatórios. A função devolve 
    True se o jogador conseguir ganhar o jogo, ou False caso contrário.
    Verifica argumentos.
    """
    try:
        g =cria_gerador(d,s)
        m = cria_campo(c,l)
    except:
        raise ValueError("minas: argumentos invalidos")
    maximo= (ord(c) - ord("A") +1) * l
    if  type(n) != int or n >= maximo or n <=0:
        raise ValueError("minas: argumentos invalidos")
    if n >= maximo - len(obtem_coordenadas_vizinhas(cria_coordenada("A",1))):
        raise ValueError("minas: argumentos invalidos")
    print("   [Bandeiras " + str(len(obtem_coordenadas(m,"marcadas"))) + \
        "/" + str(n) + "]")
    print(campo_para_str(m))
    coordenada_str= (input("Escolha uma coordenada:"))
    while  len(coordenada_str) != 3 or ord(coordenada_str[0])  < 65 \
        or ord(coordenada_str[0]) > 90 or ord(coordenada_str[1]) < 48 \
            or ord(coordenada_str[1]) >57 or ord(coordenada_str[2]) < 48 \
                or ord(coordenada_str[2]) >57 or not eh_coordenada_do_campo(m,\
                    cria_coordenada(coordenada_str[0],int(coordenada_str[1:]))):
        coordenada_str= (input("Escolha uma coordenada:"))
    coordenada= str_para_coordenada(coordenada_str)
    coloca_minas(m,coordenada,g,n)
    limpa_campo(m,coordenada)
    print("   [Bandeiras " + str(len(obtem_coordenadas(m,"marcadas"))) +\
         "/" + str(n) + "]")
    print(campo_para_str(m))
    while not jogo_ganho(m):
        if not turno_jogador(m):
            print("   [Bandeiras " + str(len(obtem_coordenadas(m,"marcadas")))\
                 + "/" + str(n) + "]")
            print(campo_para_str(m))
            print("BOOOOOOOM!!!")
            return False
        else:
            print("   [Bandeiras " + str(len(obtem_coordenadas(m,"marcadas")))\
                 + "/" + str(n) + "]")
            print(campo_para_str(m))
    print("VITORIA!!!")
    return True


