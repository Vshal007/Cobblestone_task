import streamlit as st
import numpy as np
import pandas as pd
import time
import random
import matplotlib.pyplot as plt
from generate import generate_stock_data
from detect import detect_anomalies


def introduce_random_drift(time, drift_magnitude):
    return time * np.random.uniform(0.005, 0.02) * drift_magnitude

# Streamlit App to display real-time stock data
def main():
    st.title('Real-Time Stock Data with Concept Drift and Anomalies')

    # Generate initial stock data
    stock_data = generate_stock_data(num_points=200)
    stock_data = detect_anomalies(stock_data)
    
    plot_container = st.empty()  # Empty container to update plot

    # Simulate streaming stock data (new data point every second)
    #new_point = 200
    drift_magnitude = 0
    for new_point in range(200,1000):
        # Introduce concept drift at random intervals
        if random.randint(1, 20) == 1:  # Randomly introduce concept drift
            drift_magnitude += np.random.uniform(-1.0, 1.0)
            st.write(f"Concept drift introduced at point {new_point}, drift magnitude: {drift_magnitude:.2f}")
        
        # Generate next data point with drift, seasonality, and noise
        seasonal_component = np.sin(2 * np.pi * new_point / 50)
        noise = 0.1 * np.random.randn()
        drift = introduce_random_drift(new_point, drift_magnitude)
        new_price = 100 + seasonal_component + drift + noise
        
        # Append new data point
        new_row = pd.DataFrame({'Time': [new_point], 'Price': [new_price]})
        stock_data = pd.concat([stock_data, new_row], ignore_index=True)

        # Remove the first data point to maintain a sliding window of points
        stock_data = stock_data.iloc[1:].reset_index(drop=True)
        
        # Detect anomalies on updated data
        stock_data = detect_anomalies(stock_data)
        
        # Plot the data
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(stock_data['Time'], stock_data['Price'], label='Stock Price', color='blue')
        
        # Mark anomalies in red
        anomalies = stock_data[stock_data['Anomaly'] == True]
        ax.scatter(anomalies['Time'], anomalies['Price'], color='red', label='Anomalies')
        
        ax.set_title('Real-Time Stock Price with Concept Drift and Anomalies')
        ax.set_xlabel('Time')
        ax.set_ylabel('Price')
        ax.legend()
        #new_point += 1
        
        # Update the plot in Streamlit
        plot_container.pyplot(fig)
        
        plt.close(fig)
        # Wait for a random interval before the next update (simulating unpredictable real-time data streams)
        time.sleep(1)
        

if __name__ == "__main__":
    main()
