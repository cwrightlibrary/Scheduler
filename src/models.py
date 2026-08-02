from dataclasses import dataclass, field


@dataclass
class Employee:
    name: str
    position: str
    experience: int

    @property
    def first_name(self) -> str:
        return self.name.split()[0]

    @property
    def last_name(self) -> str:
        return self.name.split()[1]

    @property
    def initials(self) -> str:
        return "".join([i[0] for i in self.name.replace("-", " ").split()])

    @property
    def sharepoint(self) -> str:
        return f"{self.first_name[0]}{self.last_name}"


@dataclass
class Location:
    name: str
    employees: list[Employee] = field(default_factory=list)
    min_staff: int = 1

    def append_employee(self, employee: Employee) -> None:
        if employee not in self.employees:
            self.employees.append(employee)
        elif self.employees[0] == employee and len(self.employees) > 1:
            self.employees.remove(employee)
            self.employees.append(employee)

    def insert_employee(self, employee: Employee) -> None:
        if employee not in self.employees:
            self.employees.insert(0, employee)
        elif self.employees[-1] == employee and len(self.employees) > 1:
            self.employees.remove(employee)
            self.employees.insert(0, employee)

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
