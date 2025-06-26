import streamlit as st
import datetime

# Set page configuration to wide mode
st.set_page_config(page_title="SWRC Ticketing System", page_icon="🎫", layout="wide")

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
    st.success("✅ Ticket submitted successfully!")
    st.write("### Ticket Details")
    st.write(f"**Requestor:** {requestor}")
    st.write(f"**Date Requested:** {date_requested}")
    st.write(f"**Product:** {product}")
    st.write(f"**Priority:** {priority}")
    st.write(f"**Request Type:** {request_type}")
    st.write(f"**Description:** {description}")
