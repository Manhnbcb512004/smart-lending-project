# Project Name: Credit Risk & Debt Repayment Capacity Analysis
# project person: Bui Tien Manh
# data source: MIT
# Sub-title: Evaluating Borrower Profiles through Capacity, Character, Stability, and Collateral

# Core KPI Domains:
# 1. Capacity: DTI (Debt-to-Income), LTI (Loan-to-Income), Net Income
# 2. Character: Credit Score, Delinquency Frequency, Prior Defaults
# 3. Stability: Job Tenure, Employment Status, Residency
# 4. Collateral: LTV (Loan-to-Value), Assets Value, PD (Probability of Default), EL (Expected Loss)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import logging
import seaborn as sns
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from scipy.stats import gaussian_kde
import matplotlib.patches as patches
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import xgboost as xgb
import shap
import plotly.express as px
 
# Đọc dữ liệu 
df = pd.read_csv("Clean_Data.csv", sep=",")

# =========================================================================================
# CẤU HÌNH PHONG CÁCH TRỰC QUAN HÓA ĐỒNG BỘ
# =========================================================================================
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Roboto']
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['grid.alpha'] = 0.3
sns.set_style("ticks")

NON_DEFAULT_COLOR = "#1f77b4" # Xanh dương nhạt
DEFAULT_COLOR = "#d62728"     # Đỏ trầm
NEUTRAL_COLOR = "#cccccc"     # Xám nhạt
HIGHLIGHT_RED = "#ff0000"     # Đỏ rực

print("Columns:", df.columns.tolist())
print("Sample columns containing 'DTI':", [c for c in df.columns if 'DTI' in c.upper()])
print("Any nulls in Updated_DTI (if exists):", df['Updated_DTI'].isnull().sum() if 'Updated_DTI' in df.columns else 'no column')

# =========================================================================================
# KPI CHÍNH 1: DTI (DEBT-TO-INCOME) - TỶ LỆ NỢ TRÊN TỔNG THU NHẬP
# =========================================================================================
def analyze_dti_foundations(df):
    # KPI Phụ 1.1: Phân bổ tỷ lệ nợ xấu theo các ngưỡng DTI
    # Bước 1: Chuẩn hóa dữ liệu để đảm bảo tính toán chính xác
    df["Default_Flag"] = pd.to_numeric(df["Default_Flag"], errors='coerce')
    df["Updated_DTI"] = pd.to_numeric(df["Updated_DTI"], errors='coerce')
    
    # Định nghĩa khoảng DTI: (0, 20%], (20, 40%], (40, 60%], (60, 100%]
    # SỬA LỖI: Đưa về chặn 1 để loại bỏ DTI > 100% theo đúng logic của Insight gốc (về lại 69.6%)
    bins = [0, 0.2, 0.4, 0.6, 1]
    dti_order = ["Tỷ lệ thấp (dưới 20%)","Tỷ lệ trung bình (20-40%)","Tỷ lệ khá (40-60%)","Tỷ lệ cao (trên 60%)"]
    
    # Gán nhóm DTI (Xóa right=False để dùng mặc định right=True nhằm loại bỏ DTI=0 ở nhóm đầu giúp khớp về 65.6%)
    df["Nhom_DTI"] = pd.cut(df["Updated_DTI"], bins=bins, labels=dti_order)

    # Bước 2: Tính toán tỷ lệ nợ xấu và kiểm tra số liệu
    DTI_summary = df.groupby("Nhom_DTI", observed=False)["Default_Flag"].agg(['mean', 'count']).reset_index()
    DTI_summary = DTI_summary.rename(columns={'mean': 'Mean', 'count': 'Count'})
    DTI_summary["Tỷ lệ nợ xấu (%)"] = DTI_summary["Mean"] * 100
    
    # Ép thứ tự dữ liệu theo đúng dti_order để tránh sai lệch biểu đồ
    DTI_summary = DTI_summary.set_index("Nhom_DTI").reindex(dti_order).reset_index()

    print("--- ĐỐI SOÁT SỐ LIỆU BIỂU ĐỒ 1.1 ---")
    print(DTI_summary[["Nhom_DTI", "Tỷ lệ nợ xấu (%)"]])

    # Bước 3: Vẽ biểu đồ cột như ban đầu
    plt.figure(figsize=(12, 7))
    # Sử dụng dải màu Blues_d hoặc tương tự như biểu đồ gốc của bạn
    ax = sns.barplot(x="Nhom_DTI", y="Tỷ lệ nợ xấu (%)", data=DTI_summary, 
                     order=dti_order, hue="Nhom_DTI", palette="Blues_d", legend=False)

    plt.axhline(df["Default_Flag"].mean() * 100, color='red', linestyle='--', alpha=0.5, label="Trung bình hệ thống")

    # Thêm label số liệu
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.1f}%", 
                    (p.get_x() + p.get_width() / 2., p.get_height() + 0.5), 
                    ha='center', va='bottom', fontsize=11, fontweight='bold', color='black')

    plt.title("BIỂU ĐỒ 1.1: TỶ LỆ NỢ XẤU THEO TỪNG KHOẢNG DTI\n(Mô tả xu hướng tăng rủi ro theo áp lực nợ)", fontsize=15, pad=20)
    plt.ylabel("Tỷ lệ nợ xấu (%)", fontsize=12)
    plt.xlabel("Phân khúc DTI (Debt-to-Income)", fontsize=12)
    
    # Giới hạn trục Y từ 0-100 để minh chứng "nợ xấu luôn duy trì ở mức cao trên 65%" 
    # như trong nhận xét khái quát của bạn.
    plt.ylim(0, 100) 
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.show()

    # KPI Phụ 1.2: Phân tích sự biến thiên DTI theo Trình độ học vấn
     # 1. Tạo một cột mới hoặc map trực tiếp nhãn hiển thị từ cột cũ
df['Trạng thái nợ'] = df['Default_Flag'].map({0: "Nợ tốt (0)", 1: "Nợ xấu (1)"})

# 2. Vẽ biểu đồ với hue mới
plt.figure(figsize=(14, 8))
sns.boxplot(
    x="Education_Level", 
    y="Updated_DTI", 
    hue="Trạng thái nợ", # Sử dụng cột đã map nhãn
    data=df, 
    palette="Set2", 
    showmeans=True
)

plt.title("KPI 1.2: BIẾN THIÊN CHỈ SỐ DTI THEO TRÌNH ĐỘ HỌC VẤN", fontsize=16, fontweight="bold")
# Không cần truyền labels vào plt.legend nữa, chỉ cần chỉnh sửa title nếu muốn
plt.legend(title="Trạng thái nợ") 
plt.show()

