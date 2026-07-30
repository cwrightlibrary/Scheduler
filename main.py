import streamlit as st


def main():
    if "employees" not in st.session_state:
        st.session_state.employees = []

    with st.form(border=True, key="employee_form"):
        st.header("Add employee")
        st.text_input("Full name")

        st.form_submit_button("Add")
        st.rerun()


if __name__ == "__main__":
    main()
