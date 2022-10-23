class Coluna:
    def __init__(self,nome:str,registros:list = []):
        self.nome = nome
        self.registros = registros
    
    def toList(self):
        return self.registros

    def __eq__(self,key):
        if type(key) == Coluna:
            selecao = []
            for registro in self.registros:
                if registro in key:
                    indices = key.index(registro)
                    selecao.append(indices)
                else:
                    selecao.append(False)
            return Coluna('relacao',selecao)
        else:   
            selecao = []
            for registro in self.registros:
                if registro == key:
                    selecao.append(True)
                else:
                    selecao.append(False)
            return Coluna('',selecao)

    def __ne__(self,key):
        if type(key) == Coluna:
            selecao = []
            indicesChaves = key.fazerIndice()
            for registro in self.registros:
                indiceIguais = key.index(registro)
                indicesDiferentes = [indice for indice in indicesChaves if indice not in indiceIguais]
                if(len(indicesDiferentes) == 0):
                    selecao.append(False)
                else:
                    selecao.append(indicesDiferentes)
            
            return Coluna('relacao',selecao)
        else:
            selecao = []
            for registro in self.registros:
                if registro != key:
                    selecao.append(True)
                else:
                    selecao.append(False)
            return Coluna('',selecao)

    def contido(self, key):
        selecao = []
        for registro in self.registros:
                if registro in key:    
                    selecao.append(True)
                else:
                    selecao.append(False)
        return Coluna('',selecao)

    def naoContido(self,key):
        selecao = []
        for registro in self.registros:
            if registro not in key:    
                selecao.append(True)
            else:
                selecao.append(False)
        return Coluna('',selecao)

    # %string% -> comeco = False, final = False
    # string% -> comeco = True, final = False
    # %string -> comeco = False, final = True
    
    def like(self,key,comeco,final):
        selecao = []
        for registro in self.registros:
            if key in registro.lower():
                reg1,reg2 = registro.lower().split(key)
                if not comeco and not final:
                    selecao.append(True)
                elif comeco and not final:
                    if len(reg1)==0:
                        selecao.append(True)
                elif not comeco and final:
                    if len(reg2)==0:
                        selecao.append(True)
                else:
                    selecao.append(False)    
            else:
                selecao.append(False)
        return Coluna('',selecao)

    def isNull(self):
        selecao = []
        for registro in self.registros:
            if registro == None:    
                selecao.append(True)
            else:
                selecao.append(False)
        return Coluna('',selecao)

    def isNotNull(self):
        selecao = []
        for registro in self.registros:
            if registro != None:    
                selecao.append(True)
            else:
                selecao.append(False)
        return Coluna('',selecao)

    def operacaoComNumero(func):
        def wrapper(*args,**kwargs):
            try:
                resultado = func(*args,**kwargs)
                return resultado
            except:
                registro = [None for i in range(len(args[0].registros))]
                return Coluna('',registro)
        return wrapper

    @operacaoComNumero
    def entre(self,key1,key2):
        selecao = []
        for registro in self.registros:
                if float(registro)>=float(key1) and float(registro)<=float(key2):
                    selecao.append(True)
                else:
                    selecao.append(False)
        return Coluna('',selecao)

    @operacaoComNumero
    def __gt__(self,key):
        selecao = []
        for registro in self.registros:
            if float(registro) > float(key):
                selecao.append(True)
            else:
                selecao.append(False)
        return Coluna('',selecao)

    @operacaoComNumero
    def __lt__(self,key):
        selecao = []
        for registro in self.registros:
            if float(registro) < float(key):
                selecao.append(True)
            else:
                selecao.append(False)
        return Coluna('',selecao)

    @operacaoComNumero
    def __ge__(self,key):
        selecao = []
        for registro in self.registros:
                if float(registro) < float(key):
                    selecao.append(True)
                else:
                    selecao.append(False)
        return Coluna('',selecao)
    
    @operacaoComNumero
    def __le__(self,key):
        selecao = []
        for registro in self.registros:
                if float(registro) < float(key):    
                    selecao.append(True)
                else:
                    selecao.append(False)
        return Coluna('',selecao)

    def __and__(self,key):
        selecao = []
        for indice in range(len(key)):
            if self.registros[indice] and key[indice]:
                selecao.append(True)
            else:
                selecao.append(False)
        return Coluna('',selecao)

    def __or__(self,key):
        selecao = []
        for indice in range(len(key)):
            if self.registros[indice] or key[indice]:
                selecao.append(True)
            else:
                selecao.append(False)
        return Coluna('',selecao)

    def __iter__(self):
        return iter(self.registros)

    def __getitem__(self, key):
        return self.registros[key]

    def __len__(self):
        return len(self.registros)

    def index(self,key):
        indices = [i for i,valor in enumerate(self.registros) if valor == key]
        return indices

    def fazerIndice(self):
        return [i for i in range(len(self.registros))]
        
    def __contains__(self,key):
        return key in self.registros
'''
=	Igual
>	Maior que
<	Menor que
>=	Maior ou igual
<=	Menor ou igual
<> ou !=	Diferente de
IN	Incluindo (múltiplos valores)
NOT IN	Excluindo (múltiplos valores)
BETWEEN	Entre dois valores
LIKE	Busca um padrão parecido
IS NULL	Traz todos os valores nulos
IS NOT NULL	Traz todos os valores que não são nulos
'''