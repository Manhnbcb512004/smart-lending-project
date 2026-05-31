import pytest
import pandas as pd
import numpy as np
import sys
import os

# Thêm đường dẫn để import taichinh
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'notebooks'))
from taichinh import analyze_behavioral_persistence_early_warning

def test_delinq_mapping_and_persistence():
    """Test Case A: Có Payment_History, không có Delinquency_Freq"""
    data = {
        'Previous_Defaults': [1, 0, 1],
        'Payment_History': ['GOOD', 'POOR', None],
        'Updated_DTI': [0.1, 0.4, 0.7],
        'Default_Flag': [0, 1, 1],
        'Loan_Purpose': ['A', 'B', 'C']
    }
    df = pd.DataFrame(data)
    
    analyze_behavioral_persistence_early_warning(df)
    
    # Kiểm tra giá trị đã map: GOOD=1, POOR=3, None=0
    assert df['Delinquency_Freq'].iloc[0] == 1
    assert df['Delinquency_Freq'].iloc[1] == 3
    assert df['Persistence_Score'].iloc[0] == 2 # 1 (prev) + 1 (delinq)

def test_missing_columns_no_exception():
    """Test Case B: Thiếu cả hai cột liên quan đến Delinquency"""
    data = {
        'Previous_Defaults': [1, 2],
        'Updated_DTI': [0.2, 0.5],
        'Default_Flag': [0, 1],
        'Loan_Purpose': ['X', 'Y']
    }
    df = pd.DataFrame(data)
    # Không được ném AttributeError
    analyze_behavioral_persistence_early_warning(df)
    assert 'Delinquency_Freq' in df.columns
    assert (df['Delinquency_Freq'] == 0).all()