import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm, expon, binom, poisson

def show():
    st.title("Probability Distributions Demonstration")
    st.sidebar.title("Settings")

    # User inputs from the sidebar
    dist_type = st.sidebar.selectbox("Choose the distribution:", ("Normal", "Exponential", "Binomial", "Poisson"))

    # Parameters for the selected distribution
    if dist_type == "Normal":
        mean = st.sidebar.number_input("Mean:", value=0.0)
        std_dev = st.sidebar.number_input("Standard Deviation:", value=1.0)
    elif dist_type == "Exponential":
        rate = st.sidebar.number_input("Rate (lambda):", value=1.0)
    elif dist_type == "Binomial":
        n = st.sidebar.number_input("Number of trials:", value=10)
        p = st.sidebar.number_input("Probability of success:", value=0.5)
    elif dist_type == "Poisson":
        lam = st.sidebar.number_input("Lambda (rate of events):", value=3.0)

    # Function to generate the data and theoretical PDF
    def generate_data(dist_type, size=1000):
        if dist_type == "Normal":
            data = np.random.normal(mean, std_dev, size)
            x = np.linspace(min(data), max(data), 100)
            pdf = norm.pdf(x, mean, std_dev)
        elif dist_type == "Exponential":
            data = np.random.exponential(1/rate, size)
            x = np.linspace(min(data), max(data), 100)
            pdf = expon.pdf(x, scale=1/rate)
        elif dist_type == "Binomial":
            data = np.random.binomial(n, p, size)
            x = np.arange(0, n+1)
            pdf = binom.pmf(x, n, p)
        elif dist_type == "Poisson":
            data = np.random.poisson(lam, size)
            x = np.arange(0, max(data)+1)
            pdf = poisson.pmf(x, lam)
        return data, x, pdf

    # Generate data
    data, x, pdf = generate_data(dist_type)

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data, bins=30, kde=False, stat='density', ax=ax, edgecolor='black')
    if dist_type in ["Normal", "Exponential"]:
        ax.plot(x, pdf, 'r-', lw=2)
    else:
        ax.stem(x, pdf, 'r-', basefmt=" ", use_line_collection=True)
    ax.set_title(f"{dist_type} Distribution")
    ax.set_xlabel("Value")
    ax.set_ylabel("Density")

    st.pyplot(fig)

    # Display summary statistics
    st.write("Summary Statistics:")
    st.write(f"Mean: {np.mean(data):.2f}")
    st.write(f"Standard Deviation: {np.std(data):.2f}")
    st.write(f"Variance: {np.var(data):.2f}")

    # Display distribution specific information
    if dist_type == "Normal":
        st.write(f"Theoretical PDF: Mean = {mean}, Std Dev = {std_dev}")
    elif dist_type == "Exponential":
        st.write(f"Theoretical PDF: Rate (lambda) = {rate}")
    elif dist_type == "Binomial":
        st.write(f"Theoretical PMF: Number of trials (n) = {n}, Probability of success (p) = {p}")
    elif dist_type == "Poisson":
        st.write(f"Theoretical PMF: Lambda (rate of events) = {lam}")
