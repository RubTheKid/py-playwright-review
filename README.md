Execute all tests
.\venv\Scripts\python.exe -m pytest -q

Execute only login tests
.\venv\Scripts\python.exe -m pytest tests\serverrest\ui\test_login.py -q

Execute a individual test
.\venv\Scripts\python.exe -m pytest tests\serverrest\ui\test_login.py::test_login_page_loads -q

Note: .env file is not in .gitignore because it uses public API URLs