# =========================================================================================
# KPI CHÍNH 2: DTI TỔNG THỂ (OVERALL DEBT-TO-INCOME) - TỶ LỆ NỢ TRÊN TỔNG THU NHẬP
# =========================================================================================
def analyze_overall_dti(df):
    """
    Hàm phân tích chỉ số rủi ro dựa trên Tỷ lệ nợ trên tổng thu nhập (Updated_DTI).
    Đây là chỉ số DTI tổng thể, bao gồm tất cả các khoản nợ của khách hàng.
    Không tính được PTI (Payment-to-Income) do thiếu dữ liệu về kỳ hạn vay và lãi suất.
    """
    # ==========================================================================
    # TÍNH TOÁN VÀ THỐNG KÊ MÔ TẢ DTI TỔNG THỂ
    # ==========================================================================
    # Ghi chú: Updated_DTI chính là chỉ số DTI tổng thể trong bộ dữ liệu này.
    # Ta sử dụng nhãn LTI (Loan-to-Income) để nhấn mạnh đây là tỷ lệ dư nợ trên thu nhập.
    if "LTI" not in df.columns:
        df["LTI"] = df["Loan_Amount"] / df["Cleaned_Income"]

    # In thống kê mô tả giữa nhóm nợ tốt (0) và nợ xuất (1) 
    print("--- THỐNG KÊ CHỈ SỐ DTI TỔNG THỂ THEO TRẠNG THÁI NỢ --- ")
    print(df.groupby("Default_Flag")["LTI"].describe())

    # KPI Phụ 2.1: Mật độ phân phối DTI tổng thể giữa nhóm nợ tốt và nợ xấu
    # TRỰC QUAN HÓA PHÂN PHỐI (KDE PLOT)
    # ------------------------------------------------------------------------
    plt.figure(figsize=(10,6))
    # Dùng kde để xem đỉnh tập trung của 2 nhóm ở đâu 
    sns.kdeplot(data=df, x="Updated_DTI", hue="Default_Flag", fill=True, common_norm=False, palette=["#d62728","#1f77b4"])

    # Vẽ đường gióng tại ngưỡng 40% ( Ngưỡng rủi ro phổ biến tại ngân hàng )
    plt.axvline(0.4, color="black", linestyle='--', label="Ngưỡng chuẩn (40%)")

    plt.title("BIỂU ĐỒ 2.1: PHÂN PHỐI CHỈ SỐ DTI THEO TRẠNG THÁI NỢ", fontsize=14, fontweight="bold")
    plt.xlabel("Debt-to-Income Ratio (DTI)")
    plt.ylabel("Mật độ")
    plt.legend(title="Trạng thái nợ", labels=["Nợ tốt (0)", "Nợ xấu (1)", "Ngưỡng chuẩn"])
    plt.show()

    # KPI Phụ 2.2: Tỷ lệ nợ xấu theo từng phân khúc DTI tổng thể
    # ----------------------------------------------------------------------------------------
    # PHÂN KHÚC DTI TỔNG THỂ VÀ TỶ LỆ NỢ XẤU (BINING)
    # ---------------------------------------------------------------------------------------
    #  Chia giỏ DTI tổng thể để xem mức nào thì nợ xấu tăng vọt 
    bins = [0, 0.2, 0.3, 0.4, 0.5, 0.6, float("inf")] 
    labels = ["< 20%", "20% - 30%", "30% - 40%", "40% - 50%", "50% - 60%", "> 60%"]
    df["LTI_Segment"] = pd.cut(
        df["LTI"], 
        bins=bins,
        labels=labels
    )

    # Tính tỷ lệ nợ xấu (%) cho từng giỏ hàng 
    seg_df = df.groupby("LTI_Segment", observed=False)["Default_Flag"].mean().reset_index()
    seg_df["bad_Rate (%)"]  = seg_df["Default_Flag"] * 100

    # Vẽ Bar chart
    plt.figure(figsize=(10,6))
    ax = sns.barplot(x="LTI_Segment", y="bad_Rate (%)", data=seg_df, palette="Reds", hue="LTI_Segment", legend=False)

    plt.title("BIỂU ĐỒ 2.2: TỶ LỆ NỢ XẤU THEO TỪNG PHÂN KHÚC DTI TỔNG THỂ", fontsize=14, fontweight="bold")
    plt.xlabel("Phân khúc DTI tổng thể")
    plt.ylabel("Tỷ lệ nợ xấu (%)")

    # Thêm số liệu (%) lên đầu mỗi cột cho trực quan 
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.1f}%",
                    (p.get_x() + p.get_width() / 2.,p.get_height()),
                    ha="center", va="bottom", fontweight="bold")
    plt.show()

# Cách chạy hàm:
# analyze_overall_dti(df)

# =========================================================================================
# KPI CHÍNH 3: NET INCOME - PHÂN TÍCH THU NHẬP RÒNG
# =========================================================================================
def analyze_income_kpi(df):
    if df["Cleaned_Income"].max() < 1000000:
        bins = [0, 30000, 50000, 70000, 100000, float("inf")]
        labels = ["< 30k", "30k-50k", "50k-70k", "70k-100k", "> 100k"]
    else:
        bins = [0, 7000000, 10000000, 15000000, 25000000, float("inf")]
        labels = ["< 7M", "7M-10M", "10M-15M", "15M-25M", "> 25M"]

    df["Income_Segment"] = pd.cut(df["Cleaned_Income"], bins=bins, labels=labels)
    income_kpi = df.groupby("Income_Segment", observed=False)["Default_Flag"].mean().reset_index()
    income_kpi["Bad_Loan_Rate (%)"] = income_kpi["Default_Flag"].fillna(0) * 100

    plt.figure(figsize=(12,7))
    sns.set_style("whitegrid")
    ax = sns.barplot(x="Income_Segment", y="Bad_Loan_Rate (%)", data=income_kpi, palette="coolwarm", hue="Income_Segment", legend=False, zorder=2)
    plt.plot(income_kpi["Income_Segment"].astype(str), income_kpi["Bad_Loan_Rate (%)"], color="red", marker='o', linestyle="-", linewidth=3, label="Xu hướng rủi ro", zorder=5)

    for p in ax.patches:
        ax.annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height()), ha="center", va="bottom", fontsize=11, fontweight="bold", color="darkblue")
        
    plt.title("BIỂU ĐỒ 3.1: TƯƠNG QUAN GIỮA THU NHẬP RÒNG VÀ TỶ LỆ NỢ XẤU", fontsize=15, fontweight="bold", pad=20)
    plt.ylim(0, max(income_kpi["Bad_Loan_Rate (%)"].max(), 10) + 10)
    plt.legend()
    plt.show()

# KPI Phụ 3.2: Thống kê mô tả và phát hiện ngoại lệ (Outliers) thu nhập
def descriptive_analysis(df):
    stats = df.groupby("Default_Flag")["Cleaned_Income"].agg(["count", "mean", "std", "min", "max"])
    print("--- THỐNG KÊ MÔ TẢ THU NHẬP THEO NHÓM NỢ ---")
    print(stats)

    # Vẽ Boxplot để so sánh dải thu nhập và điểm ngoại lệ (outliers)
    plt.figure(figsize=(10,6))
    sns.boxplot(x="Default_Flag", y="Cleaned_Income", data=df, palette="Set2")
    plt.title("BIỂU ĐỒ 3.2: PHÂN PHỐI THU NHẬP RÒNG QUA BOXPLOT", fontsize=14)
    plt.xlabel("Trạng thái nợ (0: tốt, 1: xấu)")
    plt.ylabel("Thu nhập ròng (VNĐ)")
    plt.show()

# =========================================================================================
# KPI CHÍNH 4: LTI CỤ THỂ (SPECIFIC LOAN-TO-INCOME) - TỶ LỆ KHOẢN VAY TRÊN THU NHẬP
# =========================================================================================
# Công thức: LTI_Specific = Loan_Amount / Cleaned_Income
# Giải thích: Chỉ số này đo lường tỷ lệ giữa số tiền khách hàng muốn vay và thu nhập ròng hàng năm.
# Nó cho biết khách hàng đang vay gấp bao nhiêu lần thu nhập, giúp đánh giá gánh nặng nợ cụ thể của khoản vay mới.

