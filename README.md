# Periodo Horário

cria ficheiro `excel`, com colunas com o horário legal, periodo horário e se é no vazio ou fora do vazio a um intervalo de duas datas, com frequencia de 15 minutos.

# Para instalar

É necessário ter o python instalado no computador. É necessário também instalar as dependencias:

```
  pip install -r requirements.txt
```

# Para correr

basta ir à linha de comandos e chamar o ficheiro `main.py` com os argumentos necessários, com a <b>ordem certa</b>:

```
  python main.py <abastecimento> <ciclo> <date_begin> <date_end>
```

- <b>abastecimento</b>: MT, BTE ou BTN
- <b>ciclo</b>: diario, semanal ou opcional
- <b>date_begin</b>: data no formato yyyy-mm (ex: 2020-01, 2015-12, ...)
- <b>date_end</b>: data no formato yyyy-mm (ex: 2020-01, 2015-12, ...)

## exemplo

```
  python main.py MT diario 2019-09 2020-08
```
