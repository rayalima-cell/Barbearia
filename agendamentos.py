import logging
import mysql.connector

from banco import conectar
from models import Agendamento

logger = logging.getLogger(__name__)

# A ordem deve corresponder à utilizada em reverte_tupla().
COLUNAS = """
    id, cliente, telefone, servico, preco,
    barbeiro, data, horario, status
"""


def listar_agendamentos():
    """Retorna todos os agendamentos ordenados por data e horário."""
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            f"""
            SELECT {COLUNAS}
            FROM agendamentos
            ORDER BY data ASC, horario ASC, id ASC
            """
        )

        return [
            Agendamento.reverte_tupla(linha)
            for linha in cursor.fetchall()
        ]

    except mysql.connector.Error:
        logger.exception("Erro ao listar agendamentos.")

        # Propaga o erro para o Flask exibir a página de indisponibilidade.
        # Não retorna [], pois isso confundiria falha no banco com lista vazia.
        raise

    finally:
        # O bloco interno garante o fechamento da conexão mesmo se
        # ocorrer um problema ao fechar o cursor.
        try:
            if cursor is not None:
                cursor.close()
        finally:
            if conexao is not None:
                conexao.close()


def buscar_agendamento(id):
    """Retorna um Agendamento pelo ID ou None se não existir."""
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # Parâmetros são enviados separadamente para evitar SQL injection.
        cursor.execute(
            f"""
            SELECT {COLUNAS}
            FROM agendamentos
            WHERE id = %s
            """,
            (id,),
        )

        linha = cursor.fetchone()

        return Agendamento.reverte_tupla(linha)

    except mysql.connector.Error:
        logger.exception("Erro ao buscar agendamento de ID %s.", id)
        raise

    finally:
        try:
            if cursor is not None:
                cursor.close()
        finally:
            if conexao is not None:
                conexao.close()


def listar_por_status(status):
    """Retorna os agendamentos do status informado, em ordem cronológica."""
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            f"""
            SELECT {COLUNAS}
            FROM agendamentos
            WHERE status = %s
            ORDER BY data ASC, horario ASC, id ASC
            """,
            (status,),
        )

        return [
            Agendamento.reverte_tupla(linha)
            for linha in cursor.fetchall()
        ]

    except mysql.connector.Error:
        logger.exception("Erro ao filtrar agendamentos por status.")
        raise

    finally:
        try:
            if cursor is not None:
                cursor.close()
        finally:
            if conexao is not None:
                conexao.close()