import unittest
from datetime import date
from decimal import Decimal
from unittest.mock import patch

import mysql.connector

from app import app
from models import Agendamento


def criar_agendamento():
    """Cria um objeto fictício reutilizado nos testes."""
    return Agendamento(
        id=1,
        cliente="João Silva",
        telefone="(47) 99911-0001",
        servico="Corte tradicional",
        preco="35.00",
        barbeiro="Carlos",
        data="2026-05-04",
        horario="09:00",
        status="Concluído",
    )


class TestAgendamento(unittest.TestCase):
    def test_conversao_de_tupla(self):
        original = criar_agendamento()

        convertido = Agendamento.reverte_tupla(
            original.converte_tupla()
        )

        self.assertEqual(
            convertido.converte_tupla(),
            original.converte_tupla(),
        )
        self.assertEqual(convertido.preco, Decimal("35.00"))
        self.assertEqual(convertido.data, date(2026, 5, 4))

    def test_reverte_tupla_none(self):
        self.assertIsNone(Agendamento.reverte_tupla(None))

    def test_exibir(self):
        texto = criar_agendamento().exibir()

        self.assertIn("João Silva", texto)
        self.assertIn("R$ 35,00", texto)
        self.assertIn("04/05/2026", texto)
        self.assertNotIn("\n", texto)

    def test_status_invalido(self):
        with self.assertRaises(ValueError):
            Agendamento(
                cliente="Teste",
                telefone=None,
                servico="Corte",
                preco="35.00",
                barbeiro="Carlos",
                data="2026-05-04",
                horario="09:00",
                status="Inválido",
            )


class TestRotas(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    @patch("app.listar_agendamentos")
    def test_inicio(self, consulta):
        consulta.return_value = [criar_agendamento()]

        resposta = self.client.get("/")
        html = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Barbearia Navalha de Ouro", html)
        self.assertIn('<strong class="numero">1</strong>', html)

    @patch("app.listar_agendamentos")
    def test_listagem(self, consulta):
        consulta.return_value = [criar_agendamento()]

        resposta = self.client.get("/agendamentos")
        html = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("João Silva", html)
        self.assertIn('class="linha-concluido"', html)

    @patch("app.listar_por_status")
    def test_filtro(self, consulta):
        consulta.return_value = [criar_agendamento()]

        resposta = self.client.get(
            "/agendamentos/status/Conclu%C3%ADdo"
        )

        self.assertEqual(resposta.status_code, 200)
        consulta.assert_called_once_with("Concluído")

    def test_status_invalido(self):
        resposta = self.client.get("/agendamentos/status/Inexistente")

        self.assertEqual(resposta.status_code, 404)

    @patch("app.buscar_agendamento")
    def test_detalhe_existente(self, consulta):
        consulta.return_value = criar_agendamento()

        resposta = self.client.get("/agendamento/1")
        html = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("João Silva", html)
        self.assertIn("R$ 35,00", html)
        consulta.assert_called_once_with(1)

    @patch("app.buscar_agendamento")
    def test_detalhe_inexistente(self, consulta):
        consulta.return_value = None

        resposta = self.client.get("/agendamento/999")
        html = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 404)
        self.assertIn("Agendamento não encontrado", html)

    @patch("app.listar_agendamentos")
    def test_falha_no_banco(self, consulta):
        consulta.side_effect = mysql.connector.Error(
            "Falha simulada de conexão"
        )

        resposta = self.client.get("/")
        html = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 503)
        self.assertIn("Banco de dados indisponível", html)
        self.assertNotIn("Falha simulada de conexão", html)


if __name__ == "__main__":
    unittest.main()