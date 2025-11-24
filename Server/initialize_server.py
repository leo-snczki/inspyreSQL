from connect_db import start_connection

def start_check_use_db():
    db = start_connection()
    cursor = db.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS hospytal_db")
    cursor.execute("USE hospytal_db")

    cursor.execute("CREATE TABLE IF NOT EXISTS secretaria (id INT AUTO_INCREMENT PRIMARY KEY ,nif CHAR(9) UNIQUE, nome VARCHAR(255) NOT NULL, idade INT NOT NULL, email VARCHAR(255) UNIQUE NOT NULL, senha VARCHAR(255) NOT NULL, lugar_trabalho VARCHAR(100) NOT NULL, salario DECIMAL(10,2) NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS consulta (id INT AUTO_INCREMENT PRIMARY KEY, paciente_id CHAR(9) NOT NULL, medico_id CHAR(9) NOT NULL, data DATE NOT NULL, hora TIME NOT NULL, motivo VARCHAR(255), cancelado BOOLEAN DEFAULT FALSE, atendido BOOLEAN DEFAULT FALSE, FOREIGN KEY (paciente_id) REFERENCES paciente(nif) ON DELETE CASCADE, FOREIGN KEY (medico_id) REFERENCES medico(nif) ON DELETE CASCADE, UNIQUE (medico_id, data, hora))")

    db.commit()
    cursor.close()
    db.close()
