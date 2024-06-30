from abc import ABC, ABCMeta, abstractclassmethod, abstractproperty
from datetime import datetime

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adiconar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adiconar_transacao(self)

class Historico():
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao._class_._name_,
                "valor":transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )

class Conta:
    agencia = "0001"

    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo
    
    @saldo.setter
    def saldo(self, valor):
        if valor < 0:
            raise ValueError("O saldo não pode ser negativo")
        self._saldo = valor
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def depositar(self, valor):
        try:
            self.saldo += valor
            print("Depósito feito com sucesso!")
            return True
        
        except ValueError as e:
            print(f"Erro ao depositar: {e}")
            return False

    
    def sacar(self, valor):
        try:
            excedeu_saldo = valor > self._saldo
            if excedeu_saldo:
                print("Saldo insuficiente!")
                return False
            else:
                self.saldo -= valor
                print("Saque realizado com sucesso!")
                return True
            
        except ValueError as e:
            print(f"Erro ao sacar: {e}")
            return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []
    
    @property
    def endereco(self):
        return self._endereco

    @property
    def contas(self):
        return self._contas

    def realizar_transacao(conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)
    
    def listar_contas(self):
        for conta in self._contas:
            print(conta)

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
    
    def __str__(self):
        return (f"Pessoa Física: {self.nome}, CPF: {self.CPF},"
                f"Data de Nascimento: {self.data_nascimento}, Endereço:{super()._endereco}\n")
    
class Banco:
    def __init__(self):
        self.clientes = []

    def cliente_cadastrado(self, cpf):
        for cliente in self.clientes:
            if cliente.cpf == cpf:
                return True
            return False

    def cadastrar_cliente(self):
        cpf = input("Digite seu CPF (somente números): ")

        if self.cliente_cadastrado(cpf):
            print("CPF já cadastrado!")
            return
        
        nome = input("Digite seu nome completo: ")
        data_nascimento = input("Digite data de nascimento dd-mm-yyyy: ")
        endereco = input(
            "Digite seu endereço logradouro, nro - bairro - cidade/sigla do estado: ")
        
        try:
            pessoaFisica = PessoaFisica(nome, data_nascimento, cpf, endereco)
            self.clientes.append(pessoaFisica)
            print("Usuário cadastrado com sucesso!")
            
        except ValueError as e:
            print(e)
    
    def listar_clientes(self):
        for cliente in self.clientes:
            print(cliente)

