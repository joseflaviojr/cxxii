#!/usr/bin/env python3

#----------------------------------------------------------------------------
# 
# Copyright (C) 2015 José Flávio de Souza Dias Júnior
# 
# This file is part of CXXII - http://www.joseflavio.com/cxxii/
# 
# CXXII is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# CXXII is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with CXXII. If not, see http://www.gnu.org/licenses/.
# 
#----------------------------------------------------------------------------
# 
# Direitos Autorais Reservados (C) 2015 José Flávio de Souza Dias Júnior
# 
# Este arquivo é parte de CXXII - http://www.joseflavio.com/cxxii/
# 
# CXXII é software livre: você pode redistribuí-lo e/ou modificá-lo
# sob os termos da Licença Pública Menos Geral GNU conforme publicada pela
# Free Software Foundation, tanto a versão 3 da Licença, como
# (a seu critério) qualquer versão posterior.
# 
# CXXII é distribuído na expectativa de que seja útil,
# porém, SEM NENHUMA GARANTIA; nem mesmo a garantia implícita de
# COMERCIABILIDADE ou ADEQUAÇÃO A UMA FINALIDADE ESPECÍFICA. Consulte a
# Licença Pública Menos Geral do GNU para mais detalhes.
# 
# Você deve ter recebido uma cópia da Licença Pública Menos Geral do GNU
# junto com CXXII. Se não, veja http://www.gnu.org/licenses/.
# 
#----------------------------------------------------------------------------

# "Não vos conformeis com este mundo,
# mas transformai-vos pela renovação do vosso espírito,
# para que possais discernir qual é a vontade de Deus,
# o que é bom, o que lhe agrada e o que é perfeito."
# (Bíblia Sagrada, Romanos 12:2)

# "Do not conform yourselves to this age
# but be transformed by the renewal of your mind,
# that you may discern what is the will of God,
# what is good and pleasing and perfect."
# (Holy Bible, Romans 12:2)

import sys
if sys.version_info[0] < 3:
    print('CXXII exige Python 3 ou mais recente.')
    sys.exit(1)


import os
import time
import datetime
import unicodedata
import urllib.request
import tempfile
import zipfile
import re
from xml.etree.ElementTree import ElementTree as CXXII_XML_Arvore


#----------------------------------------------------------------------------


class CXXII_XML_Arquivo:
    """Classe que representa um arquivo XML."""

    def __init__(self, endereco):
        self.endereco = endereco
        self.nome = NomeDoArquivo(endereco)
        self.arvore = CXXII_XML_Arvore()
        self.arvore.parse(endereco)

    def raiz(self):
        return self.arvore.getroot()


def CXXII_Baixar( url, destino=None, nome=None, forcar=False ):
    """Download de arquivo."""
    if url[-1]     == '/'    : url     = url[0:-1]
    if destino     is None   :
        global CXXII_Diretorio
        destino = CXXII_Diretorio
    if destino[-1] == os.sep : destino = destino[0:-1]
    if nome        is None   : nome    = url.replace('/', '_').replace(':', '_')
    endereco = destino + os.sep + nome
    existe = os.path.exists(endereco)
    baixar = forcar or not existe
    if not baixar:
        global CXXII_Gerador_TempoMaximo
        baixar = ( time.time() - os.path.getmtime(endereco) ) > CXXII_Gerador_TempoMaximo
    if baixar:
        try:
            urllib.request.urlretrieve(url, endereco)
        except:
            raise Exception('Não foi possível baixar o gerador.')
    return endereco


def CXXII_XML_Adicionar( endereco ):
    global CXXII_XML_Arquivos
    CXXII_XML_Arquivos.append( CXXII_XML_Arquivo(endereco) )


def CXXII_Separadores( endereco ):
    """Substitui os separadores "/" pelo separador real do sistema operacional."""
    return endereco.replace('/', os.sep)


def CXXII_Python_Formato( arquivo ):
    """Retorna o valor de "# coding=".

    arquivo -- Arquivo ou endereço de arquivo. Pode-se utilizar "/" como separador.
    """
    if type(arquivo) is str: arquivo = open( CXXII_Separadores(arquivo), 'r', encoding='iso-8859-1' )
    formato = 'utf-8'
    arquivo.seek(0)
    for i in range(2):
        linha = arquivo.readline()
        if linha.startswith('# coding='):
            formato = linha[9:-1]
            break
    arquivo.close()
    return formato


