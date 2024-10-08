import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Set the page configuration with a favicon
st.set_page_config(
    page_title="Company Schedule",  # Title displayed in the browser tab
    page_icon="office-building.png",  # Path to your favicon file
)

# Set up credentials and authorize gspread
def authenticate_gsheet():
    # Load credentials from Streamlit secrets
    credentials_info = st.secrets["gcp_credentials"]

    # Scopes for the API
    scopes = ["https://www.googleapis.com/auth/spreadsheets", 
              "https://www.googleapis.com/auth/drive"]

    # Create credentials object
    credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)
    
    # Authorize the gspread client
    client = gspread.authorize(credentials)

    # Open the Google Sheet
    sheet = client.open("CompanyHistory").sheet1  # Access the first sheet of the Google Sheet

    return sheet

# Load data from the Google Sheet
def load_data(sheet):
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# Update the Google Sheet with the new data
def update_data(sheet, df):
    # Clear the existing data
    sheet.clear()
    # Update the sheet with new data from the DataFrame
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

# Main Streamlit app function
def main():
    st.title("Piyush's Company (VIT, Pune)")

    # Authenticate and load the sheet
    sheet = authenticate_gsheet()

    # Load data from the sheet
    df = load_data(sheet)

    # Allow editing of the data
    edited_df = st.data_editor(df, key='data_editor')  # Ensure a unique key for the editor

    # Button to save the changes to Google Sheets
    if st.button("Save Changes"):
        # Save only if changes were made
        if not edited_df.equals(df):
            update_data(sheet, edited_df)
            st.success("Changes saved ! ALL THE BEST ")
        else:
            st.info("No changes were made.")

if __name__ == "__main__":
    main()


