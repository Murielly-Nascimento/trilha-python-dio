# Classe UsuarioTelefone e o encapsulamento dos atributos nome, numero e plano:
class UsuarioTelefone:
    def __init__(self, nome, numero, plano):
      self.nome = nome
      self.numero = numero
      self.plano = plano
    
    def fazer_chamada(self, destinatario, duracao):
      debito = self.plano.custo_chamada(duracao)
      if self.plano.deduzir_saldo(debito):
        return f"Chamada para {destinatario} realizada com sucesso. Saldo: ${self.plano.saldo:.2f}"
      else:
        return "Saldo insuficiente para fazer a chamada."
       
class Plano:
    def __init__(self, saldo_inicial):
      self.saldo = saldo_inicial
    
    def custo_chamada(self, duracao):
      return duracao * 0.10
    
    def deduzir_saldo(self, debito):
      if debito > self.saldo:
        return False
      else: 
        self.saldo -= debito
        return True
    

class UsuarioPrePago(UsuarioTelefone):
    def __init__(self, nome, numero, saldo_inicial):
      super().__init__(nome, numero, Plano(saldo_inicial))


# Recebendo as informações do usuário:
nome = input()
numero = input()
saldo_inicial = float(input())

# Objeto de UsuarioPrePago com os dados fornecidos:
usuario_pre_pago = UsuarioPrePago(nome, numero, saldo_inicial)
destinatario = input()
duracao = int(input())

# Chama o método fazer_chamada do objeto usuario_pre_pago e imprime o resultado:
print(usuario_pre_pago.fazer_chamada(destinatario, duracao))