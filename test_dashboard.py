from src.dashboard.utils.db import *

data = get_dashboard_data("Mar 2024")

print(data["ratios"].head())

print()

print(get_top_quality("Mar 2024"))