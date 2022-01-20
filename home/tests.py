from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from home.models import Subscription


class BaseTestCase(APITestCase):

    def setUp(self):
        self.signup_url = reverse("signup-list")
        self.login_url = reverse("login-list")
        self.email = "foobar@example.com"
        self.password = "Some@password"
        self.username = "Foo.bar"
        self.user_id = None

        login_data = {
            "username": self.email,
            "password": self.password,
        }

        register_data = {
            "email": self.email,
            "password": self.password,
            "name": self.username,
            "username": self.username,
        }

        response = self.client.post(
            self.signup_url,
            register_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("id" in response.data)
        self.user_id = response.data.get("id")

        User = get_user_model()
        user = User.objects.get(email=self.email)
        self.assertFalse(user is None)

        response_login = self.client.post(
            self.login_url,
            login_data,
            format="json"
        )
        self.assertTrue("token" in response_login.data)
        self.token = response_login.data.get("token")


class AppApiTestCase(BaseTestCase):

    def test_apis(self):
        """
        Ensure all API endpoints are working fine
        """
        list_url = reverse("app-list")
        data = {
            "domain_name": "Dom2",
            "name": "ABC",
            "type": "1",
            "framework": "1",
            "description": "Test",
            "screenshot": None,
            "user": self.user_id
        }

        # POST
        response = self.client.post(
            list_url,
            data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["domain_name"], data["domain_name"])
        self.assertTrue("id" in response.data)

        # GET
        detail_url = reverse("app-detail", kwargs={"pk": response.data.get("id")})
        detail_response = self.client.get(
            detail_url,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )

        self.assertTrue("id" in detail_response.data)
        self.assertEqual(detail_response.data["domain_name"], data["domain_name"])

        list_response = self.client.get(
            list_url,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)

        # DELETE
        detail_url = reverse("app-detail", kwargs={"pk": response.data.get("id")})
        delete_response = self.client.delete(
            detail_url,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)


class PlanApiTestCase(BaseTestCase):

    def test_apis(self):
        """
        Ensure all API endpoints are working fine
        """
        list_url = reverse("plan-list")
        data = {
            "name": "Free",
            "price": 0
        }

        # POST
        response = self.client.post(
            list_url,
            data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("id" in response.data)

        # PATCH
        detail_url = reverse("plan-detail", kwargs={"pk": response.data.get("id")})
        data = {
            "name": "Pro",
            "price": 25
        }
        patch_response = self.client.patch(
            detail_url,
            data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )

        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.data.get('name'), data['name'])
        self.assertEqual(patch_response.data.get('price'), str(data['price']))

        # GET
        detail_url = reverse("plan-detail", kwargs={"pk": response.data.get("id")})
        detail_response = self.client.get(
            detail_url,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )

        self.assertTrue("id" in detail_response.data)
        self.assertEqual(detail_response.data["name"], data["name"])

        list_response = self.client.get(
            list_url,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)

        # DELETE
        detail_url = reverse("plan-detail", kwargs={"pk": response.data.get("id")})
        delete_response = self.client.delete(
            detail_url,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)


class SubscriptionApiTestCase(BaseTestCase):

    def test_apis(self):
        """
        Ensure all API endpoints are working fine
        """
        # Create APP
        app_list_url = reverse("app-list")
        app_data = {
            "domain_name": "Dom2",
            "name": "ABC",
            "type": "1",
            "framework": "1",
            "description": "Test",
            "screenshot": None,
            "user": self.user_id
        }

        # POST
        app_response = self.client.post(
            app_list_url,
            app_data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )
        app_id = app_response.data.get('id')

        # Create Plan
        plan_list_url = reverse("plan-list")
        plan_data = {
            "name": "Free",
            "price": 0
        }

        plan_response = self.client.post(
            plan_list_url,
            plan_data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )
        plan_id = plan_response.data.get('id')

        # GET
        list_url = reverse("subscription-list")
        data = {
            "app": app_id,
            "plan": plan_id
        }

        # POST
        response = self.client.post(
            list_url,
            data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("id" in response.data)

        # PATCH
        detail_url = reverse("subscription-detail", kwargs={"pk": response.data.get("id")})
        data = {
            "app": app_id,
            "plan": 2
        }

        patch_response = self.client.patch(
            detail_url,
            data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )

        self.assertEqual(patch_response.status_code, status.HTTP_400_BAD_REQUEST)

        # GET
        detail_url = reverse("subscription-detail", kwargs={"pk": response.data.get("id")})
        detail_response = self.client.get(
            detail_url,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )

        self.assertTrue("id" in detail_response.data)
        self.assertEqual(detail_response.data["app"], data["app"])

        list_response = self.client.get(
            list_url,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)

        # DELETE
        detail_url = reverse("subscription-detail", kwargs={"pk": response.data.get("id")})
        delete_response = self.client.delete(
            detail_url,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.token}"
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        subscription = Subscription.objects.get(id=response.data.get("id"))
        self.assertFalse(subscription.is_active)
