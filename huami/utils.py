from huami.configs.errors import ERRORS
from huami.configs.payloads import PAYLOADS
from huami.configs.urls import URLS
from urllib import parse
import uuid
import random

import requests


def _assemble_url(name: str, *args, **kwargs) -> str:
    return URLS[name].format(*args, **kwargs)


def _assemble_payload(name: str, **kwargs) -> dict:
    return {**PAYLOADS[name].copy(), **kwargs}


def _validate_redirect_url_parameters(redirect_url_parameters: dict) -> None:
    if "error" in redirect_url_parameters:
        raise ValueError(
            f"Wrong E-mail or Password."
            f"Error: {redirect_url_parameters['error']}"
        )

    if "access" not in redirect_url_parameters:
        raise ValueError("No 'access' parameter in login url.")


def _validate_login_result(login_result: dict) -> None:
    if "error_code" in login_result:
        error_message = ERRORS.get(login_result["error_code"])
        raise ValueError(f"Login error. Error: {error_message}")

    if "token_info" not in login_result:
        raise ValueError("No 'token_info' parameter in login data.")

    token_info = login_result["token_info"]
    if "app_token" not in token_info:
        raise ValueError("No 'app_token' parameter in login data.")

    if "login_token" not in token_info:
        raise ValueError("No 'login_token' parameter in login data.")

    if "user_id" not in token_info:
        raise ValueError("No 'user_id' parameter in login data.")


class HuamiAmazfit:
    def __init__(self, email: str, password: str) -> None:
        self.email: str = email
        self.password: str = password
        self.access_token: str = ""
        self.country_code: str | None = None

        self.app_token: str | None = None
        self.login_token: str | None = None
        self.user_id: str | None = None

        self.r = str(uuid.uuid4())
        self.device_id: str = "02:00:00:%02x:%02x:%02x" % (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )

    def _set_country_code(self, redirect_url_parameters: dict) -> None:
        if "country_code" not in redirect_url_parameters:
            region = redirect_url_parameters['region'][0]
            self.country_code = region[0:2].upper()
            return

        self.country_code = redirect_url_parameters['country_code']

    def _set_access_token(self, redirect_url_parameters: dict) -> None:
        self.access_token = redirect_url_parameters["access"][0]

    def access(self):
        response = requests.post(
            url=_assemble_url(name='tokens_amazfit', user_email=parse.quote(self.email)),
            data=_assemble_payload(name='tokens_amazfit', password=self.password),
            allow_redirects=False
        )
        response.raise_for_status()

        redirect_url_parameters: dict = parse.parse_qs(
            # 'Location' parameter contains url with login status
            parse.urlparse(response.headers.get('Location')).query
        )
        _validate_redirect_url_parameters(redirect_url_parameters)

        self._set_country_code(redirect_url_parameters)
        self._set_access_token(redirect_url_parameters)

    def login(self):
        response = requests.post(
            url=_assemble_url(name='login_amazfit'),
            data=_assemble_payload(name='login_amazfit',
                                   country_code=self.country_code,
                                   device_id=self.device_id,
                                   code=self.access_token),
            allow_redirects=False
        )
        response.raise_for_status()
        login_result = response.json()
        _validate_login_result(login_result)

        self.user_id = login_result['token_info']["user_id"]
        self.login_token = login_result['token_info']["login_token"]
        self.app_token = login_result['token_info']["app_token"]

    def logout(self) -> None:
        requests.post(
            url=_assemble_url(name='logout'),
            data=_assemble_payload(name='logout', login_token=self.login_token)
        )