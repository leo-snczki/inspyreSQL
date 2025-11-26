import mysql.connector


def autenticar(cursor, nif, senha, tipo):
    if tipo == "medico":
        cursor.execute("SELECT * FROM medico WHERE nif=%s AND senha=%s", (nif, senha))
    elif tipo == "paciente":
        cursor.execute("SELECT * FROM paciente WHERE nif=%s AND senha=%s", (nif, senha))
    elif tipo == "secretario":
        cursor.execute(
            "SELECT * FROM secretaria WHERE nif=%s AND senha=%s", (nif, senha)
        )
    else:
        return "LOGIN_FALHADO"
    return cursor.fetchone()


def registar_utilizador(db, cursor, dados, tipo):
    try:
        if tipo == "medico":
            cursor.execute(
                "INSERT INTO medico (nif, nome, idade, email, senha, especialidade, salario) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (
                    dados["nif"],
                    dados["nome"],
                    dados["idade"],
                    dados["email"],
                    dados["senha"],
                    dados["especialidade"],
                    dados["salario"],
                ),
            )
        elif tipo == "paciente":
            cursor.execute(
                "INSERT INTO paciente (nif, nome, idade, email, senha, utente) VALUES (%s,%s,%s,%s,%s,%s)",
                (
                    dados["nif"],
                    dados["nome"],
                    dados["idade"],
                    dados["email"],
                    dados["senha"],
                    dados["utente"],
                ),
            )
        elif tipo == "secretario":
            cursor.execute(
                "INSERT INTO secretaria (nif, nome, idade, email, senha, lugar_trabalho, salario) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (
                    dados["nif"],
                    dados["nome"],
                    dados["idade"],
                    dados["email"],
                    dados["senha"],
                    dados["lugar_trabalho"],
                    dados["salario"],
                ),
            )
        else:
            return "TIPO_INVALIDO"

        db.commit()
        return "REGISTO_OK"

    except mysql.connector.Error as e:
        return f"ERRO: {e}"


def marcar_consulta(db, cursor, paciente_nif, medico_nif, data, hora, motivo):
    cursor.execute(
        "SELECT * FROM consulta WHERE medico_id=%s AND data=%s AND hora=%s",
        (medico_nif, data, hora),
    )

    if cursor.fetchone():
        return "HORARIO_OCUPADO"

    cursor.execute(
        "INSERT INTO consulta (paciente_id, medico_id, data, hora, motivo, cancelado, atendido) VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (paciente_nif, medico_nif, data, hora, motivo, False, False) # n sei pq o default do campo atendido e cancelado nao funciona
    )


    db.commit()
    return "CONSULTA_MARCADA"

def listar_consultas_medico(db, cursor, medico_nif):
    cursor.execute("""
        SELECT c.id, c.data, c.hora, c.motivo, c.cancelado, c.atendido,
               p.nome AS paciente_nome, m.nome AS medico_nome
        FROM consulta c
        JOIN paciente p ON c.paciente_id = p.nif
        JOIN medico m ON c.medico_id = m.nif
        WHERE m.nif = %s
        ORDER BY c.data, c.hora
    """, (medico_nif,))
    return cursor.fetchall()

def listar_consultas_paciente(db, cursor, paciente_nif):
    cursor.execute("""
        SELECT c.id, c.data, c.hora, c.motivo, c.cancelado, c.atendido,
               p.nome AS paciente_nome, m.nome AS medico_nome
        FROM consulta c
        JOIN paciente p ON c.paciente_id = p.nif
        JOIN medico m ON c.medico_id = m.nif
        WHERE p.nif = %s
        ORDER BY c.data, c.hora
    """, (paciente_nif,))
    return cursor.fetchall()


def cancelar_consulta_medico(db, cursor, consulta_id, medico_nif):
    cursor.execute("SELECT medico_id, cancelado FROM consulta WHERE id=%s", (consulta_id,))
    consulta = cursor.fetchone()

    if not consulta:
        return "CONSULTA_NAO_ENCONTRADA"

    if consulta['cancelado']:
        return "CONSULTA_JA_CANCELADA"

    if consulta['medico_id'] != medico_nif:
        return "ACESSO_NEGADO"

    cursor.execute("UPDATE consulta SET cancelado=TRUE WHERE id=%s", (consulta_id,))
    db.commit()
    return "CONSULTA_CANCELADA"


