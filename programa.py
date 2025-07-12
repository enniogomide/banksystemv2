"""
    __author__ = "Ennio Gomide"
    __version__ = "2.0.0"
    -*- coding: utf-8 -*-

    Programa de controle bancário criado segundo os requisitos expressos no desafio, utlizando utilizando POO.

    Construido segundo os requisistos apresentados: desafio
      foi utilizada a funcionaliade implementada no desafio anterior, que utilizava funçoes.
      Além do uso ao app anterior (funções), foi implementado o uso de classes conforme apresentado na resolução do deafio_v2, fazendo os ajustes necessários para manter a funcionalidade do app anterior.
      As classes foram implementadas como apresentadas.
      as classes referentes a Conta corrente, transação, histório e movimentação foram aproveitadas e realizados pequenos ajustes.
      
    Mantindas as funcionalidade atuais: depositar, sacar, extrato, cadastrar usuário, conta, além do processo de carga de dados iniciais como implementado anteriormente.

    Além das funcionalidades que já existiam, foi adicionado o proceso de seleção de cliente e conta, não requerendo que em cada funcionalidade tivesse que ser informado o cliente e/ou conta.
    
    Foi criada a classe pessoa, onde ficam guardados todos os clientes.

"""
import os
from datetime import datetime
from abc import ABC, abstractmethod


class InformarValores():
    # informar CPF
    def informar_cpf():
        cpf_valido = False
        cpf = ""
        while not cpf_valido:
            cpf = input("Informe o CPF do cliente (somente números): ").strip()
            # Validar CPF
            if not cpf.isdigit() or len(cpf) != 11:
                print("CPF inválido. Deve conter apenas números e ter 11 dígitos.")
                input()
                continue
            # Verificar se o CPF já está cadastrado
            else:
                cpf_valido = True
        return cpf

    # informar numero da conta
    def informar_numero_conta():
        numero_valido = False
        while not numero_valido:
            numero = input("Informe numero da conta(somente números): ").strip()
            # Validar numero
            if not numero.isdigit() or len(numero) != 6:
                print("Conta inválida. Deve conter apenas números "
                      "e ter 6 dígitos.")
                input()
                continue
            else:
                numero_valido = True
        return numero

    # informar o nome do cliente
    def informar_nome():
        nome_valido = False
        nome = ""
        while not nome_valido:
            nome = input("Informe o nome do cliente: ").strip()
            if not nome and len(nome) <= 20:
                print("Nome inválido."
                    "O nome não pode ser vazio. Deve ter mais de 20 caracteres.")
                input()
                continue
            nome_valido = True
        return nome

    # informar a data de nascimento do cliente
    def informar_data_nascimento():
        data_nascimento = ""
        data_valida = False
        while not data_valida:
            data_nascimento = input("Informe a data de nascimento "
                                    "(dd/mm/aaaa): ").strip()
            # Validar formato da data
            if (not data_nascimento) or \
               (len(data_nascimento) != 10) or \
               (data_nascimento[2] != '/') or \
               (data_nascimento[5] != '/'):
                input("Data inválida. Use o formato dd/mm/aaaa.")
                continue
            # Verificar se a data é válida (básico, sem validação de dias)
            try:
                dia, mes, ano = map(int, data_nascimento.split('/'))
                if (dia < 1 or dia > 31) or \
                   (mes < 1 or mes > 12) or \
                   (ano < 1900 or ano > 2025):
                    raise ValueError
                data_valida = True
            except ValueError:
                input("Data inválida. Verifique os valores informados.")
                continue
        return data_nascimento

    # informar o endereco do cliente
    def informar_endereco():
        endereco_valido = False
        endereco = ""
        while not endereco_valido:
            endereco = input("Informe o endereço do cliente (logradouro, "
                            "número - bairro - cidade/estado - cep): ").strip()
            if not endereco or len(endereco) < 20:
                input("Endereço inválido. Verifique o formato informado.")
                continue
            # Verificar se o endereço contém os componentes necessários
            if ("," not in endereco) or \
               ("-" not in endereco) or \
               ("/" not in endereco) or \
               (" " not in endereco):
                input("Endereço inválido. Verifique o formato informado.")
                continue
            endereco_valido = True
        return endereco

    # informar valor para saque ou depósito
    def informar_valor():
        valor_valido = False
        while not valor_valido:
            valor = input("Informe o valor: ")
            try:
                valor = float(valor)
            except ValueError:
                print("Valor inválido. Por favor, informe um valor numérico.")
                input("pressione <enter> para continuar...")
                continue

            if valor <= 0:
                print("Valor tem que ser maior que zero")
                input("pressione <enter> para continuar...")
            else:
                valor_valido = True
        return valor

    # informar quantidade de saques diários 
    # (não controlado no app para mais de um dia)
    def informar_limite_saque_diario():
        limite_saque_valido = False
        while not limite_saque_valido:
            limite_saque_diario = input("Informe Quantidade de saques diário: ")
            try:
                limite_saque_diario = int(limite_saque_diario)
            except ValueError:
                print("Valor inválido. Por favor, informe um valor numérico.")
                input("pressione <enter> para continuar...")
            if 0 > limite_saque_diario > 10:
                print("Limite de saques inválido. Entre 1 e 10")
                input("pressione <enter> para continuar...")
            else:
                limite_saque_valido = True
        return limite_saque_diario

