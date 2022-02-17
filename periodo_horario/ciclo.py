import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'


def ciclo_semanal(df, tt):
    """returns DataFrame, with periodo horário identified, acording to ERSE.
        aplica-se a todo o tipo de instalações(AT, MAT, MT, BTE e BTN)
        os feriados são apenas relevantes para as AT, MAT e MT

    Args:
        df (pandas Dataframe): 15min interval data
        tt (string): Type of 'abastecimento' (BTN, BTE, MT)

    Returns:
        (pandas Dataframe): 15min interval data, with periodo horário column (p_horario)
    """

    # segunda a sexta
    if tt not in ["BTN", "BTE"]:
        df_uteis = df.loc[
            (df.index.weekday.isin([0, 1, 2, 3, 4]) & df.feriado.isin([False])), :
        ].copy()
    else:
        df_uteis = df.loc[df.index.weekday.isin([0, 1, 2, 3, 4]), :].copy()

    df_uteis["p_horario"] = np.nan
    df_uteis["p_horario"].fillna(
        df_uteis.between_time("09:30", "12:00", inclusive="left")["p_horario"].fillna(
            "P"
        ),
        inplace=True,
    )
    df_uteis["p_horario"].fillna(
        df_uteis.between_time("07:00", "09:15", inclusive="left")["p_horario"].fillna(
            "C"
        ),
        inplace=True,
    )
    df_uteis["p_horario"].fillna(
        df_uteis.between_time("06:00", "07:00", inclusive="left")["p_horario"].fillna(
            "VN"
        ),
        inplace=True,
    )

    df = df.join(df_uteis["p_horario"])

    # Sabados
    df_sab = df.loc[df.index.weekday.isin([5]), :]

    df_sab["p_horario"].fillna(
        df_sab.between_time("09:30", "13:00", inclusive="left")["p_horario"].fillna(
            "C"
        ),
        inplace=True,
    )
    df_sab["p_horario"].fillna(
        df_sab.between_time("20:00", "22:00", inclusive="left")["p_horario"].fillna(
            "C"
        ),
        inplace=True,
    )
    df_sab["p_horario"].fillna(
        df_sab.between_time("06:00", "09:00", inclusive="left")["p_horario"].fillna(
            "VN"
        ),
        inplace=True,
    )
    df_sab["p_horario"].fillna(
        df_sab.between_time("22:00", "00:00", inclusive="left")["p_horario"].fillna(
            "VN"
        ),
        inplace=True,
    )

    df.fillna(df_sab, inplace=True)

    # Domingos e caso NOT BTE/BTN feriados tbm
    if tt not in ["BTN", "BTE"]:
        df_dom = df.loc[
            (df.index.weekday.isin([6]) | df.feriado.isin([True])), :
        ].copy()
    else:
        df_dom = df.loc[df.index.weekday.isin([6]), :].copy()

    df_dom["p_horario"].fillna(
        df_dom.between_time("06:00", "00:00", inclusive="left")["p_horario"].fillna(
            "VN"
        ),
        inplace=True,
    )

    df.fillna(df_dom, inplace=True)

    # Verao
    df_V = df.loc[df["horario_legal"] == "V", ["horario_legal", "feriado", "p_horario"]]

    # segunda a sexta
    df_V_uteis = df_V.loc[df_V.index.weekday.isin([0, 1, 2, 3, 4]), :]

    df_V_uteis["p_horario"].fillna(
        df_V_uteis.between_time("09:15", "09:30", inclusive="left")["p_horario"].fillna(
            "P"
        ),
        inplace=True,
    )
    df_V_uteis["p_horario"].fillna(
        df_V_uteis.between_time("12:00", "12:15", inclusive="left")["p_horario"].fillna(
            "P"
        ),
        inplace=True,
    )

    df_V_uteis["p_horario"].fillna(
        df_V_uteis.between_time("12:15", "00:00", inclusive="left")["p_horario"].fillna(
            "C"
        ),
        inplace=True,
    )

    df_V.fillna(df_V_uteis, inplace=True)

    # Sabados
    df_V_sab = df_V.loc[df_V.index.weekday.isin([5]), :]

    df_V_sab["p_horario"].fillna(
        df_V_sab.between_time("09:00", "09:30", inclusive="left")["p_horario"].fillna(
            "C"
        ),
        inplace=True,
    )
    df_V_sab["p_horario"].fillna(
        df_V_sab.between_time("13:00", "14:00", inclusive="left")["p_horario"].fillna(
            "C"
        ),
        inplace=True,
    )
    df_V_sab["p_horario"].fillna(
        df_V_sab.between_time("14:00", "20:00", inclusive="left")["p_horario"].fillna(
            "VN"
        ),
        inplace=True,
    )

    df_V.fillna(df_V_sab, inplace=True)

    # Inverno:
    df_I = df.loc[df["horario_legal"] == "I", ["horario_legal", "feriado", "p_horario"]]

    # segunda a sexta
    df_I_uteis = df_I.loc[df_I.index.weekday.isin([0, 1, 2, 3, 4]), :]

    df_I_uteis["p_horario"].fillna(
        df_I_uteis.between_time("18:30", "21:00", inclusive="left")["p_horario"].fillna(
            "P"
        ),
        inplace=True,
    )

    df_I_uteis["p_horario"].fillna(
        df_I_uteis.between_time("09:15", "09:30", inclusive="left")["p_horario"].fillna(
            "C"
        ),
        inplace=True,
    )
    df_I_uteis["p_horario"].fillna(
        df_I_uteis.between_time("12:00", "18:30", inclusive="left")["p_horario"].fillna(
            "C"
        ),
        inplace=True,
    )
    df_I_uteis["p_horario"].fillna(
        df_I_uteis.between_time("21:00", "00:00", inclusive="left")["p_horario"].fillna(
            "C"
        ),
        inplace=True,
    )

    df_I.fillna(df_I_uteis, inplace=True)

    # sabados
    df_I_sab = df_I.loc[df_I.index.weekday.isin([5]), :]
    df_I_sab["p_horario"].fillna(
        df_I_sab.between_time("18:30", "20:00", inclusive="left")["p_horario"].fillna(
            "C"
        ),
        inplace=True,
    )

    df_I_sab["p_horario"].fillna(
        df_I_sab.between_time("09:00", "09:30", inclusive="left")["p_horario"].fillna(
            "VN"
        ),
        inplace=True,
    )
    df_I_sab["p_horario"].fillna(
        df_I_sab.between_time("13:00", "18:30", inclusive="left")["p_horario"].fillna(
            "VN"
        ),
        inplace=True,
    )

    df_I.fillna(df_I_sab, inplace=True)

    df.fillna(df_I, inplace=True)
    df.fillna(df_V, inplace=True)

    # comum a todos
    df["p_horario"].fillna(
        df.between_time("00:00", "02:00", inclusive="left")["p_horario"].fillna("VN"),
        inplace=True,
    )
    df["p_horario"].fillna(
        df.between_time("02:00", "06:00", inclusive="left")["p_horario"].fillna("SV"),
        inplace=True,
    )

    return df


