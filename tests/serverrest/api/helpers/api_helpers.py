import time
import requests

from tests.serverrest.config import ServerRestConfig

def delete_user_by_email(config: ServerRestConfig, email: str) -> None:
    try:
        response = requests.get(f"{config.API_BASE_URL}/usuarios")
        if response.status_code != 200:
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
                        time.sleep(0.5) #na pratica, usamos sleep?
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

def login_admin(config: ServerRestConfig, email: str, password: str) -> str:
    """Login via API and return bearer token."""
    response = requests.post(f"{config.API_BASE_URL}/login", json={
        "email": email,
        "password": password
    })
    assert response.status_code == 200, (
        f"Failed to login. Status: {response.status_code}, response: {response.text}"
    )
    token = response.json().get("authorization")
    assert token is not None, "Token not returned"
    return token


def create_product(config: ServerRestConfig, token: str, nome: str, preco: int, descricao: str, quantidade: int) -> str:
    """Create product via API and return _id."""
    product_data = {
        "nome": nome,
        "preco": preco,
        "descricao": descricao,
        "quantidade": quantidade
    }
    headers = {"Authorization": token}
    response = requests.post(f"{config.API_BASE_URL}/produtos", json=product_data, headers=headers)
    assert response.status_code == 201, (
        f"Failed to create product. Status: {response.status_code}, response: {response.text}"
    )
    product_id = response.json().get("_id")
    assert product_id is not None, "Product ID not returned"
    print(f"Product created: {nome} (ID: {product_id})")
    return product_id


def delete_product(config: ServerRestConfig, token: str, product_id: str) -> None:
    """Delete product via API by ID."""
    headers = {"Authorization": token}
    response = requests.delete(f"{config.API_BASE_URL}/produtos/{product_id}", headers=headers)
    if response.status_code == 200:
        print(f"Product deleted with ID: {product_id}")


def delete_product_by_nome(config: ServerRestConfig, token: str, nome: str) -> None:
    """Find product by name using query param and delete it (cleanup before fixture setup)."""
    try:
        headers = {"Authorization": token}
        response = requests.get(f"{config.API_BASE_URL}/produtos", params={"nome": nome}, headers=headers)
        print(f"GET /produtos?nome={nome} → {response.status_code}: {response.text}")
        if response.status_code != 200:
            return

        products = response.json().get("produtos", [])
        for product in products:
            product_id = product.get("_id")
            if product_id:
                delete_resp = requests.delete(f"{config.API_BASE_URL}/produtos/{product_id}", headers=headers)
                print(f"DELETE /produtos/{product_id} → {delete_resp.status_code}: {delete_resp.text}")
    except Exception as e:
        print(f"Error deleting product: {e}")