def CXXII_Abrir_Python( endereco ):
    """Abre um arquivo ".py" respeitando a codificação especificada no cabeçalho "# coding=".

    endereco -- Endereço do arquivo. Pode-se utilizar "/" como separador.
    """
    endereco = CXXII_Separadores(endereco)
    return open( endereco, 'r', encoding=CXXII_Python_Formato(endereco) )


def CXXII_Atual( endereco, modo='w', formato='utf-8' ):
    """Determina o arquivo em geração atual.

    endereco -- Endereço do arquivo desejado, relativo ao CXXII_Destino. Pode-se utilizar "/" como separador.
    """
    global CXXII_Saida
    global CXXII_Destino
    endereco = CXXII_Separadores(endereco)
    if endereco[0] != os.sep: endereco = os.sep + endereco
    if CXXII_Saida != None and CXXII_Saida != sys.stdout: CXXII_Saida.close()
    arquivo = CXXII_Texto(CXXII_Destino + endereco)
    diretorio = CXXII_Texto(os.path.dirname(arquivo))
    if not os.path.exists(diretorio): os.makedirs(diretorio)
    CXXII_Saida = open( arquivo, modo, encoding=formato )


def CXXII_Escrever( texto ):
    """Escreve no arquivo em geração atual. Ver CXXII_Atual()."""
    global CXXII_Saida
    if not CXXII_Saida is None:
        CXXII_Saida.write(texto)


def CXXII_ContarIdentacao( linha ):
    comprimento = len(linha)
    if comprimento == 0: return 0
    tamanho = comprimento - len(linha.lstrip())
    if linha[0] == ' ': tamanho /= 4
    return tamanho


def CXXII_Identar( linha, total=1 ):
    espaco = '\t' if len(linha) > 0 and linha[0] == '\t' else '    '
    while total > 0:
        linha = espaco + linha
        total -= 1
    return linha


def CXXII_EscreverArquivo( endereco, inicio=1, fim=None, quebraFinal=True, formato='utf-8', dicGlobal=None, dicLocal=None ):
    """Escreve no arquivo em geração atual (CXXII_Atual()) o conteúdo de um arquivo-modelo.

    Arquivo-modelo é qualquer conteúdo que contenha instruções CXXII embutidas.
    Se o endereço do arquivo for relativo, ele primeiro será buscado em CXXII_Gerador_Diretorio.

    endereco    -- Endereço do arquivo-modelo. Pode-se utilizar "/" como separador.
    inicio      -- Número inicial do intervalo de linhas desejado. Padrão: 1
    fim         -- Número final do intervalo de linhas desejado. Padrão: None (última linha)
    quebraFinal -- Quebra de linha na última linha?
    dicGlobal   -- Ver globals()
    dicLocal    -- Ver locals()
    """
    global CXXII_Saida
    if CXXII_Saida is None: return

    if dicGlobal is None: dicGlobal = globals()
    if dicLocal  is None: dicLocal  = locals()

    endereco = CXXII_Separadores(endereco)
    if endereco[0] != os.sep and os.path.exists(CXXII_Gerador_Diretorio + os.sep + endereco):
        endereco = CXXII_Gerador_Diretorio + os.sep + endereco

    codigo = []
    modelo = open( endereco, 'r', encoding=formato )
    linhas = list(modelo)
    modelo.close()

    total = len(linhas)
    if inicio != 1 or fim != None:
        inicio = inicio - 1 if inicio != None else 0
        fim = fim if fim != None else total
        linhas = linhas[inicio:fim]
        if not quebraFinal and linhas[-1][-1] == '\n': linhas[-1] = linhas[-1][0:-1]
        total = len(linhas)

    identacao = 0
    i = 0

    while i < total:
        linha = linhas[i]
        if linha == '@@@\n':
            i += 1
            if i < total and identacao > 0 and linhas[i] == '@@@\n':
                identacao -= 1
            else:
                while i < total and linhas[i] != '@@@\n':
                    linha = linhas[i]
                    identacao = CXXII_ContarIdentacao(linha)
                    codigo.append(linha)
                    linha = linha.strip()
                    if len(linha) > 0 and linha[-1] == ':':
                        if linha.startswith('for ') or linha.startswith('while '):
                            identacao += 1
                    i += 1
        else:
            codigo.append(CXXII_Identar('"""~\n', identacao))
            finalComQuebra = False
            while i < total and linhas[i] != '@@@\n':
                linha = linhas[i]
                finalComQuebra = linha.endswith('\n')
                if not finalComQuebra: linha += '\n'
                codigo.append(linha)
                i += 1
            if finalComQuebra: codigo.append('\n')
            codigo.append(CXXII_Identar('"""\n', identacao))
            i -= 1
        i += 1

    CXXII_Executar( CXXII_CompilarPython(codigo), dicGlobal, dicLocal )


