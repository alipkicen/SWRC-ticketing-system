import streamlit as st
import datetime

# Set page configuration to wide mode
st.set_page_config(page_title="SWRC Ticketing System", page_icon="🎫", layout="wide")

# Top header
st.title("🎫 SWRC Ticketing Request")
st.write(
    """ 
    Please submit a request for any SWRC task.  Job requests will be executed based on FIFO flow.
    """
)

# Add a ticket section
st.header("➕ Add a New Ticket")

with st.form("add_ticket_form"):
    issue = st.text_area("📝 Describe the issue", placeholder="e.g., VPN not connecting from home")
    priority = st.selectbox("🚦 Priority", ["High", "Medium", "Low"])
    submitted = st.form_submit_button("Submit Ticket")

if submitted:
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    st.success("✅ Ticket submitted successfully!")
    st.write("### Ticket Details")
    st.write(f"**Issue:** {issue}")
    st.write(f"**Priority:** {priority}")
    st.write(f"**Date Submitted:** {today}")
