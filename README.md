# CXXII

Gerador de arquivos a partir de XML

File generator based on XML

    "Não vos conformeis com este mundo,
    mas transformai-vos pela renovação do vosso espírito,
    para que possais discernir qual é a vontade de Deus,
    o que é bom, o que lhe agrada e o que é perfeito."
    (Bíblia Sagrada, Romanos 12:2)

    "Do not conform yourselves to this age
    but be transformed by the renewal of your mind,
    that you may discern what is the will of God,
    what is good and pleasing and perfect."
    (Holy Bible, Romans 12:2)

## Exemplo.xml (Example)

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

## ./CXXII.sh -g Exemplo1 -d teste -a Exemplo.xml

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

## python3 CXXII.py

    Uso: CXXII -g GERADOR [-f] [-t] [-d DESTINO] [-e EXTENSAO] -a ARQUIVOS
    Argumentos:
      -g   URL ou endereço local do gerador a utilizar: .py ou .zip
           Nome sem extensão = http://www.joseflavio.com/cxxii/Nome.zip
      -f   Forçar download do gerador
      -t   Imprimir detalhes do erro que possa ocorrer
      -d   Destino dos arquivos gerados
      -e   Extensão padrão dos arquivos de entrada: xml
      -a   Arquivos XML de entrada ou diretórios que os contenham
