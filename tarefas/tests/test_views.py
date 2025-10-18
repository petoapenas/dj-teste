from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.core import mail
from tarefas.models import Task
from tarefas.views import task_list_create

class TaskViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.list_url = reverse('tarefas:lista')
        Task.objects.create(title='A')

    def test_get_lista_status_200_template_e_contexto(self):
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'tarefas/lista.html')
        self.assertIn('tasks', resp.context)
        self.assertContains(resp, 'Minhas tarefas')

    def test_post_cria_tarefa_valida_redireciona_e_envia_email(self):
        resp = self.client.post(self.list_url, data={'title': 'Nova Tarefa'})
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, self.list_url)
        self.assertTrue(Task.objects.filter(title='Nova Tarefa').exists())

        # e-mail foi para a caixa de memórias
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Nova Tarefa', mail.outbox[0].body)

    def test_post_cria_tarefa_invalida_retorna_200_com_erros(self):
        resp = self.client.post(self.list_url, data={'title': 'Oi'})
        self.assertEqual(resp.status_code, 200)  # re-render do form
        self.assertContains(resp, 'Título muito curto')
        self.assertFalse(Task.objects.filter(title='Oi').exists())

    def test_toggle_funciona_somente_post(self):
        t = Task.objects.create(title='X')
        toggle_url = reverse('tarefas:toggle', args=[t.pk])

        # GET deve ser 405 (decorator require_POST)
        resp_get = self.client.get(toggle_url)
        self.assertEqual(resp_get.status_code, 405)

        # POST alterna
        resp_post = self.client.post(toggle_url)
        self.assertEqual(resp_post.status_code, 302)
        t.refresh_from_db()
        self.assertTrue(t.done)

    def test_view_com_requestfactory(self):
        """Exemplo de teste direto na função da view (sem middleware)."""
        request = self.factory.get(self.list_url)
        response = task_list_create(request)
        self.assertEqual(response.status_code, 200)
