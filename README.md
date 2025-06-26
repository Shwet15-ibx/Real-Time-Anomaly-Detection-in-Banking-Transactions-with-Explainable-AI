# Real-Time-Anomaly-Detection-in-Banking-Transactions-with-Explainable-AI
# Real-Time Anomaly Detection in Banking Transactions with Explainable AI

## 🚀 Project Overview
This project is a real-time banking fraud detection system that monitors streaming transactions, detects anomalies using Kalman Filters, and generates natural language explanations for detected anomalies using LangChain + Groq API. The results are presented via an interactive Streamlit dashboard.

## 🎯 Objective
- Detect fraudulent or anomalous banking transactions in real time.
- Provide explainable AI outputs for flagged anomalies.
- Enable user and admin interaction for feedback and model tuning.

## ⚙️ Core Features
- **Real-Time Transaction Stream:**
  - Simulated or user-input streaming of transaction data (amount, time, location, merchant, account).
- **Anomaly Detection with Kalman Filter:**
  - Models expected transaction patterns and flags significant deviations as anomalies.
- **Explainable AI (LangChain + Groq):**
  - Generates human-readable explanations for flagged anomalies.
- **Streamlit Dashboard:**
  - Live visualization of transactions and anomalies.
  - Manual transaction prediction form.
  - Adjustable Kalman filter parameters (admin tools).
  - User feedback collection for model improvement.

## 🧩 Architecture
```
[Transaction Stream/Manual Input] → [Kalman Filter Detector] → [Anomaly Explanation (LangChain+Groq)] → [Streamlit Dashboard]
```
- **streaming/**: Simulates or ingests transaction data.
- **detection/**: Kalman filter-based anomaly detection logic.
- **explain/**: LangChain + Groq integration for explanations.
- **dashboard/**: Streamlit UI for real-time monitoring and interaction.

## 🛠️ Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd banking-fraud-detection
   ```
2. **Install dependencies:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. **Set up environment variables:**
   - Create a `.env` file in the project root with your LangChain and Groq API keys:
     ```env
     GROQ_API_KEY=your_groq_api_key_here
     LANGCHAIN_API_KEY=your_langchain_api_key_here
     ```
4. **Run the Streamlit dashboard:**
   ```bash
   streamlit run dashboard/app.py
   ```
   - The app will be available at the local URL shown in your terminal (e.g., http://localhost:8501).

## 🖥️ Usage
- **Live Streaming:**
  - Click "Start Streaming" to simulate real-time transactions and see live anomaly detection.
- **Manual Prediction:**
  - Use the "Manual Transaction Prediction" form to input custom transactions and get instant predictions and explanations.
- **Admin Tools:**
  - Adjust Kalman filter parameters in the sidebar to tune detection sensitivity.
- **Feedback:**
  - Mark flagged anomalies as accurate/inaccurate to help improve the model.

## 📊 Example Use Case
A user typically spends $20–$50/day in California. Suddenly, a $1,000 transaction is made in Germany at 3 AM. The Kalman filter flags the deviation, and the Groq-powered LLM generates a human-readable explanation, all shown in real time on the dashboard.

## 🧪 Dataset Sources
- [Kaggle Credit Card Fraud Dataset](https://www.kaggle.com/mlg-ulb/creditcardfraud) for offline testing.
- CMS Open Payments data for additional context and enrichment.

## 🧠 Tech Stack
- **Stream Processing:** Python asyncio, Streamlit
- **Anomaly Detection:** Kalman Filter (NumPy/Scikit)
- **LLM Integration:** LangChain + Groq API
- **Frontend:** Streamlit
- **Storage:** (Optional) SQLite/PostgreSQL for feedback loop
