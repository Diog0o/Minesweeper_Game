#2.1.1

def cria_gerador (b,s):
    if (type(b) != int or (b != 32 and b!= 64) or type(s)!= int or s<0): #Pode ser negativo??
        raise ValueError("cria gerador: argumentos invalidos")
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
# [atualiza_estado(g2) for n in range(5)]
# print(gerador_para_str(g2))
# print(gera_carater_aleatorio(g2, "Z"))


#2.1.2

def cria_coordenada(col,lin):
    if type(col) != str or type(lin) != int or len(col) != 1 or ord(col) < 65 or ord(col)>90 or lin>99:
        raise ValueError("cria coordenada: argumentos invalidos")
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
    if  type(key[0][0])!=str or ord(key[0][0]) < 65 or ord(key[0][0])>90 or type(int(key[0][1:])) != int or int(key[0][1:])>100 or int(key[0][1:])<1:
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
    c1=cria_coordenada(chr(ord(coluna)-1), linha - 1)
    c8=cria_coordenada(chr(ord(coluna)-1), linha)
    c7=cria_coordenada(chr(ord(coluna)-1), linha + 1)
    c6=cria_coordenada(coluna, linha + 1)
    c5=cria_coordenada(chr(ord(coluna)+1), linha +1)
    c4=cria_coordenada(chr(ord(coluna)+1), linha)
    c3=cria_coordenada(chr(ord(coluna)+1), linha-1)
    c2=cria_coordenada(coluna, linha -1 )
    res_provisorio=(c1,c2,c3,c4,c5,c6,c7,c8)
    for i in res_provisorio:
        if eh_coordenada(i) == True:
            res= res + (i,)
    return res

def obtem_coordenada_aleatoria(c,g):
    linha_aleatoria = gera_numero_aleatorio(g, int(obtem_linha(c)))
    coluna_aleatoria = gera_carater_aleatorio(g, obtem_coluna(c))
    return cria_coordenada(coluna_aleatoria,linha_aleatoria)


# c1=cria_coordenada("B", 1)
# c2 = cria_coordenada("N", 20)
# print(coordenadas_iguais(c1, c2))

# print(coordenada_para_str(c1))

# t = obtem_coordenadas_vizinhas(c1)
# print(tuple(coordenada_para_str(p) for p in t))


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
    copia = m
    return copia

def obtem_ultima_coluna(m):
    return m[1]

def obtem_ultima_linha(m):
    return m[2]

def obtem_parcela(m,c):
    for i in m[0]:
        if coordenada_para_str(c) in i:
            return i[coordenada_para_str]



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
                res = res + (key,)
    else:
        for i in m[0]:
            key= coordenada_para_str(i)
            if i[key]["mina"] == "sim":
                res = res +key
    return res

def obtem_numero_minas_vizinhas (m,c):
    coord_vizinhas = obtem_coordenadas_vizinhas(c)
    coord_vizinhas_str =()
    for j in coord_vizinhas:
        coord_vizinhas_str= coord_vizinhas_str + (coordenada_para_str(j),)
    coord_com_minas = obtem_coordenadas(m, "minadas")
    res= 0
    for i in coord_vizinhas_str:
        if i in coord_com_minas:
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
    #if  ord(obtem_coluna(c)) < 65 or ord(obtem_coluna(c)) > ord(col_max) or obtem_linha(c) < 1 or obtem_linha(c) > lin_max:
    if 65 > ord(obtem_coluna(c)) > ord(col_max) or 1 > obtem_linha(c) > lin_max:
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
            res = res + parcela_para_str(m[0][jj][key])
        res= res + "|\n"
    res= res + "  +"
    for j in range(tamanho_coluna):
        res= res + "-"
    res= res + "+"
    return res


def coloca_minas (m,c,g,n):
    coord_vizinhas = obtem_coordenadas_vizinhas(c)
    minas_colocadas =[]
    while minas_colocadas < n:
        coluna_aleatoria=gera_numero_aleatorio(g, obtem_ultima_coluna(m))
        linha_aleatoria=gera_numero_aleatorio(g,obtem_ultima_linha(m))
        c = cria_coordenada(coluna_aleatoria,linha_aleatoria)
        if coordenada_para_str(c) not in coord_vizinhas and coordenada_para_str(c) not in minas_colocadas:
            minas_colocadas= minas_colocadas +[coordenada_para_str(c)]
            obtem_parcela(m,c)["mina"] = "sim"
    return m





m = cria_campo("I",7)
print(coloca_minas(m,cria_coordenada("B",3),g2,15))
#print(m1)
print(m)
print(campo_para_str(m))
#print(campo_para_str(m))





