import os
import pytest
import requests
import psycopg2
import paramiko
import json

class Settings:
    API_BASE = os.getenv("API_BASE_URL", "http://localhost:8080")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_USER = os.getenv("DB_USER", "trader")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "trader")
    LOG_PATH = os.getenv("LOG_PATH", "/var/log/simulator/app.log")
    SSH_HOST = os.getenv("SSH_HOST", "localhost")
    SSH_USER = os.getenv("SSH_USER", "sim")
    SSH_PASSWORD = os.getenv("SSH_PASSWORD", "sim")

settings = Settings()

# --- Clients ---
class APIClient:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = settings.API_BASE

    def get(self, endpoint, params=None):
        return self.session.get(f"{self.base_url}{endpoint}", params=params, timeout=10)

    def post(self, endpoint, payload):
        return self.session.post(f"{self.base_url}{endpoint}", json=payload, timeout=10)

class DBClient:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )

    def fetch_one(self, query):
        with self.conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchone()

class SSHClient:
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(
            hostname=settings.SSH_HOST,
            username=settings.SSH_USER,
            password=settings.SSH_PASSWORD
        )

    def read_file(self, path):
        stdin, stdout, stderr = self.client.exec_command(f"cat {path}")
        return stdout.read().decode()

    def close(self):
        self.client.close()

# --- Fixtures ---
@pytest.fixture(scope="session")
def api_client():
    return APIClient()

@pytest.fixture(scope="session")
def db_client():
    return DBClient()

@pytest.fixture
def ssh_client():
    client = SSHClient()
    yield client
    client.close()
