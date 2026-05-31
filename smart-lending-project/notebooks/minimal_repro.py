import pandas as pd
import sys
import os

# Mock matplotlib để không hiện cửa sổ khi chạy script
import matplotlib.pyplot as plt
plt.switch_backend('Agg')

sys.path.append(os.path.join(os.getcwd(), 'notebooks'))
from taichinh import analyze_behavioral_persistence_early_warning

print("--- CASE A: CÓ PAYMENT_HISTORY ---")
df_a = pd.DataFrame({
    'Previous_Defaults': [1, 0, None],
    'Payment_History': ['GOOD', 'POOR', None],
    'Updated_DTI': [0.1, 0.3, 0.6],
    'Default_Flag': [0, 0, 1],
    'Loan_Purpose': ['Consumer', 'Education', 'Personal']
})
analyze_behavioral_persistence_early_warning(df_a)
print("Delinquency_Freq mapped:")
print(df_a[['Payment_History', 'Delinquency_Freq', 'Persistence_Score']])

print("\n--- CASE B: THIẾU CẢ HAI CỘT DELINQUENCY ---")
df_b = pd.DataFrame({
    'Previous_Defaults': [1, 2],
    'Updated_DTI': [0.2, 0.8],
    'Default_Flag': [0, 1],
    'Loan_Purpose': ['Home', 'Car']
})
try:
    analyze_behavioral_persistence_early_warning(df_b)
    print("Success: Function executed without AttributeError.")
    print(df_b[['Previous_Defaults', 'Delinquency_Freq', 'Persistence_Score']])
except Exception as e:
    print(f"Failed with error: {e}")

print("\nMinimal Repro Finished.")