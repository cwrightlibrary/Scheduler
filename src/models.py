import uuid
from typing import Literal

from pydantic import BaseModel, Field

PositionType = Literal[
    "manager",
    "assistant-manager",
    "supervisor",
    "full-time",
    "part-time",
    "security-full-time",
    "security-part-time",
    "shelver",
]


class Employee(BaseModel):
    """
    The employee object to be used with all other classes.

    Args:
        id (uuid): The generated employee ID
        name (str): The full name of the employee, e.g. *"Chris Wright"*
        position (PositionType): The employee's position for getting their rank
        experience (int): Number of months worked, only applicable to full-time workers
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    position: PositionType
    experience: int | None
