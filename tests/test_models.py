"""Testes automatizados das classes de dominio."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from errors import DuplicateCpfError, EmptyNameError, InvalidCpfError, PersonNotFoundError
from models import DeliveryPerson, Employee, Person, Resident, Unit, Vehicle, Visitor
from services import Condominium

CPF_ANA = "52601815906"
CPF_BRUNO = "08301661305"
CPF_JOAO = "18609139034"
CPF_PEDRO = "99603082430"


class TestPerson(unittest.TestCase):
    """Testa validacao, encapsulamento e operadores da classe base."""

    def setUp(self):
        """Roda antes de cada teste, evitando repetir a montagem."""
        self.unidade = Unit("101", "A")
        self.morador = Resident("ana souza", CPF_ANA, self.unidade)

    def test_nome_normalizado(self):
        self.assertEqual(self.morador.name, "Ana Souza")

    def test_cpf_guardado_so_com_numeros(self):
        morador = Resident("Bruno", "083.016.613-05", self.unidade)
        self.assertEqual(morador.cpf, CPF_BRUNO)

    def test_cpf_formatado(self):
        self.assertEqual(self.morador.formatted_cpf, "526.018.159-06")

    def test_classe_abstrata_nao_instancia(self):
        with self.assertRaises(TypeError):
            Person("Alguem", CPF_ANA)

    def test_nome_vazio_lanca_excecao(self):
        with self.assertRaises(EmptyNameError):
            Resident("   ", CPF_ANA, self.unidade)

    def test_cpf_invalido_lanca_excecao(self):
        with self.assertRaises(InvalidCpfError):
            Resident("Ana", "11111111111", self.unidade)

    def test_igualdade_por_cpf(self):
        outro = Visitor("Nome Diferente", CPF_ANA)
        self.assertEqual(self.morador, outro)

    def test_ordenacao_por_nome(self):
        bruno = Resident("Bruno", CPF_BRUNO, self.unidade)
        self.assertEqual(sorted([bruno, self.morador])[0], self.morador)


class TestPolimorfismo(unittest.TestCase):
    """Cada subclasse responde describe() do seu proprio jeito."""

    def setUp(self):
        unidade = Unit("101", "A")
        self.pessoas = [
            Resident("Ana", CPF_ANA, unidade),
            Visitor("Joao", CPF_JOAO),
            DeliveryPerson("Pedro", CPF_PEDRO, "iFood"),
            Employee("Bruno", CPF_BRUNO, "Porteiro", "noite"),
        ]

    def test_cada_tipo_tem_descricao_diferente(self):
        descricoes = [p.describe() for p in self.pessoas]
        self.assertEqual(len(set(descricoes)), len(descricoes))

    def test_heranca_em_tres_niveis(self):
        entregador = self.pessoas[2]
        self.assertIsInstance(entregador, DeliveryPerson)
        self.assertIsInstance(entregador, Visitor)
        self.assertIsInstance(entregador, Person)

    def test_describe_do_entregador_acumula_os_tres_niveis(self):
        texto = self.pessoas[2].describe()
        self.assertIn("Pedro", texto)        # veio de Person
        self.assertIn("Visitante", texto)    # veio de Visitor
        self.assertIn("iFood", texto)        # veio de DeliveryPerson


class TestUnit(unittest.TestCase):
    """Testa composicao e o protocolo de sequencia."""

    def setUp(self):
        self.unidade = Unit("101", "A")
        self.ana = Resident("Ana", CPF_ANA, self.unidade)
        self.bruno = Resident("Bruno", CPF_BRUNO, self.unidade)

    def test_moradores_compartilham_a_mesma_unidade(self):
        self.assertIs(self.ana.unit, self.bruno.unit)

    def test_len_da_unidade(self):
        self.assertEqual(len(self.unidade), 2)

    def test_getitem_e_contains(self):
        self.assertEqual(self.unidade[0], self.ana)
        self.assertIn(self.bruno, self.unidade)


class TestVehicle(unittest.TestCase):
    def test_placa_mercosul_e_antiga(self):
        self.assertTrue(Vehicle.is_valid_plate("ABC1D23"))
        self.assertTrue(Vehicle.is_valid_plate("ABC1234"))
        self.assertFalse(Vehicle.is_valid_plate("AB123"))

    def test_mesma_classe_serve_a_morador_e_visitante(self):
        carro = Vehicle("ABC1D23", "Onix", "Preto")
        morador = Resident("Ana", CPF_ANA, Unit("101", "A"), carro)
        visitante = Visitor("Joao", CPF_JOAO, carro)
        self.assertEqual(morador.vehicle, visitante.vehicle)


class TestCondominium(unittest.TestCase):
    """Testa as regras de negocio, os generators e o controle de acesso."""

    def setUp(self):
        self.condominio = Condominium("Teste")
        self.unidade = self.condominio.find_or_create_unit("101", "A")
        self.ana = Resident("Ana Souza", CPF_ANA, self.unidade)
        self.condominio.add_person(self.ana)

    def test_cpf_duplicado_lanca_excecao(self):
        with self.assertRaises(DuplicateCpfError):
            self.condominio.add_person(Visitor("Outra Ana", CPF_ANA))

    def test_busca_inexistente_lanca_excecao(self):
        with self.assertRaises(PersonNotFoundError):
            self.condominio.find_by_cpf(CPF_JOAO)

    def test_find_or_create_reaproveita_unidade(self):
        mesma = self.condominio.find_or_create_unit("101", "a")
        self.assertIs(mesma, self.unidade)

    def test_generator_busca_por_nome(self):
        encontrados = list(self.condominio.find_by_name("souza"))
        self.assertEqual(encontrados, [self.ana])

    def test_iteracao_e_len(self):
        self.condominio.add_person(Visitor("Joao", CPF_JOAO))
        self.assertEqual(len(self.condominio), 2)
        self.assertEqual(len(list(self.condominio)), 2)

    def test_entrada_e_saida(self):
        self.condominio.register_entry(self.ana, self.unidade)
        self.assertEqual(len(list(self.condominio.people_inside())), 1)
        log = self.condominio.register_exit(CPF_ANA)
        self.assertFalse(log.is_open)
        self.assertEqual(len(list(self.condominio.people_inside())), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
