import time
import requests

from tests.serverrest.config import ServerRestConfig

def delete_user_by_email(config: ServerRestConfig, email: str) -> None:
    try:
        response = requests.get(f"{config.API_BASE_URL}/usuarios")
        if response.status_code != 200:  # ← sai só se der erro
            return

        data = response.json()
        users = data.get("usuarios", []) if isinstance(data, dict) else data

        for user in users:
            if user.get("email") == email:
                user_id = user.get("_id")
                if user_id:
                    delete_resp = requests.delete(f"{config.API_BASE_URL}/usuarios/{user_id}")
                    if delete_resp.status_code == 200:
                        print(f"User deleted with ID: {user_id}")
                        time.sleep(0.5)
                break
    except Exception as e:
        print(f"Error deleting user: {e}")

def create_user(config: ServerRestConfig, email: str, password: str, name: str, administrador: str = "false") -> str:
    """Create user via API and return _id """
    user_data = {
        "nome": name,
        "email": email,
        "password": password,
        "administrador": administrador
    }

    response = requests.post(f"{config.API_BASE_URL}/usuarios", json=user_data)

    assert response.status_code == 201, (
        f"Failed to create user. Status: {response.status_code}, response: {response.text}"
    )

    user_id = response.json().get("_id")
    assert user_id is not None, "User ID not returned"

    print(f"User created: {email} (ID: {user_id})")
    return user_id