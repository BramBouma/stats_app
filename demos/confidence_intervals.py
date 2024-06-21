import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, t

def show():
    st.title("Confidence Intervals Demonstration")
    st.sidebar.title("Settings")

    # User inputs from the sidebar
    dist_type = st.sidebar.selectbox("Choose the original distribution:", ("Normal", "Exponential"))
    sample_size = st.sidebar.slider("Sample size (n):", min_value=1, max_value=1000, value=30)
    confidence_level = st.sidebar.slider("Confidence level (%):", min_value=80, max_value=99, value=95)

    # Parameters for the original distribution
    if dist_type == "Normal":
        mean = st.sidebar.number_input("Normal distribution - mean:", value=0.0)
        std_dev = st.sidebar.number_input("Normal distribution - standard deviation:", value=1.0)
    elif dist_type == "Exponential":
        rate = st.sidebar.number_input("Exponential distribution - rate (lambda):", value=1.0)

    # Function to generate the original distribution
    def generate_distribution(dist_type, size):
        if dist_type == "Normal":
            return np.random.normal(mean, std_dev, size)
        elif dist_type == "Exponential":
            return np.random.exponential(1/rate, size)

    # Generate sample data
    data = generate_distribution(dist_type, sample_size)
    sample_mean = np.mean(data)
    sample_std = np.std(data, ddof=1)
    alpha = 1 - confidence_level / 100

    # Calculate confidence interval
    if dist_type == "Normal" and sample_size > 30:
        # Use Z-distribution for large samples
        z_score = norm.ppf(1 - alpha / 2)
        margin_of_error = z_score * (sample_std / np.sqrt(sample_size))
    else:
        # Use t-distribution for small samples
        t_score = t.ppf(1 - alpha / 2, df=sample_size - 1)
        margin_of_error = t_score * (sample_std / np.sqrt(sample_size))

    ci_lower = sample_mean - margin_of_error
    ci_upper = sample_mean + margin_of_error

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(data, bins=30, alpha=0.6, color='g', edgecolor='black')
    ax.axvline(ci_lower, color='r', linestyle='--', label=f'CI Lower: {ci_lower:.2f}')
    ax.axvline(ci_upper, color='r', linestyle='--', label=f'CI Upper: {ci_upper:.2f}')
    ax.axvline(sample_mean, color='b', linestyle='-', label=f'Sample Mean: {sample_mean:.2f}')
    ax.set_title(f"Confidence Interval ({confidence_level}%) for {dist_type} Distribution")
    ax.legend()

    st.pyplot(fig)

    # Display results
    st.write(f"Sample Mean: {sample_mean:.2f}")
    st.write(f"Sample Standard Deviation: {sample_std:.2f}")
    st.write(f"Confidence Interval: [{ci_lower:.2f}, {ci_upper:.2f}]")
