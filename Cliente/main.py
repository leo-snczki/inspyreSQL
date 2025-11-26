import socket
import pickle
from readkeys import getch
from datetime import datetime, timedelta, time
import terminal
from valid import ValidadorInputs
from menu import (
    menu_medico,
    menu_paciente,
    menu_principal,
    menu_secretario,
    menu_tipos,
    mostrar_menu,
)

HOST = "10.237.107.59"
PORT = 5000


def enviar_request(request, timeout=10):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(timeout)
    try:
        client.connect((HOST, PORT))
        client.send(pickle.dumps(request))
        response = pickle.loads(client.recv(4096))
    except Exception as e:
        print(f"Erro de conexão: {e}")
        response = None
    finally:
        client.close()
    return response


def login():
    terminal.limpar_term()
    print("LOGIN")
    mostrar_menu(menu_tipos())
    numero_tipo = input("qual o tipo de utilizador: ")
    terminal.limpar_term()
    match numero_tipo:
        case "1":
            tipo = "medico"
        case "2":
            tipo = "paciente"
        case "3":
            tipo = "secretario"
        case "0":
            main()
        # não deve ser possivel chegar no case _

    nif = input("Digite o NIF: ")
    senha = input("Digite a senha: ")

    request = {"objetivo": "login", "tipo": tipo, "nif": nif, "senha": senha}
    resposta = enviar_request(request)

    if resposta is "LOGIN_FALHADO":
        print("\nNIF e/ou senha incorretos. Tente novamente.")
        terminal.click_para_continuar()
        login()

    else:
        print(f"\nLogin efetuado com sucesso! Bem-vindo(a) {resposta['nome']}")
        terminal.click_para_continuar()
        return {"tipo": tipo, "dados": resposta}


def registar(tipo):
    terminal.limpar_term()
    print(f" REGISTO DE {tipo.upper()} ")

    if tipo == "paciente":
        dados = ValidadorInputs.preencher_paciente()
    elif tipo == "medico":
        dados = ValidadorInputs.preencher_medico()
    elif tipo == "secretario":
        dados = ValidadorInputs.preencher_secretario()
    else:
        print("Tipo inválido.")
        getch()
        return

    request = {"objetivo": "registar", "tipo": tipo, "dados": dados}

    resposta = enviar_request(request)
    if resposta == "TIPO_INVALIDO":
        print("Tipo de utilizador inválido.")
        getch()
        login()
        return

    print(resposta)
    getch()



def pegar_data_obj():
    while True:
        data = input("\nData (YYYY-MM-DD): ")
        try:
            return datetime.strptime(data, "%Y-%m-%d").date()
        except ValueError:
            print("[ERRO]: Use formato YYYY-MM-DD e uma data real.\n")


def pegar_hora_obj():
    while True:
        hora = input("\nHora (HH:MM:SS): ")
        try:
            return datetime.strptime(hora, "%H:%M:%S").time()
        except ValueError:
            print("[ERRO]: Use formato HH:MM:SS e um horário real.\n")


def marcar_consulta(paciente_nif):
    terminal.limpar_term()
    print("MARCAR CONSULTA")

    while True:
        medico_nif = input("Digite o NIF do médico: ")
        if medico_nif.isdigit():
            break
        print("[ERRO]: NIF inválido. Digite apenas números.\n")

    while True:
        try:
            data_obj = pegar_data_obj()
            hora_obj = pegar_hora_obj()
            data_hora = datetime.combine(data_obj, hora_obj)
            validar_datahora(data_hora)
            break
        except Exception as e:
            print(f"[ERRO]: {e}\nTente novamente.\n")

    motivo = input("Motivo da consulta: ")

    request = {
        "objetivo": "marcar_consulta",
        "paciente_nif": paciente_nif,
        "medico_nif": medico_nif,
        "data": data_hora.strftime("%Y-%m-%d"),
        "hora": data_hora.strftime("%H:%M:%S"),
        "motivo": motivo,
    }

    resposta = enviar_request(request)
    print(resposta)
    getch()


