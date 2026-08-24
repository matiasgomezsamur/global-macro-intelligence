import pandas as pd
import numpy as np
import matplotlib
import requests

print("Global Macro Intelligence - Environment Check")
print("---------------------------------------------")
print(f"Pandas:     {pd.__version__}")
print(f"NumPy:      {np.__version__}")
print(f"Matplotlib: {matplotlib.__version__}")
print(f"Requests:   {requests.__version__}")
print()
print("Environment successfully configured.")