import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import asyncio
import threading
from streaming.stream_simulator import TransactionStreamSimulator
from detection.kalman_detector import TransactionAnomalyDetector
from explain.explain_anomaly import explain_anomaly

st.set_page_config(page_title="Real-Time Banking Fraud Detection", layout="wide")
st.title("Real-Time Anomaly Detection in Banking Transactions")

# Sidebar for Kalman filter parameters
st.sidebar.header("Admin Tools")
process_var = st.sidebar.slider("Process Variance", 1e-5, 1e-2, 1e-3, step=1e-5)
meas_var = st.sidebar.slider("Measurement Variance", 0.1, 10.0, 1.0, step=0.1)
threshold = st.sidebar.slider("Anomaly Threshold (std dev)", 1.0, 5.0, 3.0, step=0.1)

# State
if 'anomalies' not in st.session_state:
    st.session_state['anomalies'] = []
if 'transactions' not in st.session_state:
    st.session_state['transactions'] = []
if 'feedback' not in st.session_state:
    st.session_state['feedback'] = []

# Detector
anomaly_detector = TransactionAnomalyDetector(threshold=threshold)

# Asyncio event loop in thread for Streamlit
loop = asyncio.new_event_loop()
def run_stream():
    async def handle_txn(txn):
        result = anomaly_detector.process_transaction(txn)
        st.session_state['transactions'].append(txn)
        if result['is_anomaly']:
            explanation = explain_anomaly(result)
            result['explanation'] = explanation
            st.session_state['anomalies'].append(result)
    simulator = TransactionStreamSimulator(anomaly_rate=0.1)
    loop.run_until_complete(simulator.stream(handle_txn, interval=1.0, total=100))

if st.button("Start Streaming"):
    threading.Thread(target=run_stream, daemon=True).start()

# Live transactions
st.subheader("Live Transactions")
st.dataframe(st.session_state['transactions'][-20:])

# Flagged anomalies
st.subheader("Flagged Anomalies")
anomaly_table = [
    {**a['transaction'], 'Predicted': a['predicted'], 'Deviation': a['deviation'], 'Explanation': a.get('explanation', '')}
    for a in st.session_state['anomalies'][-10:]
]
st.dataframe(anomaly_table)

# Feedback
st.subheader("User Feedback")
for idx, anomaly in enumerate(st.session_state['anomalies'][-10:]):
    if st.button(f"Was this anomaly accurate? (Row {idx+1})"):
        st.session_state['feedback'].append({'anomaly': anomaly, 'accurate': True})
        st.success(f"Feedback recorded for anomaly {idx+1}")

st.header("Manual Transaction Prediction")

with st.form("manual_txn_form"):
    amount = st.number_input("Amount", min_value=0.0, value=30.0)
    location = st.selectbox("Location", ["California", "New York", "Texas", "Germany", "India"])
    merchant = st.selectbox("Merchant", ["Amazon", "Walmart", "Target", "BestBuy", "Starbucks"])
    time = st.text_input("Time (YYYY-MM-DD HH:MM:SS)", value="2024-06-01 12:00:00")
    account = st.text_input("Account", value="123456")
    submitted = st.form_submit_button("Predict")

    if submitted:
        txn = {
            "amount": amount,
            "location": location,
            "merchant": merchant,
            "time": time,
            "account": account,
            "is_anomaly": False
        }
        result = anomaly_detector.process_transaction(txn)
        st.write("Prediction:", "Anomaly" if result["is_anomaly"] else "Normal")
        st.write("Predicted Value:", result["predicted"])
        st.write("Deviation:", result["deviation"])
        if result["is_anomaly"]:
            explanation = explain_anomaly(result)
            st.write("Explanation:", explanation) 