def listar_consultas_medico(medico_nif):
    terminal.limpar_term()
    print("CONSULTAS DO MÉDICO")
    request = {"objetivo": "listar_consultas_medico", "medico_nif": medico_nif}
    consultas = enviar_request(request)

    if not consultas:
        print("Nenhuma consulta encontrada.")
    else:
        for c in consultas:
            status = []
            if c['cancelado']:
                status.append("CANCELADA")
            if c['atendido']:
                status.append("ATENDIDA")
            status_str = " | ".join(status) if status else "PENDENTE"

            print(
                f"ID: {c['id']}, Data: {c['data']}, Hora: {c['hora']}, "
                f"Paciente: {c['paciente_nome']}, Motivo: {c['motivo']}, Status: {status_str}"
            )
    terminal.click_para_continuar()


def listar_consultas_paciente(paciente_nif):
    terminal.limpar_term()
    print("MINHAS CONSULTAS")
    request = {"objetivo": "listar_consultas_paciente",
               "paciente_nif": paciente_nif}
    consultas = enviar_request(request)

    if not consultas:
        print("Nenhuma consulta encontrada.")
    else:
        for c in consultas:
            status = []
            if c['cancelado']:
                status.append("CANCELADA")
            if c['atendido']:
                status.append("ATENDIDA")
            status_str = " | ".join(status) if status else "PENDENTE"

            print(
                f"ID: {c['id']}, Data: {c['data']}, Hora: {c['hora']}, "
                f"Médico: {c['medico_nome']}, Motivo: {c['motivo']}, Status: {status_str}"
            )
    terminal.click_para_continuar()


def cancelar_consulta_medico(medico_nif):
    terminal.limpar_term()
    print("CANCELAR CONSULTA (MÉDICO)")
    listar_consultas_medico(medico_nif)
    consulta_id = input("Digite o ID da consulta: ")
    if not consulta_id.isdigit():
        print("ID inválido")
        terminal.click_para_continuar()
        return
    consulta_id = int(consulta_id)

    request = {"objetivo": "cancelar_consulta_medico",
               "consulta_id": consulta_id, "medico_nif": medico_nif}
    resposta = enviar_request(request)
    print(resposta)
    terminal.click_para_continuar()


def cancelar_consulta_paciente(paciente_nif):
    terminal.limpar_term()
    print("CANCELAR CONSULTA (PACIENTE)")
    listar_consultas_paciente(paciente_nif)
    consulta_id = input("Digite o ID da consulta: ")
    if not consulta_id.isdigit():
        print("ID inválido")
        terminal.click_para_continuar()
        return
    consulta_id = int(consulta_id)

    request = {"objetivo": "cancelar_consulta_paciente",
               "consulta_id": consulta_id, "paciente_nif": paciente_nif}
    resposta = enviar_request(request)
    print(resposta)
    terminal.click_para_continuar()


def atender_consulta(medico_nif):
    terminal.limpar_term()
    print("ATENDER CONSULTA")
    try:
        listar_consultas_medico(medico_nif)

        consulta_id = input("Digite o ID da consulta a atender: ")
        if not consulta_id.isdigit():
            print("ID inválido.")
            terminal.click_para_continuar()
            return

        request = {
            "objetivo": "atender_consulta",
            "consulta_id": int(consulta_id),
            "medico_nif": medico_nif
        }

    except Exception as e:
        print(f"ERRO: {e}")

    resposta = enviar_request(request)
    print(resposta)
    terminal.click_para_continuar()


def validar_datahora(
    datahora: datetime,
):  # isso não verifica se a data e ou hora já está ocupada
    # só verifica se a data e hora estão dentro dos limites
    # devia ser do lado do servidor mas pronto
    # este projeto é so para usar os sockets
    agora = datetime.now()

    if datahora <= agora:
        raise ValueError("Não é possível agendar no passado.")
    if datahora < agora + timedelta(hours=24):
        raise ValueError("A consulta deve ter pelo menos 24h de antecedência.")
    if datahora > agora + timedelta(days=180):
        raise ValueError("A data ultrapassa o limite de 6 meses.")
    if datahora.weekday() >= 5:
        raise ValueError("Não é permitido agendar no fim de semana.")
    if not (time(8, 0) <= datahora.time() <= time(18, 0)):
        raise ValueError("Horário permitido é entre 08:00 e 18:00.")
    if time(12, 0) <= datahora.time() < time(13, 0):
        raise ValueError("Horário de almoço é proibido: 12:00 a 13:00.")