def analyze_specific_lti(df):
    """
    Phân tích năng lực trả nợ dựa trên tỷ lệ khoản vay cụ thể trên thu nhập.
    """
    # Tính toán LTI cụ thể (xử lý tránh chia cho 0 nếu thu nhập bằng 0)
    df["LTI_Specific"] = np.where(df["Cleaned_Income"] > 0, df["Loan_Amount"] / df["Cleaned_Income"], 0)
    
    # Phân đoạn rủi ro để trực quan hóa
    bins = [0, 0.2, 0.5, 1.0, 1.5, float("inf")]
    labels = ["An toàn (<20%)", "Thấp (20-50%)", "Trung bình (50-100%)", "Cao (100-150%)", "Rất cao (>150%)"]
    df["LTI_Spec_Segment"] = pd.cut(df["LTI_Specific"], bins=bins, labels=labels)
    
    # KPI Phụ 4.1: Tỷ lệ nợ xấu theo phân đoạn LTI cụ thể
    spec_summary = df.groupby("LTI_Spec_Segment", observed=False)["Default_Flag"].mean().reset_index()
    spec_summary["Bad_Rate (%)"] = spec_summary["Default_Flag"] * 100

    plt.figure(figsize=(10,6))
    ax = sns.barplot(x="LTI_Spec_Segment", y="Bad_Rate (%)", data=spec_summary, palette="magma", hue="LTI_Spec_Segment", legend=False)
    plt.title("KPI 4.1: TỶ LỆ NỢ XẤU THEO ĐÒN BẨY KHOẢN VAY (LTI CỤ THỂ)", fontweight="bold")
    plt.ylabel("Tỷ lệ nợ xấu (%)")
    
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height()), ha="center", va="bottom", fontweight="bold")
    plt.show()

# =========================================================================================
# KPI CHÍNH 5: THU NHẬP TRÊN ĐẦU NGƯỜI (INCOME PER DEPENDENT - IPD)
# =========================================================================================
# Công thức: IPD = Cleaned_Income / (Number_of_Dependents + 1)
# Giải thích: Thu nhập ròng chia cho tổng số thành viên trong hộ gia đình (số người phụ thuộc + chính khách hàng).
# Chỉ số này phản ánh "Năng lực" tài chính thực tế còn lại để trả nợ sau khi trang trải chi phí sinh hoạt gia đình.

def analyze_ipd(df):
    """
    Phân tích năng lực trả nợ sau khi tính đến yếu tố số người phụ thuộc.
    """
    # Tính toán IPD
    df["IPD"] = df["Cleaned_Income"] / (df["Number_of_Dependents"] + 1)
    
    # Chia nhóm theo phân vị (Quartiles) để so sánh 4 mức năng lực tài chính gia đình
    df["IPD_Group"] = pd.qcut(df["IPD"], q=4, labels=["IPD Thấp", "IPD Trung bình", "IPD Khá", "IPD Cao"])
    
    # KPI Phụ 5.1: Tỷ lệ nợ xấu theo mức thu nhập bình quân gia đình
    ipd_summary = df.groupby("IPD_Group", observed=False)["Default_Flag"].mean().reset_index()
    ipd_summary["Bad_Rate (%)"] = ipd_summary["Default_Flag"] * 100

    plt.figure(figsize=(10,6))
    ax = sns.barplot(x="IPD_Group", y="Bad_Rate (%)", data=ipd_summary, palette="YlGnBu", hue="IPD_Group", legend=False)
    plt.title("KPI 5.1: TỶ LỆ NỢ XẤU THEO THU NHẬP BÌNH QUÂN ĐẦU NGƯỜI (IPD)", fontweight="bold")
    plt.ylabel("Tỷ lệ nợ xấu (%)")
    
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height()), ha="center", va="bottom", fontweight="bold")
    plt.show()
 
# =========================================================================================
# NHÓM MỞ RỘNG: PHÂN TÍCH CHUYÊN SÂU & DỰ BÁO RỦI RO
# =========================================================================================

# --- KPI MR 1: NHÂN KHẨU HỌC VÀ RỦI RO TẬP TRUNG ---
def plot_demographics_risk(df):
    """
    Trực quan hóa rủi ro theo đặc điểm khách hàng.
    """
    # Tự  động hóa việc chia nhóm tuổi nếu chưa có 
    if "Age_Segment" not in df.columns:
        df["Age_Segment"] = pd.cut(
            df["Age"],
            bins=[18,25, 35, 45, 60, 100],
            labels=["18-25", "26-35", "36-45","46-60", "Trên 60"])

    fig, axes = plt.subplots(1, 2, figsize=(16,6)) 

    # Chart 1: Rủi  ro theo độ tuổi
    age_risk = df.groupby("Age_Segment", observed=False)["Default_Flag"].mean() * 100
    ax1 = sns.barplot(x=age_risk.index, y=age_risk.values, ax=axes[0], palette="Blues_d", hue=age_risk.index, legend=False)
    axes[0].set_title("BIỂU ĐỒ R1.1:TỶ LỆ NỢ XẤU THEO ĐỘ TUỔI", fontweight="bold")
    axes[0].set_ylabel("Tỷ lệ (%)")

    # Bổ sung số liệu trên đầu cột cho Chart 1
    for p in ax1.patches:
        ax1.annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha="center", va="bottom", fontweight="bold", fontsize=10)

    # Chart 2: rủi ro theo học vấn (line chart để thấy xu hướng)
    # Kiểm tra nếu có cột Rank thì vẽ line chart, nếu không dùng Education_Level vẽ bar chart
    if "Education_Ordinal_Rank" in df.columns:
        edu_risk = df.groupby("Education_Ordinal_Rank", observed=False)["Default_Flag"].mean() * 100
        sns.lineplot(x=edu_risk.index, y=edu_risk.values, marker="s", ax=axes[1], color="darkred", markersize=8) 
    else:
        edu_risk = df.groupby("Education_Level", observed=False)["Default_Flag"].mean() * 100
        sns.barplot(x=edu_risk.index, y=edu_risk.values, ax=axes[1], palette="Reds_d", hue=edu_risk.index, legend=False)

    axes[1].set_title("BIỂU ĐỒ R1.2: XU HƯỚNG RỦI RO THEO TRÌNH ĐỘ HỌC VẤN",fontweight="bold")
    axes[1].set_xlabel("Trình độ học vấn")

    plt.tight_layout()
    plt.show()

# --- KPI MR 2: MA TRẬN TÀI CHÍNH VÀ ĐỘ NHẠY RỦI RO ---
def plot_financial_depth(df):
    """
    Phân tích chuyên sâu về độ nhạy LTI và sự tập trung nợ xấu 
    """
    # 2.1 Ma trận nhiệt (Heatmap)
    plt.figure(figsize=(10,6))
    # Chuyển sang observed=True để loại bỏ các vùng trắng không có dữ liệu, tập trung vào vùng thực tế
    pivot = df.pivot_table(index="Income_Segment", columns="LTI_Segment",
                           values="Default_Flag", aggfunc="mean", observed=True)* 100
    sns.heatmap(pivot, annot=True, fmt=".1f", cmap="Reds", cbar_kws={"label":"Tỷ lệ nợ xấu (%)"})
    plt.title("BIỂU ĐỒ R2.1: MA TRẬN RỦI RO: THU NHẬP VS LTI", fontweight="bold")
    plt.show()

    # 2.2 Biểu đồ Pareto/concentration
    plt.figure(figsize=(10,5))
    bad_debt_share = df[df["Default_Flag"] == 1]["LTI_Segment"].value_counts(normalize=True) * 100
    ax = sns.barplot(x=bad_debt_share.index, y=bad_debt_share.values, palette="flare", hue=bad_debt_share.index, legend=False)
    plt.title("BIỂU ĐỒ R2.2: CƠ CẤU NỢ XẤU THEO PHÂN KHÚC LTI", fontweight="bold")
    plt.ylabel("% Trên tổng số ca nợ xấu")

    # Bổ sung số liệu trên đầu cột cho Pareto Chart
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha="center", va="bottom", fontweight="bold")
    plt.show() 

