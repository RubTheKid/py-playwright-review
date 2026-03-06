## Test Commands

### Run all tests
.\venv\Scripts\python.exe -m pytest -q

### Run a single test
.\venv\Scripts\python.exe -m pytest tests\ui\login\test_login_ui.py::TestLogin::test_login_with_registered_user -q


## Allure Report (requires Java installed)

### Run tests and save results
.\venv\Scripts\python.exe -m pytest tests\serverrest\ui\ -q --alluredir=allure-results

### Open report in browser
allure serve allure-results

### if allure serve fails
manually set java home
```
$env:JAVA_HOME = "C:\Program Files\Microsoft\jdk-21.0.10.7-hotspot"
allure serve allure-results
```

## Notes
- Environment variables: SERVERREST_UI_BASE_URL, SERVERREST_API_BASE_URL

