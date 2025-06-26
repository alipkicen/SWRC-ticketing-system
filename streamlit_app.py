from shareplum import Site
from shareplum import Office365
from shareplum.site import Version
import streamlit as st
import datetime

# Function to submit a ticket to SharePoint
def submit_ticket_to_sharepoint(ticket_data):
    try:
        # SharePoint credentials (replace with secure method in production)
        username = "kbinmuhammad@micron.com"
        password = "Najuwa@990702"

        # Authenticate and connect to SharePoint
        authcookie = Office365('https://microncorp.sharepoint.com', username=username, password=password).GetCookies()
        site = Site('https://microncorp.sharepoint.com/sites/MMPGQ', version=Version.v365, authcookie=authcookie)

        # Connect to the SharePoint list
        sp_list = site.List('SWRC TASK TRACKER')

        # Submit the ticket
        sp_list.UpdateListItems(data=[ticket_data], kind='New')
        return True, "Ticket submitted successfully to SharePoint."
    except Exception as e:
        return False, f"Error submitting ticket: {e}"

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