# --- KPI MR 3: XÂY DỰNG CHÂN DUNG KHÁCH HÀNG (PERSONA PROFILING) ---
def analyze_profiling_averages(df):
    """
    Xây dựng chân dung khách hàng thông qua giá trị trung bình LTI và Thu nhập.
    """
    # Đảm bảo cột LTI đã tồn tại
    if "LTI" not in df.columns:
        df["LTI"] = df["Updated_DTI"]

    # Tính toán bảng tổng hợp
    profiling_table = df.groupby("Default_Flag").agg({
        "LTI": ["mean", "median"],
        "Cleaned_Income": ["mean", "median"],
        "Age": "mean",
        "Default_Flag": "count"
    }).reset_index()

    # Đổi tên cột để dễ đọc
    profiling_table.columns = [
        "Trạng thái nợ", 
        "LTI Trung bình", "LTI Trung vị", 
        "Thu nhập TB", "Thu nhập Trung vị", 
        "Độ tuổi TB", "Số lượng KH"
    ]

    print("\n" + "="*50)
    print("BẢNG TỔNG HỢP KPI MR 3: CHÂN DUNG KHÁCH HÀNG (AVERAGES)")
    print("="*50)
    print(profiling_table.to_string(index=False))
    
    return profiling_table


# =========================================================================================
# CORE 2.1: CREDIT SCORE ANALYSIS (PHÂN TÍCH ĐIỂM TÍN DỤNG)
# =========================================================================================
def analyze_credit_score_discriminatory_power(df):
    """
    Đánh giá khả năng phân tách rủi ro của biến Credit_Score.
    Sử dụng AUC-ROC và Gini Coefficient để kiểm chứng Model Risk theo Basel.
    """
    # 1. Tính toán AUC-ROC và Gini
    # Credit_Score cao = rủi ro thấp. Để tính AUC cho Default_Flag=1, ta đảo ngược điểm số.
    actual = df["Default_Flag"]
    scores = -df["Credit_Score"]
    
    auc_score = roc_auc_score(actual, scores)
    gini_coefficient = 2 * auc_score - 1

    print("\n" + "="*80)
    print("CORE 2.1: PHÂN TÍCH KHẢ NĂNG PHÂN TÁCH RỦI RO CỦA ĐIỂM TÍN DỤNG")
    print("="*80)
    print(f"[Định lượng] AUC-ROC Score: {auc_score:.4f}")
    print(f"[Định lượng] Gini Coefficient: {gini_coefficient:.4f}")

    # 2. KDE Plot: Overlapping Distributions
    plt.figure(figsize=(12, 6))
    sns.kdeplot(data=df[df['Default_Flag'] == 0], x='Credit_Score', 
                label='Nợ tốt (Non-Default)', fill=True, color='seagreen', alpha=0.4)
    sns.kdeplot(data=df[df['Default_Flag'] == 1], x='Credit_Score', 
                label='Nợ xấu (Default)', fill=True, color='crimson', alpha=0.4)
    
    plt.title("BIỂU ĐỒ 2.1.1: SỰ TRÙNG LẶP PHÂN PHỐI ĐIỂM TÍN DỤNG (OVERLAPPING DISTRIBUTIONS)", 
              fontsize=14, fontweight='bold')
    plt.xlabel("Credit Score")
    plt.ylabel("Mật độ phân phối (Density)")
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.show()

    # 3. ROC Curve
    fpr, tpr, _ = roc_curve(actual, scores)
    plt.figure(figsize=(8, 8))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {auc_score:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier (AUC=0.5)')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('BIỂU ĐỒ 2.1.2: ĐƯỜNG CONG ROC - CREDIT SCORE')
    plt.legend(loc="lower right")
    plt.show()

    # 4. Phân tích Bad Rate Saturation (Bão hòa nợ xấu)
    # Chia điểm số thành 5 nhóm bằng nhau (Quantiles) để kiểm tra tính ổn định của tỷ lệ nợ xấu
    df['Score_Bin'] = pd.qcut(df['Credit_Score'], q=5, duplicates='drop')
    bad_rate_bins = df.groupby('Score_Bin', observed=False)['Default_Flag'].mean() * 100
    
    print("\n--- TỶ LỆ NỢ XẤU (BAD RATE) THEO PHÂN KHÚC ĐIỂM ---")
    print(bad_rate_bins)
    
    # Nhận định chuyên gia phản biện
    print("\n[INSIGHT PHẢN BIỆN TỪ SENIOR ANALYST]:")
    if gini_coefficient < 0.2:
        print("- CẢNH BÁO: Chỉ số Gini tiệm cận mức 0. Hệ thống Credit Score đang gặp hiện tượng Zero Discriminatory Power.")
        print("- Hiện tượng Overlapping Distributions (Biểu đồ 2.1.1) xác nhận nợ xấu phân bổ đều ở mọi mức điểm.")
        print("- Kết luận: Hệ thống scorecard tĩnh đã lỗi thời, không còn khả năng sàng lọc rủi ro.")
    
    return auc_score, gini_coefficient

# ===============================================================================================
# Phân tích chuyên sâu
#================================================================================================
def analyze_advanced_risk_modules(df):
    """
    Phân tích 6 module rủi ro tín dụng chuyên sâu (Core 2.2).
    Sử dụng kỹ thuật Segmentation, Interaction Heatmaps và Random Forest Feature Importance.
    """
    # --- TIỀN XỬ LÝ & ĐỒNG BỘ CỘT ---
    analysis_df = df.copy()
    analysis_df['Delinquency_Level'] = analysis_df['Payment_History'].fillna('UNKNOWN')
    analysis_df['Income'] = analysis_df['Cleaned_Income']
    analysis_df['LTI'] = analysis_df['Updated_DTI']
    analysis_df['Previous_Defaults'] = analysis_df['Previous_Defaults'].fillna(0)

    # 1. Bad Rate Segmentation (Bar chart 10 phân khúc)
    analysis_df['Score_Bin'] = pd.qcut(analysis_df['Credit_Score'], q=10, duplicates='drop')
    bad_rate_seg = analysis_df.groupby('Score_Bin', observed=False)['Default_Flag'].mean().reset_index()
    # Rút gọn nhãn khoảng điểm bằng cách làm tròn thành số nguyên (Ví dụ: (500.1, 550.2] -> 500-550)
    bad_rate_seg['Score_Bin'] = bad_rate_seg['Score_Bin'].apply(lambda x: f"{int(x.left)}-{int(x.right)}")
    bad_rate_seg['Bad_Rate (%)'] = bad_rate_seg['Default_Flag'] * 100

    plt.figure(figsize=(12, 6))
    colors = [HIGHLIGHT_RED if x > 5 else NEUTRAL_COLOR for x in bad_rate_seg["Bad_Rate (%)"]]
    ax = sns.barplot(data=bad_rate_seg, x='Score_Bin', y='Bad_Rate (%)', palette=colors, hue='Score_Bin', legend=False)
    plt.title("Sự bão hòa tỷ lệ nợ xấu (Bad Rate Saturation) trên mọi phân khúc điểm số", pad=20)
    plt.xticks(rotation=360, ha='center', fontsize=10)
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height()), ha="center", va="bottom", fontweight='bold')
    plt.show()

    # 2. Previous Defaults Analysis (Feature Importance - Random Forest)
    le = LabelEncoder()
    rf_data = analysis_df.copy()
    rf_data['Delinquency_Enc'] = le.fit_transform(rf_data['Delinquency_Level'].astype(str))
    rf_data['Loan_Purpose_Enc'] = le.fit_transform(rf_data['Loan_Purpose'].astype(str))
    
    features = ['Credit_Score', 'Previous_Defaults', 'Income', 'LTI', 'Delinquency_Enc', 'Loan_Purpose_Enc']
    X = rf_data[features].fillna(0)
    y = rf_data['Default_Flag']
    
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X, y)
    
    feat_importance = pd.DataFrame({'Feature': features, 'Importance': rf.feature_importances_}).sort_values(by='Importance', ascending=False)
    
    plt.figure(figsize=(10, 5))
    sns.barplot(data=feat_importance, x='Importance', y='Feature', palette='viridis', hue='Feature', legend=False)
    plt.title("Các yếu tố hành vi thực tế đang chi phối rủi ro mạnh hơn Điểm tín dụng", pad=20)
    plt.show()

    # 3. Interaction (Income Bins x LTI Bins Heatmap)
    analysis_df['Income_Bin'] = pd.qcut(analysis_df['Income'], q=3, labels=['Thu nhập thấp', 'Trung bình', 'Cao'])
    analysis_df['LTI_Bin'] = pd.qcut(analysis_df['LTI'], q=3, labels=['LTI Thấp', 'Trung bình', 'LTI Cao'])
    interaction_pivot = analysis_df.pivot_table(index='Income_Bin', columns='LTI_Bin', values='Default_Flag', aggfunc='mean', observed=True) * 100
    
    plt.figure(figsize=(10, 8))
    ax = sns.heatmap(interaction_pivot, annot=True, fmt=".1f", cmap="Reds", linewidths=.5, cbar_kws={'label': 'Nợ xấu (%)'})
    
    # Rectangle cho ô rủi ro nhất
    max_val = interaction_pivot.values.max()
    for i in range(len(interaction_pivot.index)):
        for j in range(len(interaction_pivot.columns)):
            if interaction_pivot.iloc[i, j] == max_val:
                ax.add_patch(patches.Rectangle((j, i), 1, 1, fill=False, edgecolor='blue', lw=3))
                
    plt.title("Ma trận tương tác cho thấy rủi ro cực đoan tại nhóm Thu nhập thấp & LTI Cao", pad=20)
    plt.show()

    # 4. Behavioral Signals (Delinquency x Previous Defaults Heatmap)
    beh_pivot = analysis_df.pivot_table(index='Delinquency_Level', columns='Previous_Defaults', values='Default_Flag', aggfunc='mean', observed=True) * 100
    plt.figure(figsize=(12, 6))
    sns.heatmap(beh_pivot, annot=True, fmt=".1f", cmap="Reds", linewidths=.5)
    plt.title("Tín hiệu hành vi: Lịch sử vỡ nợ là biến số dự báo nợ xấu mạnh nhất", pad=20)
    plt.show()

    # 5. Risk Modeling Metrics (ROC Curve) - Đã đồng nhất phong cách

    # 5. Risk Modeling Metrics (ROC Curve, AUC, Gini)
    actual = analysis_df['Default_Flag']
    scores = -analysis_df['Credit_Score'] 
    auc_val = roc_auc_score(actual, scores)
    gini_val = 2 * auc_val - 1
    fpr, tpr, _ = roc_curve(actual, scores)
    
    plt.figure(figsize=(8, 8), dpi=100)
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {auc_val:.4f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
    plt.title(f"MODULE 5: RISK MODELING METRICS\n(AUC: {auc_val:.4f} | GINI: {gini_val:.4f})", fontsize=13, fontweight='bold')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend(loc="lower right")
    plt.grid(alpha=0.3)
    plt.show()

    # 6. Comparison Logic (Risk Orientation)
    analysis_df['Has_Prev_Defaults'] = analysis_df['Previous_Defaults'] > 0
    comparison_logic = analysis_df.groupby('Has_Prev_Defaults', observed=False)['Default_Flag'].mean().reset_index()
    comparison_logic.columns = ['Has_Previous_Defaults', 'Mean_Default_Rate']
    
    print("\n" + "="*60)
    print("MODULE 6: COMPARISON LOGIC (EVIDENCE FOR RISK ORIENTATION)")
    print("="*60)
    print(comparison_logic.to_string(index=False))
    print("="*60)
    
    return comparison_logic

# =========================================================================================
# CORE 2.2.1: BEHAVIORAL TRANSITION MATRIX (MA TRẬN DỊCH CHUYỂN HÀNH VI)
# =========================================================================================
def analyze_behavioral_transition_matrix(df):
    """
    Theo dõi sự dịch chuyển của khách hàng giữa các nhóm rủi ro.
    Phân tích nhóm nào dễ "rơi tầng" và tốc độ suy thoái hành vi.
    """
    # 1. Định nghĩa các tầng rủi ro dựa trên Credit Score (Trạng thái T0 - Lúc duyệt)
    bins = [300, 550, 650, 750, 850]
    labels = ['High Risk', 'Medium', 'Good', 'Excellent']
    
    # Giả định 'Historical_Grade' là nhóm lúc mới duyệt vay
    df['Historical_Grade'] = pd.cut(df['Credit_Score'], bins=bins, labels=labels)
    
    # 2. Xây dựng 'Current_Grade' (Trạng thái T1 - Hiện tại) dựa trên hành vi thanh toán
    def determine_current_grade(row):
        # Lấy giá trị và xử lý các giá trị trống (NaN) về 0
        prev_def = row['Previous_Defaults'] if pd.notnull(row['Previous_Defaults']) else 0
        del_freq = row.get('Delinquency_Freq', 0) if pd.notnull(row.get('Delinquency_Freq', 0)) else 0
        
        # Logic phân loại rủi ro (Risk Category) mới
        if prev_def >= 2 or del_freq >= 3:
            return 'High Risk'
        elif prev_def == 1 or del_freq == 2:
            return 'Medium'
        elif del_freq == 1:
            return 'Good'
        else:
            return 'Excellent'

    df['Current_Grade'] = df.apply(determine_current_grade, axis=1)

    # 3. Tạo Ma trận dịch chuyển (Transition Matrix)
    transition_matrix = pd.crosstab(df['Historical_Grade'], df['Current_Grade'], normalize='index') * 100
    
    # Sắp xếp lại thứ tự hiển thị để dễ quan sát (Từ rủi ro thấp đến cao)
    order = ['Excellent', 'Good', 'Medium', 'High Risk']
    transition_matrix = transition_matrix.reindex(index=order, columns=order).fillna(0)

    # 4. Trực quan hóa bằng Heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(transition_matrix, annot=True, fmt=".1f", cmap="YlOrRd", 
                linewidths=.5, cbar_kws={'label': 'Tỷ lệ dịch chuyển (%)'})
    
    plt.title("BIỂU ĐỒ 2.2.1: MA TRẬN DỊCH CHUYỂN NHÓM RỦI RO (BEHAVIORAL TRANSITION)", fontsize=14, fontweight='bold')
    plt.xlabel("Nhóm rủi ro hiện tại (Current Grade)")
    plt.ylabel("Nhóm rủi ro lúc duyệt (Historical Grade)")
    
    # Highlight đường chéo (những người giữ nguyên hạng)
    for i in range(len(order)):
        plt.gca().add_patch(patches.Rectangle((i, i), 1, 1, fill=False, edgecolor='blue', lw=3, label='Duy trì hạng' if i==0 else ""))

    plt.show()

    print("\n" + "="*80)
    print("CORE 2.2.1: INSIGHT DỊCH CHUYỂN HÀNH VI")
    print("="*80)
    print("- Đường chéo (Highlight xanh): Tỷ lệ khách hàng duy trì được uy tín tín dụng.")
    print("- Phía dưới đường chéo: Nhóm khách hàng 'rơi tầng' (Suy thoái hành vi).")
    print("- Phía trên đường chéo: Nhóm khách hàng phục hồi hoặc cải thiện điểm số.")

