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

def gera_numero_aleatorio (g,n):
    



# g1 = cria_gerador(32, 1)
# print(gerador_para_str(g1))
# print([atualiza_estado(g1) for n in range(3)])








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
    if int(key[0][1:]) < 10:
        return str(0) + key[0][1:]
    else:
        return key[0][1:]


def eh_coordenada(arg):
    if type(arg) != dict or len(arg) != 1:
        return False
    key=list(arg.keys())
    if  type(key[0][0])!=str or ord(key[0][0]) < 65 or ord(key[0][0])>90 or type(key[0][1:]) != int or key[0][1:]>99:
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

print(ord("A"))
print(ord("B")) 




c1 = cria_coordenada("B", 10)
print(obtem_linha(c1))
