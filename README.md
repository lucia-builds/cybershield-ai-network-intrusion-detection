# CyberShield AI - Network Intrusion Detection System

CyberShield AI is an ML-based Network Intrusion Detection System built using IBM watsonx.ai AutoAI and Streamlit.

## Problem Statement

The project aims to classify network traffic as normal or malicious/anomalous using machine learning. It helps detect suspicious network activity and supports cybersecurity monitoring.

## Tech Stack

- IBM Cloud Lite
- IBM watsonx.ai AutoAI
- watsonx.ai Runtime
- Python
- Streamlit
- Pandas
- Requests

## Model Details

- Dataset: Network Intrusion Detection Dataset
- Prediction column: class
- Best Model: Snap Decision Tree Classifier
- Accuracy: 0.995
- Output: Normal / Anomaly

## Features

- Upload test CSV file
- Send data to IBM watsonx.ai deployed model
- Display prediction result as normal or anomaly
- Simple Streamlit frontend

## How to Run Locally

1. Install dependencies:

```bash
pip install -r requirements.txt
```
## Deployment in IBM CLOUD:
IBM Cloud Deployment Endpoint:
https://au-syd.ml.cloud.ibm.com/ml/v4/deployments/cybershield_ai/predictions?version=2021-05-01
