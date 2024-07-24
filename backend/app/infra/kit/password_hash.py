from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError
from argon2.low_level import Type

from app.infra.config import settings

from .utils import ensure_bytes, ensure_str

# Define a secret pepper (this should be securely stored and kept secret)
PEPPER: str | bytes = settings.PEPPER_SECRET

# https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
ARGON2_TIME_COST: int = 2  # Number of iterations
ARGON2_MEMORY_COST: int = 19 * 1024  # Memory cost in KiB (19 MiB)
ARGON2_PARALLELISM: int = 1  # Degree of parallelism
ARGON2_HASH_LEN: int = 32
ARGON2_SALT_LEN: int = 16
ARGON2_TYPE: Type = Type.ID  # Argon2id type


class Argon2Hasher:
    def __init__(
        self,
        time_cost: int = ARGON2_TIME_COST,
        memory_cost: int = ARGON2_MEMORY_COST,
        parallelism: int = ARGON2_PARALLELISM,
        hash_len: int = ARGON2_HASH_LEN,
        salt_len: int = ARGON2_SALT_LEN,
        type: Type = ARGON2_TYPE,
    ) -> None:
        """
        Initialize the Argon2 hasher with the specified configuration.
        """
        self._hasher = PasswordHasher(
            time_cost=time_cost,
            memory_cost=memory_cost,
            parallelism=parallelism,
            hash_len=hash_len,
            salt_len=salt_len,
            type=type,
        )

    def _hash_password(
        self, pepper: str | bytes, password: str | bytes, salt: bytes | None = None
    ) -> str:
        """
        Internal method to hash the password with pepper (and custom salt).
        """
        pepper = ensure_str(pepper)
        password = ensure_str(password)
        peppered_password = pepper + password
        return self._hasher.hash(peppered_password, salt=salt)

    def create_password_hash(
        self,
        prefix: str | bytes,
        password: str | bytes,
        salt: bytes | None = None,
        pepper: str | bytes = PEPPER,
    ) -> str:
        """
        Create a hashed password with a prefix.

        Argon2 handles generates salts internally!
        If you want use your custom salt, implement and use it carefully!!!
        """
        prefix = ensure_str(prefix)
        pepper = ensure_str(pepper)
        hashed_password = self._hash_password(pepper, password, salt)
        return f"{prefix}${hashed_password}"

    def verify_password(
        self,
        password_hash: str | bytes,
        prefix: str | bytes,
        password: str | bytes,
        pepper: str | bytes = PEPPER,
    ) -> bool:
        try:
            """
            Verify the provided password against the stored hash.

            prefix$argon2id$hashvalue --> prefix + $argon2id$hashvalue
            """
            password_hash = ensure_str(password_hash)
            prefix = ensure_str(prefix)
            stored_prefix, stored_hash = password_hash.split("$", 1)

            if stored_prefix != prefix:
                return False

            if not stored_hash.startswith("$argon2id$"):
                return False

            pepper = ensure_bytes(pepper)
            password = ensure_bytes(password)
            peppered_password = pepper + password
            return self._hasher.verify(stored_hash, peppered_password)
        except (
            VerificationError,
            InvalidHashError,
        ):
            return False

    def check_needs_rehash(self, password_hash: str | bytes) -> bool:
        password_hash = ensure_str(password_hash)
        return self._hasher.check_needs_rehash(password_hash)


__all__ = [
    "Argon2Hasher",
    "VerificationError",
    "InvalidHashError",
]
