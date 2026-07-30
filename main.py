import streamlit as st

from dataclasses import dataclass, field


@dataclass
class Employee:
    name: str
    position: str


@dataclass
class Location:
    name: str
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


def main():
    if "employees" not in st.session_state:
        st.session_state.employees = []

    if "locations" not in st.session_state:
        st.session_state.locations = []

    st.title("Scheduler")

    employee_tab, location_tab = st.tabs(["Employees", "Locations"])

    with employee_tab:
        with st.form(border=True, key="employee_form"):
            st.header("Add employee")

            employee_name = st.text_input("Full name")

            employee_position = st.pills(
                "Position",
                [
                    "Manager",
                    "Assistant Manager",
                    "Supervisor",
                    "Full Time",
                    "Part Time",
                    "Security Full Time",
                    "Security Part Time",
                    "Shelver",
                ],
            )

            if st.form_submit_button("Add") and employee_position:
                st.session_state.employees.append(
                    Employee(name=employee_name, position=employee_position)
                )

        with st.popover("Employees"):
            for employee in st.session_state.employees:
                st.write(f"{employee.name} ({employee.position})")

    with location_tab:
        with st.form(border=True, key="location_form"):
            st.header("Add location")

            loc_col1, loc_col2 = st.columns(2)
            with loc_col1:
                location_name = st.text_input("Location name")

            with loc_col2:
                location_min_employees = st.number_input(
                    "Minimum employees required", 0, 4
                )

            if (
                st.form_submit_button("Add")
                and location_name
                and location_min_employees
            ):
                st.session_state.locations.append(
                    Location(location_name, [], location_min_employees)
                )

        with st.popover("Locations"):
            for location in st.session_state.locations:
                st.write(f"{location.name} ({', '.join(location.employees)} - {location.min_staff})")


if __name__ == "__main__":
    main()
