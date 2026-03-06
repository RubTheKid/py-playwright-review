"""API tests for GET /usuarios."""

import pytest
import requests

from src.config import ServerRestConfig
from src.api.helpers.api_helpers import create_user, delete_user_by_email


class GetUsersAPI:

    @pytest.mark.api
    def test_get_usuarios_returns_list(
        self, serverrest_config: ServerRestConfig
    ) -> None:
        """GET /usuarios returns 200 with users array."""
        response = requests.get(f"{serverrest_config.API_BASE_URL}/usuarios")

        assert response.status_code == 200
        data = response.json()
        assert "quantidade" in data
        assert "usuarios" in data
        assert isinstance(data["usuarios"], list)
        assert data["quantidade"] == len(data["usuarios"])

    @pytest.mark.api
    def test_get_usuarios_filter_by_email(
        self, serverrest_config: ServerRestConfig
    ) -> None:
        """GET /usuarios?email=X returns only users matching the email."""
        email = "filtertest@qa.com"
        nome = "Filter Test User"
        password = "teste"

        delete_user_by_email(serverrest_config, email)
        create_user(serverrest_config, email, password, nome, administrador="false")

        try:
            response = requests.get(
                f"{serverrest_config.API_BASE_URL}/usuarios",
                params={"email": email},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["quantidade"] >= 1
            assert len(data["usuarios"]) >= 1
            matching = [u for u in data["usuarios"] if u["email"] == email]
            assert len(matching) >= 1
            assert matching[0]["nome"] == nome
            assert matching[0]["email"] == email
            assert matching[0]["password"] == password
            assert matching[0]["administrador"] == "false"
            assert "_id" in matching[0]
        finally:
            delete_user_by_email(serverrest_config, email)

    @pytest.mark.api
    def test_get_usuarios_user_has_required_fields(
        self, serverrest_config: ServerRestConfig
    ) -> None:
        """GET /usuarios returns users with nome, email, password, administrador, _id."""
        response = requests.get(f"{serverrest_config.API_BASE_URL}/usuarios")

        assert response.status_code == 200
        data = response.json()
        assert data["quantidade"] >= 1, "Expected at least one user in the system"

        user = data["usuarios"][0]
        assert "nome" in user
        assert "email" in user
        assert "password" in user
        assert "administrador" in user
        assert "_id" in user
