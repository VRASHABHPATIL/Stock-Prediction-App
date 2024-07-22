import streamlit as st
import base64
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from stock_predictor import StockPredictor
from database import register_user, verify_user, create_user_table

def plot_stock_data(data, predictions):
    fig = go.Figure()

    # Historical data
    fig.add_trace(go.Scatter(
        x=data.index, 
        y=data['Close'], 
        name='Historical Close', 
        line=dict(color='blue')
    ))

    # Prediction
    prediction_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=4), periods=3)
    all_dates = data.index.tolist() + prediction_dates.tolist()
    all_values = data['Close'].tolist() + predictions[:3]

    fig.add_trace(go.Scatter(
        x=all_dates,
        y=all_values,
        name='Price',
        line=dict(color='blue'),
        showlegend=False
    ))

    # Add markers for predictions
    fig.add_trace(go.Scatter(
        x=prediction_dates, 
        y=predictions[:3], 
        name='3-Day Prediction', 
        mode='markers',
        marker=dict(color='red', size=10)
    ))

    fig.update_layout(
        title='Stock Price Prediction (3-Day Forecast)',
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_dark',
        hovermode='x'
    )

    return fig

def plot_candlestick(data):
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'])])
    fig.update_layout(title='Candlestick Chart (Last 30 Days)', xaxis_title='Date', yaxis_title='Price', template='plotly_dark')
    return fig

def plot_volume(data):
    fig = px.bar(data.last('30D'), x=data.last('30D').index, y='Volume', title='Trading Volume (Last 30 Days)')
    fig.update_layout(template='plotly_dark')
    return fig

def calculate_rsi(data, periods=14):
    close_delta = data['Close'].diff()
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
    ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
    rsi = ma_up / ma_down
    rsi = 100 - (100/(1 + rsi))
    return rsi

def plot_rsi(data):
    rsi = calculate_rsi(data.last('90D'))
    fig = go.Figure(data=go.Scatter(x=rsi.index, y=rsi, mode='lines'))
    fig.add_hline(y=70, line_dash="dash", line_color="red")
    fig.add_hline(y=30, line_dash="dash", line_color="green")
    fig.update_layout(title='Relative Strength Index (RSI)', xaxis_title='Date', yaxis_title='RSI', template='plotly_dark')
    return fig

def plot_moving_averages(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.last('90D').index, y=data.last('90D')['Close'], name='Close Price'))
    fig.add_trace(go.Scatter(x=data.last('90D').index, y=data.last('90D')['Close'].rolling(window=20).mean(), name='20-day MA'))
    fig.add_trace(go.Scatter(x=data.last('90D').index, y=data.last('90D')['Close'].rolling(window=50).mean(), name='50-day MA'))
    fig.update_layout(title='Moving Averages (Last 90 Days)', template='plotly_dark')
    return fig

def display_stock_details(data):
    # Get the last 30 trading days of data
    last_month_data = data.last('30D')
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Latest Close", f"₹{data['Close'].iloc[-1]:.2f}")
    with col2:
        st.metric("Today's High", f"₹{data['High'].iloc[-1]:.2f}")
    with col3:
        st.metric("Today's Low", f"₹{data['Low'].iloc[-1]:.2f}")
    with col4:
        st.metric("Today's Volume", f"{data['Volume'].iloc[-1]:,.0f}")

    st.subheader("30-Day Statistics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("30-Day High", f"₹{last_month_data['High'].max():.2f}")
    with col2:
        st.metric("30-Day Low", f"₹{last_month_data['Low'].min():.2f}")
    with col3:
        st.metric("30-Day Avg Close", f"₹{last_month_data['Close'].mean():.2f}")
    with col4:
        st.metric("30-Day Avg Volume", f"{last_month_data['Volume'].mean():,.0f}")


def add_footer():
    st.info('Note: This prediction is for educational purposes only. Do not use it for actual trading decisions.', icon="ℹ️")
    st.markdown("""
        <footer style='text-align: center; padding: 20px; color: white;'>
            &copy; 2024 All rights reserved.
        </footer>
    """, unsafe_allow_html=True)

def login_page():
    st.subheader("Login")
    col1, col2, col3 = st.columns([1, 2, 1])  # Create three columns
    with col2:  # Center the content in the middle column
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if verify_user(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")
    add_footer()

def register_page():
    st.subheader("Register")
    col1, col2, col3 = st.columns([1, 2, 1])  # Create three columns
    with col2:  # Center the content in the middle column
        new_username = st.text_input("Choose a username")
        new_password = st.text_input("Choose a password", type="password")
        if st.button("Register"):
            if register_user(new_username, new_password):
                st.success("Registration successful. You can now log in.")
            else:
                st.error("Username already exists. Please choose a different one.")
    add_footer()
def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.experimental_rerun()



def add_animated_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
        @keyframes backgroundAnimation {{
            0% {{ background-position: 0% 0%; }}
            50% {{ background-position: 100% 100%; }}
            100% {{ background-position: 0% 0%; }}
        }}
        .stApp {{
            background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
            background-size: cover;
            background-position: center;
            animation: backgroundAnimation 10s ease infinite;  /* Adjust duration and ease as needed */
            height: 100vh;  /* Ensures full viewport height */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )



    
def run_streamlit_app():
    create_user_table()
    st.set_page_config(page_title="Stock Prediction App", layout="wide")
    add_animated_bg_from_local('background.jpg')
    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        tab1, tab2 = st.tabs(["Login", "Register"])
        with tab1:
            login_page()
        with tab2:
            register_page()
    else:
        st.title('📈 Stock Prediction App')
        st.sidebar.text(f"Logged in as: {st.session_state['username']}")
        if st.sidebar.button("Logout"):
            logout()
        
        predictor = StockPredictor()
        predictor.load_models()
        
        symbol = st.selectbox('Select Stock Symbol:', predictor.symbols)
        
        if st.button('Predict', key='predict_button'):
            with st.spinner('Fetching data and making prediction...'):
                predictions, data = predictor.predict_stock(symbol, days=15)
            
            st.success('Prediction complete!')
            
            st.plotly_chart(plot_stock_data(data, predictions), use_container_width=True)
            
            st.subheader('Stock Details')
            display_stock_details(data)
            
            st.plotly_chart(plot_candlestick(data.last('30D')), use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(plot_volume(data), use_container_width=True)
            with col2:
                st.plotly_chart(plot_rsi(data), use_container_width=True)
            
            st.plotly_chart(plot_moving_averages(data), use_container_width=True)
            
            st.subheader('15-Day Prediction')
            prediction_df = pd.DataFrame({
                'Date': pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=15),
                'Predicted Close': predictions
            })
            
            styled_df = prediction_df.style.format({
                'Date': lambda x: x.strftime('%Y-%m-%d'),
                'Predicted Close': '₹{:.2f}'.format
            })

            st.dataframe(styled_df, use_container_width=True)
            
            add_footer()

if __name__ == '__main__':
    run_streamlit_app()
