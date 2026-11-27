"""Testes HTTP com sessões sintéticas; qualquer acesso ao MySQL falha."""

import copy
import importlib.util
import json
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch


def carregar_app_sem_banco():
    extensao = types.ModuleType("flask_mysqldb")

    class MySQLProibido:
        def __init__(self, app):
            pass

        @property
        def connection(self):
            raise AssertionError("Os testes do carrinho não podem acessar um banco")

    extensao.MySQL = MySQLProibido
    driver = types.ModuleType("MySQLdb")
    cursores = types.ModuleType("MySQLdb.cursors")
    cursores.DictCursor = object()
    driver.cursors = cursores
    caminho = Path(__file__).resolve().parents[1] / "main.py"
    spec = importlib.util.spec_from_file_location("conict_test_app", caminho)
    modulo = importlib.util.module_from_spec(spec)
    substitutos = {
        "flask_mysqldb": extensao,
        "MySQLdb": driver,
        "MySQLdb.cursors": cursores,
        "conict_test_app": modulo,
    }
    with patch.dict(sys.modules, substitutos), patch("os.makedirs"):
        spec.loader.exec_module(modulo)
    modulo.app.config.update(TESTING=True, SECRET_KEY="synthetic-test-session-key")
    return modulo.app


class AtualizarQuantidadeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = carregar_app_sem_banco()

    def setUp(self):
        self.client = self.app.test_client()
        self.carrinho = [
            {"id": 17, "nome": "Produto sintético A", "marca": "Teste",
             "preco": 12.5, "quantidade": 2, "imagem": "synthetic.jpg"},
            {"id": 23, "nome": "Produto sintético B", "marca": "Teste",
             "preco": 7.0, "quantidade": 2, "imagem": "synthetic.jpg"},
        ]
        with self.client.session_transaction() as sessao:
            sessao.update(loggedin=True, id=1, nome="Cliente sintético", tipo="cliente",
                          carrinho=copy.deepcopy(self.carrinho))

    def post(self, dados):
        # Cada subcaso começa com o mesmo carrinho, mesmo se o código antigo o corromper.
        with self.client.session_transaction() as sessao:
            if sessao.get("loggedin"):
                sessao["carrinho"] = copy.deepcopy(self.carrinho)
        return self.client.post("/atualizar-quantidade", data=json.dumps(dados),
                                content_type="application/json")

    def conferir_rejeicao(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        self.assertFalse(response.get_json()["success"])
        with self.client.session_transaction() as sessao:
            self.assertEqual(sessao["carrinho"], self.carrinho)

    def test_rejeita_quantidades_negativas_sem_alterar_carrinho(self):
        for quantidade in (-1, -4, "-2"):
            with self.subTest(quantidade=quantidade):
                self.conferir_rejeicao(self.post({"produto_id": 17, "quantidade": quantidade}))

    def test_rejeita_quantidade_zero_inclusive_texto(self):
        for quantidade in (0, "0"):
            with self.subTest(quantidade=quantidade):
                self.conferir_rejeicao(self.post({"produto_id": 17, "quantidade": quantidade}))

    def test_rejeita_quantidades_sem_inteiro_positivo_valido(self):
        for quantidade in (True, False, 1.5, 3.0, "1.5", "abc", None, [], {},
                           2_147_483_648, "2147483648"):
            with self.subTest(quantidade=quantidade):
                self.conferir_rejeicao(self.post({"produto_id": 17, "quantidade": quantidade}))

    def test_rejeita_corpos_json_que_nao_sao_objetos(self):
        for dados in (None, [], "texto", 3, True):
            with self.subTest(dados=dados):
                self.conferir_rejeicao(self.post(dados))

    def test_rejeita_json_malformado_ou_conteudo_sem_json(self):
        for content_type, dados in (("application/json", "{"), ("text/plain", "texto")):
            with self.subTest(content_type=content_type):
                response = self.client.post("/atualizar-quantidade", data=dados,
                                            content_type=content_type)
                self.conferir_rejeicao(response)

    def test_rejeita_identificadores_invalidos_sem_editar_outro_produto(self):
        for produto_id in (17.5, True, "abc", None, [], {}, 0, -17):
            with self.subTest(produto_id=produto_id):
                self.conferir_rejeicao(self.post({"produto_id": produto_id, "quantidade": 3}))

    def test_quantidade_inteira_atualiza_totais_e_sessao_persistida(self):
        response = self.post({"produto_id": 17, "quantidade": 3})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"success": True, "total_item": 37.5,
                                               "total_carrinho": 51.5})
        with self.client.session_transaction() as sessao:
            self.assertEqual(sessao["carrinho"][0]["quantidade"], 3)
            self.assertEqual(sessao["carrinho"][1], self.carrinho[1])
        pagina = self.client.get("/carrinho")
        self.assertEqual(pagina.status_code, 200)
        self.assertIn('value="3"', pagina.get_data(as_text=True))

    def test_aceita_inteiros_em_texto_enviados_pelo_campo_da_interface(self):
        response = self.post({"produto_id": "17", "quantidade": "4"})
        self.assertEqual(response.get_json(), {"success": True, "total_item": 50.0,
                                               "total_carrinho": 64.0})
        with self.client.session_transaction() as sessao:
            self.assertEqual(sessao["carrinho"][0]["quantidade"], 4)
            self.assertIs(type(sessao["carrinho"][0]["quantidade"]), int)

    def test_produto_ausente_nao_altera_carrinho(self):
        self.conferir_rejeicao(self.post({"produto_id": 99, "quantidade": 3}))

    def test_sessao_nao_autenticada_continua_recusada(self):
        with self.client.session_transaction() as sessao:
            sessao.clear()
        response = self.post({"produto_id": 17, "quantidade": 3})
        self.assertFalse(response.get_json()["success"])
        with self.client.session_transaction() as sessao:
            self.assertNotIn("carrinho", sessao)


if __name__ == "__main__":
    unittest.main()
