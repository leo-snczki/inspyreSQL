def mostrar_menu(menu):
    for i in range(len(menu) - 1):
        print(f"{i + 1} - {menu[i]}")
    print(f"0 - {menu[-1]}")


def menu_principal():
    lista_itens = ("Logar", "registar", "Sair")
    return lista_itens


def menu_tipos():
    lista_itens = ("Médico(a)", "Paciente", "Secretário(a)", "voltar")
    return lista_itens
