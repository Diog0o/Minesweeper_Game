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
    
def gera_caracter_aleatorio (g,c): # c nao pode ser "A" <--------------
    atualiza_estado(g)
    l = ord(c) - ord("A")
    return chr( ord("A") + obtem_estado(g) % l)


g1 = cria_gerador(32, 1)
# print(gerador_para_str(g1))
# print([atualiza_estado(g1) for n in range(3)])
# print(gera_numero_aleatorio(g1,134))
# print(type(gera_numero_aleatorio(g1,100)))
# print(gera_caracter_aleatorio(g1, "B"))


#2.1.2

def cria_coordenada(col,lin):
    if type(col) != str or type(lin) != int or len(col) != 1 or ord(col) < 65 or ord(col)>90 or lin>99:
        raise ValueError("cria coordenada: argumentos invalidos")
    else:
        dicionario ={}
        coordenada = col + str(lin)
        dicionario[coordenada] = 0 
    return dicionario

def obtem_coluna(c):
    key=list(c.keys())
    return key[0][0]
    
def obtem_linha(c):
    key=list(c.keys())
    return int(key[0][1:])


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
    key=list(c.keys())
    if int(key[0][1:]) < 10:
        linha = str(0) + key[0][1:]
    else:
        linha = key[0][1:]
    return obtem_coluna(c) + linha

def str_para_coordenada(s):
    if s[1] == 0:
        return cria_coordenada(s[0], int(s[2]))
    else:
        return cria_coordenada(s[0],int(s[1:]))

def obtem_coordenadas_vizinhas (c):
    res=()
    coluna = obtem_coluna(c)
    linha = obtem_linha(c)
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
    linha_aleatoria = gera_numero_aleatorio(g, obtem_linha(c))
    coluna_aleatoria = gera_caracter_aleatorio(g, obtem_coluna(c))
    return cria_coordenada(coluna_aleatoria,linha_aleatoria)



c3 = cria_coordenada("Z", 99)
c4 = obtem_coordenada_aleatoria(c3, g1)
print(coordenada_para_str(c4))

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





    