def CXXII_Texto( texto, decodificar=False ):
    if decodificar and type(texto) is bytes: texto = texto.decode(sys.getfilesystemencoding())
    return unicodedata.normalize('NFC', texto)


def CXXII_EscapeParaTexto( texto ):
    return texto.replace('\n','\\n').replace('\r','\\r').replace('\t','\\t').replace('\'','\\\'')


def CXXII_TextoParaEscape( texto ):
    return texto.replace('\\n','\n').replace('\\r','\r').replace('\\t','\t').replace('\\\'','\'')


def NomeDoArquivo( endereco, extensao=True ):
    if endereco[-1] == os.sep: endereco = endereco[0:-1]
    nome = endereco[endereco.rfind(os.sep)+1:]
    if not extensao:
        nome = nome[0:len(nome)-nome.rfind('.')]
    return nome


def CXXII_Compilar( endereco ):
    """Compila um arquivo codificado com a linguagem Python.

    Se o endereço do arquivo for relativo, ele primeiro será buscado em CXXII_Gerador_Diretorio.
    
    endereco -- Endereço do arquivo ".py". Pode-se utilizar "/" como separador.
    """
    endereco = CXXII_Separadores(endereco)
    if endereco[0] != os.sep and os.path.exists(CXXII_Gerador_Diretorio + os.sep + endereco):
        endereco = CXXII_Gerador_Diretorio + os.sep + endereco
    
    py_arquivo = CXXII_Abrir_Python(endereco)
    py = list(py_arquivo)
    py_arquivo.close()

    return CXXII_CompilarPython(py)


def CXXII_CompilarPython( codigoFonte ):
    """Compila um código fonte codificado com a linguagem Python."""
    py = list(codigoFonte) if type(codigoFonte) != list else codigoFonte
    
    if py[0].startswith('# coding='):
        py = py[1:]
    elif py[1].startswith('# coding='):
        py = py[2:]

    py[-1] += '\n'

    i = 0
    total = len(py)
    embutido = re.compile('({{{[^{}]*}}})')

    while i < total:

        linha = py[i]
        passo = 1

        if linha.endswith('"""~\n'):

            desconsiderar = False
            tokenstr = None
            cpre = None
            for c in linha:
                if tokenstr != None:
                    if c == tokenstr and cpre != '\\': tokenstr = None
                elif c == '#':
                    desconsiderar = True
                    break
                elif c == '\'' or c == '\"':
                    tokenstr = c
                cpre = c

            if desconsiderar:
                i += passo
                continue

            linha = linha[:-5] + 'CXXII_Escrever(\''

            a = i
            b = a + 1
            
            while b < total and not py[b].lstrip().startswith('"""'): b += 1
            if b >= total: raise Exception('Bloco de escrita não finalizado: linha ' + str(i))
            
            py[b] = py[b][py[b].index('"""')+3:]
            passo = b - a

            if (b-a) > 1:
                primeiro = True
                a += 1
                while a < b:
                    linha += ( '\\n' if not primeiro else '' ) + CXXII_EscapeParaTexto( py[a][:-1] )
                    py[a] = ''
                    primeiro = False
                    a += 1

            linhapos = 0
            while True:
                codigo = embutido.search(linha, linhapos)
                if not codigo is None:
                    parte1 = \
                        linha[0:codigo.start(0)] +\
                        '\'+' +\
                        CXXII_TextoParaEscape(codigo.group(0)[3:-3]) +\
                        '+\''
                    parte2 = linha[codigo.end(0):]
                    linha = parte1 + parte2
                    linhapos = len(parte1)
                else:
                    break

            linha += '\');'
            py[i] = linha

        i += passo

    return compile( ''.join(py), 'CXXII_Python', 'exec' )


