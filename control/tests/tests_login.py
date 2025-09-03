import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group

class LoginTestCase(TestCase):

    def setUp(self):
        # Crear grupos
        self.group_autorizado = Group.objects.create(name="Secretaria Talento Humano")
        self.group_no_autorizado = Group.objects.create(name="Otro Grupo")

        # Usuario con grupo autorizado
        self.user_ok = User.objects.create_user(username="ana", password="12345")
        self.user_ok.groups.add(self.group_autorizado)

        # Usuario sin grupo autorizado
        self.user_sin_permiso = User.objects.create_user(username="carlos", password="12345")
        self.user_sin_permiso.groups.add(self.group_no_autorizado)

        # URL del endpoint
        self.url = reverse("validateAuthentication")

    def test_json_invalido(self):
        response = self.client.post(self.url, data="no-json", content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_credenciales_incompletas(self):
        payload = {"username": "ana"}  # falta contraseña
        response = self.client.post(self.url, data=json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_usuario_no_existente(self):
        payload = {"username": "fantasma", "password": "12345"}
        response = self.client.post(self.url, data=json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_usuario_sin_grupo_autorizado(self):
        payload = {"username": "carlos", "password": "12345"}
        response = self.client.post(self.url, data=json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_usuario_con_grupo_autorizado(self):
        payload = {"username": "ana", "password": "12345"}
        response = self.client.post(self.url, data=json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)
