import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def show():
    st.title("Bayesian Inference Demonstration")
    st.sidebar.title("Settings")

    # User inputs from the sidebar
    prior_mean = st.sidebar.number_input("Prior mean (μ₀):", value=0.0)
    prior_std_dev = st.sidebar.number_input("Prior standard deviation (σ₀):", value=1.0)
    likelihood_mean = st.sidebar.number_input("Likelihood mean (μₗ):", value=0.0)
    likelihood_std_dev = st.sidebar.number_input("Likelihood standard deviation (σₗ):", value=1.0)
    num_samples = st.sidebar.slider("Number of samples:", min_value=10, max_value=1000, value=100)

    # Generate sample data from likelihood
    sample_data = np.random.normal(likelihood_mean, likelihood_std_dev, num_samples)
    sample_mean = np.mean(sample_data)
    sample_var = np.var(sample_data)
    sample_std_dev = np.std(sample_data)

    # Compute posterior parameters
    prior_var = prior_std_dev ** 2
    likelihood_var = likelihood_std_dev ** 2
    posterior_mean = (prior_var * sample_mean + num_samples * likelihood_var * prior_mean) / (num_samples * likelihood_var + prior_var)
    posterior_std_dev = np.sqrt((prior_var * likelihood_var) / (num_samples * likelihood_var + prior_var))

    # Plotting
    x = np.linspace(
        min(prior_mean - 3 * prior_std_dev, sample_mean - 3 * sample_std_dev),
        max(prior_mean + 3 * prior_std_dev, sample_mean + 3 * sample_std_dev),
        1000
    )
    prior_pdf = norm.pdf(x, prior_mean, prior_std_dev)
    likelihood_pdf = norm.pdf(x, sample_mean, sample_std_dev / np.sqrt(num_samples))
    posterior_pdf = norm.pdf(x, posterior_mean, posterior_std_dev)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, prior_pdf, 'b-', label=f'Prior: μ₀={prior_mean}, σ₀={prior_std_dev}')
    ax.plot(x, likelihood_pdf, 'g--', label=f'Likelihood: μₗ={sample_mean:.2f}, σₗ={sample_std_dev/np.sqrt(num_samples):.2f}')
    ax.plot(x, posterior_pdf, 'r-', label=f'Posterior: μ={posterior_mean:.2f}, σ={posterior_std_dev:.2f}')
    ax.fill_between(x, 0, prior_pdf, color='b', alpha=0.1)
    ax.fill_between(x, 0, likelihood_pdf, color='g', alpha=0.1)
    ax.fill_between(x, 0, posterior_pdf, color='r', alpha=0.1)
    ax.set_title("Bayesian Inference")
    ax.legend()

    st.pyplot(fig)

    # Display results
    st.write(f"Sample Mean: {sample_mean:.2f}")
    st.write(f"Sample Standard Deviation: {sample_std_dev:.2f}")
    st.write(f"Posterior Mean: {posterior_mean:.2f}")
    st.write(f"Posterior Standard Deviation: {posterior_std_dev:.2f}")
