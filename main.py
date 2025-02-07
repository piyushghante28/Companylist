# # import streamlit as st
# # import gspread
# # from google.oauth2.service_account import Credentials
# # import pandas as pd

# # # Set the page configuration with a favicon
# # st.set_page_config(
# #     page_title="Company Schedule",  # Title displayed in the browser tab
# #     page_icon="office-building.png",  # Path to your favicon file
# # )

# # # Set up credentials and authorize gspread
# # def authenticate_gsheet():
# #     # Load credentials from Streamlit secrets
# #     credentials_info = st.secrets["gcp_credentials"]

# #     # Scopes for the API
# #     scopes = ["https://www.googleapis.com/auth/spreadsheets", 
# #               "https://www.googleapis.com/auth/drive"]

# #     # Create credentials object
# #     credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)
    
# #     # Authorize the gspread client
# #     client = gspread.authorize(credentials)

# #     # Open the Google Sheet
# #     sheet = client.open("CompanyHistory").sheet1  # Access the first sheet of the Google Sheet

# #     return sheet

# # # Load data from the Google Sheet
# # def load_data(sheet):
# #     data = sheet.get_all_records()
# #     return pd.DataFrame(data)

# # # Update the Google Sheet with the new data
# # def update_data(sheet, df):
# #     # Clear the existing data
# #     sheet.clear()
# #     # Update the sheet with new data from the DataFrame
# #     sheet.update([df.columns.values.tolist()] + df.values.tolist())

# # # Main Streamlit app function
# # def main():
# #     st.title("DO TO LIST")

# #     # Authenticate and load the sheet
# #     sheet = authenticate_gsheet()

# #     # Load data from the sheet
# #     df = load_data(sheet)

# #     # Allow editing of the data
# #     edited_df = st.data_editor(df, key='data_editor')  # Ensure a unique key for the editor

# #     # Button to save the changes to Google Sheets
# #     if st.button("Save Changes"):
# #         # Save only if changes were made
# #         if not edited_df.equals(df):
# #             update_data(sheet, edited_df)
# #             st.success("Changes saved ! ALL THE BEST ")
# #         else:
# #             st.info("No changes were made.")

# # if __name__ == "__main__":
# #     main()

# # # import streamlit as st
# # # import gspread
# # # from google.oauth2.service_account import Credentials
# # # import pandas as pd

# # # # Set page configuration with a title and icon
# # # st.set_page_config(page_title="Company Schedule", page_icon="📅")

# # # # Function to authenticate and connect to Google Sheets
# # # @st.cache_resource(show_spinner="Connecting to Google Sheets...")
# # # def authenticate_gsheet():
# # #     try:
# # #         credentials_info = st.secrets["gcp_credentials"]
# # #         scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
# # #         credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)
# # #         client = gspread.authorize(credentials)
# # #         sheet = client.open("CompanyHistory").sheet1  # Access the first sheet
# # #         return sheet
# # #     except Exception as e:
# # #         st.error(f"Failed to connect to Google Sheets: {e}")
# # #         return None

# # # # Function to load data from the Google Sheet
# # # def load_data(sheet):
# # #     try:
# # #         data = sheet.get_all_records()
# # #         return pd.DataFrame(data) if data else pd.DataFrame(columns=["Column1", "Column2"])  # Ensure a valid DataFrame
# # #     except Exception as e:
# # #         st.error(f"Error loading data: {e}")
# # #         return pd.DataFrame()

# # # # Function to update Google Sheet with edited data
# # # def update_data(sheet, df):
# # #     try:
# # #         sheet.clear()
# # #         sheet.update([df.columns.values.tolist()] + df.values.tolist())
# # #         st.success("✅ Changes saved successfully!")
# # #     except Exception as e:
# # #         st.error(f"Error updating data: {e}")

# # # # Main Streamlit app function
# # # def main():
# # #     st.title("📊 Piyush's Company Schedule")

# # #     sheet = authenticate_gsheet()
# # #     if not sheet:
# # #         return  # Stop execution if sheet authentication fails

# # #     df = load_data(sheet)
    
# # #     # Editable table
# # #     edited_df = st.data_editor(df, key="data_editor", num_rows="dynamic")

# # #     # Save changes button
# # #     if st.button("💾 Save Changes"):
# # #         if not edited_df.equals(df):
# # #             update_data(sheet, edited_df)
# # #         else:
# # #             st.info("No changes detected.")

# # # if __name__ == "__main__":
# # #     main()

# import streamlit as st
# import gspread
# from google.oauth2.service_account import Credentials
# import pandas as pd

# # Set page configuration
# st.set_page_config(page_title="Company Schedule", page_icon="📅")

