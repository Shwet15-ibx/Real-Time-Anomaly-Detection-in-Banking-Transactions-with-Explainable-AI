import asyncio
import random
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# Transaction fields: amount, time, location, merchant, account, is_anomaly
LOCATIONS = ['California', 'New York', 'Texas', 'Germany', 'India']
MERCHANTS = ['Amazon', 'Walmart', 'Target', 'BestBuy', 'Starbucks']

class TransactionStreamSimulator:
    def __init__(self, base_account='123456', anomaly_rate=0.05):
        self.base_account = base_account
        self.anomaly_rate = anomaly_rate
        self.last_location = 'California'
        self.last_time = datetime.now() - timedelta(days=1)

    def generate_normal_transaction(self):
        amount = round(random.uniform(20, 50), 2)
        location = self.last_location if random.random() > 0.1 else random.choice(LOCATIONS)
        merchant = random.choice(MERCHANTS)
        self.last_time += timedelta(minutes=random.randint(30, 180))
        return {
            'amount': amount,
            'time': self.last_time.strftime('%Y-%m-%d %H:%M:%S'),
            'location': location,
            'merchant': merchant,
            'account': self.base_account,
            'is_anomaly': False
        }

    def generate_anomalous_transaction(self):
        # Large amount, odd hour, new location
        amount = round(random.uniform(500, 2000), 2)
        location = random.choice([loc for loc in LOCATIONS if loc != self.last_location])
        merchant = random.choice(MERCHANTS)
        anomaly_time = self.last_time + timedelta(hours=random.randint(1, 6))
        anomaly_time = anomaly_time.replace(hour=random.choice([2, 3, 4]))
        return {
            'amount': amount,
            'time': anomaly_time.strftime('%Y-%m-%d %H:%M:%S'),
            'location': location,
            'merchant': merchant,
            'account': self.base_account,
            'is_anomaly': True
        }

    async def stream(self, callback, interval=1.0, total=100):
        for _ in range(total):
            if random.random() < self.anomaly_rate:
                txn = self.generate_anomalous_transaction()
            else:
                txn = self.generate_normal_transaction()
            await callback(txn)
            await asyncio.sleep(interval)

# Example usage for testing
if __name__ == '__main__':
    async def print_txn(txn):
        print(txn)
    sim = TransactionStreamSimulator()
    asyncio.run(sim.stream(print_txn, interval=0.5, total=10)) 