import importlib
import sqlite3
import sys
import pytest
from init_db import initialize_database

@pytest.fixture
def application(tmp_path, monkeypatch):
    database = tmp_path / "finance.db"
    initialize_database(database)
    monkeypatch.setenv("FINANCESG_DATABASE", str(database))
    monkeypatch.setenv("FINANCESG_SESSION_DIR", str(tmp_path / "sessions"))
    sys.modules.pop("app", None)
    module = importlib.import_module("app")
    module.app.config.update(TESTING=True)
    yield module
    sys.modules.pop("app", None)

def test_initializer_is_empty_and_refuses_overwrite(tmp_path):
    database = tmp_path / "finance.db"
    initialize_database(database)
    with sqlite3.connect(database) as connection:
        assert connection.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0
    with pytest.raises(FileExistsError):
        initialize_database(database)

def test_registration_login_and_duplicate(application):
    client = application.app.test_client()
    data = {"username":"fictional-user","password":"fictional-test-password","confirm_password":"fictional-test-password"}
    assert client.post("/register", data=data).status_code == 302
    with client.session_transaction() as session:
        assert session["user_id"] > 0
    assert client.get("/logout").status_code == 302
    assert client.post("/login",data=data).status_code == 302
    assert client.post("/register",data=data).status_code == 200
    assert len(application.db.execute("SELECT id FROM users")) == 1

@pytest.mark.parametrize("path", ["/salary","/vehicle","/property","/university"])
def test_unvalidated_financial_forms_cannot_produce_results(application,path):
    client = application.app.test_client()
    assert client.get(path).status_code == 200
    response = client.post(path,data={"salary":"5000","omv":"30000"})
    assert response.status_code == 501
    assert b"Calculation unavailable" in response.data

@pytest.mark.parametrize("income", ["0","-1","invalid","nan","inf"])
def test_budget_rejects_invalid_income(application,income):
    response = application.app.test_client().post("/budget",data={"income":income,"mandatory_expenses":"1","wants_cost":"1","savings":"1"})
    assert response.status_code == 400
    assert b"greater than zero" in response.data

def test_budget_accepts_finite_positive_income(application):
    response = application.app.test_client().post("/budget",data={"income":"1000","mandatory_expenses":"500","wants_cost":"300","savings":"200"})
    assert response.status_code == 200
    assert b"50.0" in response.data
