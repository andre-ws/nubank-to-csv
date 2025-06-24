# `nubank-to-csv`

Script que converte o PDF da fatura do NuBank para CSV, incluindo o número do cartão onde foi feita cada compra (informação que falta no CSV oficial).

Primeiro o PDF precisa ser convertido para HTML (através do softwar e `pdftohtml`, contido no
pacote `poppler-utils`) e depois faz *parsing* do HTML, pegando somente os
dados desejados.

## Instalação

### Dependências

Dependências do sistema:

    apt-get install poppler-utils

## Uso

Primeiro converta o PDF para HTML e depois rode o script em cima do HTML.

Converter de PDF para HTML:

    pdftohtml XXX.pdf

onde `XXX.pdf` é o caminho para o arquivo de sua fatura. Isso irá gerar um
arquivo `XXXs.html` (dentre outros) no mesmo diretório.

Converter de HTML para CSV:

    python3 nubank.py XXXs.html -o minha-linda-fatura.csv

Agora é só brincar com o arquivo `minha-linda-fatura.csv`! ;-)


## Contribua!

O software é livre e você pode contribuir. :) Sugestões de contribuição:

- Criar função para já rodar o `pdftohtml` automaticamente, de forma que
  precisemos rodar apenas um comando (o próprio `nubank-to-csv`).
- Transformar a data que está como "01 JAN" pra um formato numérico melhor