# =========================================================================================
# CORE 2.2.2: DELINQUENCY ESCALATION CURVE (ĐƯỜNG CONG LEO THANG RỦI RO)
# =========================================================================================
def analyze_delinquency_escalation_curve(df):
    """
    Đo lường tốc độ gia tăng nợ xấu theo số lần quá hạn (Delinquency Frequency).
    Xác định điểm bùng nổ rủi ro (Risk Explosion Threshold) để thiết lập cảnh báo sớm.
    """
    # 1. Kiểm tra và xử lý dữ liệu đầu vào
    # Sử dụng Delinquency_Freq nếu có, nếu không sử dụng Previous_Defaults làm biến thay thế tương đương
    plot_col = 'Delinquency_Freq' if 'Delinquency_Freq' in df.columns else 'Previous_Defaults'
    
    # Tính toán Bad Rate theo từng cấp độ quá hạn
    escalation = df.groupby(plot_col, observed=False)['Default_Flag'].mean().reset_index()
    escalation['Bad_Rate (%)'] = escalation['Default_Flag'] * 100
    
    # Tính toán mức tăng trưởng biên (Marginal Risk Increase)
    escalation['Risk_Jump'] = escalation['Bad_Rate (%)'].diff().fillna(0)
    
    # 2. Trực quan hóa đường cong leo thang
    plt.figure(figsize=(10, 6))
    
    # Vẽ đường hồi quy đa thức (Polynomial Regression order 2) để thấy xu hướng phi tuyến
    sns.regplot(x=plot_col, y='Bad_Rate (%)', data=escalation, 
                order=2, scatter_kws={'s':150, 'color': DEFAULT_COLOR}, 
                line_kws={'color': 'black', 'linestyle': '--', 'alpha': 0.5}, label='Trendline (Non-linear)')
    
    # Vẽ đường Line nối các điểm thực tế
    plt.plot(escalation[plot_col], escalation['Bad_Rate (%)'], marker='o', color=DEFAULT_COLOR, linewidth=3, label='Actual Bad Rate')

    # 3. Xác định Risk Explosion Threshold (Điểm bùng nổ)
    # Giả định điểm bùng nổ là nơi Risk_Jump cao nhất hoặc Bad Rate vượt ngưỡng an toàn (ví dụ 10%)
    explosion_point = escalation.loc[escalation['Risk_Jump'].idxmax()]
    threshold_val = explosion_point[plot_col]
    
    plt.axvline(x=threshold_val, color=HIGHLIGHT_RED, linestyle=':', linewidth=2)
    plt.annotate(f'EXPLOSION THRESHOLD\n(Level {threshold_val:.0f})', 
                 xy=(threshold_val, explosion_point['Bad_Rate (%)']),
                 xytext=(threshold_val + 0.2, explosion_point['Bad_Rate (%)'] + 5),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=8),
                 fontweight='bold', color=HIGHLIGHT_RED)

    plt.title("BIỂU ĐỒ 2.2.2: ĐƯỜNG CONG LEO THANG RỦI RO (DELINQUENCY ESCALATION)", fontsize=14, fontweight='bold')
    plt.xlabel(f"Số lần quá hạn ({plot_col})")
    plt.ylabel("Tỷ lệ nợ xấu thực tế (%)")
    plt.grid(True, alpha=0.2)
    plt.legend()
    plt.show()

    # 4. In insight phân tích
    print("\n" + "="*80)
    print("CORE 2.2.2: INSIGHT LEO THANG RỦI RO HÀNH VI")
    print("="*80)
    for _, row in escalation.iterrows():
        print(f"- Cấp độ {row[plot_col]:.0f}: Bad Rate = {row['Bad_Rate (%)']:.2f}% (Tăng +{row['Risk_Jump']:.2f}% so với bậc trước)")
    
    print(f"\n[KẾT LUẬN CHIẾN LƯỢC]:")
    print(f"- Ngưỡng cảnh báo sớm (Early Warning): Delinquency = {max(0, threshold_val-1):.0f}")
    print(f"- Điểm bùng nổ (Risk Explosion): Delinquency = {threshold_val:.0f}. Tại đây rủi ro tăng mạnh nhất.")
    print(f"- Khuyến nghị: Tự động khóa thẻ hoặc dừng giải ngân ngay khi khách hàng chạm ngưỡng {threshold_val:.0f}.")

