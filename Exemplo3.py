"""
Terceiro exemplo de gerador.
"""

### CXXII
gerador_nome = 'Exemplo 3'
gerador_versao = 1
gerador_multiplo = True
###

CXXII_Atual('/Exemplos Saída/' + CXXII_XML.nome + ' [Exemplo 3].html', formato='iso-8859-1')

titulo = 'Exemplo 3'

"""~
<html>
    <head>
        <title>{{{titulo}}}</title>
        <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
    </head>
    <body>
        <h1><b>Exemplo 3 - Pessoas</b></h1>

"""

for pessoa in CXXII_XML.raiz().findall('pessoa'):
    """~
        <p><b>Nome:</b> {{{pessoa.find('nome').text}}}</p>
        <p><b>Endereço:</b> {{{pessoa.find('endereco').text}}}</p>
        <hr>

    """

"""~
    </body>
</html>
"""