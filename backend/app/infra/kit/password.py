import re

from app.infra.core.exceptions import PasswordNotValidError


class PasswordValidator:
    def __init__(
        self,
        min_length: int = 8,
        max_length: int = 128,
        special_characters: str = r"[!@#$%^&*(),.?\":{}|<>]",
    ):
        self.min_length = min_length
        self.max_length = max_length
        self.special_characters = special_characters
        self.special_characters_set = set(re.findall(r"\W", special_characters))

    def validate(self, password: str) -> str:
        if len(password) < self.min_length:
            raise PasswordNotValidError(
                password, f"Password must be at least {self.min_length} characters long"
            )
        if len(password) > self.max_length:
            raise PasswordNotValidError(
                password,
                f"Password must be no more than {self.max_length} characters long",
            )
        if not re.search(r"[A-Z]", password):
            raise PasswordNotValidError(
                password, "Password must contain at least one uppercase letter"
            )
        if not re.search(r"[a-z]", password):
            raise PasswordNotValidError(
                password, "Password must contain at least one lowercase letter"
            )
        if not re.search(r"[0-9]", password):
            raise PasswordNotValidError(
                password, "Password must contain at least one digit"
            )
        if not re.search(self.special_characters, password):
            special_chars_list = ", ".join(self.special_characters_set)
            raise PasswordNotValidError(
                password,
                f"Password must contain at least one special character from: {special_chars_list}",
            )
        return password


__all__ = ["PasswordNotValidError", "PasswordValidator"]
