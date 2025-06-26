import streamlit as st
import sqlite3
import datetime
import pandas as pd

# Set up SQLite connection
conn = sqlite3.connect("tickets.db", check_same_thread=False)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS Tickets (
    TicketID INTEGER PRIMARY KEY AUTOINCREMENT,
    Requestor TEXT,
    DateRequested TEXT,
    Product TEXT,
    Priority TEXT,
    RequestType TEXT,
    Description TEXT
)
""")
conn.commit()

# Streamlit UI
st.set_page_config(page_title="SWRC Ticketing System", page_icon="🎫", layout="wide")
st.title("🎫 SWRC Ticketing Request")
st.write("Submit a request for any SWRC task. Tickets are processed FIFO.")

st.header("➕ Add a New Ticket")

with st.form("add_ticket_form"):
    requestor = st.text_input("👤 Requestor Name")
    product = st.selectbox("📦 Product", ["SSD", "Module", "Component"])
    priority = st.selectbox("🚦 Priority", ["P1 - High Priority", "P2 - Medium Priority", "P3 - Low Priority"])
    request_type = st.selectbox("📄 Type of Request", ["Scrap Request", "Sampling", "Lot Transfer", "Shipment"])
    description = st.text_area("📝 Job Request Description")
    submitted = st.form_submit_button("Submit Ticket")

if submitted:
    date_requested = datetime.datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        INSERT INTO Tickets (Requestor, DateRequested, Product, Priority, RequestType, Description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (requestor, date_requested, product, priority, request_type, description))
    conn.commit()
    st.success("✅ Ticket submitted successfully!")

# Display all tickets
st.header("📋 Submitted Tickets")
tickets_df = pd.read_sql_query("SELECT * FROM Tickets ORDER BY TicketID DESC", conn)
st.dataframe(tickets_df, use_container_width=True, hide_index=True)
