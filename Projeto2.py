#2.1.1

def cria_gerador (b,s): #falta verificar muitos argumentos
    if (type(b) != int or (b != 32 and b!= 64) or type(s)!= int or s<=0): #Pode ser negativo??
        raise ValueError("cria_gerador: argumentos invalidos")
    return {"dimensao":b , "seed":s , "estado": s}

def cria_copia_gerador (g):
    return {"dimensao": g["dimensao"], "seed": g["seed"], "estado": g["estado"]}

def obtem_estado (g):
    return g["estado"]

def define_estado (g,s):
    g["estado"] = s
    return s

def atualiza_estado (g):
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
    if type(arg) != dict or "dimensao" not in arg or "seed" not in arg or "estado" not in arg:
        return False
    if arg["dimensao"] != 32 and arg["dimensao"] != 64:
        return False
    if type(arg["seed"]) != int or arg["seed"] < 0 or type(arg["estado"]) != int or arg["estado"] < 0:
        return False
    return True

def geradores_iguais (g1,g2):
    if (eh_gerador(g1) and eh_gerador (g2)):
        if g1["dimensao"] == g2["dimensao"] and g1["seed"] == g2["seed"] and g1["estado"] == g2["estado"]:
            return True
    return False

def gerador_para_str(g):
    return "xorshift" + str(g["dimensao"]) + "(s=" +  str(g["estado"]) +")"


#Provavelmente falta verificar os argumentos

def gera_numero_aleatorio (g,n):
    atualiza_estado(g)
    return 1 + obtem_estado(g) % n
    
def gera_carater_aleatorio (g,c): # c nao pode ser "A" <--------------
    atualiza_estado(g)
    l = ord(c) - ord("A") + 1
    return chr( ord("A") + obtem_estado(g) % l)


g2 = cria_gerador(64, 1)



#2.1.2

def cria_coordenada(col,lin): # nao pode ser 00 e o len tem que ser 3
    if type(col) != str or type(lin) != int or len(col) != 1 or lin>99 or lin <1 or ord(col) < 65 or ord(col)>90 : #Tirei o or ord(col) < 65 or ord(col)>90
        raise ValueError("cria_coordenada: argumentos invalidos")
    else:
        dicionario ={}
        if lin >= 10:
            coordenada =col + str(lin)
        else:
            coordenada = col + "0" + str(lin)
    dicionario[coordenada] = 0 
    return dicionario

def obtem_coluna(c):
    key=list(c.keys())
    return key[0][0]
    
def obtem_linha(c):
    key=list(c.keys())
    return key[0][1:]


def eh_coordenada(arg):
    if type(arg) != dict or len(arg) != 1:
        return False
    key=list(arg.keys())
    if  type(key[0][0])!=str or ord(key[0][0]) < 65 or ord(key[0][0])>90 or type(int(key[0][1:])) != int or int(key[0][1:])>100 or int(key[0][1:])<1 or len(key[0]) !=3:
        return False
    return True

def coordenadas_iguais (c1,c2):
    if eh_coordenada(c1) == False or eh_coordenada(c2) == False:
        return False
    if obtem_coluna(c1) == obtem_coluna(c2) and obtem_linha(c1) == obtem_linha(c2):
        return True
    return False

def coordenada_para_str(c):
    return obtem_coluna(c) + obtem_linha(c)

def str_para_coordenada(s):
    if s[1] == 0:
        return cria_coordenada(s[0], int(s[2]))
    else:
        return cria_coordenada(s[0],int(s[1:]))

def obtem_coordenadas_vizinhas (c):
    res=()
    coluna = obtem_coluna(c)
    linha = int(obtem_linha(c))
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
        if ord(i[0]) >= 65 and ord(i[0]) <= 90 and i[1] <=99 and i[1] >=1:
            res= res + (cria_coordenada(i[0],i[1]),)
    return res

def obtem_coordenada_aleatoria(c,g):
    coluna_aleatoria = gera_carater_aleatorio(g, obtem_coluna(c))
    linha_aleatoria = gera_numero_aleatorio(g, int(obtem_linha(c)))
    return cria_coordenada(coluna_aleatoria,linha_aleatoria)



# 2.1.3

def cria_parcela ():
    return {"estado": "tapada", "mina": "nao"}

def cria_copia_parcela (p):
    return {"estado": p["estado"], "mina": p["mina"]}

def limpa_parcela (p):
    p["estado"] = "limpa"
    return p

def marca_parcela (p):
    p["estado"] = "marcada"
    return p

def desmarca_parcela (p):
    p["estado"] = "tapada"
    return p

def esconde_mina (p):
    p["mina"] = "sim"
    return p

def eh_parcela (arg):
    if type(arg) != dict or "estado" not in arg or "mina" not in arg:
        return False
    if (arg["estado"] != "tapada" and arg["estado"] != "limpa" and arg["estado"] != "marcada" ) or (arg["mina"] != "sim" and arg["mina"] != "nao"):
        return False
    return True

