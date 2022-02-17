import pandas as pd
from datetime import date
from datetime import datetime as dt
import calendar
from periodo_horario.ciclo import *
from periodo_horario.horario import cria_horario_legal, cria_feriados
import sys
import os
from common.utils import write_excel


dir_path = os.path.dirname(os.path.realpath(__file__))


def create_df(date_begin, date_end):
    year_begin = int(date_begin.split("-")[0])
    month_begin = int(date_begin.split("-")[1])
    date_begin = dt(year_begin, month_begin, 1)
    year_end = int(date_end.split("-")[0])
    month_end = int(date_end.split("-")[1])
    date_end = dt(
        year_end, month_end, calendar.monthrange(year_end, month_end)[1], 23, 59
    )
    date_range = pd.date_range(date_begin, date_end, freq="15min")
    df = pd.DataFrame(index=date_range)
    df["date"] = df.index.strftime("%Y/%m/%d")
    df["hour"] = df.index.strftime("%H:%M")
    return df


def periodo_horario(abastecimento, ciclo, date_begin, date_end):
    """
    Creates column with 'periodo_horario' and column with 'fora_vazio'.
    example:
    abastecimento = 'MT' # (or 'BTE' or 'BTN' or 'AT')
    ciclo = 'semanal' # or 'diario' por 'opcional'
    date_begin = '2019-09'
    date_end = '2020-08'
    """
    print("\n\nTrying to get periodo horario data...")
    print(f"abastecimento: {abastecimento}")
    print(f"ciclo: {ciclo}")
    print(f"date_begin: {date_begin}")
    print(f"date_end: {date_end}")

    abastecimento = abastecimento.upper()
    df = create_df(date_begin, date_end)
    df = cria_horario_legal(df)

    feriados = [cria_feriados(a, "Lisboa") for a in df.index.year.unique()]
    feriados = [item for sublist in feriados for item in sublist]
    df["feriado"] = df.date.isin([f.strftime("%Y/%m/%d") for f in feriados])

    if ciclo == "semanal":
        df = ciclo_semanal(df, abastecimento)

    elif ciclo == "diario":
        if abastecimento not in ["BTE", "BTN"]:
            print(
                "If not BTE or BTN cant have ciclo diario. Calculation as ciclo semanal."
            )

            df = ciclo_semanal(df, abastecimento)
        else:
            df = ciclo_diario(df)

    elif ciclo == "opcional":
        df = ciclo_opcional(df, abastecimento)
    else:
        print("No ciclo!choose ciclo diario by default.")
        df = ciclo_diario(df)

    df.loc[df["p_horario"].isin(["P", "C"]), "fora_vazio"] = True
    df.loc[df["p_horario"].isin(["SV", "VN"]), "fora_vazio"] = False

    filename = f"ph_{abastecimento}_{ciclo}_{date_begin}_{date_end}.xlsx"
    write_excel(df, dir_path, filename)


if __name__ == "__main__":
    args = list(sys.argv)

    if len(args) == 5:
        periodo_horario(args[1], args[2], args[3], args[4])
    else:
        print(
            "4 arguments are expected (ciclo, abastecimento, date_begin, date_end)..."
        )
        print(f"------> only {len(args) - 1} where given")