def ciclo_opcional(df, tt):
    """returns DataFrame, with periodo horário identified, acording to ERSE.
        aplica-se apenas a MT, MAT e AT.


    Args:
        df (pandas Dataframe): 15min interval data
        tt (string): Type of 'abastecimento' (BTN, BTE, MT)

    Returns:
        (pandas Dataframe): 15min interval data, with periodo horário column (p_horario)
    """

    if tt not in ["BTN", "BTE"]:
        df_uteis = df.loc[
            (df.index.weekday.isin([0, 1, 2, 3, 4]) & df.feriado.isin([False])), :
        ].copy()
    else:
        df_uteis = df.loc[df.index.weekday.isin([0, 1, 2, 3, 4]), :].copy()

    df_uteis["p_horario"] = np.nan
    df_uteis["p_horario"].fillna(
        df_uteis.between_time("00:00", "00:30", inclusive="left")["p_horario"].fillna(
            "C"
        ),
        inplace=True,
    )
    df_uteis["p_horario"].fillna(
        df_uteis.between_time("07:30", "14:00", inclusive="left")["p_horario"].fillna(
            "C"
        ),
        inplace=True,
    )
    df_uteis["p_horario"].fillna(
        df_uteis.between_time("22:00", "00:00", inclusive="left")["p_horario"].fillna(
            "C"
        ),
        inplace=True,
    )

    df_uteis["p_horario"].fillna(
        df_uteis.between_time("00:30", "02:00", inclusive="left")["p_horario"].fillna(
            "VN"
        ),
        inplace=True,
    )
    df_uteis["p_horario"].fillna(
        df_uteis.between_time("06:00", "07:30", inclusive="left")["p_horario"].fillna(
            "VN"
        ),
        inplace=True,
    )

    df_uteis["p_horario"].fillna(
        df_uteis.between_time("02:00", "06:00", inclusive="left")["p_horario"].fillna(
            "SV"
        ),
        inplace=True,
    )

    df = df.join(df_uteis["p_horario"])

    # Sabados
    df_sab = df.loc[df.index.weekday.isin([5]), :].copy()

    df_sab["p_horario"].fillna(
        df_sab.between_time("10:30", "12:30", inclusive="left")["p_horario"].fillna(
            "C"
        ),
        inplace=True,
    )
    df_sab["p_horario"].fillna(
        df_sab.between_time("19:30", "22:30", inclusive="left")["p_horario"].fillna(
            "C"
        ),
        inplace=True,
    )
    df_sab["p_horario"].fillna(
        df_sab.between_time("00:00", "03:00", inclusive="left")["p_horario"].fillna(
            "VN"
        ),
        inplace=True,
    )
    df_sab["p_horario"].fillna(
        df_sab.between_time("07:30", "10:00", inclusive="left")["p_horario"].fillna(
            "VN"
        ),
        inplace=True,
    )

    df_sab["p_horario"].fillna(
        df_sab.between_time("13:30", "17:30", inclusive="left")["p_horario"].fillna(
            "VN"
        ),
        inplace=True,
    )

    df_sab["p_horario"].fillna(
        df_sab.between_time("23:00", "00:00", inclusive="left")["p_horario"].fillna(
            "VN"
        ),
        inplace=True,
    )

    df_sab["p_horario"].fillna(
        df_sab.between_time("03:30", "07:00", inclusive="left")["p_horario"].fillna(
            "SV"
        ),
        inplace=True,
    )

    df.fillna(df_sab, inplace=True)

    # Domingos e caso NOT BTE/BTN feriados tbm
    if tt not in ["BTN", "BTE"]:
        df_dom = df.loc[
            (df.index.weekday.isin([6]) | df.feriado.isin([True])), :
        ].copy()
    else:
        df_dom = df.loc[df.index.weekday.isin([6]), :].copy()

    df_dom["p_horario"].fillna(
        df_dom.between_time("00:00", "04:00", inclusive="left")["p_horario"].fillna(
            "VN"
        ),
        inplace=True,
    )
    df_dom["p_horario"].fillna(
        df_dom.between_time("08:00", "00:00", inclusive="left")["p_horario"].fillna(
            "VN"
        ),
        inplace=True,
    )

    df_dom["p_horario"].fillna(
        df_dom.between_time("04:00", "08:00", inclusive="left")["p_horario"].fillna(
            "SV"
        ),
        inplace=True,
    )
    df.fillna(df_dom, inplace=True)

    # Verao
    df_V = df.loc[
        df["horario_legal"] == "V", ["horario_legal", "feriado", "p_horario"]
    ].copy()

    # segunda a sexta
    df_V_uteis = df_V.loc[df_V.index.weekday.isin([0, 1, 2, 3, 4]), :].copy()

    df_V_uteis["p_horario"].fillna(
        df_V_uteis.between_time("14:00", "17:00", inclusive="left")["p_horario"].fillna(
            "P"
        ),
        inplace=True,
    )

    df_V_uteis["p_horario"].fillna(
        df_V_uteis.between_time("17:00", "22:00", inclusive="left")["p_horario"].fillna(
            "C"
        ),
        inplace=True,
    )

    df_V.fillna(df_V_uteis, inplace=True)

    # Sabados
    df_V_sab = df_V.loc[df_V.index.weekday.isin([5]), :].copy()

    df_V_sab["p_horario"].fillna(
        df_V_sab.between_time("10:00", "10:30", inclusive="left")["p_horario"].fillna(
            "C"
        ),
        inplace=True,
    )
    df_V_sab["p_horario"].fillna(
        df_V_sab.between_time("12:30", "13:30", inclusive="left")["p_horario"].fillna(
            "C"
        ),
        inplace=True,
    )
    df_V_sab["p_horario"].fillna(
        df_V_sab.between_time("22:30", "23:00", inclusive="left")["p_horario"].fillna(
            "C"
        ),
        inplace=True,
    )

    df_V_sab["p_horario"].fillna(
        df_V_sab.between_time("17:30", "19:30", inclusive="left")["p_horario"].fillna(
            "VN"
        ),
        inplace=True,
    )

    df_V_sab["p_horario"].fillna(
        df_V_sab.between_time("03:00", "03:30", inclusive="left")["p_horario"].fillna(
            "VN"
        ),
        inplace=True,
    )

    df_V_sab["p_horario"].fillna(
        df_V_sab.between_time("07:00", "07:30", inclusive="left")["p_horario"].fillna(
            "SV"
        ),
        inplace=True,
    )

    df_V.fillna(df_V_sab, inplace=True)

    # Inverno:
    df_I = df.loc[
        df["horario_legal"] == "I", ["horario_legal", "feriado", "p_horario"]
    ].copy()

    # segunda a sexta
    df_I_uteis = df_I.loc[df_I.index.weekday.isin([0, 1, 2, 3, 4]), :].copy()

    df_I_uteis["p_horario"].fillna(
        df_I_uteis.between_time("17:00", "22:00", inclusive="left")["p_horario"].fillna(
            "P"
        ),
        inplace=True,
    )

    df_I_uteis["p_horario"].fillna(
        df_I_uteis.between_time("14:00", "17:00", inclusive="left")["p_horario"].fillna(
            "C"
        ),
        inplace=True,
    )

    df_I.fillna(df_I_uteis, inplace=True)

    # sabados
    df_I_sab = df_I.loc[df_I.index.weekday.isin([5]), :].copy()
    df_I_sab["p_horario"].fillna(
        df_I_sab.between_time("17:30", "19:30", inclusive="left")["p_horario"].fillna(
            "C"
        ),
        inplace=True,
    )

    df_I_sab["p_horario"].fillna(
        df_I_sab.between_time("07:00", "07:30", inclusive="left")["p_horario"].fillna(
            "VN"
        ),
        inplace=True,
    )
    df_I_sab["p_horario"].fillna(
        df_I_sab.between_time("10:00", "10:30", inclusive="left")["p_horario"].fillna(
            "VN"
        ),
        inplace=True,
    )
    df_I_sab["p_horario"].fillna(
        df_I_sab.between_time("12:30", "13:30", inclusive="left")["p_horario"].fillna(
            "VN"
        ),
        inplace=True,
    )
    df_I_sab["p_horario"].fillna(
        df_I_sab.between_time("22:30", "23:00", inclusive="left")["p_horario"].fillna(
            "VN"
        ),
        inplace=True,
    )

    df_I_sab["p_horario"].fillna(
        df_I_sab.between_time("03:00", "03:30", inclusive="left")["p_horario"].fillna(
            "SV"
        ),
        inplace=True,
    )
    df_I.fillna(df_I_sab, inplace=True)

    df.fillna(df_I, inplace=True)
    df.fillna(df_V, inplace=True)

    return df


