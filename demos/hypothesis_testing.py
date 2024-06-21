import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, ttest_1samp, ttest_ind


def show():
    st.title("Hypothesis Testing Demonstration")
    st.sidebar.title("Settings")

    # User inputs from the sidebar
    test_type = st.sidebar.selectbox("Choose the test type:", ("One-Sample t-Test", "Two-Sample t-Test"))
    dist_type = st.sidebar.selectbox("Choose the distribution for sample data:", ("Normal", "Exponential"))
    sample_size = st.sidebar.slider("Sample size (n):", min_value=1, max_value=1000, value=30)
    alpha = st.sidebar.slider("Significance level (alpha):", min_value=0.01, max_value=0.10, value=0.05)

    # Parameters for the original distribution
    if dist_type == "Normal":
        mean = st.sidebar.number_input("Normal distribution - mean:", value=0.0)
        std_dev = st.sidebar.number_input("Normal distribution - standard deviation:", value=1.0)
    elif dist_type == "Exponential":
        rate = st.sidebar.number_input("Exponential distribution - rate (lambda):", value=1.0)

    # Hypothesis parameters
    null_mean = st.sidebar.number_input("Null hypothesis mean:", value=0.0)

    if test_type == "Two-Sample t-Test":
        sample_size2 = st.sidebar.slider("Sample size for second sample (n):", min_value=1, max_value=1000, value=30)
        if dist_type == "Normal":
            mean2 = st.sidebar.number_input("Normal distribution for second sample - mean:", value=0.0)
            std_dev2 = st.sidebar.number_input("Normal distribution for second sample - standard deviation:", value=1.0)
        elif dist_type == "Exponential":
            rate2 = st.sidebar.number_input("Exponential distribution for second sample - rate (lambda):", value=1.0)

    # Function to generate the original distribution
    def generate_distribution(dist_type, size, mean=0, std_dev=1, rate=1):
        if dist_type == "Normal":
            return np.random.normal(mean, std_dev, size)
        elif dist_type == "Exponential":
            return np.random.exponential(1 / rate, size)

    # Generate sample data
    data = generate_distribution(dist_type, sample_size, mean, std_dev, rate)

    # Perform the hypothesis test
    if test_type == "One-Sample t-Test":
        t_stat, p_value = ttest_1samp(data, null_mean)
        test_result = "Reject" if p_value < alpha else "Fail to Reject"
        st.write(f"One-Sample t-Test Results:")
        st.write(f"T-statistic: {t_stat:.4f}")
        st.write(f"P-value: {p_value:.4f}")
        st.write(f"Decision: {test_result} the null hypothesis at alpha = {alpha:.2f}")

        # Plotting
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(data, bins=30, alpha=0.6, color='g', edgecolor='black')
        ax.axvline(null_mean, color='r', linestyle='--', label=f'Null Hypothesis Mean: {null_mean:.2f}')
        ax.axvline(np.mean(data), color='b', linestyle='-', label=f'Sample Mean: {np.mean(data):.2f}')
        ax.set_title(f"One-Sample t-Test for {dist_type} Distribution")
        ax.legend()

    elif test_type == "Two-Sample t-Test":
        data2 = generate_distribution(dist_type, sample_size2, mean2, std_dev2, rate2)
        t_stat, p_value = ttest_ind(data, data2)
        test_result = "Reject" if p_value < alpha else "Fail to Reject"
        st.write(f"Two-Sample t-Test Results:")
        st.write(f"T-statistic: {t_stat:.4f}")
        st.write(f"P-value: {p_value:.4f}")
        st.write(f"Decision: {test_result} the null hypothesis at alpha = {alpha:.2f}")

        # Plotting
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(data, bins=30, alpha=0.6, color='g', edgecolor='black', label='Sample 1')
        ax.hist(data2, bins=30, alpha=0.6, color='b', edgecolor='black', label='Sample 2')
        ax.axvline(np.mean(data), color='g', linestyle='-', label=f'Sample 1 Mean: {np.mean(data):.2f}')
        ax.axvline(np.mean(data2), color='b', linestyle='-', label=f'Sample 2 Mean: {np.mean(data2):.2f}')
        ax.set_title(f"Two-Sample t-Test for {dist_type} Distribution")
        ax.legend()

    st.pyplot(fig)