# =========================================================================================
# CORE 2.2.3: BEHAVIORAL PERSISTENCE & EARLY WARNING ANALYSIS
# =========================================================================================
def analyze_behavioral_persistence_early_warning(df):
    """
    Phân tích mức độ lì rủi ro và xác định vùng cảnh báo sớm.
    Kết hợp hành vi lịch sử (Persistence) với áp lực nợ hiện tại (LTI).
    """
    # Mapping quy tắc rủi ro từ Payment_History
    RISK_MAPPING = {'POOR': 3, 'FAIR': 2, 'GOOD': 1, 'EXCELLENT': 0}

    # 1. Tính toán Behavioral Persistence Score
    # Đảm bảo Delinquency_Freq là Series trước khi tính toán
    if 'Delinquency_Freq' in df.columns:
        delinq_series = df['Delinquency_Freq']
    elif 'Payment_History' in df.columns:
        # Tạo Delinquency_Freq từ Payment_History nếu cột này tồn tại
        delinq_series = df['Payment_History'].str.upper().str.strip().map(RISK_MAPPING)
    else:
        # Trường hợp cả hai đều thiếu
        logging.warning("CORE 2.2.3: Both 'Delinquency_Freq' and 'Payment_History' are missing. Defaulting to 0.")
        delinq_series = pd.Series(0, index=df.index)

    # Lưu lại vào dataframe với kiểu Int64 nullable
    df['Delinquency_Freq'] = delinq_series.fillna(0).astype('Int64')

    # Tổng hợp số lần quá hạn và vỡ nợ trong quá khứ
    df['Persistence_Score'] = df['Previous_Defaults'].fillna(0).astype(int) + df['Delinquency_Freq'].fillna(0).astype(int)
    
    # 2. Phân đoạn LTI (Leverage) để tìm điểm gãy tài chính
    df['LTI_Tier'] = pd.qcut(df['Updated_DTI'], q=3, labels=['Low Leverage', 'Mid Leverage', 'High Leverage'], duplicates='drop')

    # 3. Xây dựng Ma trận Early Warning (Xác suất vỡ nợ thực tế)
    ew_matrix = df.pivot_table(index='Persistence_Score', columns='LTI_Tier', 
                               values='Default_Flag', aggfunc='mean', observed=True) * 100
    ew_matrix = ew_matrix.fillna(0)

    # 4. Trực quan hóa Ma trận Cảnh báo sớm
    plt.figure(figsize=(12, 7))
    ax = sns.heatmap(ew_matrix, annot=True, fmt=".1f", cmap="YlOrRd", linewidths=1, 
                cbar_kws={'label': 'Xác suất vỡ nợ hiện tại (%)'})
    
    # Vẽ khung cho "Vùng đỏ" - Early Warning Zone (Persistence >= 1 và Leverage >= Mid)
    # Tìm vị trí index của Persistence_Score >= 1 và Column >= Mid Leverage
    try:
        y_idx = [i for i, val in enumerate(ew_matrix.index) if val >= 1]
        x_idx = [i for i, val in enumerate(ew_matrix.columns) if val in ['Mid Leverage', 'High Leverage']]
        
        if x_idx and y_idx:
            rect = patches.Rectangle((min(x_idx), min(y_idx)), len(x_idx), len(y_idx), 
                                     linewidth=3, edgecolor='blue', facecolor='none', linestyle='--')
            ax.add_patch(rect)
            ax.text(0.98, 0.98, 'EARLY WARNING ZONE',
                transform=ax.transAxes,
                ha='right', va='top',
                color='white', fontweight='bold', fontsize=11,
                bbox=dict(facecolor='blue', alpha=0.6, boxstyle='round,pad=0.3'))
    except Exception as e:
        logging.warning(f"Could not draw Early Warning Box: {e}")

    plt.title("BIỂU ĐỒ 2.2.3.1: MA TRẬN CẢNH BÁO SỚM (BEHAVIORAL PERSISTENCE vs LEVERAGE)", fontsize=14, fontweight='bold')
    plt.xlabel("Mức độ đòn bẩy tài chính (LTI Tier)")
    plt.ylabel("Điểm lì hành vi (Persistence Score)")
    plt.show()

    # 5. Phân tích xu hướng theo Loan Purpose
    purpose_risk = df.groupby('Loan_Purpose', observed=True).agg({
        'Default_Flag': 'mean',
        'Persistence_Score': 'mean'
    }).reset_index()
    purpose_risk['Default_Rate (%)'] = purpose_risk['Default_Flag'] * 100

    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=purpose_risk, x='Persistence_Score', y='Default_Rate (%)', 
                    hue='Loan_Purpose', s=200, palette='viridis')
    
    # Thêm đường trung bình để phân loại mục đích vay rủi ro
    plt.axhline(purpose_risk['Default_Rate (%)'].mean(), color='red', linestyle='--', alpha=0.5)
    plt.axvline(purpose_risk['Persistence_Score'].mean(), color='red', linestyle='--', alpha=0.5)

    plt.title("BIỂU ĐỒ 2.2.3.2: TƯƠNG QUAN MỤC ĐÍCH VAY, ĐỘ LÌ HÀNH VI VÀ NỢ XẤU", fontsize=14, fontweight='bold')
    plt.xlabel("Điểm lì hành vi trung bình (Persistence Score)")
    plt.ylabel("Tỷ lệ nợ xấu (%)")
    plt.grid(True, alpha=0.2)
    plt.show()

    # 6. Thống kê quan trọng
    print("\n" + "="*80)
    print("CORE 2.2.3: INSIGHT VỀ ĐỘ LÌ HÀNH VI & CẢNH BÁO SỚM")
    print("="*80)
    
    high_persistence = df[df['Persistence_Score'] >= 2]['Default_Flag'].mean() * 100
    print(f"- Nhóm 'Lì rủi ro' (Persistence >= 2) có tỷ lệ vỡ nợ thực tế: {high_persistence:.2f}%")
    
    warning_group = df[(df['Persistence_Score'] >= 1) & (df['Updated_DTI'] > df['Updated_DTI'].median())]
    warning_rate = warning_group['Default_Flag'].mean() * 100
    print(f"- Nhóm 'Cảnh báo sớm' (Persistence >= 1 & LTI > Median) chiếm {len(warning_group)/len(df)*100:.1f}% tệp khách hàng.")
    print(f"- Tỷ lệ nợ xấu trong vùng cảnh báo: {warning_rate:.2f}%")
    
    print("\n[CHIẾN LƯỢC HÀNH ĐỘNG]:")
    print("- Cần xây dựng Behavioral Scorecard riêng cho nhóm có Persistence >= 1.")
    print("- Thắt chặt điều kiện giải ngân đối với các Loan Purpose nằm ở góc trên bên phải Biểu đồ 2.2.3.2.")

    return ew_matrix
