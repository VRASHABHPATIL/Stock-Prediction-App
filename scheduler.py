import schedule
import time
from datetime import datetime
from stock_predictor import StockPredictor

def train_and_save_models():
    print(f"Training models at {datetime.now()}")
    predictor = StockPredictor()
    predictor.train_all_models()
    print(f"Models trained and saved at {datetime.now()}")

def run_scheduler():
    schedule.every(24).hours.do(train_and_save_models)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    train_and_save_models()  # Train immediately on start
    run_scheduler()
