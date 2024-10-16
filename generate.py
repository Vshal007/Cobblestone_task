import numpy as np
import pandas as pd

# Generate initial stock data with seasonality, noise, and drift
def generate_stock_data(num_points=1000, seasonality=50, noise_level=0.1, concept_drift_point=500):
    
    # Time series component with seasonality
    time = np.arange(num_points)
    seasonal_component = np.sin(2 * np.pi * time / seasonality)
    
    # Add noise
    noise = noise_level * np.random.randn(num_points)
    
    # Simulate concept drift (change behavior after a certain point)
    drift = np.piecewise(time, [time < concept_drift_point, time >= concept_drift_point],
                         [lambda t: t * 0.005, lambda t: (t - concept_drift_point) * 0.01 + concept_drift_point * 0.005])
    
    # Final stock prices (with drift, seasonality, and noise)
    stock_prices = 100 + seasonal_component + drift + noise
    
    return pd.DataFrame({'Time': time, 'Price': stock_prices})