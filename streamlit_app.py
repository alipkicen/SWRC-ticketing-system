import streamlit as st
import datetime
import pandas as pd

# Set page configuration to wide mode
st.set_page_config(page_title="SWRC Ticketing System", page_icon="🎫", layout="wide")

# Initialize session state for ticket storage
if "tickets" not in st.session_state:
    st.session_state.tickets = pd.DataFrame(columns=[
        "Requestor", "Date Requested", "Product", "Priority", "Request Type", "Description"
    ])

# Top header
st.title("🎫 SWRC Ticketing Request")
st.write(
    """
    Welcome to the SWRC Ticketing System.  
    Please submit a request for any SWRC task.  
    Job requests will be executed based on FIFO flow.
    """
)

# Add a ticket section
st.header("➕ Add a New Ticket")

with st.form("add_ticket_form"):
    requestor = st.text_input("👤 Requestor Name", placeholder="Enter your full name")
    date_requested = datetime.datetime.now().strftime("%Y-%m-%d")
    product = st.selectbox("📦 Product", ["SSD", "Module", "Component"])
    priority = st.selectbox("🚦 Priority", ["P1 - High Priority", "P2 - Medium Priority", "P3 - Low Priority"])
    request_type = st.selectbox("📄 Type of Request", ["Scrap Request", "Sampling", "Lot Transfer", "Shipment"])
    description = st.text_area("📝 Job Request Description", placeholder="Describe the job request in detail")
    submitted = st.form_submit_button("Submit Ticket")

if submitted:
    new_ticket = {
        "Requestor": requestor,
        "Date Requested": date_requested,
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

# Display all submitted tickets
st.header("📋 Submitted Tickets")
st.dataframe(st.session_state.tickets, use_container_width=True, hide_index=True)
