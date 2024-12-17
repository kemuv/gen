import pandas as pd
from datetime import datetime

experiment = pd.DataFrame({
    "exp_id": [1, 2, 3],
    "start_date": ["2022-01-01", "2022-05-17", "2023-10-22"],
    "end_date": ["2022-02-10", "2022-06-21", "2023-11-15"],
    "description": ["Test new button X", "Test new onboarding flow", "Test new feature B"],
    "fraction": [10, 16, 20]
})

experiment_tracking = pd.DataFrame({
    "timestamp": ["2022-01-02 15:30:00", "2022-01-03 18:39:00", "2022-05-03 07:01:18", "2023-10-23 19:14:45"],
    "user_id": ["user1", "user2", "user3", "user54"],
    "exp_id": [1, 1, 1, 3],
    "exp_variant": ["a", "b", "b", "a"],
    "event_type": ["purchase", "purchase", "unsubscribe", "purchase"],
    "value": [20.00, 30.00, 1.00, 10.00]
})

experiment_users = pd.DataFrame({
    "user_id": ["user1", "user2", "user8"],
    "exp_id": [1, 1, 4],
    "variant": ["a", "b", "c"]
})

# converting 
experiment["start_date"] = pd.to_datetime(experiment["start_date"])
experiment["end_date"] = pd.to_datetime(experiment["end_date"])
experiment_tracking["timestamp"] = pd.to_datetime(experiment_tracking["timestamp"])

discount_factor = 0.8 

def calculate_gross_impact(daily_impact, total_units, duration, fraction):   # calculate gross projected future impact
    return daily_impact * total_units * duration / fraction

def calculate_future_impact(gross_impact, discount_factor):   # calculate future estimated impact
    return gross_impact * discount_factor

def evaluate_impacts():
    estimated_impact = 0
    estimated_risk = 0

    for _, exp in experiment.iterrows():
        exp_id = exp["exp_id"]
        fraction = exp["fraction"]
        duration = (exp["end_date"] - exp["start_date"]).days
        
        exp_data = experiment_tracking[experiment_tracking["exp_id"] == exp_id]           # Filter experiment tracking data
        daily_impact = exp_data[exp_data["event_type"] == "purchase"]["value"].sum()   # daily impact per unit (purchase)
        total_units = len(exp_data["user_id"].unique())   # Total exposed units
        
        gross_impact = calculate_gross_impact(daily_impact, total_units, duration, fraction)   # Gross projected future impact
        future_impact = calculate_future_impact(gross_impact, discount_factor)   # Future estimated impact

        if "a" in exp_data["exp_variant"].unique():   # Classify experiment variant
            estimated_impact += future_impact
        else:
            estimated_risk += future_impact
    return estimated_impact, estimated_risk

estimated_impact, estimated_risk = evaluate_impacts()

print("Estimated Impact of Successful Experiments:", estimated_impact)
print("Estimated Risk Mitigated:", estimated_risk)