# informar valor referente ao limite para saque
    def informar_valor_limite_saque():
        valor_limite_valido = False
        while not valor_limite_valido:
            valor_limite_saque = input("Informe o valor limite para Saque: ")
            try:
                valor_limite_saque = float(valor_limite_saque)
            except ValueError:
                print("Valor inválido. Por favor, informe um valor.")
                input("pressione <enter> para continuar...")
            if valor_limite_saque <= 0:
                print("Valor limite para saque invalido.")
                input("pressione <enter> para continuar...")
            else:
                valor_limite_valido = True
        return valor_limite_saque

    # informar valor de saldo inicial para depósito na abertura da conta
    def informar_saldo_inicial():
        saldo_inicial_valido = False
        while not saldo_inicial_valido:
            saldo_inicial = input("Informe deposito inicial: ")
            try:
                saldo_inicial = float(saldo_inicial)
            except ValueError:
                print("Valor inválido. Por favor, informe um valor.")
                input("pressione <enter> para continuar...")
            if saldo_inicial <= 0:
                print("Depósito inical tem que ser maior que zero.")
                input("pressione <enter> para continuar...")
            else:
                saldo_inicial_valido = True
        return saldo_inicial


# ************************************************************
# **** Conta de cliente                                   ****
# ************************************************************
# guarda todos os clientes cadastrados
class Pessoa:
    def __init__(self):
        self._ultima_conta = 0
        self._clientes = {}

    @property
    def clientes(self):
        return self._clientes

    def obter_ultima_conta(self):
        return self._ultima_conta

    def atualizar_ultima_conta(self, numero):
        if numero > self._ultima_conta:
            self._ultima_conta = numero

    def adicionar_cliente(self, chave, cliente):
        novo_cliente = PessoaFisica(
           nome=cliente["nome"],
           cpf=cliente["cpf"],
           endereco=cliente["endereco"],
           data_nascimento=cliente["data_nascimento"],
        )
        self._clientes.update({chave: novo_cliente})
        return self._clientes

    def obter_cliente(self, cpf):
        cliente = self._clientes.get(cpf)
        if not cliente:
            print(f"Cliente com CPF {cpf} não encontrado.")
            input()
            return None
        return cliente

    def atualizar_cliente(self, chave, cliente):
        self._clientes.update({chave: cliente})

    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{chave}={valor}'
                                                        for chave, valor in
                                                        self.__dict__.items()
                                                        ])}"


