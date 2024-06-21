import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr, linregress

def show():
    st.title("Correlation and Regression Demonstration")
    st.sidebar.title("Settings")

    # User inputs from the sidebar
    dist_type = st.sidebar.selectbox("Choose the distribution for sample data:", ("Normal", "Uniform"))
    sample_size = st.sidebar.slider("Sample size (n):", min_value=10, max_value=1000, value=100)
    correlation_type = st.sidebar.selectbox("Choose the type of correlation:", ("Pearson", "Spearman"))

    # Parameters for the original distribution
    if dist_type == "Normal":
        mean_x = st.sidebar.number_input("Normal distribution for X - mean:", value=0.0)
        std_dev_x = st.sidebar.number_input("Normal distribution for X - standard deviation:", value=1.0)
        mean_y = st.sidebar.number_input("Normal distribution for Y - mean:", value=0.0)
        std_dev_y = st.sidebar.number_input("Normal distribution for Y - standard deviation:", value=1.0)
    elif dist_type == "Uniform":
        low_x = st.sidebar.number_input("Uniform distribution for X - lower bound:", value=0.0)
        high_x = st.sidebar.number_input("Uniform distribution for X - upper bound:", value=1.0)
        low_y = st.sidebar.number_input("Uniform distribution for Y - lower bound:", value=0.0)
        high_y = st.sidebar.number_input("Uniform distribution for Y - upper bound:", value=1.0)

    # Function to generate the original distribution
    def generate_distribution(dist_type, size, params):
        if dist_type == "Normal":
            return np.random.normal(params['mean'], params['std_dev'], size)
        elif dist_type == "Uniform":
            return np.random.uniform(params['low'], params['high'], size)

    # Generate sample data
    if dist_type == "Normal":
        params_x = {'mean': mean_x, 'std_dev': std_dev_x}
        params_y = {'mean': mean_y, 'std_dev': std_dev_y}
    elif dist_type == "Uniform":
        params_x = {'low': low_x, 'high': high_x}
        params_y = {'low': low_y, 'high': high_y}

    x = generate_distribution(dist_type, sample_size, params_x)
    y = generate_distribution(dist_type, sample_size, params_y)

    # Compute correlation
    if correlation_type == "Pearson":
        corr, p_value = pearsonr(x, y)
    elif correlation_type == "Spearman":
        corr, p_value = spearmanr(x, y)

    # Perform linear regression
    slope, intercept, r_value, p_value_reg, std_err = linregress(x, y)

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x=x, y=y, ax=ax)
    ax.plot(x, intercept + slope * x, 'r', label=f'Linear Regression: y = {intercept:.2f} + {slope:.2f}x')
    ax.set_title(f"Scatter Plot with {correlation_type} Correlation and Linear Regression")
    ax.legend()

    st.pyplot(fig)

    # Display results
    st.write(f"{correlation_type} Correlation Coefficient: {corr:.4f}")
    st.write(f"P-value: {p_value:.4f}")
    st.write(f"Linear Regression: y = {intercept:.2f} + {slope:.2f}x")
    st.write(f"R-squared: {r_value**2:.4f}")
    st.write(f"Regression P-value: {p_value_reg:.4f}")
    st.write(f"Standard Error: {std_err:.4f}")
