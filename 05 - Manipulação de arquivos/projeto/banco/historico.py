from datetime import datetime

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
                "data": datetime.now(),
            }
        )
    
    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao
    
    def transacoes_do_dia(self):
        data_atual = datetime.utcnow().date()
        transacoes_diarias = []
        for transacao in self.transacoes:
            if transacao["data"].date() == data_atual:
                transacoes_diarias.append(transacao)
        
        return transacoes_diarias