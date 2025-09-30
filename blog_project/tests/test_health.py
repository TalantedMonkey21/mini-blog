from django.test import TestCase, Client

class HealthzTest(TestCase):
    def test_healthz(self):
        c = Client()
        resp = c.get("/healthz")
        assert resp.status_code in (200, 204)