# dados do cliente
class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = {}

    @property
    def endereco(self):
        return self._endereco

    @property
    def contas(self):
        return self._contas

    def realizar_transacao(self, conta, transacao):
        resultado = transacao.registrar(conta)
        return resultado

    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{chave}={valor}'
                                                        for chave, valor in
                                                        self.__dict__.items()
                                                        ])}"


# ************************************************************
# **** Conta de cliente - Pessoa Física                   ****
# ************************************************************
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self._nome = nome
        self._data_nascimento = data_nascimento
        self._cpf = cpf

    @property
    def nome(self):
        return self._nome

    @property
    def data_nascimento(self):
        return self._data_nascimento

    @property
    def cpf(self):
        return self._cpf

    def obter_conta(self, numero):
        conta = self._contas.get(numero)
        if not conta:
            return None
        return conta

    def atualizar_contas_cliente(self, numero, conta, cliente):
        self._contas.update({numero: conta})
        return cliente

    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{chave}={valor}'
                                                        for chave, valor in
                                                        self.__dict__.items()
                                                        ])}"


# ************************************************************
# **** Contas de clientes                                 ****
# ************************************************************
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True

    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{chave}={valor}'
                                                        for chave, valor in
                                                        self.__dict__.items()
                                                        ])}"


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    @property
    def limite(self):
        return self._limite

    @property
    def limite_saques(self):
        return self._limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes
             if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            resultado = super().sacar(valor)
            return resultado

        return False

    @classmethod
    def adicionar_conta(cls, chave_conta, conta_corrente, cliente):
        nova_conta = ContaCorrente(
            numero=chave_conta[2],
            cliente=cliente,
            limite=conta_corrente["valor_limite_saque"],
            limite_saques=conta_corrente["limite_saque_diario"],
        )

        # realizar o depósito inicial
        valor = conta_corrente["saldo"]
        transacao = Deposito(valor)
        cliente.realizar_transacao(nova_conta, transacao)

        cliente = cliente.atualizar_contas_cliente(
            nova_conta.numero,
            nova_conta,
            cliente
        )

        numero = int(chave_conta[2])

        return cliente, numero

    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{chave}={valor}'
                                                        for chave, valor in
                                                        self.__dict__.items()
                                                        ])}"


# ************************************************************
# **** Movimentações                                      ****
# ************************************************************
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,

            }
        )

    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{chave}={valor}'
                                                        for chave, valor in
                                                        self.__dict__.items()
                                                        ])}"


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

        return sucesso_transacao


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


# ************************************************************
# **** classe para carga inicial  dos dados de cliente    ****
# ************************************************************
class CarregarDadosClientes:
    @classmethod
    def fazer_carga_clientes(cls):
        lista_clientes = {
            "12345678901": {
                "nome": "Jose da Siva jr.",
                "cpf": "12345678901",
                "data_nascimento": "10/10/2020",
                "endereco": "rua cem, 123 - cidade/uf - 12345678"},
            "23456789012": {
                "nome": "Roberto Limita e Silva",
                "cpf": "23456789012",
                "data_nascimento": "12/12/2010",
                "endereco": "rua cem, 123 - cidade/uf - 12345678"}
            }
        clientes = Pessoa()
        for cpf in lista_clientes:
            clientes.adicionar_cliente(
                cpf,
                lista_clientes[cpf]
            )

        return clientes