# # Authenticate and connect to Google Sheets
# @st.cache_resource(show_spinner="Connecting to Google Sheets...")
# def authenticate_gsheet():
#     try:
#         credentials_info = st.secrets["gcp_credentials"]
#         scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
#         credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)
#         client = gspread.authorize(credentials)
#         sheet = client.open("CompanyHistory").sheet1  # Access the first sheet
#         return sheet
#     except Exception as e:
#         st.error(f"❌ Failed to connect to Google Sheets: {e}")
#         return None

# # Fetch data dynamically
# def load_data(sheet):
#     try:
#         raw_data = sheet.get_all_values()  # Fetches all data including headers
#         if not raw_data:
#             return pd.DataFrame()  # Return empty DataFrame if no data
#         df = pd.DataFrame(raw_data[1:], columns=raw_data[0])  # Set first row as headers
#         return df
#     except Exception as e:
#         st.error(f"❌ Error loading data: {e}")
#         return pd.DataFrame()

# # Function to update Google Sheets
# def update_data(sheet, df):
#     try:
#         sheet.clear()
#         sheet.update([df.columns.tolist()] + df.values.tolist())  # Preserve headers
#         st.success("✅ Changes saved successfully!")
#     except Exception as e:
#         st.error(f"❌ Error updating data: {e}")

# # Main Streamlit app function
# def main():
#     st.title("📊 Piyush's Schedule")

#     sheet = authenticate_gsheet()
#     if not sheet:
#         return  # Stop execution if authentication fails

#     df = load_data(sheet)
    
#     # Ensure at least one column exists
#     if df.empty:
#         df = pd.DataFrame(columns=["Column1"])  # Placeholder for new data

#     # Editable table (allows dynamic row & column additions)
#     edited_df = st.data_editor(df, key="data_editor", num_rows="dynamic")

#     # Save changes button
#     if st.button("💾 Save Changes"):
#         if not edited_df.equals(df):
#             update_data(sheet, edited_df)
#         else:
#             st.info("ℹ No changes detected.")

# if __name__ == "__main__":
#     main()


import streamlit as st
import pandas as pd
import requests
import base64

# --- Authentication Credentials (Hardcoded) ---
VALID_ID = "idk"  # Change this to your preferred ID
VALID_PASSWORD = "idk"  # Change this to your password

# --- GitHub Repository Details ---
GITHUB_USER = "piyushghante28"  # Your GitHub username
GITHUB_REPO = "Companylist"  # Your GitHub repository name
FILE_PATH = "data.txt"  # Path to the file in GitHub repo
GITHUB_BRANCH = "main"  # Change if using a different branch

# --- GitHub Token from Streamlit Secrets ---
GITHUB_TOKEN = st.secrets["github"]["token"]

# --- GitHub API Headers ---
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# --- Authenticate & Fetch Data from GitHub ---
def fetch_data():
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{FILE_PATH}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        file_data = response.json()
        content = base64.b64decode(file_data["content"]).decode("utf-8")
        return file_data["sha"], pd.read_csv(pd.compat.StringIO(content))
    
    elif response.status_code == 404:
        # File does not exist, create an empty DataFrame
        return None, pd.DataFrame(columns=["Name", "Email", "Phone"])
    
    else:
        st.error(f"❌ Error fetching file: {response.json()}")
        return None, pd.DataFrame()

# --- Update File on GitHub ---
def update_github_file(df, sha):
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{FILE_PATH}"
    
    # Convert DataFrame to CSV string
    csv_content = df.to_csv(index=False)
    encoded_content = base64.b64encode(csv_content.encode("utf-8")).decode("utf-8")

    # Prepare the commit payload
    payload = {
        "message": "Updated data.txt via Streamlit",
        "content": encoded_content,
        "sha": sha,
        "branch": GITHUB_BRANCH
    }

    # Send update request
    response = requests.put(url, json=payload, headers=HEADERS)
    
    if response.status_code == 200 or response.status_code == 201:
        st.success("✅ Changes saved & pushed to GitHub!")
    else:
        st.error(f"❌ Error updating file: {response.json()}")

# --- Authentication Function ---
def authenticate_user():
    st.title("🔐 Secure Login")

    user_id = st.text_input("Enter ID:")
    password = st.text_input("Enter Password:", type="password")

    if st.button("🔓 Login"):
        if user_id == VALID_ID and password == VALID_PASSWORD:
            st.session_state["authenticated"] = True
            st.experimental_rerun()
        else:
            st.error("🚫 Invalid credentials! Try again.")

# --- Main Streamlit App ---
def main():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        authenticate_user()
        return

    st.title("📊 Secure Data Storage (GitHub Auto-Update)")

    # Fetch Data from GitHub
    sha, df = fetch_data()

    # Editable table
    edited_df = st.data_editor(df, key="data_editor", num_rows="dynamic")

    if st.button("💾 Save Changes"):
        if not edited_df.equals(df):
            update_github_file(edited_df, sha)
        else:
            st.info("ℹ No changes detected.")

if __name__ == "__main__":
    main()



