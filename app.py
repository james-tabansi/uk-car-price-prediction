import streamlit as st
import pandas as pd
import requests

st.markdown(
        """
        <style>
        /* Style the sidebar */
        [data-testid="stSidebar"] {
        background-color: rgb(30, 144, 255); /* Light Blue */
            color: black; /* Text color inside the sidebar */
        }
        </style>
        """,
        unsafe_allow_html=True)

# get the data
df = pd.read_csv("data/Cleaned_used_cars_data.csv")

# design side bar
    # mileage
mileage = st.sidebar.text_input(label="Enter Mileage in Miles", value='0')
mileage = int(mileage)

    # registration year
year = st.sidebar.slider(label="Select Length of Registration",
                         min_value=df['Registration_Year'].min(), max_value=df['Registration_Year'].max())

    # fuel_type
fuel_type = st.sidebar.selectbox(label="Select Fuel Type", 
                                 options=df['Fuel type'].unique())

    # body_type
body_type = st.sidebar.selectbox(label="Select Body Type", 
                                 options=df['Body type'].unique())

    # engine
engine = float(st.sidebar.slider(label="Select Engine Volume",
                         min_value=df['Engine'].min(), max_value=df['Engine'].max()))

    # Gearbox
gearbox = st.sidebar.selectbox(label="Select Gearbox Type", 
                                 options=df['Gearbox'].unique())

    # Doors
doors = int(st.sidebar.selectbox(label="Select Number of Doors",
                        options=df['Doors'].unique()))

    # Seats
seats = int(st.sidebar.selectbox(label="Select Number of Seats",
                        options=df['Seats'].unique()))

    # Emission class
emission_class = st.sidebar.selectbox(label="Select Emission Class", 
                                 options=df['Emission Class'].unique())


# Design main page
st.markdown(
    """
    <style>
        .header-container {
            text-align: center;
            font-family: Arial, sans-serif;
            margin-top: 50px;
        }
        .small-text {
            font-size: 1rem;
            font-weight: bold;
            display: block;
        }
        .big-text {
            font-size: 3rem;
            font-weight: bold;
            margin-top: -10px;
        }
    </style>

    <div class="header-container">
        <span class="big-text">Accurate Car Price Predictions at Your Fingertips!</span>
        <span class="small-text">Know Your Car's Worth Before You Sell or Buy! By James</span>
    </div>
    """,
    unsafe_allow_html=True)

# add spacing
st.markdown("<br><br>", unsafe_allow_html=True)
# get the input data
data = pd.DataFrame(
    {
        "Mileage(miles)": [mileage],
        "Registration_Year": [year],
        "Fuel type": [fuel_type],
        "Body type": [body_type],
        "Engine": [engine],
        "Gearbox": [gearbox],
        "Doors": [doors],
        "Seats": [seats],
        "Emission Class": [emission_class]
    }
)

# display the data dynamically
st.write(data)


def makeRequest(data):
    url = "http://127.0.0.1:8000/predStream/"

    # Convert DataFrame to JSON dictionary
    json_data = {"data": data.to_dict(orient="list")}  

    response = requests.post(url, json=json_data)
    
    # return the response
    return response.json()['prediction']


# Custom button styling for the button
button_style = """
        <style>
        div.stButton > button {
            display: block;
            margin: 0 auto;
            font-size: 18px;
            font-weight: bold;
            background-color: rgb(30, 144, 255);
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            transition: 0.3s;
            border: none;
        }
        div.stButton > button:hover {
            background-color: rgb(82, 74, 92);
            transform: scale(1.05);
        }
        </style>
    """
st.markdown(button_style, unsafe_allow_html=True)

# wrap button to the endpoint
if st.button("Predict Car Price"):
    price = makeRequest(data)
    # display the prediction in desired format
    st.markdown(
        f"""
        <div style="text-align: center; font-weight: bold; font-size: 24px;">
            The estimated car price is: ${price:,.2f}
        </div>
        """,
        unsafe_allow_html=True
    )