# ************************************************************
# **** classe para carga inicial  dos dados de cliente    ****
# ************************************************************
class CarregarDadosConta:

    @classmethod
    def fazer_carga_conta(cls, cadastro_pessoas):
        lista_contas_correntes = {
            ('12345678901', '0001', '000001'): {
                'agencia': '0001',
                'numero_conta': '000001',
                'cliente': '12345678901',
                'saldo': 1000.0,
                'limite_saque_diario': 3,
                'valor_limite_saque': 200.0,
                'numero_saques_no_dia': 0
                },
            ('12345678901', '0001', '000002'): {
                'agencia': '0001',
                'numero_conta': '000002',
                'cliente': '12345678901',
                'saldo': 5000.0,
                'limite_saque_diario': 5,
                'valor_limite_saque': 600.0,
                'numero_saques_no_dia': 0
                },
            ('23456789012', '0001', '000003'): {
                'agencia': '0001',
                'numero_conta': '000003',
                'cliente': '12345678901',
                'saldo': 10000.0,
                'limite_saque_diario': 4,
                'valor_limite_saque': 1000.0,
                'numero_saques_no_dia': 0
                }
        }

        for chave_conta in lista_contas_correntes:
            cliente = cadastro_pessoas.obter_cliente(chave_conta[0])
            if cliente:
                conta_corrente = ContaCorrente(chave_conta[2], cliente)
                cliente, numero = conta_corrente.adicionar_conta(
                    chave_conta,
                    lista_contas_correntes[chave_conta],
                    cliente
                )

                cadastro_pessoas.atualizar_ultima_conta(numero)
                cadastro_pessoas.atualizar_cliente(
                    chave_conta[0],
                    cliente
                )

        return cadastro_pessoas


# **********************************************************************
# **** LIstagens referente a aos dados clientes, conta e movimentos ****
# **********************************************************************
class ListagemDeDados:
    @classmethod
    def listar_dados_dos_clientes(cls, cadastro_pessoas):
        clientes = cadastro_pessoas.clientes
        os.system("cls" if os.name == "nt" else "clear")
        for cpf, cliente in clientes.items():
            print("-" * 80)
            print(f"Cliente: {cpf} - Nome: {cliente.nome}")
            contas = cliente.contas
            for numero, conta in contas.items():
                print(f"\tConta: {numero} - Saldo: {conta.saldo:.2f}"
                      f" Valor limite para Saque: {conta.limite:.2f}  "
                      f" qtde Saques dia: {conta.limite_saques}")

                historico = conta.historico
                transacoes = historico.transacoes
                print("\t\tHistorico de transações:")
                for transacao in transacoes:
                    print(f"\t\t{transacao['data']}"
                          f" - {transacao['tipo']}\t"
                          f" - Valor: {transacao['valor']:8.2f}")

        print()

    @classmethod
    def listar_extrado_cliente(cls, cliente, conta):
        os.system("cls" if os.name == "nt" else "clear")
        print("-" * 80)
        print("Extrato da conta corrente")
        print("-" * 80)
        print(f"Cliente: {cliente.cpf} - Nome: {cliente.nome} \n"
              f"Conta: {conta.numero} Saldo: {conta.saldo:.2f} "
              f"Valor Saque: {conta.limite:.2f}  "
              f"qtde Saques dia: {conta.limite_saques}")

        historico = conta.historico
        transacoes = historico.transacoes
        print("\tHistorico de transações:")
        for transacao in transacoes:
            print(f"\t{transacao['data']}"
                  f" - {transacao['tipo']}\t"
                  f" - Valor: {transacao['valor']:8.2f}")

        print(f"\t\t\t\t\t   Saldo: {conta.saldo:8.2f} \n")
        print("-" * 80)

        print()


