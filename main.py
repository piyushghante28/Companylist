import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import json

# Embedded JSON credentials (ensure to replace this with your actual credentials)
JSON_CREDENTIALS = """
{
    "type": "service_account",
  "project_id": "fluent-radar-436616-d7",
  "private_key_id": "108f34fc4a3261e7a395d00b345dfdedd1e9309c",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDJubmMutaqfjlv\nqrbxCzw6CSYFsjPQVcPUNTqW3ujRKQlrfc0yZbXN/f0o3TkaV6X9mJtc0j6IBRDY\nzC5pMiszNbecXbIkI5/w/fL8Ury5xjIfNmNtfOMY+KkjiC+CMEVVTC/9U7uwpkqv\nClPjj4xmO46t/KyJCZKKd83pbIlCsv//9euk/jWWkzfh1sN94013UIjW299jzPvA\nAtaHopf0JBFqAD06jOTpxVlrPNegYTzy8nn8Xjl3HuPqdVSBeIfjBGSGPdxIuvgL\ns80laweJ+9gzm4EhbHo09NuHq1ld9bEi8aR9gn01IEV2SfvkRgdE9N2yFfFZGuK4\nrUXAWeazAgMBAAECggEAKTGDAYj54zEJe5Mp7okz0Eoj+I/OYuHQrpn8D+kPM/8k\nTE4RRBRfDuSp+NlMGuQBIosyVr8cQ9x89zii1ZqIFdoHV6gOg7C+rZC+OOaQYYNm\notcRcL9LBMNqjrX1takzz1pShnG95zHeGGaMgPDEY/APj9oERautwBb89ojScssL\n5lf97sekAEQXtTSIe36E9RRik0z0ccs2bzHAQb/0/BprkjclxaKkGVLv/oWlWYLR\n96IXjE4ptJSjTS6toQ+h6VBYZOOF9RuvMs61+bkpBJjl3NA87aimd0X9oqIRTSzQ\nRFlfrAwxWhCafK0D8Vo5Xwi+DHLd8+VaW73dwdMJGQKBgQDwDzMVth3ptH7T2kxX\n3DIWb1K2/dw8EZXcbmnP2VMNR8m5NtA3pVqHeVnjMMaWUATsBRii3X5iLax45i3Z\nF31anAYTIIDjDXCTNSYxGFvO1nSxxKxPms0xrUrQFu0Vlt9jHauK86ad7oP6fPOc\nfLjWS0jmH5JnXYI5eBVlbX4BLQKBgQDXHuHvCM3DzZJkbOsfScuuNgI51mfzr5H1\n2+UheH9ZeRSC/3gFzCBofwiPZJwEifQ6O9ZzeKuUvi7gbrFdARfe2bmh2TNr9Chb\npZq8bXwgWuMOEZ9V/Lsrr2yV9XbR9P5xWSkGDrEEIcnduXAR40XnXOjVSjpYQKoV\nIvpIu/mzXwKBgBCprW0TYA4pxifkXio3EY73GTG0e0X8Hn/XdibEOfyRABKIGHnU\nU21V4gRgDVi/oyfSzrv3Td94tiEKMSKBe+T/MXjAZ9Hay/ab2NPNkgnQXvc75I39\n+8I3+hppjPlTqJvTomWZtfX+aVDIvYweKCJPxXabuGjOV8yvZiTNLdLdAoGBAMDK\nTpWZAD+Qxrf13SonSsEQaiJHgtYj7N24errqcMdQ+g8EwR4A+LJt1tAbzK9Mq3Jd\nGi5WYP9nCj/dNFszlZ8E5ZalP65qHJk1610fifS9P2vmYzP+0geuqdQjLp+vvzD6\nRQfGtuILHgz2GfgOBSH6ZDhy06MwIL3coQ36WShlAoGBAKeKp/tJEj3rWRqXdGWK\ndDQV1WQWezFhaTKm116bd+mB7ZS2TrTKFR3NvtEBfTYGqR1pr89IpAnonJKdW7Bq\nt+ro6CJ5HOhVvGvXrOrjRGayol2oCyid7BR8EC1HHJBDkunowgy3/c1qA+TY6cvo\nIPROtC/3eRXLiS59f0fkKt0w\n-----END PRIVATE KEY-----\n",
  "client_email": "piyush@fluent-radar-436616-d7.iam.gserviceaccount.com",
  "client_id": "111897587394306164947",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/piyush%40fluent-radar-436616-d7.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
"""

st.set_page_config(
    page_title="Piyush's Company (VIT, Pune)",
    page_icon="office-building.png",
)

# Set up credentials and authorize gspread
def authenticate_gsheet(sheet_name: str):
    # Load credentials from embedded JSON
    credentials_info = json.loads(JSON_CREDENTIALS)
    credentials = Credentials.from_service_account_info(credentials_info)

    # Authorize the gspread client
    client = gspread.authorize(credentials)

    # Open the Google Sheet
    sheet = client.open(sheet_name).sheet1  # Access the first sheet of the Google Sheet

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

    # Google Sheets sheet name
    sheet_name = "CompanyHistory"

    # Authenticate and load the sheet
    sheet = authenticate_gsheet(sheet_name)

    # Load data from the sheet
    df = load_data(sheet)

    # Display the data in Streamlit
    st.subheader("Google Sheet Data")

    # Allow editing of the data
    edited_df = st.data_editor(df)

    # Button to save the changes to Google Sheets
    if st.button("Save Changes"):
        # Save only if changes were made
        if not edited_df.equals(df):
            update_data(sheet, edited_df)
            st.success("Changes saved to Google Sheet!")
        else:
            st.info("No changes were made.")

if __name__ == "__main__":
    main()
