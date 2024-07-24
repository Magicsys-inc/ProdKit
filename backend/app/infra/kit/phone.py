import re

from app.infra.core.exceptions import PhoneNotValidError


class PhoneNumberValidator:
    def __init__(self, pattern: str = r"^(?:\+|00)\d{9,15}$"):
        self.pattern = pattern

    def validate(self, phone: str) -> str:
        if not re.match(self.pattern, phone):
            raise PhoneNotValidError(
                phone,
                "Phone number must start with + or 00 and be between 9 and 15 digits",
            )
        return phone


__all__ = ["PhoneNotValidError", "PhoneNumberValidator"]
