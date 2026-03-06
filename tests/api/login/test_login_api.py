"""API tests for POST /login."""

import pytest
import requests

from src.config import ServerRestConfig
from src.api.helpers.api_helpers import create_user, delete_user_by_email


class TestLoginAPI:

    @pytest.mark.api
    def test_login_success(
        self, serverrest_config: ServerRestConfig
    ) -> None:
        """POST /login with valid credentials returns 200 with message and Bearer token."""
        email = "apilogin@qa.com"
        password = "teste"

        delete_user_by_email(serverrest_config, email)
        create_user(serverrest_config, email, password, "API Login User", administrador="false")

        try:
            response = requests.post(
                f"{serverrest_config.API_BASE_URL}/login",
                json={"email": email, "password": password},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Login realizado com sucesso"
            assert "authorization" in data
            assert data["authorization"].startswith("Bearer ")
        finally:
            delete_user_by_email(serverrest_config, email)

    @pytest.mark.api
    def test_login_invalid_credentials(
        self, serverrest_config: ServerRestConfig
    ) -> None:
        """POST /login with invalid credentials returns 401."""
        response = requests.post(
            f"{serverrest_config.API_BASE_URL}/login",
            json={"email": "invalid@qa.com", "password": "wrongpassword"},
        )

        assert response.status_code == 401
        data = response.json()
        assert data["message"] == "Email e/ou senha inválidos"
