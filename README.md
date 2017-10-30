# CXXII

Gerador de arquivos a partir de XML.

File generator based on XML.

## Versão Atual / Current Version

1.0-A1

Padrão de versionamento: [JFV](http://joseflavio.com/jfv)

## Exemplo / Example

Considerando o arquivo de entrada [Exemplo.xml](https://github.com/joseflaviojr/cxxii/blob/master/Exemplo.xml) e o gerador [Exemplo1](https://github.com/joseflaviojr/cxxii/blob/master/Exemplo1.py).

Considering the input file [Exemplo.xml](https://github.com/joseflaviojr/cxxii/blob/master/Exemplo.xml) and the generator [Exemplo1](https://github.com/joseflaviojr/cxxii/blob/master/Exemplo1.py).

``` xml
<pessoas>
    <pessoa>
        <nome>Maria</nome>
        <endereco>Rua M</endereco>
    </pessoa>
    <pessoa>
        <nome>José</nome>
        <endereco>Rua J</endereco>
    </pessoa>
</pessoas>
```

Executar `cxxii -g Exemplo1 -d teste -a Exemplo.xml`, obtendo:

Run `cxxii -g Exemplo1 -d teste -a Exemplo.xml`, obtaining:

``` html
<html>
    <head>
        <title>Exemplo 1</title>
        <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
    </head>
    <body>
        <h1><b>Pessoas</b></h1>
        <p><b>Nome:</b> Maria</p>
        <p><b>Endereço:</b> Rua M</p>
        <hr>
        <p><b>Nome:</b> José</p>
        <p><b>Endereço:</b> Rua J</p>
        <hr>
    </body>
</html>
```

## Requisitos / Requirements

- Python 3

## Instalação / Installation

Execute as seguintes instruções no terminal de comandos do Linux ou macOS.

Run the following instructions on the Linux or macOS command terminal.

``` bash
sudo wget https://github.com/joseflaviojr/cxxii/archive/1.0-A1.zip -O /usr/local/CXXII.zip
sudo unzip /usr/local/CXXII.zip -d /usr/local/
sudo rm -f /usr/local/CXXII.zip
sudo chmod 755 /usr/local/cxxii-1.0-A1/CXXII.py
sudo ln -s /usr/local/cxxii-1.0-A1/CXXII.py /usr/local/bin/cxxii
```

## Desinstalação / Uninstall

``` bash
sudo rm -f /usr/local/bin/cxxii
sudo rm -rf /usr/local/cxxii-1.0-A1
```

## Modo de Uso / Mode of Use

    Uso: cxxii -g GERADOR [-f] [-t] [-d DESTINO] [-e EXTENSAO] -a ARQUIVOS
    Argumentos:
      -g   URL ou endereço local do gerador a utilizar: .py ou .zip
           Nome sem extensão = http://www.joseflavio.com/cxxii/Nome.zip
      -f   Forçar download do gerador
      -t   Imprimir detalhes do erro que possa ocorrer
      -d   Destino dos arquivos gerados
      -e   Extensão padrão dos arquivos de entrada: xml
      -a   Arquivos XML de entrada ou diretórios que os contenham
