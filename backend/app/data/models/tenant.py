from datetime import datetime
from typing import Any

from citext import CIText
from sqlalchemy import TIMESTAMP, Boolean, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.data.dbs.postgres.extensions.sqlalchemy import StringEnum
from app.data.dbs.postgres.models import RecordModel
from app.infra.kit.enums import Status, TenantLevel, TierType

"""
tenant --> tenant_type --> TenantLevel
    account --> account_type --> AccountLevel
        organization -->
        user -->

anonymous
"""


class Tenant(RecordModel):
    __tablename__ = "tenants"
    __table_args__ = ()

    schema: str = ""

    status: Mapped[Status] = mapped_column(
        StringEnum(Status), nullable=False, default=Status.PENDING
    )
    # TODO: Correct it based on tenant_type table
    # TenantLevel: The classification of tenants based on their characteristics or roles within the system.
    # Used to define different categories of tenants that may not necessarily be related to service levels or pricing.
    tenant_type: Mapped[TenantLevel] = mapped_column(
        StringEnum(TenantLevel), nullable=False, default=TenantLevel.DEFAULT
    )
    # Tire: Level of service or pricing plan that a tenant subscribes to.
    # Commonly associated with the features, limitations, and pricing of the service.
    tire: Mapped[TierType] = mapped_column(
        StringEnum(TierType), nullable=False, default=TierType.DEFAULT
    )
    name: Mapped[str] = mapped_column(CIText(), nullable=False, unique=True)
    domain: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None)
    email: Mapped[str | None] = mapped_column(String(254), nullable=True, default=None)
    phone_number: Mapped[str | None] = mapped_column(
        String(15), nullable=True, default=None
    )
    address: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=None
    )
    country: Mapped[str] = mapped_column(String(2), nullable=False)
    currency: Mapped[str | None] = mapped_column(String(3))
    api_key: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=None
    )
    app_client_id: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=None
    )
    dedicated_tenancy: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    is_charges_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_payouts_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False)
    api_gateway_url: Mapped[str | None] = mapped_column(
        String(1024), nullable=True, default=None
    )
    settings: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )
    data: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    last_login_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True,
        default=None,
    )
    # business_type:
    description: Mapped[str | None] = mapped_column(
        String(1024), nullable=True, default=None
    )


"""
| Attribute           | Description                                      |
|---------------------|--------------------------------------------------|
| tenant_id           | Foreign key referencing the tenant.              |
| type                | Type of the tenant (e.g., 'origin').             |
| status              | Status of the tenant (e.g., active, suspended).  |
| tier                | Tier level of the tenant (e.g., free, premium).  |
| name                | Name of the tenant.                              |
| domain              | Domain name associated with the tenant.          |
| email               | Contact email of the tenant.                     |
| phone               | Contact phone number of the tenant.              |
| address             | Physical address of the tenant.                  |
| country             | Country where the tenant is located.             |
| currency            | Currency used by the tenant for financial transactions.|
| api_key             | API key for tenant access.                       |
| app_client_id       | Application client ID associated with the tenant.|
| dedicated_tenancy   | Boolean indicating if dedicated tenancy is enabled.|
| is_charges_enabled  | Boolean indicating whether the tenant can process payments.|
| is_payouts_enabled  | Boolean indicating whether the tenant can receive payouts.|
| api_gateway_url     | URL of the API gateway for the tenant.           |
| metadata            | JSON field for additional tenant metadata.       |
| description         | Description of the tenant.                       |
| created_at          | Timestamp when the attribute was created.        |
| updated_at          | Timestamp when the attribute was last updated.   |
| deleted_at          | Timestamp when the attribute was deleted.        |
"""
