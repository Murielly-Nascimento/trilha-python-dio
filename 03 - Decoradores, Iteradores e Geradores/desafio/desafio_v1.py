from abc import ABC, ABCMeta, abstractclassmethod, abstractproperty
from datetime import datetime

class ContasIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\
            Agência:\t{conta.agencia}
            Número:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
        """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1

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
            conta.historico.adicionar_transacao(self)

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

class Historico():
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor":transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )
    
    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao

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

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)
    
    def listar_contas(self):
        id = 0
        for conta in self._contas:
            print(f"ID da conta: {id}")
            print(conta)
            id += 1

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
                return cliente
            return None

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
            pessoa_fisica = PessoaFisica(nome, data_nascimento, cpf, endereco)
            self.clientes.append(pessoa_fisica)
            print("Cliente cadastrado com sucesso!")
        except ValueError as e:
            print(e)
    
    def listar_clientes(self):
        for cliente in self.clientes:
            print(cliente)

def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f"{datetime.now()}: {func.__name__.upper()}")
        return resultado
    return envelope

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta!")
        return
    
    cliente.listar_contas()
    id = int(input("Informe o id da conta: "))

    return cliente.contas[id]

@log_transacao
def depositar(banco):
    cpf = input("Informe o CPF do cliente: ")
    cliente_encontrado = banco.cliente_cadastrado(cpf)

    if cliente_encontrado is None:
        print("Cliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente_encontrado)
    if not conta:
        return
    
    cliente_encontrado.realizar_transacao(conta, transacao)

    return

@log_transacao
def sacar(banco):
    cpf = input("Informe o CPF do cliente: ")
    cliente_encontrado = banco.cliente_cadastrado(cpf)

    if cliente_encontrado is None:
        print("Cliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente_encontrado)
    if not conta:
        return
    
    cliente_encontrado.realizar_transacao(conta, transacao)

@log_transacao
def exibir_extrato(banco):
    cpf = input("Informe o CPF do cliente: ")
    cliente_encontrado = banco.cliente_cadastrado(cpf)

    if not cliente_encontrado:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente_encontrado)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    extrato = ""
    tem_transacao = False
    for transacao in conta.historico.gerar_relatorio(tipo_transacao="saque"):
        tem_transacao = True
        extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    if not tem_transacao:
        extrato = "Não foram realizadas movimentações"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


@log_transacao   
def cadastrar_conta(banco):
    cpf = input("Informe o CPF do cliente: ")
    cliente_encontrado = banco.cliente_cadastrado(cpf)

    if not cliente_encontrado:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    numero_conta = len(cliente_encontrado.contas) + 1
    conta = ContaCorrente.nova_conta(cliente=cliente_encontrado, numero=numero_conta)
    cliente_encontrado.adicionar_conta(conta)
    print("\n=== Conta criada com sucesso! ===")

@log_transacao
def listar_contas(banco):
    cpf = input("Informe o CPF do cliente: ")
    cliente_encontrado = banco.cliente_cadastrado(cpf)

    if not cliente_encontrado:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    for conta in ContasIterador(cliente_encontrado.contas):
        print("=" * 100)
        print(print(conta))

def menu():
    print("""
        Bem vindo ao banco Lisboa!

        1 - Depositar.
        2 - Sacar.
        3 - Extrato.
        4 - Nova Conta.
        5 - Listar Contas.
        6 - Novo Usuário.
        0 - Sair.
    """)
    

def main():
    banco = Banco()

    while True:
        menu()
        opcao = int(input("Digite uma das opções do menu: "))

        if opcao == 1:
            depositar(banco)

        elif opcao == 2:
            sacar(banco)

        elif opcao == 3:
            exibir_extrato(banco)
        
        elif opcao == 4:
            cadastrar_conta(banco)
        
        elif opcao == 5:
            listar_contas(banco)
        
        elif opcao == 6:
            banco.cadastrar_cliente()
            
        elif opcao == 0:
            print("Volte sempre!")
            break

        else:
            print("Opcao inválida! Tente novamente.")

main()

