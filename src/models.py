from dataclasses import dataclass, field


@dataclass
class Employee:
    name: str


@dataclass
class Location:
    name: str
    required: bool = True
    employees: list[Employee] = field(default_factory=list)
    min_staff: int = 1

    def add_employee(self, employee: Employee) -> None:
        if employee not in self.employees:
            self.employees.append(employee)

    def remove_employee(self, employee: Employee) -> None:
        if employee in self.employees:
            self.employees.remove(employee)

    def is_empty(self) -> bool:
        return len(self.employees) == 0

    def needs_staff(self) -> bool:
        return len(self.employees) < self.min_staff


@dataclass
class TimeSlot:
    start_time: int
    end_time: int
    locations: dict[str, Location] = field(default_factory=dict)

    def get_time_label(self) -> str:
        t1 = self.start_time - 12 if self.start_time > 12 else self.start_time
        t2 = self.end_time - 12 if self.end_time > 12 else self.end_time
        return f"{t1}-{t2}"
