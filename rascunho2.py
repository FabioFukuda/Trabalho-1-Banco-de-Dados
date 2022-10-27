def produtoCartesianoRecursivo(tabelas:list):
        if(len(tabelas)>1):
            tabela1 = tabelas.pop(0)
            tabela2 = tabelas.pop(0)
            registros = []

            for i in range(len(tabela1)):
                registros.append([])
            for i in range(len(tabela2)):
                registros.append([])
            inicioTabela2 = len(tabela1)

            for indiceGeralTabela1 in range(len(tabela1[0])):
                for indiceGeralTabela2 in range(len(tabela2[0])):
                    for indiceColuna,registroTabela1 in enumerate(tabela1):
                        registros[indiceColuna].append(registroTabela1[indiceGeralTabela1])
                    for indiceColuna,registroTabela2 in enumerate(tabela2):
                        registros[inicioTabela2+indiceColuna].append(registroTabela2[indiceGeralTabela2])
            tabelas.insert(0,registros) 

            return produtoCartesianoRecursivo(tabelas)
        else:
            return tabelas

a = [1,2,3,4]
print(a.index(5))
