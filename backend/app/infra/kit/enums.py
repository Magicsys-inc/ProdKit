from enum import StrEnum


class Environment(StrEnum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class TenantLevel(StrEnum):
    ORIGIN = "origin"
    INTERNAL = "internal"
    PARTNER = "partner"
    TRIAL = "trial"
    INDIVIDUAL = "individual"
    CUSTOMER = "customer"
    NONPROFIT = "non-profit"
    RESELLER = "reseller"
    EDUCATIONAL = "educational"
    DEFAULT = "default"


class TierType(StrEnum):
    ENTERPRISE = "enterprise"
    PREMIUM = "premium"
    STANDARD = "standard"
    FREE = "free"
    DEFAULT = "default"


class AccountLevel(StrEnum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    STAFF = "staff"
    MEMBER = "member"
    CLIENT = "client"
    CUSTOMER = "customer"
    GUEST = "guest"
    SUPPORT = "support"
    BILLING = "billing"
    DEFAULT = "default"


class Status(StrEnum):
    CREATED = "created"
    ONBOARDING = "onboarding"
    ONBOARDED = "onboarded"
    PROVISIONING = "provisioning"
    PROVISIONED = "provisioned"
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    SUSPENDED = "suspended"
    BLOCKED = "blocked"
    EXPIRED = "expired"
    DISABLED = "disabled"
    DELETED = "deleted"


class CredentialType(StrEnum):
    PASSWORD = "password"
    TOKEN = "token"
    API_KEY = "api_key"
    OAUTH = "oauth"
    SSO = "sso"
    MFA = "mfa"
    CERTIFICATE = "certificate"
    OTHER = "other"


class Locale(StrEnum):
    ENGLISH_US = "en-us"


class AccessType(StrEnum):
    READ = "read"
    WRITE = "write"


class Visibility(StrEnum):
    PUBLIC = "public"
    PRIVATE = "private"


class IsolationType(StrEnum):
    SILO = "silo"
    POOL = "pool"
    BRIDGE = "bridge"
    VIRTUAL = "virtual"


class ResourceType(StrEnum):
    USER = "user"
    ORGANIZATION = "organization"
    PROJECT = "project"
    TASK = "task"
    DOCUMENT = "document"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DATABASE = "database"
    SERVER = "server"
    NETWORK = "network"
    STORAGE = "storage"
    API = "api"
    WEBHOOK = "webhook"
    APPLICATION = "application"
    SERVICE = "service"
    ROLE = "role"
    PERMISSION = "permission"
    TEAM = "team"
    SESSION = "session"
    OTHER = "other"
