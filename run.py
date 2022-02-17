import sys
from typing import List
from periodo_horario.main import periodo_horario
from telecontagem.main import get_telecontagem
from enum import Enum
import os

CPES_FILE_PATH = "telecontagem/cpes.txt"


class Programs(Enum):
    TELECONTAGEM = "telecontagem"
    PERIODO_HORARIO = "periodo_horario"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


def run_periodo_horario(args: List[str]):
    if len(args) == 6:
        periodo_horario(args[2], args[3], args[4], args[5])
    else:
        print(
            "4 arguments are expected (ciclo, abastecimento, date_begin, date_end)..."
        )
        print(f"------> only {len(args) - 2} where given")


def run_get_telecontagem(args: List[str]):
    cpes = args[2:-2]
    date_start = args[-2]
    date_end = args[-1]

    if not cpes:  # if no cpes are passed in the comand, read them from the .txt file
        if not os.path.exists(CPES_FILE_PATH):
            print(
                f"No cpes were passed in the comand and theres no {CPES_FILE_PATH} file"
            )
            return

        with open("telecontagem/cpes.txt", "r") as cpes_file:
            cpes = [c.strip() for c in cpes_file]

    cpes = list(set(cpes))
    if not cpes:
        print("no cpes passed")
        return
    for cpe in cpes:
        get_telecontagem(cpe, date_start, date_end)


if __name__ == "__main__":
    args = list(sys.argv)

    if args[1] == Programs.PERIODO_HORARIO.value:
        run_periodo_horario(args)

    elif args[1] == Programs.TELECONTAGEM.value:
        run_get_telecontagem(args)

    else:
        print(
            f'{args[1]} is not a valid program name: it should be one of {" or ".join(Programs.list())}'
        )
