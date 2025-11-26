import socket
import pickle
import threading

from initialize_server import start_check_use_db
from connect_db import start_connection_db
from handlers import (
    autenticar,
    registar_utilizador,
    marcar_consulta,
    cancelar_consulta_medico,
    cancelar_consulta_paciente,
    atualizar_consulta_medico,
    atualizar_consulta_paciente,
    atender_consulta,
    listar_consultas_medico,
    listar_consultas_paciente
)


def handle_client(conn, addr):
    print(f"Conexão de {addr}")

    db = start_connection_db()
    cursor = db.cursor(dictionary=True)

    try:
        while True:
            data = conn.recv(4096)

            if not data:
                break

            request = pickle.loads(data)
            objetivo = request.get("objetivo")

            match objetivo:
                case "login":
                    resposta = autenticar(
                        db, cursor, request["nif"], request["senha"], request["tipo"]
                    )

                case "registar":
                    resposta = registar_utilizador(
                        db, cursor, request["dados"], request["tipo"]
                    )

                case "marcar_consulta":
                    resposta = marcar_consulta(
                        db,
                        cursor,
                        request["paciente_nif"],
                        request["medico_nif"],
                        request["data"],
                        request["hora"],
                        request["motivo"],
                    )

                case "listar_consultas_medico":
                    resposta = listar_consultas_medico(db, cursor, request["medico_nif"])

                case "atualizar_consulta_medico":
                    resposta = atualizar_consulta_medico(
                        db, cursor,
                        request['consulta_id'],
                        request['medico_nif'],
                        request['nova_data'],
                        request['nova_hora']
                    )

                case "atualizar_consulta_paciente":
                    resposta = atualizar_consulta_paciente(
                        db, cursor,
                        request['consulta_id'],
                        request['paciente_nif'],
                        request['nova_data'],
                        request['nova_hora']
                    )

                case "cancelar_consulta_medico":
                    resposta = cancelar_consulta_medico(
                        db, cursor, request['consulta_id'], request['medico_nif']
                    )

                case "cancelar_consulta_paciente":
                    resposta = cancelar_consulta_paciente(
                        db, cursor, request['consulta_id'], request['paciente_nif']
                    )

                case "atender_consulta":
                    resposta = atender_consulta(
                        db, cursor, request["consulta_id"], request["medico_nif"]
                    )

                case "listar_consultas_paciente":
                    resposta = listar_consultas_paciente(db, cursor, request["paciente_nif"])

                case _:
                    resposta = "ACAO_INVALIDA"

            conn.send(pickle.dumps(resposta))

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        cursor.close()
        db.close()
        conn.close()
        print(f"Conexão encerrada: {addr}")


def main():
    start_check_use_db()
    host = "10.237.107.59"  # endereco zerotier
    port = 5000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print(f"Servidor rodando em {host}:{port}")

    while True:
        conn, addr = server.accept()

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        print(f"Threads ativas: {threading.active_count() - 1}")


if __name__ == "__main__":
    main()
