import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import seaborn as sns


def show():
    st.title("Time Series Analysis Demonstration")
    st.sidebar.title("Settings")

    # User inputs from the sidebar
    num_periods = st.sidebar.slider("Number of periods:", min_value=50, max_value=500, value=200)
    noise_level = st.sidebar.slider("Noise level:", min_value=0.0, max_value=5.0, value=1.0)
    trend_type = st.sidebar.selectbox("Trend type:", ["None", "Linear", "Exponential"])
    seasonality_type = st.sidebar.selectbox("Seasonality type:", ["None", "Additive", "Multiplicative"])
    seasonality_period = st.sidebar.slider("Seasonality period:", min_value=2, max_value=50, value=12)

    # Generate time series data
    np.random.seed(42)
    time = np.arange(num_periods)
    noise = np.random.normal(scale=noise_level, size=num_periods)

    if trend_type == "None":
        trend = np.zeros(num_periods)
    elif trend_type == "Linear":
        trend = time * 0.1
    elif trend_type == "Exponential":
        trend = np.exp(time * 0.01)

    if seasonality_type == "None":
        seasonality = np.zeros(num_periods)
    else:
        seasonality = 10 * np.sin(2 * np.pi * time / seasonality_period)
        if seasonality_type == "Multiplicative":
            seasonality = 1 + seasonality / 100

    if seasonality_type == "None":
        data = trend + noise
    else:
        if seasonality_type == "Additive":
            data = trend + seasonality + noise
        elif seasonality_type == "Multiplicative":
            data = trend * seasonality + noise

    time_series = pd.Series(data, index=pd.date_range(start='1/1/2000', periods=num_periods, freq='M'))

    # Decompose time series
    if seasonality_type != "None":
        decomposition = seasonal_decompose(time_series, model=seasonality_type.lower(), period=seasonality_period)
        trend_component = decomposition.trend
        seasonal_component = decomposition.seasonal
        residual_component = decomposition.resid
    else:
        trend_component = None
        seasonal_component = None
        residual_component = None

    # Plotting
    fig, ax = plt.subplots(4, 1, figsize=(10, 18))
    time_series.plot(ax=ax[0], title="Original Time Series", color='blue')
    ax[0].set_ylabel("Value")

    if trend_component is not None:
        trend_component.plot(ax=ax[1], title="Trend Component", color='green')
        ax[1].set_ylabel("Value")

    if seasonal_component is not None:
        seasonal_component.plot(ax=ax[2], title="Seasonal Component", color='red')
        ax[2].set_ylabel("Value")

    if residual_component is not None:
        residual_component.plot(ax=ax[3], title="Residual Component", color='orange')
        ax[3].set_ylabel("Value")

    st.pyplot(fig)

    # Forecasting
    st.header("Forecasting")
    forecast_periods = st.slider("Forecast periods:", min_value=10, max_value=100, value=24)
    model = ExponentialSmoothing(time_series, trend="add", seasonal=seasonality_type.lower(),
                                 seasonal_periods=seasonality_period)
    fit = model.fit()
    forecast = fit.forecast(forecast_periods)

    # Plot forecasting
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    time_series.plot(ax=ax2, label='Observed', color='blue')
    forecast.plot(ax=ax2, label='Forecast', color='red')
    ax2.fill_between(
        forecast.index,
        fit.conf_int(alpha=0.05)["lower time_series"],
        fit.conf_int(alpha=0.05)["upper time_series"],
        color='pink',
        alpha=0.3
    )
    ax2.set_title("Forecasting with Exponential Smoothing")
    ax2.set_ylabel("Value")
    ax2.legend()

    st.pyplot(fig2)

    # Display model summary
    st.write(f"Model Summary:\n{fit.summary()}")