def eh_parcela_tapada (p):
    if (eh_parcela(p)):
        if (p["estado"] == "tapada"):
            return True
    return False

def eh_parcela_marcada (p):
    if (eh_parcela(p)):
        if (p["estado"] == "marcada"):
            return True
    return False

def eh_parcela_limpa (p):
    if (eh_parcela(p)):
        if (p["estado"] == "limpa"):
            return True
    return False

def eh_parcela_minada (p):
    if (eh_parcela(p)):
        if (p["mina"] == "sim"):
            return True
    return False

def parcelas_iguais(p1,p2):
    if (eh_parcela(p1) and eh_parcela(p2)):
        if (p1["estado"] == p2["estado"] and p1["mina"] == p2["mina"]):
            return True
    return False

def parcela_para_str (p):
    if p["estado"] == "tapada":
        return "#"
    if p["estado"] == "marcada":
        return "@"
    if p["estado"] == "limpa" and p["mina"] == "nao":
        return "?"
    else:
        return "X"

def alterna_bandeira(p):
    if eh_parcela_marcada(p):
        desmarca_parcela(p)
        return True
    if eh_parcela_tapada(p):
        marca_parcela(p)
        return True
    return False


#2.1.4
#Devia devolver sempre cria_campo: argumentos invalidos. Talvez fazer um try ???
def cria_campo (c,l):
    if type(c) != str or type(l) != int or len(c) != 1 or ord(c) < 65 or ord(c)>90 or l>100 or l<1:
        raise ValueError("cria_campo: argumentos invalidos")
    res=[]
    for j in range (1,l +1):
        for i in range (ord("A"), ord(c) +1):  
            coordenada= cria_coordenada(chr(i),j)
            if j >= 10:
                key= chr(i) + str(j)
            else:
                key = chr(i) + "0" + str(j)
            coordenada[key]= cria_parcela()
            res= res + [coordenada,]
    return (res,c,l)

def cria_copia_campo(m):
    copia= m.copy()
    return copia

def obtem_ultima_coluna(m):
    return m[1]

def obtem_ultima_linha(m):
    return m[2]

def obtem_parcela(m,c):
    for i in m[0]:
        if coordenada_para_str(c) in i:
            return i[coordenada_para_str(c)]


#Usar as funcoes das parcelas esconde_mina, marca_parcela ....
def obtem_coordenadas (m,s):
    res=()
    if s == "tapadas" or s=="limpas" or s=="marcadas":
        if s == "tapadas":
            s_aux="tapada"
        if s == "marcadas":
            s_aux = "marcada"
        if s == "limpas":
            s_aux= "limpa"
        for i in m[0]:
            key= coordenada_para_str(i)
            if i[key]["estado"] == s_aux:
                res = res + (i,)
    else:
        for i in m[0]:
            if eh_parcela_minada(obtem_parcela(m,i)):
                res = res +(i,)
    return res

def obtem_numero_minas_vizinhas (m,c):
    coord_vizinhas = obtem_coordenadas_vizinhas(c)
    res= 0
    for i in coord_vizinhas:
        if eh_parcela_minada(obtem_parcela(m,i)) == True:
            res= res +1
    return res


def eh_campo (arg):
    if type(arg) != list or len(arg) != 3:
        return False
    if  type(arg[0]) != list or type(arg[1]) != str or ord(arg[1]) < 65 or ord(arg[1])>90 or type(arg[2]) != int or arg[2]>100 or arg[1]<1:
        return False
    for i in arg[0]:
        if ( eh_coordenada(i) == False):
            return False
        key= coordenada_para_str(i)
        if (eh_parcela(i[key]) == False):
            return False
    return True

def eh_coordenada_do_campo(m,c):
    col_max = m[1]
    lin_max = m[2]
    if  ord(obtem_coluna(c)) < 65 or ord(obtem_coluna(c)) > ord(col_max) or int(obtem_linha(c)) < 1 or int(obtem_linha(c)) > lin_max:
        return False
    return True


def campos_iguais(m1,m2):
    if eh_campo(m1) == False or eh_campo(m2) == False:
        return False
    if m1[1] != m2[1] or m1[2] != m2[2] or len(m1[0]) != len(m2[0]):
        return False
    for i in range(len(m1[0])):
        if coordenadas_iguais(m1[0][i], m2[0][i]) == False:
            return False
        else:
            key = coordenada_para_str(m1[0][i])
            if parcelas_iguais(m1[0][i][key], m2[0][i][key]) == False:
                return False
    return True


def campo_para_str (m):
    res="   "
    col_max= obtem_ultima_coluna(m)
    lin_max= obtem_ultima_linha(m)
    tamanho_coluna = ord(col_max) - ord("A") +1
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
        for jj in range(contador * tamanho_coluna, contador*tamanho_coluna + tamanho_coluna ): 
            key= coordenada_para_str(m[0][jj])
            if parcela_para_str(m[0][jj][key]) == "?":
                if obtem_numero_minas_vizinhas(m,m[0][jj]) == 0:
                    res= res + " "
                else:
                    res= res + str(obtem_numero_minas_vizinhas(m,m[0][jj]))
            else:
                res = res + parcela_para_str(m[0][jj][key])
        res= res + "|\n"
    res= res + "  +"
    for j in range(tamanho_coluna):
        res= res + "-"
    res= res + "+"
    return res