def cancelar_consulta_paciente(db, cursor, consulta_id, paciente_nif):
    cursor.execute("SELECT paciente_id, cancelado FROM consulta WHERE id=%s", (consulta_id,))
    consulta = cursor.fetchone()

    if not consulta:
        return "CONSULTA_NAO_ENCONTRADA"

    if consulta['cancelado']:
        return "CONSULTA_JA_CANCELADA"

    if consulta['paciente_id'] != paciente_nif:
        return "ACESSO_NEGADO"

    cursor.execute("UPDATE consulta SET cancelado=TRUE WHERE id=%s", (consulta_id,))
    db.commit()
    return "CONSULTA_CANCELADA"


def atualizar_consulta_medico(db, cursor, consulta_id, medico_nif, nova_data, nova_hora):
    cursor.execute("SELECT medico_id, cancelado FROM consulta WHERE id=%s", (consulta_id,))
    consulta = cursor.fetchone()

    if not consulta:
        return "CONSULTA_NAO_ENCONTRADA"

    if consulta['cancelado']:
        return "CONSULTA_CANCELADA"

    if consulta['medico_id'] != medico_nif:
        return "ACESSO_NEGADO"

    # Verifica conflito de horário
    cursor.execute(
        "SELECT * FROM consulta WHERE medico_id=%s AND data=%s AND hora=%s AND id!=%s",
        (medico_nif, nova_data, nova_hora, consulta_id),
    )

    if cursor.fetchone():
        return "HORARIO_OCUPADO"

    cursor.execute(
        "UPDATE consulta SET data=%s, hora=%s WHERE id=%s",
        (nova_data, nova_hora, consulta_id),
    )
    db.commit()
    return "ATUALIZACAO_OK"


def atualizar_consulta_paciente(db, cursor, consulta_id, paciente_nif, nova_data, nova_hora):
    cursor.execute("SELECT paciente_id, cancelado FROM consulta WHERE id=%s", (consulta_id,))
    consulta = cursor.fetchone()

    if not consulta:
        return "CONSULTA_NAO_ENCONTRADA"

    if consulta['cancelado']:
        return "CONSULTA_CANCELADA"

    if consulta['paciente_id'] != paciente_nif:
        return "ACESSO_NEGADO"

    # Verifica conflito de horário com o médico da consulta
    cursor.execute("SELECT medico_id FROM consulta WHERE id=%s", (consulta_id,))
    medico_id = cursor.fetchone()['medico_id']

    cursor.execute(
        "SELECT * FROM consulta WHERE medico_id=%s AND data=%s AND hora=%s AND id!=%s",
        (medico_id, nova_data, nova_hora, consulta_id),
    )
    if cursor.fetchone():
        return "HORARIO_OCUPADO"

    cursor.execute(
        "UPDATE consulta SET data=%s, hora=%s WHERE id=%s",
        (nova_data, nova_hora, consulta_id),
    )
    db.commit()
    return "ATUALIZACAO_OK"



def atender_consulta(db, cursor, consulta_id, medico_nif):
    # Verifica se a consulta existe e pertence ao médico
    cursor.execute(
        "SELECT cancelado, atendido, medico_id FROM consulta WHERE id=%s",
        (consulta_id,),
    )
    consulta = cursor.fetchone()

    if not consulta:
        return "CONSULTA_NAO_ENCONTRADA"

    if consulta["cancelado"]:
        return "CONSULTA_CANCELADA"

    if consulta["medico_id"] != medico_nif:
        return "ACESSO_NEGADO"

    if consulta["atendido"]:
        return "CONSULTA_JA_ATENDIDA"

    cursor.execute("UPDATE consulta SET atendido=TRUE WHERE id=%s", (consulta_id,))
    db.commit()
    return "CONSULTA_ATENDIDA"
