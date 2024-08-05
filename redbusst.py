import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# MySQL connection details
mysql_password = 'Shyam1234@'
encoded_password = quote_plus(mysql_password)
database_name = 'redbus'
mysql_connection_string = f'mysql+pymysql://root:{encoded_password}@localhost:3306/{database_name}'
engine = create_engine(mysql_connection_string)

# Function to load data from SQL database
def load_data():
    query = "SELECT * FROM redbus_data"
    with engine.connect() as connection:
        df = pd.read_sql(query, connection)
    return df

# Load data
redbus_df = load_data()

# Set Streamlit page configuration for wider layout
st.set_page_config(layout="wide")

st.markdown("""
    <style>
    .reportview-container {
        background: white;
    }
    .sidebar .sidebar-content {
        background: white;
    }
    h1 {
        color: #FF6347;  /* Tomato color for the title */
    }
    h2 {
        color: #4682B4;  /* SteelBlue color for the headers */
    }
    </style>
    """, unsafe_allow_html=True)

# Define pages
def home_page():
    st.markdown('<h1>Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit</h1>', unsafe_allow_html=True)

    st.markdown('<h2>Introduction</h2>', unsafe_allow_html=True)
    st.write("""
    This project automates the collection of bus travel data from the Redbus website using Selenium, storing it in a structured SQL database. The goal is to develop an interactive Streamlit application that allows users to filter and analyze this data efficiently. By leveraging web scraping techniques and dynamic filtering capabilities, this project aims to provide valuable insights and tools for enhancing operational efficiency and strategic planning in the transportation industry.
    """)

    st.markdown('<h2>Approach</h2>', unsafe_allow_html=True)
    st.write("""
    **Data Scraping:**
    - Use Selenium to automate the extraction of Redbus data including routes, schedules, prices, and seat availability.

    **Data Storage:**
    - Store the scraped data in a SQL database.

    **Streamlit Application:**
    - Develop a Streamlit application to display and filter the scraped data.
    - Implement various filters such as bustype, route, price range, star rating, availability.

    **Data Analysis/Filtering using Streamlit:**
    - Use SQL queries to retrieve and filter data based on user inputs.
    - Use Streamlit to allow users to interact with and filter the data through the application.
             
    **Results and Insights:**
    - Ensure successful scraping of data for at least 10 Government State Bus Transport and private bus routes.
    - Provide valuable insights into bus travel patterns, pricing strategies, and seat availability.
    - Enhance user experience by offering customized travel options based on data insights.
    """)

def select_bus_page():
    st.markdown('<h1>Select the Bus</h1>', unsafe_allow_html=True)

    # Filters
    st.sidebar.markdown('<h2>Filters</h2>', unsafe_allow_html=True)
    state = st.sidebar.multiselect("Select the State", redbus_df['State'].unique())
    
    # Filter route_name options based on selected state
    if state:
        filtered_routes = redbus_df[redbus_df['State'].isin(state)]['Route_name'].unique()
    else:
        filtered_routes = redbus_df['Route_name'].unique()

    route_name = st.sidebar.multiselect("Select the Route", filtered_routes)
    bustype_category = st.sidebar.multiselect("Select the Bus Type Category", redbus_df['Bustype_Category'].unique())
    price_range = st.sidebar.slider("Bus Fare Range", int(redbus_df['Price'].min()), int(redbus_df['Price'].max()), (int(redbus_df['Price'].min()), int(redbus_df['Price'].max())))
    ratings = st.sidebar.slider("Select the Ratings", float(redbus_df['Ratings'].min()), float(redbus_df['Ratings'].max()), (float(redbus_df['Ratings'].min()), float(redbus_df['Ratings'].max())))
    availability = st.sidebar.slider("Select Seat Availability", int(redbus_df['Seats_Available'].min()), int(redbus_df['Seats_Available'].max()), (int(redbus_df['Seats_Available'].min()), int(redbus_df['Seats_Available'].max())))

    # Apply filters
    filtered_df = redbus_df.copy()
    if state:
        filtered_df = filtered_df[filtered_df['State'].isin(state)]
    if route_name:
        filtered_df = filtered_df[filtered_df['Route_name'].isin(route_name)]
    if bustype_category:
        filtered_df = filtered_df[filtered_df['Bustype_Category'].isin(bustype_category)]
    filtered_df = filtered_df[(filtered_df['Price'] >= price_range[0]) & (filtered_df['Price'] <= price_range[1])]
    filtered_df = filtered_df[(filtered_df['Ratings'] >= ratings[0]) & (filtered_df['Ratings'] <= ratings[1])]
    filtered_df = filtered_df[(filtered_df['Seats_Available'] >= availability[0]) & (filtered_df['Seats_Available'] <= availability[1])]

    # Display filtered data
    st.dataframe(filtered_df)

# Main menu
st.sidebar.title("Main Menu")
menu_options = ["Home", "Select the Bus"]
choice = st.sidebar.selectbox("Choose a page", menu_options)

if choice == "Home":
    home_page()
elif choice == "Select the Bus":
    select_bus_page()

