from datetime import time

import pandas as pd
import streamlit as st

from src.models import Employee, Location, TimeSlot


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

            employee_experience = st.number_input(
                "Months of experience", min_value=0, max_value=780
            )

            if st.form_submit_button("Add", type="primary"):
                if employee_position and employee_experience:
                    st.session_state.employees.append(
                        Employee(
                            name=employee_name,
                            position=employee_position,
                            experience=employee_experience,
                        )
                    )
                    st.toast(
                        f"Added {employee_name} ({employee_position})",
                        icon=":material/person_add:",
                    )
                else:
                    st.toast(
                        f"Please add position and/or experience for {employee_name}",
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
                with open("test.json", "w") as f:
                    f.write(hours_editor.to_json())

        with st.popover("Slots"):
            pass


if __name__ == "__main__":
    main()
