import streamlit as st
import pandas as pd
import datetime

# Set page configuration to wide mode
st.set_page_config(page_title="SWRC Ticketing System", page_icon="🎫", layout="wide")

# Initialize session state for ticket storage
if "tickets" not in st.session_state:
    st.session_state.tickets = pd.DataFrame(columns=[
        "Requestor", "Date Requested", "Product", "Priority", "Request Type", "Description"
    ])

# --- UI Header ---
st.title("🎫 SWRC Ticketing Request")
st.write(
    """
    Welcome to the SWRC Ticketing System.  
    Please submit a request for any SWRC task.  
    Job requests will be executed based on FIFO flow.
    """
)

# --- Add Ticket Form ---
st.header("➕ Add a New Ticket")

with st.form("add_ticket_form"):
    requestor = st.text_input("👤 Requestor Name", placeholder="Enter your full name")
    product = st.selectbox("📦 Product", ["SSD", "Module", "Component"])
    priority = st.selectbox("🚦 Priority", ["P1 - High Priority", "P2 - Medium Priority", "P3 - Low Priority"])
    request_type = st.selectbox("📄 Type of Request", ["Scrap Request", "Sampling", "Lot Transfer", "Shipment"])
    description = st.text_area("📝 Job Request Description", placeholder="Describe the job request in detail")
    submitted = st.form_submit_button("Submit Ticket")

if submitted:
    new_ticket = {
        "Requestor": requestor,
        "Date Requested": datetime.datetime.now().strftime("%Y-%m-%d"),
        "Product": product,
        "Priority": priority,
        "Request Type": request_type,
        "Description": description
    }

    st.session_state.tickets = pd.concat(
        [pd.DataFrame([new_ticket]), st.session_state.tickets],
        ignore_index=True
    )

    st.success("✅ Ticket submitted successfully!")
    st.write("### Ticket Details")
    st.write(new_ticket)

# --- Display Submitted Tickets ---
st.header("📋 Submitted Tickets")
st.dataframe(st.session_state.tickets, use_container_width=True, hide_index=True)
