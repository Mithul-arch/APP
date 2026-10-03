import pandas as pd
import numpy as np

rng = np.random.default_rng(7)                 
numbers = rng.integers(low=1, high=101, size=10)  

labels = [f"item_{i}" for i in range(1, 11)]    
random_series = pd.Series(numbers, index=labels, name="random_numbers")

print(random_series)