# coding=iso-8859-1

"""
Segundo exemplo de gerador.
"""

### CXXII
gerador_nome = 'Exemplo 2'
gerador_versao = 1
gerador_multiplo = True
###

CXXII_Atual('/Exemplos Saída/' + CXXII_XML.nome + ' [Exemplo 2].html', formato='iso-8859-1')

titulo = 'Exemplo 2'

CXXII_EscreverArquivo('Exemplo.html', 1, 6)

"""~
        <h1><b>Relatório</b></h1>

"""

CXXII_EscreverArquivo('Exemplo.html', 8)