# Rotinas

Diversas rotinas para trabalho interno da Lisboa E-Nova. <a href="https://developerlen.github.io/rotinas/" >Clique aqui</a> Para aceder à versão online e formatada deste documento.

# Setup

## Python

Se não tiver o python instalado no computador, pode ir <a href="https://www.python.org/downloads/">aqui</a> e instalar a versão mais recente.

## Bibliotecas

Estes programas usam algumas bibliotecas externas.
Para garantir que não há incompatibildades de versões de bibliotecas, o melhor é criar um ambiente virutal, activar e instalar as bibliotecas.

_WINDOWS_

```dos
C:\Windows\...\rotinas> python -m venv venv
C:\Windows\...\rotinas> .\venv\scripts\activate
C:\Windows\...\rotinas> pip install -r requirements.txt
```

_MAC/LINUX_

```bash
~$ python3 -m venv venv
~$ source venv/bin/activate
~$ pip install -r requirements.txt
```

# Run

Sempre que quiser correr qualquer um dos programas aqui existentes, deve-se activar primeiro o ambiente virtual:

_WINDOWS_

```dos
C:\Windows\...\rotinas> .\venv\scripts\activate
```

_MAC/LINUX_

```bash
~$ source venv/bin/activate
```

# Programas

## Periodo Horário

cria ficheiro `excel`, com colunas com o horário legal, periodo horário e se é no vazio ou fora do vazio a um intervalo de duas datas, com frequencia de 15 minutos.

Para correr basta ir à linha de comandos e chamar o ficheiro `run.py` com os argumentos necessários, com a <b>ordem certa</b>:

<br/>

> ⚠️ **Não esquecer**: activar o ambiente virtual primeiro!

<br/>

```
C:\Windows\...\rotinas> python run.py periodo_horario <abastecimento> <ciclo> <date_begin> <date_end>
```

- <b>abastecimento</b>: MT, BTE ou BTN
- <b>ciclo</b>: diario, semanal ou opcional
- <b>date_begin</b>: data no formato yyyy-mm (ex: 2020-01, 2015-12, ...)
- <b>date_end</b>: data no formato yyyy-mm (ex: 2020-01, 2015-12, ...)

_Exemplo_

```
C:\Windows\...\rotinas> python run.py periodo_horario BTE semanal 2019-09 2020-08
```

## Telecontagem

cria 1 ou mais ficheiros `excel` com dados de telecontagem, proveniente da API dos observatórios, para cada um dos cpes pretendidos entre 2 datas

### Setup

É necessário criar um ficheiro `secret.py` na pasta `telecontagem` com as varíaveis `USER` e `PASSWORD` para aceder à API dos observatórios. Basta copiar o ficheiro `telecontagem/secret.example.py` editar com a informação correcta e gravar como `telecontagem/secret.py`.

### Run

Para correr basta ir à linha de comandos e chamar o ficheiro `run.py` com os argumentos necessários, com a <b>ordem certa</b>:

<br/>

> ⚠️ **Não esquecer**: activar o ambiente virtual primeiro!

<br/>

_Para um só cpe_

```
C:\Windows\...\rotinas> python run.py telecontagem <cpe> <date_begin> <date_end>
```

_Para vários cpes_

```
C:\Windows\...\rotinas> python run.py telecontagem <cpe1> <cpe2> <cpe3> <date_begin> <date_end>
```

- <b>cpe(s)</b>: um ou vários cpes (separados por um espaço)
- <b>date_begin</b>: data no formato yyyy-mm-dd (ex: 2020-01-01, 2015-12-14, ...)
- <b>date_end</b>: data no formato yyyy-mm-dd (ex: 2020-01-01, 2015-12-14, ...)

### Examples

- **Um só CPE**

```
C:\Windows\...\rotinas> python run.py telecontagem PT0002000038740856ZG 2019-09-01 2020-08-31
```

- **Vários CPEs**

```
C:\Windows\...\rotinas> python run.py telecontagem PT0002000039321285LM PT0002000038740856ZG 2019-09-01 2020-08-31
```

- **Muitos CPEs**

podem ainda editar o ficheiro `telecontagem/cpes.txt` e colocar vários cpes, um em cada linha. Nesse caso, não se devem passar CPEs ao chamar o comando:

```
C:\Windows\...\rotinas> python run.py telecontagem 2019-09-01 2020-08-31
```
