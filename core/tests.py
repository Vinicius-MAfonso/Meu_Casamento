from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
import json
import re
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
        self.assertEqual(convidado.status_confirmacao, False)


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
        self.assertEqual(self.convidado1.status_confirmacao, True)
        self.assertEqual(self.convidado2.status_confirmacao, False)
        self.grupo.refresh_from_db()
        self.assertTrue(self.grupo.status_confirmacao)

    def test_confirmar_presenca_invalid_code(self):
        response = self.client.post('/api/confirmar/invalid-code/', {}, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_confirmar_presenca_already_confirmed(self):
        url = reverse('core:api_confirmar', args=[self.grupo.codigo_acesso])
        data = {'confirmacao': [str(self.convidado1.id)]}
        self.client.post(url, data, content_type='application/json')
        
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("já foi confirmada", response.json()['error'])

    def test_rate_limit_uses_remote_addr_only(self):
        from django.test import RequestFactory
        from .views import rate_limit_ip

        cache.clear()
        factory = RequestFactory()
        request = factory.post(
            reverse('core:api_confirmar', args=[self.grupo.codigo_acesso]),
            content_type='application/json',
            REMOTE_ADDR='1.2.3.4',
            HTTP_X_FORWARDED_FOR='8.8.8.8',
        )

        for _ in range(5):
            self.assertTrue(rate_limit_ip(request, max_requests=5, window=60))

        self.assertFalse(rate_limit_ip(request, max_requests=5, window=60))


def _wedding_date_in(days):
    """A WEDDING_DATE string `days` from now, formatted the same way settings.py uses."""
    return timezone.localtime(timezone.now() + timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%S")


def _is_container_hidden(html, container_id):
    """Whether the container with this id has Tailwind's `hidden` class. Content is
    always present in the DOM either way, so this checks the class list directly
    rather than checking whether text appears in the response."""
    match = re.search(
        r'id="%s"\s*\n?\s*class="([^"]*)"' % re.escape(container_id), html
    )
    assert match, f"container #{container_id} not found in response"
    return "hidden" in match.group(1).split()


class RsvpDeadlineTest(TestCase):
    def setUp(self):
        self.grupo = Grupo.objects.create(nome="Família Silva")
        self.convidado = Convidado.objects.create(nome="João Silva", grupo=self.grupo)

    @override_settings(WEDDING_DATE=_wedding_date_in(10))
    def test_rsvp_page_shows_closed_state_within_deadline_window(self):
        # Wedding in 10 days, RSVP_CLOSE_DAYS_BEFORE=30 -> deadline already passed.
        url = reverse('core:home', args=[self.grupo.codigo_acesso])
        response = self.client.get(url)
        html = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['rsvp_closed'])
        self.assertFalse(_is_container_hidden(html, "closed-container"))
        self.assertTrue(_is_container_hidden(html, "form-container"))

    @override_settings(WEDDING_DATE=_wedding_date_in(60))
    def test_rsvp_page_still_open_outside_deadline_window(self):
        # Wedding in 60 days -> deadline (30 days before) hasn't arrived yet.
        url = reverse('core:home', args=[self.grupo.codigo_acesso])
        response = self.client.get(url)
        html = response.content.decode()
        self.assertFalse(response.context['rsvp_closed'])
        self.assertTrue(_is_container_hidden(html, "closed-container"))
        self.assertFalse(_is_container_hidden(html, "form-container"))

    @override_settings(WEDDING_DATE=_wedding_date_in(10))
    def test_already_confirmed_group_still_sees_success_state_after_deadline(self):
        self.grupo.status_confirmacao = True
        self.grupo.save()
        url = reverse('core:home', args=[self.grupo.codigo_acesso])
        response = self.client.get(url)
        html = response.content.decode()
        self.assertFalse(_is_container_hidden(html, "success-container"))
        self.assertTrue(_is_container_hidden(html, "closed-container"))
        self.assertTrue(_is_container_hidden(html, "form-container"))

    @override_settings(WEDDING_DATE=_wedding_date_in(10))
    def test_api_confirmar_presenca_rejected_after_deadline(self):
        url = reverse('core:api_confirmar', args=[self.grupo.codigo_acesso])
        data = {'confirmacao': [str(self.convidado.id)]}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.assertIn("encerrou", response.json()['error'])
        self.convidado.refresh_from_db()
        self.assertFalse(self.convidado.status_confirmacao)

    @override_settings(WEDDING_DATE=_wedding_date_in(60))
    def test_api_confirmar_presenca_still_works_before_deadline(self):
        url = reverse('core:api_confirmar', args=[self.grupo.codigo_acesso])
        data = {'confirmacao': [str(self.convidado.id)]}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
