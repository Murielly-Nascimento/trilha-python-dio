# Este programa simula operações bancárias como depósito, saque e exibição de extrato.

LIMITE_SAQUES = 3

def sacar(saldo, extrato, numero_saques):
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


def depositar(saldo, extrato):
    valor = float(input("Digite o valor que deseja depositar: "))
    if valor < 0:
        print("O valor do depósito deve ser maior que 0!")
    else:
        saldo += valor
        extrato += f"Depósito de R$ {valor} realizado.\n"
        print("Depósito feito com sucesso!")

    return saldo, extrato

def imprimir_extrato(extrato, saldo):
    print("\n*****************Extrato******************\n")
    print("Não houve movimentações." if not extrato else extrato)
    print(f"O saldo da conta é R$ {saldo:.2f}.\n")
    print("******************************************")


menu = """
    Bem vindo ao banco Lisboa!

    1 - Sacar.
    2 - Depositar.
    3 - Exibir extrato da conta.
    0 - Sair.
"""

opcao, saldo, extrato, numero_saques = (-1,0,"",0)
while True:
    print(menu)
    opcao = int(input("Digite uma das opções do menu: "))

    if opcao == 1:
        saldo, extrato, numero_saques = sacar(saldo, extrato, numero_saques)
    elif opcao == 2:
        saldo, extrato = depositar(saldo, extrato)
    elif opcao == 3:
        imprimir_extrato(extrato, saldo)
    elif opcao == 0:
        print("Volte sempre!")
        break
    else:
        print("Opcao inválida! Tente novamente.")