def CXXII_Executar( python, dicGlobal=None, dicLocal=None ):
    """Executa um código Python pré-compilado com CXXII_Compilar() ou um arquivo Python.

    Se o endereço do arquivo for relativo, ele primeiro será buscado em CXXII_Gerador_Diretorio.

    python    -- Código pré-compilado ou endereço do arquivo. Pode-se utilizar "/" como separador.
    dicGlobal -- Ver globals()
    dicLocal  -- Ver locals()
    """
    if dicGlobal is None: dicGlobal = globals()
    if dicLocal  is None: dicLocal  = locals()
    exec( CXXII_Compilar(python) if type(python) is str else python, dicGlobal, dicLocal )


#----------------------------------------------------------------------------


CXXII_Repositorio = 'http://www.joseflavio.com/cxxii/'

CXXII_Inicio = datetime.datetime.today()
CXXII_Gerador_Endereco = None
CXXII_Gerador_Diretorio = None
CXXII_Gerador_TempoMaximo = 6*60*60 #6h
CXXII_Gerador_Baixar = False
CXXII_Destino = None
CXXII_XML_Arquivos = []
CXXII_Extensao = 'xml'
CXXII_Saida = sys.stdout

CXXII_Diretorio = CXXII_Texto(os.path.expanduser('~')) + os.sep + 'CXXII'
CXXII_Geradores = CXXII_Diretorio + os.sep + 'Geradores'
if not os.path.exists(CXXII_Geradores): os.makedirs(CXXII_Geradores)


#----------------------------------------------------------------------------


try:

#----------------------------------------------------------------------------

    argumentos = CXXII_Texto(' '.join(sys.argv), True)
    argumentos = argumentos.replace(' -g', '###g')
    argumentos = argumentos.replace(' -f', '###fSIM')
    argumentos = argumentos.replace(' -t', '###tSIM')
    argumentos = argumentos.replace(' -d', '###d')
    argumentos = argumentos.replace(' -e', '###e')
    argumentos = argumentos.replace(' -a', '###a')
    argumentos = argumentos.split('###')

    argumento_g = None
    argumento_f = None
    argumento_t = None
    argumento_d = None
    argumento_e = None
    argumento_a = None

    for argumento in argumentos[1:]:
        valor = argumento[1:].strip()
        if len(valor) == 0: continue
        exec( 'argumento_' + argumento[0] + '=\'' + valor + '\'' )

    if argumento_g is None or argumento_a is None:
        print('\nCXXII 1.0-A1 : Gerador de arquivos a partir de XML\n')
        print('cxxii -g GERADOR [-f] [-t] [-d DESTINO] [-e EXTENSAO] -a ARQUIVOS\n')
        print('Argumentos:')
        print('  -g   URL ou endereço local do gerador a utilizar: .py ou .zip')
        print('       Nome sem extensão = ' + CXXII_Repositorio + 'Nome.zip')
        print('  -f   Forçar download do gerador')
        print('  -t   Imprimir detalhes do erro que possa ocorrer')
        print('  -d   Destino dos arquivos gerados')
        print('  -e   Extensão padrão dos arquivos de entrada: xml')
        print('  -a   Arquivos XML de entrada ou diretórios que os contenham\n')
        sys.exit(1)

#----------------------------------------------------------------------------

    if argumento_e != None: CXXII_Extensao = argumento_e.lower()

    argumento_a = argumento_a.replace('.' + CXXII_Extensao, '.' + CXXII_Extensao + '###')
    argumento_a = argumento_a.split('###')

    for xml in argumento_a:
        xml = xml.strip()
        if len(xml) == 0: continue
        xml = CXXII_Texto(os.path.abspath(xml))
        if os.path.isdir(xml):
            for arquivo in os.listdir(xml):
                arquivo = CXXII_Texto(arquivo)
                if arquivo.lower().endswith('.' + CXXII_Extensao):
                    CXXII_XML_Adicionar(xml + os.sep + arquivo)
        else:
            CXXII_XML_Adicionar(xml)

    if len(CXXII_XML_Arquivos) == 0:
        sys.exit(0)

