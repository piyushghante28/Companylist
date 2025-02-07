# import streamlit as st
# import gspread
# from google.oauth2.service_account import Credentials
# import pandas as pd

# # Set the page configuration with a favicon
# st.set_page_config(
#     page_title="Company Schedule",  # Title displayed in the browser tab
#     page_icon="office-building.png",  # Path to your favicon file
# )

# # Set up credentials and authorize gspread
# def authenticate_gsheet():
#     # Load credentials from Streamlit secrets
#     credentials_info = st.secrets["gcp_credentials"]

#     # Scopes for the API
#     scopes = ["https://www.googleapis.com/auth/spreadsheets", 
#               "https://www.googleapis.com/auth/drive"]

#     # Create credentials object
#     credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)
    
#     # Authorize the gspread client
#     client = gspread.authorize(credentials)

#     # Open the Google Sheet
#     sheet = client.open("CompanyHistory").sheet1  # Access the first sheet of the Google Sheet

#     return sheet

# # Load data from the Google Sheet
# def load_data(sheet):
#     data = sheet.get_all_records()
#     return pd.DataFrame(data)

# # Update the Google Sheet with the new data
# def update_data(sheet, df):
#     # Clear the existing data
#     sheet.clear()
#     # Update the sheet with new data from the DataFrame
#     sheet.update([df.columns.values.tolist()] + df.values.tolist())

# # Main Streamlit app function
# def main():
#     st.title("DO TO LIST")

#     # Authenticate and load the sheet
#     sheet = authenticate_gsheet()

#     # Load data from the sheet
#     df = load_data(sheet)

#     # Allow editing of the data
#     edited_df = st.data_editor(df, key='data_editor')  # Ensure a unique key for the editor

#     # Button to save the changes to Google Sheets
#     if st.button("Save Changes"):
#         # Save only if changes were made
#         if not edited_df.equals(df):
#             update_data(sheet, edited_df)
#             st.success("Changes saved ! ALL THE BEST ")
#         else:
#             st.info("No changes were made.")

# if __name__ == "__main__":
#     main()

# # import streamlit as st
# # import gspread
# # from google.oauth2.service_account import Credentials
# # import pandas as pd

# # # Set page configuration with a title and icon
# # st.set_page_config(page_title="Company Schedule", page_icon="📅")

# # # Function to authenticate and connect to Google Sheets
# # @st.cache_resource(show_spinner="Connecting to Google Sheets...")
# # def authenticate_gsheet():
# #     try:
# #         credentials_info = st.secrets["gcp_credentials"]
# #         scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
# #         credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)
# #         client = gspread.authorize(credentials)
# #         sheet = client.open("CompanyHistory").sheet1  # Access the first sheet
# #         return sheet
# #     except Exception as e:
# #         st.error(f"Failed to connect to Google Sheets: {e}")
# #         return None

# # # Function to load data from the Google Sheet
# # def load_data(sheet):
# #     try:
# #         data = sheet.get_all_records()
# #         return pd.DataFrame(data) if data else pd.DataFrame(columns=["Column1", "Column2"])  # Ensure a valid DataFrame
# #     except Exception as e:
# #         st.error(f"Error loading data: {e}")
# #         return pd.DataFrame()

# # # Function to update Google Sheet with edited data
# # def update_data(sheet, df):
# #     try:
# #         sheet.clear()
# #         sheet.update([df.columns.values.tolist()] + df.values.tolist())
# #         st.success("✅ Changes saved successfully!")
# #     except Exception as e:
# #         st.error(f"Error updating data: {e}")

# # # Main Streamlit app function
# # def main():
# #     st.title("📊 Piyush's Company Schedule")

# #     sheet = authenticate_gsheet()
# #     if not sheet:
# #         return  # Stop execution if sheet authentication fails

# #     df = load_data(sheet)
    
# #     # Editable table
# #     edited_df = st.data_editor(df, key="data_editor", num_rows="dynamic")

# #     # Save changes button
# #     if st.button("💾 Save Changes"):
# #         if not edited_df.equals(df):
# #             update_data(sheet, edited_df)
# #         else:
# #             st.info("No changes detected.")

# # if __name__ == "__main__":
# #     main()

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Company Schedule", page_icon="📅")

# Authenticate and connect to Google Sheets
@st.cache_resource(show_spinner="Connecting to Google Sheets...")
def authenticate_gsheet():
    try:
        credentials_info = st.secrets["gcp_credentials"]
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)
        client = gspread.authorize(credentials)
        sheet = client.open("CompanyHistory").sheet1  # Access the first sheet
        return sheet
    except Exception as e:
        st.error(f"❌ Failed to connect to Google Sheets: {e}")
        return None

# Fetch data dynamically
def load_data(sheet):
    try:
        raw_data = sheet.get_all_values()  # Fetches all data including headers
        if not raw_data:
            return pd.DataFrame()  # Return empty DataFrame if no data
        df = pd.DataFrame(raw_data[1:], columns=raw_data[0])  # Set first row as headers
        return df
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return pd.DataFrame()

# Function to update Google Sheets
def update_data(sheet, df):
    try:
        sheet.clear()
        sheet.update([df.columns.tolist()] + df.values.tolist())  # Preserve headers
        st.success("✅ Changes saved successfully!")
    except Exception as e:
        st.error(f"❌ Error updating data: {e}")

# Main Streamlit app function
def main():
    st.title("📊 Piyush's Schedule")

    sheet = authenticate_gsheet()
    if not sheet:
        return  # Stop execution if authentication fails

    df = load_data(sheet)
    
    # Ensure at least one column exists
    if df.empty:
        df = pd.DataFrame(columns=["Column1"])  # Placeholder for new data

    # Editable table (allows dynamic row & column additions)
    edited_df = st.data_editor(df, key="data_editor", num_rows="dynamic")

    # Save changes button
    if st.button("💾 Save Changes"):
        if not edited_df.equals(df):
            update_data(sheet, edited_df)
        else:
            st.info("ℹ No changes detected.")

if __name__ == "__main__":
    main()


