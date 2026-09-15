import logging
import mysql.connector
from flask import Flask, render_template

from agendamentos import (
    buscar_agendamento,
    listar_agendamentos,
    listar_por_status,
)
from models import Agendamento


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


@app.template_filter("moeda")
def formatar_moeda(valor):
    """Formata valores monetários no padrão brasileiro."""
    if valor is None:
        return "Não informado"

    formatado = f"{valor:,.2f}"
    formatado = formatado.replace(",", "_").replace(".", ",").replace("_", ".")

    return f"R$ {formatado}"


@app.template_filter("data_br")
def formatar_data(valor):
    """Formata uma data como DD/MM/AAAA."""
    if valor is None:
        return "Não informada"

    return valor.strftime("%d/%m/%Y")


@app.route("/")
def index():
    """Página inicial com o total de agendamentos."""
    registros = listar_agendamentos()

    return render_template(
        "index.html",
        agendamentos=registros,
    )


@app.route("/agendamentos")
def agendamentos():
    """Listagem completa dos agendamentos."""
    registros = listar_agendamentos()

    return render_template(
        "agendamentos.html",
        agendamentos=registros,
        status_atual=None,
        status_validos=Agendamento.STATUS_VALIDOS,
    )


@app.route("/agendamentos/status/<status>")
def agendamentos_por_status(status):
    """Listagem filtrada por um dos três status permitidos."""
    if status not in Agendamento.STATUS_VALIDOS:
        abort(404)

    registros = listar_por_status(status)

    return render_template(
        "agendamentos.html",
        agendamentos=registros,
        status_atual=status,
        status_validos=Agendamento.STATUS_VALIDOS,
    )


@app.route("/agendamento/<int:id>")
def detalhe_agendamento(id):
    """Exibe um agendamento ou uma mensagem de registro não encontrado."""
    agendamento = buscar_agendamento(id)

    # O template trata None com um if; o HTTP também informa o resultado.
    codigo_http = 200 if agendamento is not None else 404

    return (
        render_template(
            "detalhe.html",
            agendamento=agendamento,
        ),
        codigo_http,
    )


@app.errorhandler(mysql.connector.Error)
def erro_banco(erro):
    """Exibe uma mensagem amigável sem revelar credenciais ou SQL."""
    return (
        render_template(
            "erro.html",
            titulo="Banco de dados indisponível",
            mensagem=(
                "Não foi possível consultar os agendamentos. "
                "Verifique se o MySQL está iniciado e se as "
                "credenciais em config.py estão corretas."
            ),
        ),
        503,
    )


@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    """Trata URLs inexistentes e filtros inválidos."""
    return (
        render_template(
            "erro.html",
            titulo="Página não encontrada",
            mensagem="O endereço acessado não existe ou o status é inválido.",
        ),
        404,
    )


if __name__ == "__main__":
    # Servidor local para desenvolvimento e avaliação do trabalho.
    # O modo debug fica desativado por padrão.
    app.run(host="127.0.0.1", port=5000, debug=False)