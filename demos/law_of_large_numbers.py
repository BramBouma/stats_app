import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def show():
    st.title("Law of Large Numbers Demonstration")
    st.sidebar.title("Settings")

    # User inputs from the sidebar
    dist_type = st.sidebar.selectbox("Choose the distribution:", ("Uniform", "Exponential", "Binomial"))
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
    sample_means = []
    for i in range(1, num_samples + 1):
        sample = generate_distribution(dist_type, sample_size)
        sample_mean = np.mean(sample)
        sample_means.append(sample_mean)

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(range(1, num_samples + 1), sample_means, label='Sample Mean')
    ax.axhline(np.mean(sample_means), color='r', linestyle='--', label='Population Mean')
    ax.set_title("Law of Large Numbers")
    ax.set_xlabel("Number of Samples")
    ax.set_ylabel("Sample Mean")
    ax.legend()

    st.pyplot(fig)
