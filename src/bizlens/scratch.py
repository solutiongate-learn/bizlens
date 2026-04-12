import numpy as np

activities = ["Admission", "Triage", "Diagnosis", "Lab Test", "Treatment", "Surgery", "Discharge"]
np.random.seed(42)
print(np.random.choice(activities, 4, replace=False))
