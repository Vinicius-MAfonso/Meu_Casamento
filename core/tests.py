from django.test import TestCase
from django.urls import reverse
from .models import Grupo, Convidado


class GrupoModelTest(TestCase):
    def test_grupo_creation(self):
        grupo = Grupo.objects.create(nome="Família Silva")
        self.assertEqual(grupo.nome, "Família Silva")
        self.assertFalse(grupo.status_confirmacao)
        self.assertIsNotNone(grupo.codigo_acesso)


class ConvidadoModelTest(TestCase):
    def setUp(self):
        self.grupo = Grupo.objects.create(nome="Família Silva")

    def test_convidado_creation(self):
        convidado = Convidado.objects.create(
            nome="João Silva",
            grupo=self.grupo
        )
        self.assertEqual(convidado.nome, "João Silva")
        self.assertEqual(convidado.grupo, self.grupo)
        self.assertEqual(convidado.status_confirmacao, "pendente")


class HomeViewTest(TestCase):
    def setUp(self):
        self.grupo = Grupo.objects.create(nome="Família Silva")

    def test_home_view_with_valid_code(self):
        url = reverse('core:home', args=[self.grupo.codigo_acesso])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.grupo.nome)

    def test_home_view_with_invalid_code(self):
        response = self.client.get('/invalid-code/')
        self.assertEqual(response.status_code, 404)


class APIConfirmarPresencaTest(TestCase):
    def setUp(self):
        self.grupo = Grupo.objects.create(nome="Família Silva")
        self.convidado1 = Convidado.objects.create(
            nome="João Silva", grupo=self.grupo
        )
        self.convidado2 = Convidado.objects.create(
            nome="Maria Silva", grupo=self.grupo
        )

    def test_confirmar_presenca_success(self):
        url = reverse('core:api_confirmar', args=[self.grupo.codigo_acesso])
        data = {'confirmacao': [str(self.convidado1.id)]}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.convidado1.refresh_from_db()
        self.convidado2.refresh_from_db()
        self.assertEqual(self.convidado1.status_confirmacao, 'confirmado')
        self.assertEqual(self.convidado2.status_confirmacao, 'pendente')
        self.grupo.refresh_from_db()
        self.assertTrue(self.grupo.status_confirmacao)

    def test_confirmar_presenca_invalid_code(self):
        response = self.client.post('/api/confirmar/invalid-code/', {}, content_type='application/json')
        self.assertEqual(response.status_code, 404)
