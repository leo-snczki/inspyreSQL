class ValidadorInputs:

    @classmethod
    def solicitar_nif(cls):
        while True:
            nif = input("Digite o NIF (apenas números, 9 dígitos): ")
            if nif.isdigit() and len(nif) == 9:
                return nif
            print("NIF inválido.")

    @classmethod
    def solicitar_senha(cls):
        while True:
            senha = input("Digite a senha (mínimo 6 caracteres): ")
            if len(senha) >= 6:
                return senha
            print("Senha inválida.")

    @classmethod
    def solicitar_nome(cls):
        while True:
            nome = input("Digite o nome: ")
            if nome.strip():
                return nome
            print("Nome inválido.")

    @classmethod
    def solicitar_idade(cls):
        while True:
            try:
                idade = int(input("Digite a idade: "))
                if idade > 0:
                    return idade
                print("Idade deve ser positiva.")
            except ValueError:
                print("Digite um número válido para idade.")

    @classmethod
    def solicitar_email(cls):
        while True:
            email = input("Digite o email: ")
            if "@" in email and "." in email:
                return email
            print("Email inválido.")

    @classmethod
    def solicitar_utente(cls):
        while True:
            utente = input("Digite o número de utente: ")
            if utente.strip().isdigit():
                return utente
            print("Número de utente inválido.")

    @classmethod
    def solicitar_especialidade(cls):
        while True:
            esp = input("Digite a especialidade: ")
            if esp.strip():
                return esp
            print("Especialidade inválida.")

    @classmethod
    def solicitar_salario(cls):
        while True:
            try:
                salario = float(input("Digite o salário: "))
                if salario > 0:
                    return salario
                print("Salário deve ser positivo.")
            except ValueError:
                print("Digite um valor numérico válido.")

    @classmethod
    def solicitar_lugar_trabalho(cls):
        while True:
            lugar = input("Digite o lugar de trabalho: ")
            if lugar.strip():
                return lugar
            print("Lugar inválido.")

    @classmethod
    def solicitar_basicos(cls):
        return {
            "nif": cls.solicitar_nif(),
            "senha": cls.solicitar_senha(),
            "nome": cls.solicitar_nome(),
            "idade": cls.solicitar_idade(),
            "email": cls.solicitar_email()
        }

    @classmethod
    def preencher_paciente(cls):
        dados = cls.solicitar_basicos()
        dados["utente"] = cls.solicitar_utente()
        return dados

    @classmethod
    def preencher_medico(cls):
        dados = cls.solicitar_basicos()
        dados["especialidade"] = cls.solicitar_especialidade()
        dados["salario"] = cls.solicitar_salario()
        return dados

    @classmethod
    def preencher_secretario(cls):
        dados = cls.solicitar_basicos()
        dados["lugar_trabalho"] = cls.solicitar_lugar_trabalho()
        dados["salario"] = cls.solicitar_salario()
        return dados
