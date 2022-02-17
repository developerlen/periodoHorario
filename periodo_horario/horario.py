from datetime import timedelta, date
import calendar


def cria_horario_legal(df):
    """tells if is summer or winter. adds a column to given df.

    Args:
        df (pandas DataFrame): dataframe cujo index vem em datetime64

    Returns:
        pandas DataFrame: a mesma dataframe mas com mais uma coluna, que diz se é verão ou inverno
    """

    # definição dos ultimos domingos dos meses de março e outubro, datas em que muda o horario legal
    last_sundays = []
    for year in df.index.year.unique():
        last_sundays_year = []

        for month in [3, 10]:
            day = max(week[-1] for week in calendar.monthcalendar(year, month))
            last_sunday = date(year, month, day)
            last_sundays_year.append(last_sunday)
        last_sundays.append(last_sundays_year)

    # define se é verão ou inverno e cria essa coluna nova "horario_legal"
    for changes in last_sundays:
        df.loc[((df.index >= changes[0].strftime('%Y-%m-%d')) & (
            df.index < changes[1].strftime('%Y-%m-%d'))), 'horario_legal'] = 'V'

    df['horario_legal'] = df['horario_legal'].fillna('I')

    return df


def data_pascoa(ano):

    a = ano % 19
    b = ano // 100
    c = ano % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mes = (h + l - 7 * m + 114) // 31
    dia = ((h + l - 7 * m + 114) % 31) + 1

    data = date(ano, mes, dia)
    return (data)


def cria_feriados(ano, municipio):

    # ano = data.year

    feriados = ["01-01", "04-25", "05-01", "06-10", "08-15", "10-05", "11-01", "12-01", "12-08", "12-25"]

    if municipio in ["Lisboa", "Cascais"]:
        feriados = feriados + ["06-13"]
    elif municipio == 'Amadora':
        feriados = feriados + ["09-11"]
    elif municipio == 'Porto':
        feriados = feriados + ["06-24"]
    elif municipio == 'Loures':
        feriados = feriados + ["07-26"]
    elif municipio == 'Mafra':
        feriados = feriados + ["05-10"]
    elif municipio == 'Sintra':
        feriados = feriados + ["06-29"]

    feriados = [str(ano) + '-' + f for f in feriados]
    feriados = [f.split('-') for f in feriados]
    feriados = [date(int(f[0]), int(f[1]), int(f[2])) for f in feriados]

    pascoa = data_pascoa(ano)
    sexta_santa = pascoa - timedelta(days=2)

    carnaval = pascoa - timedelta(days=47)
    # tem que ser 3a feira
    if carnaval.weekday() != 1:
        diff = 1 - carnaval.weekday()
        carnaval = carnaval + timedelta(days=diff)

    corpo_cristo = pascoa + timedelta(days=60)
    # tem que ser 5a feira
    if corpo_cristo.weekday() != 3:
        diff = 3 - corpo_cristo.weekday()
        corpo_cristo = corpo_cristo + timedelta(days=diff)

    feriados = feriados + [pascoa, sexta_santa, carnaval, corpo_cristo]

    return feriados
