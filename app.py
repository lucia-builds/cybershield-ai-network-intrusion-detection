import os
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="CyberShield AI",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ CyberShield AI")
st.subheader("ML-Based Network Intrusion Detection System")

st.write(
    "This frontend uses an IBM watsonx.ai deployed AutoAI model to classify "
    "network traffic as Normal or Intrusion."
)

IBM_API_KEY = os.getenv("IBM_API_KEY")
IBM_DEPLOYMENT_URL = os.getenv("IBM_DEPLOYMENT_URL")


def get_ibm_access_token(api_key):
    token_url = "https://iam.cloud.ibm.com/identity/token"

    data = {
        "apikey": api_key,
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
    }

    response = requests.post(token_url, data=data)

    if response.status_code != 200:
        st.error("Failed to generate IBM access token. Check your API key.")
        st.write(response.text)
        st.stop()

    return response.json()["access_token"]


def predict_from_ibm_model(df):
    token = get_ibm_access_token(IBM_API_KEY)

    fields = df.columns.tolist()
    values = df.values.tolist()

    payload = {
        "input_data": [
            {
                "fields": fields,
                "values": values
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    response = requests.post(
        IBM_DEPLOYMENT_URL,
        json=payload,
        headers=headers
    )

    return response


uploaded_file = st.file_uploader("Upload your test CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.write("### Uploaded Data Preview")
    st.dataframe(df.head())

    if "class" in df.columns:
        df = df.drop(columns=["class"])
        st.info("Removed 'class' column because it is the target/output column.")

    st.write("### Data Sent to Model")
    st.dataframe(df.head())

    if st.button("Predict Intrusion"):
        if not IBM_API_KEY:
            st.error("IBM API key not found. Please check your .env file.")
            st.stop()

        if not IBM_DEPLOYMENT_URL:
            st.error("IBM deployment URL not found. Please check your .env file.")
            st.stop()

        with st.spinner("Calling IBM deployed model..."):
            response = predict_from_ibm_model(df)

        st.write("### Prediction Result")

        if response.status_code == 200:
            result = response.json()
            st.success("Prediction completed successfully.")
            st.json(result)

            try:
                predictions = result["predictions"][0]["values"]
                output_df = pd.DataFrame(predictions)
                output_df.columns = ["Prediction", "Probability"]
                st.write("### Simplified Prediction Output")
                st.dataframe(output_df)
            except Exception:
                st.warning("Prediction received, but output format is different.")
        else:
            st.error("Prediction failed.")
            st.write("Status code:", response.status_code)
            st.write(response.text)
else:
    st.info("Please upload your test.csv file to start prediction.")