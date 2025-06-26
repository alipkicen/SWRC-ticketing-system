import streamlit as st
import pyodbc
import datetime

# Set page layout
st.set_page_config(page_title="SWRC Ticketing System", page_icon="🎫", layout="wide")

# Function to insert ticket into SQL Server
def insert_ticket(requestor, product, priority, request_type, description):
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=ITLOAN197-LAP\SQLEXPRESS;"
            "DATABASE=TicketingSystem;"
            "Trusted_Connection=yes;"
        )
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Tickets (Requestor, DateRequested, Product, Priority, RequestType, Description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            requestor,
            datetime.datetime.now().date(),
            product,
            priority,
            request_type,
            description
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "✅ Ticket submitted successfully to SQL Server."
    except Exception as e:
        return False, f"❌ Error: {e}"

# UI
st.title("🎫 SWRC Ticketing Request")
st.write("Please submit a request for any SWRC task. Job requests will be executed based on FIFO flow.")

st.header("➕ Add a New Ticket")

with st.form("add_ticket_form"):
    requestor = st.text_input("👤 Requestor Name")
    product = st.selectbox("📦 Product", ["SSD", "Module", "Component"])
    priority = st.selectbox("🚦 Priority", ["P1 - High Priority", "P2 - Medium Priority", "P3 - Low Priority"])
    request_type = st.selectbox("📄 Type of Request", ["Scrap Request", "Sampling", "Lot Transfer", "Shipment"])
    description = st.text_area("📝 Job Request Description")
    submitted = st.form_submit_button("Submit Ticket")

if submitted:
    success, message = insert_ticket(requestor, product, priority, request_type, description)
    if success:
        st.success(message)
        st.write("### Ticket Details")
        st.write({
            "Requestor": requestor,
            "Date Requested": datetime.datetime.now().strftime("%Y-%m-%d"),
            "Product": product,
            "Priority": priority,
            "Request Type": request_type,
            "Description": description
        })
    else:
        st.error(message)
