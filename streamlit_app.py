import streamlit as st
import datetime
from shareplum import Site
from shareplum import Office365
from shareplum.site import Version

# Set page configuration to wide mode
st.set_page_config(page_title="SWRC Ticketing System", page_icon="🎫", layout="wide")

# --- SharePoint Submission Function ---
def submit_ticket_to_sharepoint(ticket_data):
    try:
        # Replace with your actual SharePoint credentials
        username = "kbinmuhammad@micron.com"
        password = "Najuwa@990702"

        # Authenticate and connect to SharePoint
        authcookie = Office365('https://microncorp.sharepoint.com', username=username, password=password).GetCookies()
        site = Site('https://microncorp.sharepoint.com/sites/MMPGQ', version=Version.v365, authcookie=authcookie)

        # Connect to the SharePoint list
        sp_list = site.List('SWRC TASK REQUEST')

        # Submit the ticket
        sp_list.UpdateListItems(data=[ticket_data], kind='New')
        return True, "✅ Ticket submitted successfully to SharePoint."
    except Exception as e:
        return False, f"❌ Error submitting ticket: {e}"

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
    ticket = {
        'Title': f"{request_type} - {product}",
        'Requestor': requestor,
        'Product': product,
        'Priority': priority,
        'Request': request_type,
        'Job Request Description': description,
        'Date of request': datetime.datetime.now().strftime("%Y-%m-%d")
    }

    success, message = submit_ticket_to_sharepoint(ticket)
    if success:
        st.success(message)
        st.write("### Ticket Details")
        st.write(ticket)
    else:
        st.error(message)