def coloca_minas (m,c,g,n):
    coord_vizinha_aux = obtem_coordenadas_vizinhas(c)
    coord_vizinhas=[coordenada_para_str(c)]
    coord_final = cria_coordenada(obtem_ultima_coluna(m),obtem_ultima_linha(m))
    for i in coord_vizinha_aux:
        coord_vizinhas=coord_vizinhas + [coordenada_para_str(i)]
    minas_colocadas =[]
    while len(minas_colocadas) < n:
        c_aux = obtem_coordenada_aleatoria(coord_final,g)
        if coordenada_para_str(c_aux) not in coord_vizinhas and coordenada_para_str(c_aux) not in minas_colocadas:
            minas_colocadas= minas_colocadas +[coordenada_para_str(c_aux)]
            esconde_mina(obtem_parcela(m,c_aux))
    return m

def limpa_campo(m,c):
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
                if eh_parcela_tapada(obtem_parcela(m,j)) == True and eh_parcela_minada(obtem_parcela(m,j)) == False:
                    coord_vizinhas_tapadas= coord_vizinhas_tapadas + [j]
            for l in coord_vizinhas_tapadas:
                if obtem_numero_minas_vizinhas(m,l) == 0 and eh_parcela_tapada(obtem_parcela(m,l)):
                    coord_analisar = coord_analisar + [l]
            for k in coord_vizinhas_tapadas:
                limpa_parcela(obtem_parcela(m,k))
    return m


def  jogo_ganho (m):
    coord_limpas= obtem_coordenadas(m,"limpas")
    num_coord_sem_minas = ((1 + ord(obtem_ultima_coluna(m))- ord("A")) * obtem_ultima_linha(m)) - len(obtem_coordenadas(m,"minadas"))
    if len(coord_limpas) != num_coord_sem_minas:
        return False
    else:
        for i in coord_limpas:
            if eh_parcela_minada(obtem_parcela(m,i)):
                return False
    return True
    

def turno_jogador(m):
    M_ou_L = (input("Escolha uma ação, [L]impar ou [M]arcar:"))
    while M_ou_L != "M" and M_ou_L != "L":
        M_ou_L = (input("Escolha uma ação, [L]impar ou [M]arcar:"))
    coordenada_str= (input("Escolha uma coordenada:"))
    coordenada = str_para_coordenada(coordenada_str)
    while  eh_coordenada(coordenada) == False or eh_coordenada_do_campo(m,coordenada) == False or coordenada_str != coordenada_para_str(coordenada):
        coordenada_str= (input("Escolha uma coordenada:"))
        coordenada= str_para_coordenada(coordenada_str)
    if M_ou_L == "M":
        alterna_bandeira(obtem_parcela(m,coordenada))
    else:
        limpa_campo(m,coordenada)
        if eh_parcela_minada(obtem_parcela(m,coordenada)):
            return False
        return True

def minas (c,l,n,d,s): # n não pode ser igual a 0 tem que ser um int e não pode haver mais bombas do que casas possiveis 
    try:
        g =cria_gerador(d,s)
        m = cria_campo(c,l)
    except:
        raise ValueError("minas: argumentos invalidos")
    maximo= (ord(c) +1) * l
    if  type(n) != int or n >= maximo or n <=0:
        raise ValueError("minas: argumentos invalidos")
    print("   [Bandeiras " + str(len(obtem_coordenadas(m,"marcadas"))) + "/" + str(n) + "]")
    print(campo_para_str(m))
    coordenada_str= (input("Escolha uma coordenada:"))
    coordenada = str_para_coordenada(coordenada_str)
    while  eh_coordenada(coordenada) == False or eh_coordenada_do_campo(m,coordenada) == False or coordenada_str != coordenada_para_str(coordenada):
        coordenada_str= (input("Escolha uma coordenada:"))
        coordenada= str_para_coordenada(coordenada_str)
    coloca_minas(m,coordenada,g,n)
    limpa_campo(m,coordenada)
    print("   [Bandeiras " + str(len(obtem_coordenadas(m,"marcadas"))) + "/" + str(n) + "]")
    print(campo_para_str(m))
    while jogo_ganho(m) == False:
        if turno_jogador(m) == False:
            print("   [Bandeiras " + str(len(obtem_coordenadas(m,"marcadas"))) + "/" + str(n) + "]")
            print(campo_para_str(m))
            print("BOOOOOOOM!!!")
            return False
        else:
            print("   [Bandeiras " + str(len(obtem_coordenadas(m,"marcadas"))) + "/" + str(n) + "]")
            print(campo_para_str(m))
    print("VITORIA!!!")
    return True


c1 = cria_coordenada('B', 1)
t = obtem_coordenadas_vizinhas(c1)
print(tuple(coordenada_para_str(p) for p in t))



        



    





