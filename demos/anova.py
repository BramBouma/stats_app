import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway

def show():
    st.title("ANOVA (Analysis of Variance) Demonstration")
    st.sidebar.title("Settings")

    # User inputs from the sidebar
    num_groups = st.sidebar.slider("Number of groups:", min_value=2, max_value=10, value=3)
    sample_size = st.sidebar.slider("Sample size per group (n):", min_value=5, max_value=100, value=30)
    dist_type = st.sidebar.selectbox("Choose the distribution for sample data:", ("Normal", "Uniform"))

    # Parameters for the original distribution
    if dist_type == "Normal":
        mean_values = [st.sidebar.number_input(f"Group {i+1} - mean:", value=0.0) for i in range(num_groups)]
        std_dev_values = [st.sidebar.number_input(f"Group {i+1} - standard deviation:", value=1.0) for i in range(num_groups)]
    elif dist_type == "Uniform":
        low_values = [st.sidebar.number_input(f"Group {i+1} - lower bound:", value=0.0) for i in range(num_groups)]
        high_values = [st.sidebar.number_input(f"Group {i+1} - upper bound:", value=1.0) for i in range(num_groups)]

    # Function to generate the original distribution
    def generate_distribution(dist_type, size, params):
        if dist_type == "Normal":
            return np.random.normal(params['mean'], params['std_dev'], size)
        elif dist_type == "Uniform":
            return np.random.uniform(params['low'], params['high'], size)

    # Generate sample data for each group
    data = []
    for i in range(num_groups):
        if dist_type == "Normal":
            params = {'mean': mean_values[i], 'std_dev': std_dev_values[i]}
        elif dist_type == "Uniform":
            params = {'low': low_values[i], 'high': high_values[i]}
        group_data = generate_distribution(dist_type, sample_size, params)
        data.append(group_data)

    # Perform ANOVA test
    f_stat, p_value = f_oneway(*data)

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, group_data in enumerate(data):
        sns.histplot(group_data, bins=15, kde=True, label=f'Group {i+1}', ax=ax, stat="density", alpha=0.6)
    ax.set_title("ANOVA Test: Distribution of Groups")
    ax.legend()

    st.pyplot(fig)

    # Display results
    st.write(f"ANOVA F-statistic: {f_stat:.4f}")
    st.write(f"P-value: {p_value:.4f}")
    st.write(f"Decision: {'Reject' if p_value < 0.05 else 'Fail to Reject'} the null hypothesis at alpha = 0.05")
