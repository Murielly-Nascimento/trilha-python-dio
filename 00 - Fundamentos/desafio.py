def sacar(*, saldo, extrato, numero_saques, LIMITE_SAQUES):
    valor = float(input("Digite o valor que deseja sacar: "))

    valor_negativo = valor <= 0
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > 500
    excedeu_saques = numero_saques >= LIMITE_SAQUES

    if valor_negativo:
        print("O valor do saque deve ser maior que 0!")
    elif excedeu_saldo:
        print("Saldo insuficiente!")
    elif excedeu_limite:
        print("Excedeu o limite de R$ 500,00 para saque!")
    elif excedeu_saques:
        print("Excedeu número de 3 saques diários!")
    else:
        saldo -= valor
        numero_saques += 1
        extrato += f"Saque de R$ {valor:.2f} realizado.\n"
        print("Saque realizado com sucesso!")

    return saldo, extrato, numero_saques


def depositar(saldo, extrato, /):
    valor = float(input("Digite o valor que deseja depositar: "))
    if valor < 0:
        print("O valor do depósito deve ser maior que 0!")
    else:
        saldo += valor
        extrato += f"Depósito de R$ {valor} realizado.\n"
        print("Depósito feito com sucesso!")

    return 

def imprimir_extrato(saldo, /, *, extrato):
    print("\n*****************Extrato******************\n")
    print("Não houve movimentações." if not extrato else extrato)
    print(f"O saldo da conta é R$ {saldo:.2f}.\n")
    print("******************************************")


def menu():
    print("""
        Bem vindo ao banco Lisboa!

        1 - Cadastrar Usuário.
        2 - Cadastrar Conta.
        3 - Listar Conta.
        4 - Sacar.
        5 - Depositar.
        6 - Exibir extrato da conta.
        0 - Sair.
    """)

def usuario_cadastrado(usuarios, cpf):
    for usuario in usuarios:
        if usuario.get("CPF") == cpf:
            return True
    return False

def cadastrar_usuario(usuarios):
    cpf = input("Digite seu CPF (somente números): ")
    if usuario_cadastrado(usuarios, cpf):
        print("CPF já cadastrado!")
        return
    nome = input("Digite seu nome completo: ")
    data_nascimento = input("Digite data de nascimento dd-mm-yyyy: ")
    endereco = input("Digite seu endereço logradouro, nro - bairro - cidade/sigla do estado: ")
    usuario = {"CPF": cpf, "nome": nome, "data_nascimento": data_nascimento, "endereco": endereco}
    usuarios.append(usuario)

    print("Usuário cadastrado com sucesso!")
    return

def cadastrar_conta(usuarios, numero_conta):
    CPF = input("Informe CPF do cliente: ")
    if not usuario_cadastrado:
        print("CPF não encontrado!")
        return
    else:
        print("Conta cadastrada com sucesso!")
        numero_conta += 1
        return {"CPF": CPF, "conta": numero_conta,"agencia": "0001"}   

def listar_contas(contas):
    for conta in contas:
        print(conta)     

def main():
    LIMITE_SAQUES = 3
    usuarios = []
    contas = []
    opcao, saldo, extrato, numero_saques, numero_conta = (-1,0,"",0, 0)
    
    while True:
        menu()
        opcao = int(input("Digite uma das opções do menu: "))

        if opcao == 1:
            cadastrar_usuario(usuarios)
        
        elif opcao == 2:
            contas.append(cadastrar_conta(usuarios, numero_conta))

        elif opcao == 3:        
            listar_contas(contas)

        elif opcao == 4:
            sacar(saldo=saldo, extrato=extrato, numero_saques=numero_saques, LIMITE_SAQUES=LIMITE_SAQUES)
        
        elif opcao == 5:
            saldo, extrato = depositar(saldo, extrato)
        
        elif opcao == 6:
            imprimir_extrato(saldo, extrato=extrato)
        
        elif opcao == 0:
            print("Volte sempre!")
            break
        
        else:
            print("Opcao inválida! Tente novamente.")

main()