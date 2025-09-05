from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from control.models import Sede


class RenderViewsTestCase(TestCase):

    def setUp(self):
        # Usuario de prueba
        self.user = User.objects.create_user(
            username="testuser", password="12345")
        # Sede de prueba
        self.sede = Sede.objects.create(
            ubicacion="Principal", ciudad="Barranquilla")

    # ---------------------
    # Lobby
    # ---------------------

    def test_lobby_render_template(self):
        response = self.client.get(reverse("appLobbyRender"))
        self.assertTemplateUsed(response, "lobby.html")
        self.assertEqual(response.status_code, 200)

    # ---------------------
    # QR Reader
    # ---------------------

    def test_qr_reader_render_without_sede(self):
        response = self.client.get(reverse("appQrReaderRender"))
        self.assertTemplateUsed(response, "qr_reader.html")
        self.assertIsNone(response.context["sede_info"])

    def test_qr_reader_render_with_valid_sede(self):
        session = self.client.session
        session["sede_id"] = self.sede.id
        session.save()

        response = self.client.get(reverse("appQrReaderRender"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "qr_reader.html")
        self.assertEqual(
            response.context["sede_info"]["location"],
            "Principal - Barranquilla"
        )

    def test_qr_reader_render_with_invalid_sede(self):
        session = self.client.session
        session["sede_id"] = 9999  # No existe
        session.save()

        response = self.client.get(reverse("appQrReaderRender"))
        self.assertTemplateUsed(response, "qr_reader.html")
        # Como la sede no existe, sede_info debería ser None
        self.assertIsNone(response.context["sede_info"])

    # ---------------------
    # Dashboard
    # ---------------------

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("appDashboardHomeRender"))
        self.assertEqual(response.status_code, 302)  # Redirect al login

    def test_dashboard_authenticated_user(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("appDashboardHomeRender"))
        self.assertTemplateUsed(response, "block_content/home.html")
        self.assertEqual(response.status_code, 200)

    def test_dashboard_active_employees_authenticated(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(
            reverse("appDashboardActiveEmployeesRender"))
        self.assertTemplateUsed(
            response, "block_content/active_employees.html")
        self.assertEqual(response.status_code, 200)

    def test_dashboard_inactive_employees_authenticated(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(
            reverse("appDashboardInactiveEmployeesRender"))
        self.assertTemplateUsed(
            response, "block_content/inactive_employees.html")
        self.assertEqual(response.status_code, 200)

    def test_dashboard_assistance_records_authenticated(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(
            reverse("appDashboardAssistanceRecordRender"))
        self.assertTemplateUsed(
            response, "block_content/assistance_records.html")
        self.assertEqual(response.status_code, 200)

    # ---------------------
    # Dashboard Settings
    # ---------------------

    def test_dashboard_location_settings_authenticated(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(
            reverse("appDashboardLocationSettingsRender"))
        self.assertTemplateUsed(
            response, "block_content/location_settings.html")
        self.assertEqual(response.status_code, 200)

    def test_dashboard_work_area_settings_authenticated(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(
            reverse("appDashboardWorkAreaSettingsRender"))
        self.assertTemplateUsed(
            response, "block_content/work_area_settings.html")
        self.assertEqual(response.status_code, 200)
