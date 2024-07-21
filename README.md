# Stock Prediction App

## Disclaimer

**IMPORTANT: This application is for educational and demonstration purposes only.**

This stock prediction app is not intended for use in real-world trading or investment decisions. The predictions and analyses provided by this tool are based on historical data and machine learning models, which have inherent limitations and may not accurately reflect future market conditions. Users should not rely on this application for making financial decisions. Always consult with qualified financial advisors and conduct thorough research before making any investment choices.

## Overview

This Stock Prediction App is a comprehensive tool for predicting stock prices using machine learning techniques. It features a user-friendly web interface built with Streamlit, backend prediction models using TensorFlow, and a robust data pipeline for real-time stock data retrieval.

## Features

- User Authentication: Secure login and registration system
- Stock Selection: Choose from a variety of stock symbols
- Real-time Data: Fetch up-to-date stock data using yfinance
- Advanced Predictions: Utilize GAN (Generative Adversarial Network) models for stock price forecasting
- Interactive Visualizations: Display stock data and predictions using Plotly
- Technical Indicators: Show RSI, Moving Averages, and Volume charts
- Automated Training: Scheduled model retraining for improved accuracy

## Project Structure

- `app.py`: Main Streamlit application file
- `data_collection.py`: Functions for fetching and preprocessing stock data
- `database.py`: User authentication and database management
- `model.py`: GAN model architecture and training functions
- `prediction.py`: Functions for making stock price predictions
- `scheduler.py`: Automated model training scheduler
- `stock_predictor.py`: Core class for managing stock predictions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/VRASHABHPATIL/stock-prediction-app.git
```
```bash
cd stock-prediction-app
```
2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up the MySQL database:
- Install MySQL if not already installed
- Create a new database for the application
- Update the connection details in `database.py`

4. Run the Streamlit app:
```bash
streamlit run app.py
```

## Database Setup

This application uses MySQL for user management. To set up the database:

1. Install MySQL if not already installed on your system.

2. Create a new database for the application:
```sql
CREATE DATABASE stock_prediction_app;
```
3.The `database.py` file contains the logic to create the necessary tables. It uses the following connection parameters:
```python
db = mysql.connector.connect(
    host="localhost",
    user="your_user_name or root",
    password=your_password",
    database="stock_prediction_app"
)
```
4. Update these parameters in `database.py` to match your MySQL setup.
5. The `create_user_table()` function in `database.py` will automatically create the required users table when the application is run for the first time.
6. Ensure that the MySQL server is running before starting the application.


## Usage

1. Register for a new account or login with existing credentials
2. Select a stock symbol from the dropdown menu
3. Click "Predict" to generate forecasts and view analysis
4. Explore various charts and metrics provided for the selected stock

## Screenshots

### Login Page
<img src="https://github.com/user-attachments/assets/0945d063-91d5-43c3-8e90-a1062496e945" width=700 height=500/>


### Main Dashboard
<img src="https://github.com/user-attachments/assets/e53bffdf-364d-45ec-9fc0-7a2aee83ef26" width=700 height=500/>


### Stock Prediction Chart
<img src="https://github.com/user-attachments/assets/fd6e8c9d-2ff3-41b5-bb3f-161124a2dbed" width=700 height=500/>



### Technical Indicators
<img src="https://github.com/user-attachments/assets/e894f9ea-377b-44f9-9db9-16a4361a8ac9" width=700 height=500/>


## Technical Details


### Machine Learning Model

- Architecture: Generative Adversarial Network (GAN)
- Implementation: TensorFlow/Keras
- Input: Sequence of historical stock prices and returns
- Output: Predicted future stock prices

### Data Pipeline

- Data Source: Yahoo Finance (via yfinance library)
- Preprocessing: MinMaxScaler for normalization
- Sequence Creation: Time series data converted to supervised learning format

### Web Interface

- Framework: Streamlit
- Visualizations: Plotly for interactive charts
- Styling: Custom CSS for enhanced user experience

### Backend

- Database: MySQL for user management
- Authentication: Bcrypt for password hashing
- Scheduling: Python's `schedule` library for automated model training

## Automated Model Training

The `scheduler.py` script runs continuously, retraining all models every 24 hours to ensure predictions are based on the most recent data.

## Future Improvements

- Implement more advanced feature engineering
- Add support for cryptocurrency predictions
- Enhance the user interface with more customization options
- Integrate sentiment analysis from news and social media

## License

[MIT License](LICENSE)


`Feel free to contribute to this project by submitting pull requests or reporting issues!`
