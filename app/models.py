from dataclasses import dataclass


@dataclass
class User:
    email: str
    password: str
    full_name: str
    is_2fa_enabled: bool = False