# ************************************************************
# **** Controle da aplicação e menu                       ****
# ************************************************************
class ExecutarFuncoesApp:

    # *** apresentação do MENU
    @classmethod
    def apresentar_menu(cls, cliente, conta):
        menu = """
[d] Depositar
[s] Sacar
[e] Extrato

[x] Selecionar Cliente e Conta
[u] Criar cliente
[c] Criar Conta Corrente
[l] Listar contas

[q] Sair

=>"""
        os.system("cls" if os.name == "nt" else "clear")
        if cliente and conta:
            print(f"Cliente: {cliente.nome} - CPF: {cliente.cpf} - "
                  f"Conta: {conta.numero} - Saldo: {conta.saldo:.2f}")
            print("-" * 80)
            print()
        print(menu)

    # ** Selecionar cliente a trabalhar
    @classmethod
    def selecionar_cliente(cls, cadastro_pessoas):

        cpf_valido = False
        while not cpf_valido:
            cpf = InformarValores.informar_cpf()
            cliente = cadastro_pessoas.obter_cliente(cpf)
            if cliente:
                cpf_valido = True
            else:
                print(f"Cliente {cliente.nome} não encontrado.")
                print("pressione <enter> para continuar...")
                input()

        return cliente

    # ** Selecionar conta a trabalhar
    @classmethod
    def selecionar_conta(cls, cliente):

        conta_valida = False
        while not conta_valida:
            numero = InformarValores.informar_numero_conta()
            conta = cliente.obter_conta(numero)
            if conta:
                conta_valida = True
            else:
                print(f"Conta {numero} não encontrada para "
                      f" o cliente {cliente.nome}.")
                print("pressione <enter> para continuar...")
                input()

        return conta

    # ** Cadastrar cliente
    @classmethod
    def incluir_cadastro_cliente(cls, cadastro_pessoas):
        cpf_valido = False
        while not cpf_valido:
            cpf = InformarValores.informar_cpf()
            clientes = cadastro_pessoas.clientes
            cliente = clientes.get(cpf, "")
            if cliente:
                print("@@@ Já existe cliente com esse CPF! @@@")
                input("pressione <enter> para continuar...")
            else:
                cpf_valido = True

        nome = InformarValores.informar_nome()
        data_nascimento = InformarValores.informar_data_nascimento()
        endereco = InformarValores.informar_endereco()

        cliente = PessoaFisica(
            cpf=cpf,
            nome=nome,
            data_nascimento=data_nascimento,
            endereco=endereco
        )

        cadastro_pessoas.atualizar_cliente(
            cpf,
            cliente
        )
        print("\n=== Cliente criado com sucesso! ===")
        return cadastro_pessoas

    @classmethod
    def criar_conta_corrente(cls, cadastro_pessoas):
        cpf_valido = False
        while not cpf_valido:
            cpf = InformarValores.informar_cpf()
            clientes = cadastro_pessoas.clientes
            cliente = clientes.get(cpf, None)
            if not cliente:
                print("@@@ Não existe cliente cadastrado para este CPF! @@@")
                input("pressione <enter> para continuar...")
            else:
                cpf_valido = True

        ultima_conta = cadastro_pessoas.obter_ultima_conta()
        numero_conta = "000000"[0:6-len(str(ultima_conta + 1))] + \
                       str(ultima_conta + 1)
        agencia = "0000"
        valor = InformarValores.informar_saldo_inicial()
        limite_saque_diario = InformarValores.informar_limite_saque_diario()
        valor_limite_saque = InformarValores.informar_valor_limite_saque()
        chave_conta = (cpf, agencia, numero_conta)
        dados_conta = {
            "cliente": cliente,
            "valor_limite_saque": valor_limite_saque,
            "limite_saque_diario": limite_saque_diario,
            "saldo": valor,
        }
        cliente, numero = ContaCorrente.adicionar_conta(
            chave_conta,
            dados_conta,
            cliente
        )

        cadastro_pessoas.atualizar_ultima_conta(numero)
        cadastro_pessoas.atualizar_cliente(
            chave_conta[0],
            cliente
        )
        return cadastro_pessoas

    # ** Realizar depósito na conta corrente
    @classmethod
    def realizar_deposito(cls, cliente, conta):

        if (not cliente) or (not conta):
            return None, None, "Cliente e/ou conta não selecionado."

        os.system("cls" if os.name == "nt" else "clear")
        print(f"Cliente: {cliente.nome} - CPF: {cliente.cpf} - "
              f"Conta: {conta.numero} - Saldo: {conta.saldo:.2f}")
        print("-" * 80)
        print("Realizar Depósito na conta corrente")
        print("-" * 80)
        print()

        valor = InformarValores.informar_valor()

        transacao = Deposito(valor)

        cliente.realizar_transacao(conta, transacao)
        return cliente, conta, " "

    # ** Realizar saque na conta corrente
    @classmethod
    def realizar_saque(cls, cliente, conta):

        if (not cliente) or (not conta):
            return None, None, "Cliente e/ou conta não selecionado."

        os.system("cls" if os.name == "nt" else "clear")
        print(f"Cliente: {cliente.nome} - CPF: {cliente.cpf} - "
              f"Conta: {conta.numero} - Saldo: {conta.saldo:.2f}")
        print("-" * 80)
        print("Realizar Saque na conta corrente")
        print("-" * 80)
        print()
        valor = InformarValores.informar_valor()

        transacao = Saque(valor)

        resultado = cliente.realizar_transacao(conta, transacao)
        if resultado:
            mensagem = ""
        else:
            mensagem = "Saque não realizado!"

        return cliente, conta, mensagem

    # ** Controle de seleção do MENU da aplicação
    @classmethod
    def selecionar_atividade(cls, cadastro_pessoas):

        executar_aplicacao = True
        conta = []
        cliente = []

        while executar_aplicacao:
            cls.apresentar_menu(cliente, conta)
            opcao = input().strip().lower()

            # validar o informado com as opçoes disponíveis
            if opcao not in ["d", "s", "e", "c", "u", "l", "q", "x"]:
                print("Opção inválida! Por favor, escolha uma opção válida.")
                input("pressione <enter> para continuar...")
                continue

            # para sair da aplicação usa o opcao "q"
            if opcao == "q":
                executar_aplicacao = False

            # opção para fazer o depósito
            elif opcao == "d":
                cliente, conta, mensagem \
                    = cls.realizar_deposito(cliente, conta)
                print(mensagem)
                input("pressione <enter> para continuar...")

            # fazer o saque na conta corrente
            elif opcao == "s":
                cliente, conta, mensagem \
                    = cls.realizar_saque(cliente, conta)
                print(mensagem)
                input("pressione <enter> para continuar...")

            # opção para exibir o extrato da conta corrente
            elif opcao == "e":
                if (not cliente) or (not conta):
                    print("Cliente e/ou conta não selecionado.")
                    input("pressione <enter> para continuar...")
                else:
                    ListagemDeDados.listar_extrado_cliente(cliente, conta)
                    input("pressione <enter> para continuar...")

            # opção selecionar Cliente e conta
            elif opcao == "x":
                cliente = \
                    cls.selecionar_cliente(
                        cadastro_pessoas
                        )
                conta = cls.selecionar_conta(cliente)
                print(f"Cliente: {cliente.nome} - CPF: {cliente.cpf} - "
                      f"conta: {conta.numero} - saldo: {conta.saldo}" )
                input()

            # opção criar cliente
            elif opcao == "u":
                cadastro_pessoas = \
                    cls.incluir_cadastro_cliente(cadastro_pessoas)
                input()

            # opção criar Conta corrente
            elif opcao == "c":
                cadastro_pessoas = cls.criar_conta_corrente(cadastro_pessoas)
                input()

            # opção criar Conta corrente
            elif opcao == "l":
                ListagemDeDados.listar_dados_dos_clientes(
                    cadastro_pessoas
                )
                input("pressione <enter> para continuar...")


# ************************************************************
# **** classe para carga inicial  dos dados de cliente    ****
# ************************************************************
def __main__():
    cadastro_pessoas = CarregarDadosClientes.fazer_carga_clientes()
    cadastro_pessoas = CarregarDadosConta.fazer_carga_conta(cadastro_pessoas)

    ListagemDeDados.listar_dados_dos_clientes(cadastro_pessoas)
    print("Pressione <enter> para continuar.")
    input()

    ExecutarFuncoesApp.selecionar_atividade(cadastro_pessoas)

    os.system("cls" if os.name == "nt" else "clear")
    print("Obrigado por utilizar nossos serviços!")
    print("Saindo...")
    print("-------------------------------------------")


__main__()
