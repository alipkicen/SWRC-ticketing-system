# Ensure the 'openpyxl' library is installed and used as the engine for pandas to_excel function
import streamlit as st
import pandas as pd
import datetime
import os

# Set page configuration to wide mode
st.set_page_config(page_title="SWRC Ticketing System", page_icon="🎫", layout="wide")

# Excel file path
EXCEL_FILE = "tickets.xlsx"

# Load existing tickets or create a new DataFrame
if os.path.exists(EXCEL_FILE):
    tickets_df = pd.read_excel(EXCEL_FILE, engine='openpyxl')
else:
    tickets_df = pd.DataFrame(columns=[
        "Requestor", "Date Requested", "Product", "Priority", "Request Type", "Description"
    ])

# --- Streamlit UI ---
st.title("🎫 SWRC Ticketing Request")
st.write(
    """
    Welcome to the SWRC Ticketing System.  
    Please submit a request for any SWRC task.  
    Job requests will be executed based on FIFO flow.
    """
)

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

    # Append and save to Excel
    tickets_df = pd.concat([pd.DataFrame([new_ticket]), tickets_df], ignore_index=True)
    tickets_df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')

    st.success("✅ Ticket submitted and saved to Excel!")
    st.write("### Ticket Details")
    st.write(new_ticket)

# Display all submitted tickets
st.header("📋 Submitted Tickets")
st.dataframe(tickets_df, use_container_width=True, hide_index=True)