#----------------------------------------------------------------------------

    try:

        CXXII_Gerador_Baixar = not argumento_f is None

        gerurl = argumento_g.startswith('http://')
        if( gerurl and argumento_g[-1] == '/' ): argumento_g = argumento_g[0:-1]

        gernome = argumento_g[argumento_g.rfind('/' if gerurl else os.sep)+1:]
        gerpy = gernome.endswith('.py')
        gerzip = gernome.endswith('.zip')

        if gerurl:
            argumento_g = CXXII_Baixar(url=argumento_g, destino=CXXII_Geradores, forcar=CXXII_Gerador_Baixar)
        elif gerpy or gerzip:
            argumento_g = CXXII_Texto(os.path.abspath(argumento_g))
        else:
            gerurl = True
            gernome += '.zip'
            gerzip = True
            argumento_g = CXXII_Baixar(url=CXXII_Repositorio + gernome, destino=CXXII_Geradores, forcar=CXXII_Gerador_Baixar)

        if gerzip:
            
            destino = argumento_g[0:-4]
            if not os.path.exists(destino): os.makedirs(destino)

            CXXII_Gerador_Endereco = destino + os.sep + gernome[0:-4] + '.py'

            descompactar = not os.path.exists(CXXII_Gerador_Endereco)
            if not descompactar:
                descompactar = os.path.getmtime(argumento_g) > os.path.getmtime(CXXII_Gerador_Endereco)

            if descompactar:
                zip = zipfile.ZipFile(argumento_g, 'r')
                zip.extractall(destino)
                del zip

        else:
            CXXII_Gerador_Endereco = argumento_g

        CXXII_Gerador_Diretorio = CXXII_Texto(os.path.dirname(CXXII_Gerador_Endereco))

    except:
        raise Exception('Gerador inválido.')

#----------------------------------------------------------------------------

    CXXII_Destino = argumento_d if not argumento_d is None else 'CXXII_' + CXXII_Inicio.strftime('%Y%m%d%H%M%S')
    CXXII_Destino = CXXII_Texto(os.path.abspath(CXXII_Destino))
    if not os.path.exists(CXXII_Destino): os.makedirs(CXXII_Destino)

#----------------------------------------------------------------------------

    gerador_nome     = ''
    gerador_versao   = ''
    gerador_multiplo = True

    cxxii_con = CXXII_Abrir_Python(CXXII_Gerador_Endereco)
    cxxii_lin = list(cxxii_con)
    cxxii_ini = 0
    cxxii_tot = len(cxxii_lin)

    while cxxii_ini < cxxii_tot and cxxii_lin[cxxii_ini] != '### CXXII\n': cxxii_ini += 1

    if cxxii_ini < cxxii_tot:
        fim = cxxii_ini + 1
        while fim < cxxii_tot and cxxii_lin[fim] != '###\n': fim += 1
        if fim < cxxii_tot: exec(''.join(cxxii_lin[(cxxii_ini+1):fim]))

    cxxii_con.close()
    del cxxii_con
    del cxxii_lin
    del cxxii_ini
    del cxxii_tot

    gerador_nome = gerador_nome if gerador_nome != None and len(gerador_nome) > 0 else NomeDoArquivo(argumento_g)

    if gerador_versao == None: gerador_versao = 'Desconhecida'
    if not type(gerador_versao) is str: gerador_versao = str(gerador_versao)

    print( 'Gerador: ' + gerador_nome )
    print( 'Versão:  ' + gerador_versao )

#----------------------------------------------------------------------------

    CXXII_Gerador_Compilado = CXXII_Compilar( CXXII_Gerador_Endereco )
    CXXII_XML = CXXII_XML_Arquivos[0]

    if gerador_multiplo:
        for xml in CXXII_XML_Arquivos:
            print(xml.endereco)
            CXXII_XML = xml
            CXXII_Executar( CXXII_Gerador_Compilado, globals(), locals() )
    else:
        CXXII_Executar( CXXII_Gerador_Compilado, globals(), locals() )

#----------------------------------------------------------------------------

except Exception as e:
    if not argumento_t is None:
        import traceback
        traceback.print_exc()
    print('Erro: ' + str(e))


#----------------------------------------------------------------------------