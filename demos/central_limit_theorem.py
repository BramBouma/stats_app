import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

def show():
    st.title("Central Limit Theorem Demonstration")
    st.sidebar.title("Settings")

    # User inputs from the sidebar
    dist_type = st.sidebar.selectbox("Choose the original distribution:", ("Uniform", "Exponential", "Binomial"))
    sample_size = st.sidebar.slider("Sample size (n):", min_value=1, max_value=1000, value=30)
    num_samples = st.sidebar.slider("Number of samples:", min_value=1, max_value=10000, value=1000)

    # Parameters for the original distribution
    if dist_type == "Uniform":
        low = st.sidebar.number_input("Uniform distribution - lower bound:", value=0)
        high = st.sidebar.number_input("Uniform distribution - upper bound:", value=10)
    elif dist_type == "Exponential":
        rate = st.sidebar.number_input("Exponential distribution - rate (lambda):", value=1.0)
    elif dist_type == "Binomial":
        n = st.sidebar.number_input("Binomial distribution - number of trials:", value=10)
        p = st.sidebar.number_input("Binomial distribution - probability of success:", value=0.5)

    # Function to generate the original distribution
    def generate_distribution(dist_type, size):
        if dist_type == "Uniform":
            return np.random.uniform(low, high, size)
        elif dist_type == "Exponential":
            return np.random.exponential(1/rate, size)
        elif dist_type == "Binomial":
            return np.random.binomial(n, p, size)

    # Generate samples and compute sample means
    original_data = generate_distribution(dist_type, sample_size * num_samples)
    samples = original_data.reshape((num_samples, sample_size))
    sample_means = samples.mean(axis=1)

    # Plotting
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Original distribution
    sns.histplot(original_data, kde=True, ax=axes[0], bins=30)
    axes[0].set_title(f"Original {dist_type} Distribution")

    # Sample means distribution
    sns.histplot(sample_means, kde=True, ax=axes[1], bins=30, stat='density')

    # Scale the normal curve to the sample means distribution
    mean = np.mean(sample_means)
    std = np.std(sample_means)
    x = np.linspace(min(sample_means), max(sample_means), 100)
    y = norm.pdf(x, mean, std)
    axes[1].plot(x, y, 'r-', lw=2)
    axes[1].set_title("Distribution of Sample Means")

    st.pyplot(fig)