# =========================================================================================
# CORE 2.2.4: BEHAVIORAL CLUSTERING (PHÂN NHÓM CHÂN DUNG HÀNH VI ẨN)
# =========================================================================================
def analyze_behavioral_clustering(df):
    """
    Sử dụng KMeans để tìm ra các nhóm chân dung rủi ro ẩn.
    Kết hợp PCA để trực quan hóa đa chiều lên 2D không gian.
    """
    print("\n" + "="*80)
    print("CORE 2.2.4: PHÂN NHÓM CHÂN DUNG HÀNH VI (BEHAVIORAL CLUSTERING)")
    print("="*80)

    # 1. Chuẩn bị dữ liệu
    features = ['Previous_Defaults', 'Delinquency_Freq', 'Loan_Amount', 'Updated_DTI', 'Cleaned_Income']
    X = df[features].fillna(0)
    
    # Chuẩn hóa dữ liệu (quan trọng cho KMeans)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 2. Thực hiện KMeans (Phân 3 cụm đại diện cho 3 Persona chính)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df['Behavioral_Cluster'] = kmeans.fit_predict(X_scaled)

    # 3. PCA để trực quan hóa (Giảm 5 chiều về 2 chiều)
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    df.loc[X.index, 'PCA1'] = X_pca[:, 0]
    df.loc[X.index, 'PCA2'] = X_pca[:, 1]

    plt.figure(figsize=(10, 7))
    sns.scatterplot(data=df, x='PCA1', y='PCA2', hue='Behavioral_Cluster', palette='viridis', s=100, alpha=0.7)
    plt.title("BIỂU ĐỒ 2.2.4: PHÂN CỤM PERSONA QUA PCA", fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.2)
    plt.show()

    # 4. Giải thích Cluster (Insight kỳ vọng)
    cluster_stats = df.groupby('Behavioral_Cluster', observed=True)[features + ['Default_Flag']].mean()
    print("\n[ĐẶC TRƯNG CÁC NHÓM PERSONA HÀNH VI]:")
    for i, row in cluster_stats.iterrows():
        print(f"\nNHÓM (CLUSTER) {i}:")
        if row['Previous_Defaults'] > 1.5:
            label = "Strategic Defaulters (Vỡ nợ có tính toán - Lịch sử xấu lặp lại)"
        elif row['Updated_DTI'] > 0.5 and row['Cleaned_Income'] < df['Cleaned_Income'].median():
            label = "Financial Distress (Kiệt quệ tài chính - Thu nhập thấp, nợ cao)"
        else:
            label = "Temporary Liquidity Shock (Sốc thanh khoản tạm thời - Thu nhập tốt nhưng quá hạn)"
        print(f" -> Nhãn định danh: {label}")
        print(f" -> Bad Rate: {row['Default_Flag']*100:.1f}% | Thu nhập TB: {row['Cleaned_Income']:,.0f}")

    return cluster_stats

