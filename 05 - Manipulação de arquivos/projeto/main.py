from banco import ContaCorrente, Deposito, Saque, PessoaFisica
from utils import log_transacao, ContasIterador
from datetime import datetime
    
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

    def __repr__(self):
        return f"<{self.__class__.__name__}: ({len(self.clientes)})"

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
        extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}\n\tData: {transacao['data'].strftime('%d-%m-%Y %H:%M:%S')}"

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

