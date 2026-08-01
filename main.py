from dataclasses import dataclass, field
from datetime import time

import pandas as pd
import streamlit as st


@dataclass
class Employee:
    name: str
    position: str

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


def main():
    if "employees" not in st.session_state:
        st.session_state.employees = []

    if "locations" not in st.session_state:
        st.session_state.locations = []

    if "time_slots" not in st.session_state:
        st.session_state.time_slots = []

    st.title("Scheduler")

    employee_tab, location_tab, setup_hours_tab = st.tabs(
        ["Employees", "Floor Locations", "Setup Hours"]
    )

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

            if st.form_submit_button("Add", type="primary"):
                if employee_position:
                    st.session_state.employees.append(
                        Employee(name=employee_name, position=employee_position)
                    )
                    st.toast(
                        f"Added {employee_name} ({employee_position})",
                        icon=":material/person_add:",
                    )
                else:
                    st.toast(
                        f"Please add position for {employee_name}",
                        icon=":material/person_alert:",
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

            if st.form_submit_button("Add", type="primary"):
                if location_name and location_min_employees:
                    st.session_state.locations.append(
                        Location(location_name, [], location_min_employees)
                    )
                elif not location_name:
                    st.toast("Please enter a location name", icon=":material/error:")

        with st.popover("Locations"):
            for location in st.session_state.locations:
                st.write(
                    f"{location.name} ({', '.join(location.employees)} - {location.min_staff})"
                )

    with setup_hours_tab:
        with st.form(border=True, key="setup_hours_form"):
            st.header("Setup hours")

            hours_df = pd.DataFrame(
                [
                    {"weekday": "Sunday", "open": time(14, 0), "close": time(18, 0)},
                    {"weekday": "Monday", "open": time(9, 0), "close": time(20, 0)},
                    {"weekday": "Tuesday", "open": time(9, 0), "close": time(20, 0)},
                    {"weekday": "Wednesday", "open": time(9, 0), "close": time(20, 0)},
                    {"weekday": "Thursday", "open": time(9, 0), "close": time(20, 0)},
                    {"weekday": "Friday", "open": time(9, 0), "close": time(20, 0)},
                    {"weekday": "Saturday", "open": time(9, 0), "close": time(20, 0)},
                ]
            )

            hours_editor = st.data_editor(
                hours_df,
                column_config={
                    "weekday": st.column_config.TextColumn(
                        disabled=True,
                    ),
                    "open": st.column_config.TimeColumn(
                        "Open",
                        min_value=time(8, 0),
                        max_value=time(20, 0),
                        format="hh:mm a",
                        step=15,
                    ),
                    "close": st.column_config.TimeColumn(
                        "Close",
                        min_value=time(8, 0),
                        max_value=time(20, 0),
                        format="hh:mm a",
                        step=15,
                    ),
                },
                hide_index=True,
            )

            if st.form_submit_button("Save", type="primary"):
                pass

        with st.popover("Slots"):
            pass


if __name__ == "__main__":
    main()
