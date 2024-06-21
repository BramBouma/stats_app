import streamlit as st
from demos import (
    central_limit_theorem,
    law_of_large_numbers,
    confidence_intervals,
    hypothesis_testing,
    correlation_regression,
    anova,
    probability_distributions,
    bootstrap_sampling,
    bayesian_inference,
    sampling_methods,
    time_series_analysis
)

st.sidebar.title("Statistics Demonstrations")

# Sidebar menu for selecting the demonstration
demo = st.sidebar.selectbox("Choose a demonstration", [
    "Central Limit Theorem",
    "Law of Large Numbers",
    "Confidence Intervals",
    "Hypothesis Testing",
    "Correlation and Regression",
    "ANOVA",
    "Probability Distributions",
    "Bootstrap Sampling",
    "Bayesian Inference",
    "Sampling Methods",
    "Time Series Analysis"
])

# Display the selected demonstration
if demo == "Central Limit Theorem":
    central_limit_theorem.show()
elif demo == "Law of Large Numbers":
    law_of_large_numbers.show()
elif demo == "Confidence Intervals":
    confidence_intervals.show()
elif demo == "Hypothesis Testing":
    hypothesis_testing.show()
elif demo == "Correlation and Regression":
    correlation_regression.show()
elif demo == "ANOVA":
    anova.show()
elif demo == "Probability Distributions":
    probability_distributions.show()
elif demo == "Bootstrap Sampling":
    bootstrap_sampling.show()
elif demo == "Bayesian Inference":
    bayesian_inference.show()
elif demo == "Sampling Methods":
    sampling_methods.show()
elif demo == "Time Series Analysis":
    time_series_analysis.show()
