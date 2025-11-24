from readkeys import getch
import os
import sys

if sys.platform in ("linux", "darwin"):
    CLEAR = "clear"
elif sys.platform == "win32":
    CLEAR = "cls"
else:
    print("Platform not supported", file=sys.stderr)
    getch()
    exit()


def limpar_term() -> None:
    os.system(CLEAR)


def click_para_continuar() -> None:
    print("\n Pressione para continuar...")
    getch()