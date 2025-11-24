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

def menu_paciente():
    lista_itens = (
        "Marcar consulta",
        "Ver consulta",
        "Cancelar consulta",
        "Atualizar consulta",
        "Deslogar",
    )
    return lista_itens


def menu_secretario():
    lista_itens = ("Registar Cliente", "Marcar Consulta para cliente", "Deslogar")
    return lista_itens


def menu_medico():
    lista_itens = (
        "Ver consulta",
        "Cancelar consulta",
        "Atualizar consulta",
        "Atender consulta",
        "Deslogar",
    )
    return lista_itens

