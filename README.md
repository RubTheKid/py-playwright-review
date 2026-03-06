## Test Commands

### Run all tests
.\venv\Scripts\python.exe -m pytest -q

### Run only login tests
.\venv\Scripts\python.exe -m pytest tests\serverrest\ui\login-register\ -q

### Run only admin tests
.\venv\Scripts\python.exe -m pytest tests\serverrest\ui\admin\ -q

### Run a single test
.\venv\Scripts\python.exe -m pytest tests\ui\login\test_login.py::TestLogin::test_login_with_registered_user -q


## Allure Report (requires Java installed)

### Run tests and save results
.\venv\Scripts\python.exe -m pytest tests\serverrest\ui\ -q --alluredir=allure-results

### Open report in browser
allure serve allure-results

## Notes
- Environment variables: SERVERREST_UI_BASE_URL, SERVERREST_API_BASE_URL

