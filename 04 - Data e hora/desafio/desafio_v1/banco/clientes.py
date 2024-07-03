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
        if len(conta.historico.transacoes_do_dia()) >= 10:
            print("@@@ Você excedeu o número de transações permitidas para hoje! @@@")
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