def ciclo_diario(df):
    """returns DataFrame, with periodo horário identified, acording to ERSE.
        aplica-se apenas a BTEs e BTNs.


    Args:
        df (pandas Dataframe): 15min interval data

    Returns:
        (pandas Dataframe): 15min interval data, with periodo horário column (p_horario)
    """

    df["p_horario"] = np.nan

    # Inverno
    # df_i = copy.deepcopy(df.loc[df['horario_legal'] == 'I', ['horario_legal', 'feriado', 'p_horario']])

    df["p_horario"].fillna(
        df.loc[df["horario_legal"] == "I", :]
        .between_time("09:00", "10:30", inclusive="left")["p_horario"]
        .fillna("P"),
        inplace=True,
    )
    df["p_horario"].fillna(
        df.loc[df["horario_legal"] == "I", :]
        .between_time("18:00", "19:30", inclusive="left")["p_horario"]
        .fillna("P"),
        inplace=True,
    )

    df["p_horario"].fillna(
        df.loc[df["horario_legal"] == "I", :]
        .between_time("10:30", "13:00", inclusive="left")["p_horario"]
        .fillna("C"),
        inplace=True,
    )
    df["p_horario"].fillna(
        df.loc[df["horario_legal"] == "I", :]
        .between_time("20:30", "21:00", inclusive="left")["p_horario"]
        .fillna("C"),
        inplace=True,
    )

    # df.fillna(df_i, inplace=True, axis=1)

    # Verão
    # df_v = df.loc[df['horario_legal'] == 'V', ['horario_legal', 'feriado', 'p_horario']]
    df["p_horario"].fillna(
        df.loc[df["horario_legal"] == "V", :]
        .between_time("10:30", "13:00", inclusive="left")["p_horario"]
        .fillna("P"),
        inplace=True,
    )
    df["p_horario"].fillna(
        df.loc[df["horario_legal"] == "V", :]
        .between_time("20:30", "21:00", inclusive="left")["p_horario"]
        .fillna("P"),
        inplace=True,
    )

    df["p_horario"].fillna(
        df.loc[df["horario_legal"] == "V", :]
        .between_time("09:00", "10:30", inclusive="left")["p_horario"]
        .fillna("C"),
        inplace=True,
    )
    df["p_horario"].fillna(
        df.loc[df["horario_legal"] == "V", :]
        .between_time("18:00", "19:30", inclusive="left")["p_horario"]
        .fillna("C"),
        inplace=True,
    )

    # df.fillna(df_v, inplace=True)

    # comum a todos
    df["p_horario"].fillna(
        df.between_time("19:30", "20:30", inclusive="left")["p_horario"].fillna("P"),
        inplace=True,
    )

    df["p_horario"].fillna(
        df.between_time("08:00", "09:00", inclusive="left")["p_horario"].fillna("C"),
        inplace=True,
    )
    df["p_horario"].fillna(
        df.between_time("13:00", "18:00", inclusive="left")["p_horario"].fillna("C"),
        inplace=True,
    )
    df["p_horario"].fillna(
        df.between_time("21:00", "22:00", inclusive="left")["p_horario"].fillna("C"),
        inplace=True,
    )

    df["p_horario"].fillna(
        df.between_time("06:00", "08:00", inclusive="left")["p_horario"].fillna("VN"),
        inplace=True,
    )
    df["p_horario"].fillna(
        df.between_time("22:00", "02:00", inclusive="left")["p_horario"].fillna("VN"),
        inplace=True,
    )

    df["p_horario"].fillna(
        df.between_time("02:00", "06:00", inclusive="left")["p_horario"].fillna("SV"),
        inplace=True,
    )

    return df
