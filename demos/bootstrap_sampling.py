import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def show():
    st.title("Bootstrap Sampling Demonstration")
    st.sidebar.title("Settings")

    # User inputs from the sidebar
    dist_type = st.sidebar.selectbox("Choose the distribution:", ("Normal", "Exponential", "Uniform"))
    sample_size = st.sidebar.slider("Sample size (n):", min_value=10, max_value=1000, value=100)
    num_bootstrap_samples = st.sidebar.slider("Number of bootstrap samples:", min_value=100, max_value=5000, value=1000)

    # Parameters for the original distribution
    if dist_type == "Normal":
        mean = st.sidebar.number_input("Mean:", value=0.0)
        std_dev = st.sidebar.number_input("Standard Deviation:", value=1.0)
    elif dist_type == "Exponential":
        rate = st.sidebar.number_input("Rate (lambda):", value=1.0)
    elif dist_type == "Uniform":
        low = st.sidebar.number_input("Lower bound:", value=0.0)
        high = st.sidebar.number_input("Upper bound:", value=1.0)

    # Function to generate the original distribution
    def generate_distribution(dist_type, size):
        if dist_type == "Normal":
            return np.random.normal(mean, std_dev, size)
        elif dist_type == "Exponential":
            return np.random.exponential(1 / rate, size)
        elif dist_type == "Uniform":
            return np.random.uniform(low, high, size)

    # Generate sample data
    original_sample = generate_distribution(dist_type, sample_size)

    # Perform bootstrap sampling
    bootstrap_means = []
    for _ in range(num_bootstrap_samples):
        bootstrap_sample = np.random.choice(original_sample, size=sample_size, replace=True)
        bootstrap_means.append(np.mean(bootstrap_sample))

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(bootstrap_means, bins=30, kde=True, ax=ax, edgecolor='black')
    ax.axvline(np.mean(original_sample), color='r', linestyle='--',
               label=f'Original Sample Mean: {np.mean(original_sample):.2f}')
    ax.axvline(np.mean(bootstrap_means), color='g', linestyle='-',
               label=f'Bootstrap Mean: {np.mean(bootstrap_means):.2f}')
    ax.set_title("Bootstrap Sampling Distribution")
    ax.legend()

    st.pyplot(fig)

    # Display summary statistics
    st.write("Original Sample Summary Statistics:")
    st.write(f"Mean: {np.mean(original_sample):.2f}")
    st.write(f"Standard Deviation: {np.std(original_sample):.2f}")
    st.write("Bootstrap Sample Summary Statistics:")
    st.write(f"Mean of Bootstrap Means: {np.mean(bootstrap_means):.2f}")
    st.write(f"Standard Deviation of Bootstrap Means: {np.std(bootstrap_means):.2f}")
