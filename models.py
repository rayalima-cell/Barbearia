from datetime import date
from decimal import Decimal

class Agendamento:
    """Representa um registro da tabela agendamentos."""

    STATUS_VALIDOS = ("Agendado", "Concluído", "Cancelado")

    def __init__(
        self,
        cliente,
        telefone,
        servico,
        preco,
        barbeiro,
        data,
        horario,
        status="Agendado",
        id=None,
    ):
        if status not in self.STATUS_VALIDOS:
            raise ValueError("Status de agendamento inválido.")

        self.id = id
        self.cliente = cliente
        self.telefone = telefone
        self.servico = servico

        # Decimal evita imprecisões comuns de float em valores monetários.
        self.preco = Decimal(str(preco)) if preco is not None else None

        self.barbeiro = barbeiro

        # Aceita tanto uma data do MySQL quanto uma string ISO: AAAA-MM-DD.
        self.data = date.fromisoformat(data) if isinstance(data, str) else data

        self.horario = horario
        self.status = status

    def exibir(self):
        """Retorna todos os dados formatados em uma única linha."""
        preco_formatado = (
            f"R$ {self.preco:.2f}".replace(".", ",")
            if self.preco is not None
            else "Não informado"
        )

        return (
            f"ID: {self.id if self.id is not None else 'Novo'} | "
            f"Cliente: {self.cliente} | "
            f"Telefone: {self.telefone or 'Não informado'} | "
            f"Serviço: {self.servico or 'Não informado'} | "
            f"Preço: {preco_formatado} | "
            f"Barbeiro: {self.barbeiro or 'Não informado'} | "
            f"Data: {self.data.strftime('%d/%m/%Y')} | "
            f"Horário: {self.horario or 'Não informado'} | "
            f"Status: {self.status}"
        )

    def converte_tupla(self):
        """Converte o objeto em uma tupla, incluindo o ID.

        Ordem:
        id, cliente, telefone, servico, preco, barbeiro,
        data, horario, status.
        """
        return (
            self.id,
            self.cliente,
            self.telefone,
            self.servico,
            self.preco,
            self.barbeiro,
            self.data,
            self.horario,
            self.status,
        )

    @staticmethod
    def reverte_tupla(tupla):
        """Converte uma linha do banco em um objeto Agendamento."""
        if tupla is None:
            return None

        if len(tupla) != 9:
            raise ValueError("A tupla deve conter exatamente 9 campos.")

        return Agendamento(
            id=tupla[0],
            cliente=tupla[1],
            telefone=tupla[2],
            servico=tupla[3],
            preco=tupla[4],
            barbeiro=tupla[5],
            data=tupla[6],
            horario=tupla[7],
            status=tupla[8],
        )