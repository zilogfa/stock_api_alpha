# Stock Data Visualization App

## Overview
This application provides a platform for real-time visualization and analysis of stock market data. Users can enter a stock symbol to view various charts and statistics, offering insights into stock performance and market trends.

## Features
- **Real-Time Data Visualization**: Generates multiple charts to visualize stock data, including closing prices, trading volume, and more.
- **Interactive User Interface**: Users can input any stock symbol to retrieve and visualize relevant data.
- **Statistical Analysis**: Displays key statistics like mean, max, min, and standard deviation for the selected stock.

## Technologies Used
- **Backend**: Python, Flask
  - **Data Fetching**: Requests library to retrieve data from the Alpha Vantage API.
  - **Data Processing**: Pandas for data manipulation and analysis.
  - **Data Visualization**: Matplotlib for generating various stock data charts.
- **Frontend**:
  - **HTML/CSS**: For structuring and styling the web interface.
  - **JavaScript/jQuery**: For handling AJAX requests and dynamically updating the web page.
- **API**: Alpha Vantage for stock market data.

## Installation and Setup
1. Clone the repository.
2. Install required Python packages: `Flask`, `pandas`, `matplotlib`, `requests`.
3. Insert your Alpha Vantage API key in `api_key.txt`.
4. Run the Flask application: `python app.py`.
5. Access the web interface via a web browser at `http://127.0.0.1:5000/`.

## Usage
- Enter a stock symbol in the input field.
- Click "Get Data" to retrieve and display the stock data and visualizations.

## Limitations
- The application uses a free API with a limit of 25 requests per day.
- It is intended for portfolio and demonstration purposes, not for commercial or personal investment decisions.

## Developer
Developed by Ali Jafarbeglou. Visit [www.alijafarbeglou.com](https://www.alijafarbeglou.com) to learn more about my work.
