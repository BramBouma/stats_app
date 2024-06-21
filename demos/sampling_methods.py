import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def show():
    st.title("Sampling Methods Demonstration")
    st.sidebar.title("Settings")

    # User inputs from the sidebar
    population_size = st.sidebar.slider("Population size:", min_value=100, max_value=10000, value=1000)
    sample_size = st.sidebar.slider("Sample size:", min_value=10, max_value=500, value=100)
    dist_type = st.sidebar.selectbox("Choose the population distribution:", ("Normal", "Uniform"))

    # Parameters for the population distribution
    if dist_type == "Normal":
        pop_mean = st.sidebar.number_input("Population mean:", value=0.0)
        pop_std_dev = st.sidebar.number_input("Population standard deviation:", value=1.0)
    elif dist_type == "Uniform":
        pop_low = st.sidebar.number_input("Population lower bound:", value=0.0)
        pop_high = st.sidebar.number_input("Population upper bound:", value=1.0)

    # Generate population data
    if dist_type == "Normal":
        population = np.random.normal(pop_mean, pop_std_dev, population_size)
    elif dist_type == "Uniform":
        population = np.random.uniform(pop_low, pop_high, population_size)

    # Simple Random Sampling
    srs_sample = np.random.choice(population, sample_size, replace=False)

    # Stratified Sampling
    if dist_type == "Normal":
        strata_1 = population[population < np.median(population)]
        strata_2 = population[population >= np.median(population)]
    elif dist_type == "Uniform":
        strata_1 = population[population < (pop_low + pop_high) / 2]
        strata_2 = population[population >= (pop_low + pop_high) / 2]

    stratified_sample = np.concatenate([
        np.random.choice(strata_1, sample_size // 2, replace=False),
        np.random.choice(strata_2, sample_size // 2, replace=False)
    ])

    # Systematic Sampling
    interval = population_size // sample_size
    start_point = np.random.randint(0, interval)
    systematic_sample = population[start_point::interval]

    # Plotting
    fig, ax = plt.subplots(3, 1, figsize=(10, 18))

    sns.histplot(srs_sample, bins=30, kde=True, ax=ax[0], color='blue', edgecolor='black')
    ax[0].set_title("Simple Random Sampling")

    sns.histplot(stratified_sample, bins=30, kde=True, ax=ax[1], color='green', edgecolor='black')
    ax[1].set_title("Stratified Sampling")

    sns.histplot(systematic_sample, bins=30, kde=True, ax=ax[2], color='red', edgecolor='black')
    ax[2].set_title("Systematic Sampling")

    st.pyplot(fig)

    # Display sample statistics
    def display_statistics(sample, method_name):
        st.write(f"### {method_name} Sample Statistics")
        st.write(f"Mean: {np.mean(sample):.2f}")
        st.write(f"Standard Deviation: {np.std(sample):.2f}")
        st.write(f"Variance: {np.var(sample):.2f}")

    display_statistics(srs_sample, "Simple Random Sampling")
    display_statistics(stratified_sample, "Stratified Sampling")
    display_statistics(systematic_sample, "Systematic Sampling")

