import uuid
from datetime import datetime
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

WeekdayName = Literal[
    "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
]


class Employee(BaseModel):
    """
    The employee object to be used with all other classes.

    Args:
        id (uuid4): The generated employee ID
        name (str): The full name of the employee, e.g. *"Chris Wright"*
        position (PositionType): The employee's position for getting their rank
        experience (int): Number of months worked, only applicable to full-time workers
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    position: PositionType
    experience: int | None


class Location(BaseModel):
    """
    A location to which employees are assigned to work.

    Args:
        id (uuid4): The generated location ID
        name (str): The name of the location, e.g. *"Service Pt. 1"* or *"Floor Lead"*
        required (bool): If this location must be staffed
        assigned (dict[datetime, list[Employee]]): A dictionary of datetime objects for daily shift segments with a list of Employees at each shift
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    required: bool = True
    num_employees: int = Field(ge=0, default=0)
    assigned: dict[datetime, list[Employee]] = Field(default_factory=dict)


class Template(BaseModel):
    """
    The template object that ties the `Employee` and `Location` classes together.

    Args:
        id (uuid4): The generated template ID
        weekday (WeekdayName): The name of the weekday
        alternate (int): The alternate schedule for this template for use with certain days that have alternating/rotating employees
        employees (dict[tuple[datetime, datetime], list[Employee]]): An dictionary where the keys are working hours for an employee and the value is a list of employees
        locations (dict[str, Location]): Each location sorted as a dictionary by the location's name
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    weekday: WeekdayName
    alternate: int = Field(ge=0, default=0)
    operating_hours: tuple[datetime, datetime]
    employees: dict[tuple[datetime, datetime], list[Employee]]
    locations: dict[str, Location]