# =========================================================================================
# CORE 2.2.5: PORTFOLIO CONCENTRATION RISK (RỦI RO TẬP TRUNG DƯ NỢ)
# =========================================================================================
def analyze_portfolio_concentration_risk(df):
    """
    Đo lường mức độ tập trung dư nợ để phát hiện rủi ro hệ thống.
    Sử dụng Treemap và Bubble Chart để xác định vùng dễ gây Liquidity Crisis.
    """
    print("\n" + "="*80)
    print("CORE 2.2.5: PHÂN TÍCH RỦI RO TẬP TRUNG (PORTFOLIO CONCENTRATION)")
    print("="*80)

    # 1. Tính toán Bad Rate theo Mục đích vay và Xếp hạng rủi ro
    conc_df = df.groupby(['Loan_Purpose', 'Risk_Rating'], observed=True).agg({
        'Loan_Amount': 'sum',
        'Default_Flag': 'mean',
        'id': 'count'
    }).reset_index()
    conc_df.columns = ['Loan_Purpose', 'Risk_Rating', 'Total_Loan_Amount', 'Bad_Rate', 'Customer_Count']
    conc_df['Bad_Rate (%)'] = conc_df['Bad_Rate'] * 100

    # 2. Treemap Visualization
    fig = px.treemap(conc_df, 
                     path=['Loan_Purpose', 'Risk_Rating'], 
                     values='Total_Loan_Amount',
                     color='Bad_Rate (%)',
                     color_continuous_scale='RdYlGn_r',
                     title='BIỂU ĐỒ 2.2.5.1: TREEMAP TẬP TRUNG DƯ NỢ & TỶ LỆ NỢ XẤU')
    fig.show()

    # 3. Bubble Chart (Exposure vs Risk)
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=conc_df, x='Total_Loan_Amount', y='Bad_Rate (%)', 
                    size='Customer_Count', hue='Loan_Purpose', sizes=(100, 2000), alpha=0.6)
    
    # Ngưỡng cảnh báo rủi ro hệ thống (Bad rate trung bình)
    plt.axhline(conc_df['Bad_Rate (%)'].mean(), color='red', linestyle='--', alpha=0.5)
    plt.title("BIỂU ĐỒ 2.2.5.2: TƯƠNG QUAN DƯ NỢ, QUY MÔ KH VÀ RỦI RO", fontsize=14, fontweight='bold')
    plt.xlabel("Tổng dư nợ (Total Exposure)")
    plt.ylabel("Tỷ lệ nợ xấu thực tế (%)")
    plt.grid(True, alpha=0.2)
    plt.show()

    # 4. Cảnh báo
    top_exp = conc_df.sort_values(by='Total_Loan_Amount', ascending=False).iloc[0]
    print(f"- CẢNH BÁO TẬP TRUNG: Nhóm '{top_exp['Loan_Purpose']}' đang chiếm tỷ trọng dư nợ lớn nhất.")
    print(f"- Rủi ro thanh khoản: Vùng có Bad Rate cao và Exposure lớn là vùng nguy hiểm nhất.")

# =========================================================================================
# CORE 2.2.6: EXPLAINABLE AI FOR BEHAVIORAL RISK (XAI)
# =========================================================================================
def analyze_explainable_behavioral_risk(df):
    """
    Sử dụng XGBoost và SHAP Values để giải thích tại sao khách hàng bị coi là rủi ro.
    Minh bạch hóa các biến số tác động mạnh nhất đến hành vi.
    """
    print("\n" + "="*80)
    print("CORE 2.2.6: GIẢI THÍCH MÔ HÌNH RỦI RO (EXPLAINABLE AI - SHAP)")
    print("="*80)

    # 1. Huấn luyện mô hình XGBoost nhanh để lấy đặc trưng hành vi
    features = ['Credit_Score', 'Previous_Defaults', 'Delinquency_Freq', 'Updated_DTI', 'Cleaned_Income', 'Loan_Amount']
    X = df[features].fillna(0)
    y = df['Default_Flag']

    model = xgb.XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42)
    model.fit(X, y)

    # 2. Tính toán SHAP Values
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)
    
    # Xử lý SHAP values cho binary classification (nếu trả về list thì lấy class 1)
    if isinstance(shap_values, list) and len(shap_values) == 2:
        shap_values = shap_values[1]

    # 3. Trực quan hóa Summary Plot
    plt.figure(figsize=(10, 6))
    plt.title("BIỂU ĐỒ 2.2.6.1: TÁC ĐỘNG CỦA CÁC BIẾN ĐẾN XÁC SUẤT NỢ XẤU (SHAP SUMMARY)")
    shap.summary_plot(shap_values, X, show=False)
    plt.show()

    # 4. Trọng số ảnh hưởng thực tế (%)
    importance = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False)
    plt.figure(figsize=(10, 5))
    ax = sns.barplot(x=importance.values * 100, y=importance.index, palette='rocket')
    
    for p in ax.patches:
        ax.annotate(f"{p.get_width():.1f}%", (p.get_width(), p.get_y() + p.get_height()/2), 
                    ha="left", va="center", fontweight='bold', color='darkred')

    plt.title("BIỂU ĐỒ 2.2.6.2: TRỌNG SỐ TÁC ĐỘNG CỦA CÁC BIẾN HÀNH VI (%)", fontsize=12, fontweight='bold')
    plt.xlabel("Mức độ đóng góp (%)")
    plt.show()

    # 5. Insight
    top_feat = importance.index[0]
    print(f"- Biến số chi phối mạnh nhất: {top_feat} ({importance.iloc[0]*100:.1f}%)")
    print(f"- Ý nghĩa: Giải thích chính xác tại sao khách hàng bị hệ thống chấm điểm thấp.")
    print("- Tính ứng dụng: Cung cấp bằng chứng cho hội đồng tín dụng khi thẩm định hồ sơ.")

    return importance

 # Thực thi phân tích profiling
def run_analysis(df):
    # ==========================================================================
    # CORE 1: CAPACITY ANALYSIS (PHÂN TÍCH NĂNG LỰC TRẢ NỢ)
    # ==========================================================================
    analyze_dti_foundations(df)
    analyze_overall_dti(df)
    analyze_income_kpi(df)
    analyze_specific_lti(df)
    analyze_ipd(df)
    descriptive_analysis(df)
    analyze_behavioral_persistence_early_warning(df)
    analyze_behavioral_clustering(df)
    analyze_portfolio_concentration_risk(df)
    analyze_explainable_behavioral_risk(df)

    # ==========================================================================
    # CORE 2: CHARACTER ANALYSIS (PHÂN TÍCH ĐIỂM TÍN DỤNG - HỆ THỐNG CŨ)
    # ==========================================================================
    analyze_credit_score_discriminatory_power(df)
    analyze_behavioral_transition_matrix(df)
    analyze_advanced_risk_modules(df)
    analyze_delinquency_escalation_curve(df)

    # ==========================================================================
    # EXTENDED ANALYSIS (PHẦN MỞ RỘNG & DỰ BÁO)
    # ==========================================================================
    plot_demographics_risk(df)
    plot_financial_depth(df)
    analyze_profiling_averages(df)

if __name__ == "__main__":
    # Thực thi toàn bộ pipeline
    run_analysis(df)

 
 