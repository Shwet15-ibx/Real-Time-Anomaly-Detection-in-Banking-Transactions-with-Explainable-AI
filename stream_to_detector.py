import asyncio
from stream_simulator import TransactionStreamSimulator
from detection.kalman_detector import TransactionAnomalyDetector

async def process_and_print(txn):
    result = detector.process_transaction(txn)
    print(f"Transaction: {txn}\nPrediction: {result['predicted']:.2f} | Deviation: {result['deviation']:.2f} | Anomaly: {result['is_anomaly']}\n")

if __name__ == '__main__':
    detector = TransactionAnomalyDetector()
    simulator = TransactionStreamSimulator(anomaly_rate=0.1)
    asyncio.run(simulator.stream(process_and_print, interval=0.5, total=20)) 