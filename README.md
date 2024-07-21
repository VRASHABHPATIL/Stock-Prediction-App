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
