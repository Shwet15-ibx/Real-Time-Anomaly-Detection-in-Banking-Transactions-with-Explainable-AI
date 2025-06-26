import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from pydantic import SecretStr

load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')

if groq_api_key:
    llm = ChatGroq(
        model="llama3-8b-8192",  # or another supported model
        api_key=SecretStr(groq_api_key),
        temperature=0.2
    )
else:
    llm = ChatGroq(
        model="llama3-8b-8192",
        temperature=0.2
    )

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI assistant that explains why a banking transaction was flagged as anomalous."),
    ("human", "Transaction details: Amount: {amount}, Predicted: {predicted}, Location: {location}, Merchant: {merchant}, Deviation: {deviation}, Time: {timestamp}. Explain in natural language why this transaction might be suspicious.")
])

def explain_anomaly(anomaly_data):
    input_vars = {
        "amount": anomaly_data['transaction']['amount'],
        "predicted": anomaly_data['predicted'],
        "location": anomaly_data['transaction']['location'],
        "merchant": anomaly_data['transaction']['merchant'],
        "deviation": anomaly_data['deviation'],
        "timestamp": anomaly_data['transaction']['time']
    }
    chain = prompt | llm
    response = chain.invoke(input_vars)
    return response.content

# Example usage
if __name__ == '__main__':
    sample = {
        'transaction': {'amount': 1000, 'location': 'Germany', 'merchant': 'Amazon', 'time': '2024-06-01 03:00:00'},
        'predicted': 40.0,
        'deviation': 960.0
    }
    print(explain_anomaly(sample)) 