class Coluna:
    def __init__(self,nome:str,registros:list = []):
        self.nome = nome
        self.registros = registros
        self.relacao = False
        self.tabelasRelacao = []
        
    def toList(self):
        return self.registros

    def __eq__(self,key):
        selecao = []
        for registro in self.registros:
            if registro.lower() == key.lower():
                selecao.append(True)
            else:
                selecao.append(False)
        return Coluna('',selecao)

    def __ne__(self,key):
        selecao = []
        for registro in self.registros:
            if registro.lower() != key.lower():
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
                if float(registro) >= float(key):
                    selecao.append(True)
                else:
                    selecao.append(False)
        return Coluna('',selecao)
    
    @operacaoComNumero
    def __le__(self,key):
        selecao = []
        for registro in self.registros:
                if float(registro) <= float(key):    
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
