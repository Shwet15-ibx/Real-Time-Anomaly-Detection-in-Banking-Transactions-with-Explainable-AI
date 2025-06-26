import numpy as np

class KalmanFilter:
    def __init__(self, process_variance=1e-3, measurement_variance=1.0, initial_estimate=30.0):
        self.process_variance = process_variance
        self.measurement_variance = measurement_variance
        self.estimate = initial_estimate
        self.error_estimate = 1.0

    def update(self, measurement):
        # Prediction update
        self.error_estimate += self.process_variance
        # Measurement update
        kalman_gain = self.error_estimate / (self.error_estimate + self.measurement_variance)
        self.estimate = self.estimate + kalman_gain * (measurement - self.estimate)
        self.error_estimate = (1 - kalman_gain) * self.error_estimate
        return self.estimate

    def get_estimate(self):
        return self.estimate

class TransactionAnomalyDetector:
    def __init__(self, threshold=3.0):
        self.kf = KalmanFilter()
        self.threshold = threshold
        self.history = []

    def process_transaction(self, txn):
        amount = txn['amount']
        pred = self.kf.get_estimate()
        self.kf.update(amount)
        deviation = abs(amount - pred)
        anomaly = deviation > self.threshold * np.sqrt(self.kf.error_estimate)
        result = {
            'transaction': txn,
            'predicted': pred,
            'deviation': deviation,
            'is_anomaly': anomaly
        }
        self.history.append(result)
        return result

# Example usage for testing
if __name__ == '__main__':
    detector = TransactionAnomalyDetector()
    test_txns = [
        {'amount': 35}, {'amount': 40}, {'amount': 38}, {'amount': 1200}, {'amount': 36}
    ]
    for txn in test_txns:
        print(detector.process_transaction(txn)) 