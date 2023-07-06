from starlette.background import P

from .typedefs import *

LeadSource = Literal[
    "website",
    "email",
    "phone",
    "chat",
    "facebook",
    "twitter",
    "linkedin",
    "instagram",
    "youtube",
    "whatsapp",
    "other",
]
LeadStatus = Literal[
    "new", "contacted", "qualified", "unqualified", "converted", "rejected", "other"
]
ProductType = Literal["service", "product", "subscription", "other"]
PaymentMethod = Literal["cash", "card", "bank", "paypal", "stripe", "other"]
DealStatus = Literal["proposal", "negotiation", "won", "lost", "other"]


class User(FaunaModel):
    """
    Auth0 User, Github User or Cognito User
    """

    email: Optional[str] = Field(default=None, index=True)
    email_verified: Optional[bool] = Field(default=False)
    family_name: Optional[str] = Field(default=None)
    given_name: Optional[str] = Field(default=None)
    locale: Optional[str] = Field(default=None, index=True)
    name: str = Field(...)
    nickname: Optional[str] = Field(default=None)
    picture: Optional[str] = Field(default=None)
    sub: str = Field(..., unique=True)
    updated_at: Optional[str] = Field(default=None)
 


class Upload(FaunaModel):
    """

    S3 Upload Record

    """

    user: str = Field(..., description="User sub", index=True)
    name: str = Field(..., description="File name")
    key: str = Field(..., description="File key", unique=True)
    size: int = Field(..., description="File size", gt=0)
    type: str = Field(..., description="File type", index=True)
    lastModified: float = Field(
        default_factory=lambda: datetime.now().timestamp(),
        description="Last modified",
        index=True,
    )
    url: Optional[str] = Field(None, description="File url")


class Lead(FaunaModel):
    email: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    phone: Optional[str] = Field(default=None)
    message: Optional[str] = Field(default=None)
    source: LeadSource = Field(default="website")
    status: LeadStatus = Field(default="new")
    lead_id: str = Field(..., unique=True)
    ipaddr : str = Field(..., index=True)
    attachments: Optional[List[Upload]] = Field(default=None)
    user: Optional[User] = Field(default=None)
    visits: Optional[List[float]] = Field(default=None)
    geo_data: Optional[dict] = Field(default=None)

class Product(FaunaModel):
    name: str = Field(...)
    description: Optional[str] = Field(default=None)
    price: Optional[float] = Field(default=None)
    type: ProductType = Field(default="product")
    media: Optional[List[Upload]] = Field(default=None)
    user: Optional[User] = Field(default=None)


class Deal(FaunaModel):
    payment_method: PaymentMethod = Field(default="cash")
    product: Product = Field(...)
    lead: str = Field(...)
    owner: str = Field(...)
    status: DealStatus = Field(default="proposal")
    attachments: Optional[List[Upload]] = Field(default=None)
    size: Optional[float] = Field(default=None)
    profit: Optional[float] = Field(default=None)
    expected_close_date: Optional[str] = Field(default=None)


class Payment(FaunaModel):
    deal: Deal = Field(...)
    amount: float = Field(...)
    method: PaymentMethod = Field(default="cash")
    date: str = Field(...)
    attachments: Optional[List[Upload]] = Field(default=None)
    user: Optional[User] = Field(default=None)


class Task(FaunaModel):
    deal: Deal = Field(...)
    name: str = Field(...)
    description: Optional[str] = Field(default=None)
    due_date: Optional[str] = Field(default=None)
    attachments: Optional[List[Upload]] = Field(default=None)
    user: Optional[User] = Field(default=None)


class Note(FaunaModel):
    deal: Deal = Field(...)
    name: str = Field(...)
    description: Optional[str] = Field(default=None)
    attachments: Optional[List[Upload]] = Field(default=None)
    user: Optional[User] = Field(default=None)


class Comment(FaunaModel):
    deal: Deal = Field(...)
    name: str = Field(...)
    description: Optional[str] = Field(default=None)
    attachments: Optional[List[Upload]] = Field(default=None)
    user: Optional[User] = Field(default=None)


class Event(FaunaModel):
    deal: Deal = Field(...)
    name: str = Field(...)
    description: Optional[str] = Field(default=None)
    attachments: Optional[List[Upload]] = Field(default=None)
    user: Optional[User] = Field(default=None)
    type: Literal["call", "meeting", "email", "other"] = Field(default="other")
    date: str = Field(...)
    duration: Optional[float] = Field(default=None)
    location: Optional[str] = Field(default=None)
    attendees: Optional[List[str]] = Field(default=None)
    status: Literal["planned", "completed", "cancelled", "other"] = Field(
        default="planned"
    )


class LeadsReport(FaunaModel):
    leads: List[Lead] = Field(...)
    criteria: Literal["source", "status"] = Field(...)


class DealsReport(FaunaModel):
    deals: List[Deal] = Field(...)
    criteria: Literal["status", "product", "payment_method"] = Field(...)


class PaymentsReport(FaunaModel):
    payments: List[Payment] = Field(...)
    criteria: Literal["method", "date"] = Field(...)


class TasksReport(FaunaModel):
    tasks: List[Task] = Field(...)
    criteria: Literal["due_date", "status"] = Field(...)
