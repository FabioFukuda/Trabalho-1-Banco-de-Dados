class Coluna:
    def __init__(self,nome:str,registros:list = []):
        self.nome = nome
        self.registros = registros
    
    def toList(self):
        return self.registros
    
    def __eq__(self,key):
        selecao = []
        for registro in self.registros:
            if registro == key:
                selecao.append(True)
            else:
                selecao.append(False)
        return selecao

    def __gt__(self,key):
        selecao = []
        for registro in self.registros:
            if registro > key:
                selecao.append(True)
            else:
                selecao.append(False)
        return selecao

    def __lt__(self,key):
        selecao = []
        for registro in self.registros:
            if registro < key:
                selecao.append(True)
            else:
                selecao.append(False)
        return selecao

    def __ge__(self,key):
        selecao = []
        for registro in self.registros:
            if registro >= key:
                selecao.append(True)
            else:
                selecao.append(False)
        return selecao
    
    def __le__(self,key):
        selecao = []
        for registro in self.registros:
            if registro <= key:
                selecao.append(True)
            else:
                selecao.append(False)
        return selecao

    def __ne__(self,key):
        selecao = []
        for registro in self.registros:
            if registro != key:
                selecao.append(True)
            else:
                selecao.append(False)
        return selecao
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