import pytest
import requests
from tests.serverrest.config import ServerRestConfig
from playwright.sync_api import Page, expect
from faker import Faker

faker = Faker()

@pytest.mark.ui
def test_login_page_loads(page: Page) -> None:
    """Go to login page and verify if the elements are visible."""

    page.goto("https://front.serverest.dev/login")
    
    expect(page.locator('input[data-testid="email"]')).to_be_visible()
    expect(page.locator('input[data-testid="senha"]')).to_be_visible()
    expect(page.locator('button[data-testid="entrar"]')).to_be_visible()

@pytest.mark.ui 
def test_login_with_unregistered_user(page: Page) -> None:
    """Try to login with an unregistered user and verify if the error message is visible."""

    page.goto("https://front.serverest.dev/login")
    
    page.locator('input[data-testid="email"]').fill("unregistered@example.com")
    page.locator('input[data-testid="senha"]').fill("123456")
    page.locator('button[data-testid="entrar"]').click()

    error_alert = page.locator('div.alert.alert-secondary')
    
    #expect(page.locator('div.alert.alert.secondary')).to_be_visible()
    expect(error_alert).to_be_visible(timeout=10000)

    #expect(error_alert).to_have_text("Email e/ou senha inválidos")

@pytest.mark.ui
def test_navigate_and_register(page: Page) -> None:
    """Go to register page and register a new user."""

    email = faker.email()
    password = 'password123'
    name = "John Doe"

    page.goto("https://front.serverest.dev/login")
    
    expect(page.locator('a[data-testid="cadastrar"]')).to_be_visible()

    page.locator('a[data-testid="cadastrar"]').click()

    expect(page.locator('input[data-testid="nome"]')).to_be_visible()
    expect(page.locator('input[data-testid="email"]')).to_be_visible()
    expect(page.locator('input[data-testid="password"]')).to_be_visible()
    expect(page.locator('button[data-testid="cadastrar"]')).to_be_visible()

    page.locator('input[data-testid="nome"]').fill(name)

    page.locator('input[data-testid="email"]').fill(email)
    page.locator('input[data-testid="password"]').fill(password)
    page.locator('button[data-testid="cadastrar"]').click()

    expect(page.locator('div.alert.alert-primary')).to_be_visible()

@pytest.mark.ui
def test_login_with_registered_user(page: Page, serverrest_config: ServerRestConfig) -> None:
    """Create user via API, then login in UI."""

    email = "testerava@email.com"
    password = "teste123"
    nome = "Ava Test"

    try:
        response = requests.get(f"{serverrest_config.api_base_url}/usuarios")
        
        if response.status_code == 200:
            data = response.json()
            users = data.get("usuarios", []) if isinstance(data, dict) else data
            
            for user in users:
                if user.get("email") == email:
                    user_id = user.get("_id")
                    if user_id:
                        delete_resp = requests.delete(
                            f"{serverrest_config.api_base_url}/usuarios/{user_id}"
                        )
                        if delete_resp.status_code == 200:
                            print(f"user deleted: {user_id}")
                            import time
                            time.sleep(0.5)
                        break
    except Exception as e:
        print(f"delete error: {e}")

    user_data = {
        "nome": nome,
        "email": email,
        "password": password,
        "administrador": "true"
    }

    create_response = requests.post(
        f"{serverrest_config.api_base_url}/usuarios",
        json=user_data
    )
    
    if create_response.status_code == 400:
        error_text = create_response.text.lower()
        if "email" in error_text and ("já" in error_text or "já está sendo usado" in error_text):
            pytest.fail(f"Email already in use. Response: {create_response.text}")
    
    assert create_response.status_code == 201, (
        f"Failed to create user. Status: {create_response.status_code}, "
        f"Response: {create_response.text}"
    )

    response_data = create_response.json()
    user_id = response_data.get("_id")
    
    assert user_id is not None, "User ID not returned"
    
    print(f"User created: {email} (ID: {user_id})")

    page.goto("https://front.serverest.dev/login")
    
    expect(page.locator('input[data-testid="email"]')).to_be_visible()
    expect(page.locator('input[data-testid="senha"]')).to_be_visible()
    expect(page.locator('button[data-testid="entrar"]')).to_be_visible()
    
    page.locator('input[data-testid="email"]').fill(email)
    page.locator('input[data-testid="senha"]').fill(password)
    page.locator('button[data-testid="entrar"]').click()
    
    page.wait_for_load_state("networkidle")
    
    welcome_h1 = page.locator('h1:has-text("bem vindo")')
    expect(welcome_h1).to_be_visible(timeout=5000)
    expect(welcome_h1).to_contain_text(nome, timeout=5000)