def atualizar_consulta_medico(medico_nif):
    terminal.limpar_term()
    print("ATUALIZAR CONSULTA (MÉDICO)")
    listar_consultas_medico(medico_nif)
    consulta_id = input("Digite o ID da consulta: ")
    if not consulta_id.isdigit():
        print("ID inválido")
        terminal.click_para_continuar()
        return
    consulta_id = int(consulta_id)

    data = pegar_data_obj()
    hora = pegar_hora_obj()
    nova_datahora = datetime.combine(data, hora)
    validar_datahora(nova_datahora)

    request = {
        "objetivo": "atualizar_consulta_medico",
        "consulta_id": consulta_id,
        "medico_nif": medico_nif,
        "nova_data": nova_datahora.strftime("%Y-%m-%d"),
        "nova_hora": nova_datahora.strftime("%H:%M:%S"),
    }
    resposta = enviar_request(request)
    print(resposta)
    terminal.click_para_continuar()


def atualizar_consulta_paciente(paciente_nif):
    terminal.limpar_term()
    print("ATUALIZAR CONSULTA (PACIENTE)")
    listar_consultas_paciente(paciente_nif)
    consulta_id = input("Digite o ID da consulta: ")
    if not consulta_id.isdigit():
        print("ID inválido")
        terminal.click_para_continuar()
        return
    consulta_id = int(consulta_id)

    data = pegar_data_obj()
    hora = pegar_hora_obj()
    nova_datahora = datetime.combine(data, hora)
    validar_datahora(nova_datahora)

    request = {
        "objetivo": "atualizar_consulta_paciente",
        "consulta_id": consulta_id,
        "paciente_nif": paciente_nif,
        "nova_data": nova_datahora.strftime("%Y-%m-%d"),
        "nova_hora": nova_datahora.strftime("%H:%M:%S"),
    }
    resposta = enviar_request(request)
    print(resposta)
    terminal.click_para_continuar()


def menu_pos_login(utilizador):
    while True:
        terminal.limpar_term()
        if utilizador["tipo"] == "paciente":
            mostrar_menu(menu_paciente())
            op = input("Escolha a opção: ")
            match op:
                case "1":
                    marcar_consulta(utilizador["dados"]["nif"])
                case "2":
                    listar_consultas_paciente(utilizador["dados"]["nif"])
                    terminal.click_para_continuar()
                case "3":
                    cancelar_consulta_paciente(utilizador["dados"]["nif"])
                case "4":
                    atualizar_consulta_paciente(utilizador["dados"]["nif"])
                case "0":
                    break
                case _:
                    print("\nOpção inválida")
                    terminal.click_para_continuar()

        elif utilizador["tipo"] == "secretario":
            mostrar_menu(menu_secretario())
            op = input("Escolha a opção: ")
            match op:
                case "1":
                    registar("paciente")
                case "2":
                    nif_paciente = input("insira o nif do paciente: ")
                    marcar_consulta(nif_paciente)
                    # hum
                case "0":
                    break
                case _:
                    print("\nOpção inválida")
                    terminal.click_para_continuar()

        elif utilizador["tipo"] == "medico":
            mostrar_menu(menu_medico())
            op = input("Escolha a opção: ")
            match op:
                case "1":
                    listar_consultas_medico(utilizador["dados"]["nif"])
                case "2":
                    cancelar_consulta_medico(utilizador["dados"]["nif"])
                case "3":
                    atualizar_consulta_medico(utilizador["dados"]["nif"])
                case "4":
                    atender_consulta(utilizador["dados"]["nif"])
                    pass
                case "0":
                    break
                case _:
                    print("\nOpção inválida")
                    terminal.click_para_continuar()
        else:
            print("tipo de utilizador não existe")
            terminal.click_para_continuar()
            terminal.limpar_term()


def main():
    while True:
        terminal.limpar_term()
        mostrar_menu(menu_principal())
        op = input("Escolha a opção: ")
        match op:
            case "1":
                utilizador = login()
                if utilizador:
                    menu_pos_login(utilizador)
            case "2":
                terminal.limpar_term()
                mostrar_menu(menu_tipos())
                tipo = input("Escolha o tipo para registo: ")
                match tipo:
                    case "1":
                        registar("medico")
                    case "2":
                        registar("paciente")
                    case "3":
                        registar("secretario")
                    case "0":
                        main()
                    case _:
                        print("esta opção não existe.")

            case "0":
                terminal.limpar_term()
                if input("Tem a certeza? ('s' para sair): ").lower() == "s":
                    exit()
            case _:
                print("Opção inválida")
                getch()


if __name__ == "__main__":
    main()
