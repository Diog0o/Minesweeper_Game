#2.1.1





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
