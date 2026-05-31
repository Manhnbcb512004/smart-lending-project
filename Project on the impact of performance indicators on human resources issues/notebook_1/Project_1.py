# === 1. LIBRARIES ===
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns 

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
 
# ML nâng cao (OPTIONAL – chỉ chạy khi cần)
import xgboost as xgb
import shap

# === 2. LOAD DATA ===
# === Data gốc ===
df_goc = pd.read_csv("Cleaned_HR_Data_Analysis (1).csv",sep=",") 
print(df_goc)

df = pd.read_csv("pjhieusuat.csv", sep=";")  # bỏ sep
print(df.shape)
print(df.isnull().sum())
# Chạy lại df.info() để kiểm tra kết quả
print("--- Bảng số liệu tổng quát về tình hình hiệu xuất của doanh nghiệp và các chỉ số liên quan ---")
print(df)

# ============================================================
# SECTION 3: PAYZONE – PERFORMANCE – ENGAGEMENT ANALYSIS
# Mục tiêu:
# - Đánh giá mối quan hệ giữa lương (PayZone) và hiệu suất thực tế
# - Kiểm tra giả định: Lương cao có thực sự đi kèm hiệu suất & động lực cao?
# ============================================================
# phân nhóm 
group_per = df.groupby("PayZone")["Performance Score"].value_counts()
print(f"Phân nhóm cho chỉ số thể hiện là: {group_per}")
# KPI 1: Performance Distribution by PayZone
# Ý nghĩa:
# - Phân tích cơ cấu hiệu suất (Exceeds, Fully Meets, Needs Improvement, PIP)
#   trong từng vùng lương (PayZone)
# - Trả lời câu hỏi: PayZone cao có thực sự tập trung nhiều nhân sự hiệu suất cao? 
def performance_distribution_by_payzone(df):
    return (
        df.groupby("PayZone")["Performance Score"]
        .value_counts(normalize=True)
        .mul(100)
        .round(2)
        .reset_index(name="Percentage")
    )
perf_dist = performance_distribution_by_payzone(df)
print(perf_dist)
# === VISUALIZATION - KPI 1 ===
plt.figure(figsize=(10,6))
sns.barplot(
    data=perf_dist,
    x="PayZone",
    y="Percentage",
    hue="Performance Score"
)
plt.title("KPI 1 - Performance Distribution by PayZone (%)")
plt.ylabel("Tỷ lệ (%)")
plt.xlabel("PayZone")
plt.legend(title="Performance Score")
plt.tight_layout()

# KPI 2: Exceeds Ratio by PayZone
# Ý nghĩa:
# - Đo lường tỷ trọng nhân sự Xuất sắc (Exceeds) trong từng PayZone
# - Kiểm tra mức độ tập trung nhân tài theo vùng lương
# - Phát hiện nguy cơ trả lương cao nhưng không tạo ra khác biệt hiệu suất 
def exceeds_by_payzone(df):
    xs = df[df["Performance Score"].str.strip() == "Exceeds"]
    summary = xs["PayZone"].value_counts().to_frame("Count")
    summary["Percentage"] = summary["Count"] / summary["Count"].sum() * 100
    return summary.round(2)

# Gộp lại thành bảng để xem 
result_xs = exceeds_by_payzone(df)
print("Thống kê trong nhóm Payzone = Exceeds")
print(result_xs)
 

# KPI 3: Performance Mix across PayZones (%)
# Ý nghĩa:
# - Với mỗi mức hiệu suất, phân bổ nhân sự đang nằm ở PayZone nào
# - Là nền tảng để vẽ biểu đồ cột chồng (% stacked bar)
# - Phát hiện các nhóm bất thường (ví dụ: PIP nhưng vẫn ở Zone A)
def performance_ratio_by_group(df):
    stat = (
        df.groupby(["Performance Score", "PayZone"])
        .size()
        .reset_index(name="Count")
    )
    stat["Percentage"] = stat.groupby("Performance Score")["Count"] \
        .transform(lambda x: x / x.sum() * 100)
    return stat.round(2)

thong_ke = performance_ratio_by_group(df)
plot_data = thong_ke.pivot(
    index="Performance Score",
    columns="PayZone",
    values="Percentage"
)


# Insight sơ bộ:
# - Phân bổ PayZone theo từng nhóm hiệu suất 
# 1 xoay bảng dữ liệu để vẽ cột chồng 
# 2 Vẽ biểu đồ
ax = plot_data.plot(kind="bar",stacked=True,figsize=(10,6),colormap="viridis")

# 3 thêm các chi tiết cho biểu đồ 
plt.title("Tỷ lệ % các PayZone theo nhóm hiệu suất",fontsize=15)
plt.xlabel("Nhóm hiệu suất",fontsize=12)
plt.ylabel("Tỷ lệ (%)",fontsize=12)
plt.xticks(rotation=0) # để chữ nằm ngang 
plt.legend(title="PayZone",bbox_to_anchor=(1.05,1),loc="upper left")

# 4 hiển thị con số % trực tiếp trên cột 
for p in ax.patches:
    width,height = p.get_width(), p.get_height()
    if height > 0: # chỉ hiện nếu tỷ lệ > 0 
        x,y = p.get_xy()
        ax.text(x + width/2,y + height/2,f"{height:.1f}%",ha="center",va="center",color="white",fontweight="bold")

plt.tight_layout() 
plt.show()
 
# KPI 4: Engagement Score by PayZone
# Ý nghĩa:
# - Đo lường mức độ gắn kết trung bình của nhân viên theo từng PayZone
# - So sánh động lực giữa các vùng lương
# - Phát hiện PayZone lương cao nhưng Engagement không tương xứng
def engagement_summary(df):
    avg = df.groupby("PayZone")["Engagement Score"].mean()
    contrib = df.groupby("PayZone")["Engagement Score"].sum() / df["Engagement Score"].sum()
    return avg.round(2), (contrib * 100).round(2)

avg_eng, eng_contrib = engagement_summary(df)
print(avg_eng)
print(eng_contrib)


# KPI 5 (Supporting): Engagement Deviation vs Zone Mean
# Ý nghĩa:
# - Đếm số nhân viên có Engagement Score cao/thấp hơn mức trung bình của PayZone
# - Phát hiện sự phân hóa nội bộ trong từng vùng lương
# - Hỗ trợ quyết định can thiệp nhân sự (coaching / giữ chân / tái cấu trúc)
def count_relative_to_mean(df):
    # NHóm theo Payzone và tính toán cho mỗi nhóm 
    results = {}
    # Lấy danh sách các Zone duy nhất 
    zones = df["PayZone"].unique()

    for zone in zones:
        # lọc dữ liệu theo từng Zone 
        zone_data = df[df["PayZone"] == zone]["Engagement Score"]

        # Tính trung bình Zone đó 
        avg = zone_data.mean()

        # đếm số lượng 
        above_avg = (zone_data > avg).sum()
        below_avg = (zone_data < avg).sum()
        equal_avg = (zone_data == avg).sum() # trường hợp đúng trung bình 

        results[zone] = {
            "Average":round(avg,2),
            "Above Mean":above_avg,
            "Below Mean":below_avg,
            "Equal Mean":equal_avg
        }

    return pd.DataFrame(results).T
# Sử dụng hàm 
analysis_df = count_relative_to_mean(df)
print(analysis_df)
 
# Phân tích chỉ số này theo 3 chỉ tiêu 
# PayZone,Performance Score,và Engagement Score

# KPI 6 (Drill-down): Engagement Summary by PayZone × Performance
# Ý nghĩa:
# - Phân rã Engagement theo từng tổ hợp Lương × Hiệu suất
# - So sánh Mean vs Median để phát hiện phân phối lệch
# - Cơ sở phát hiện nhóm trả lương cao nhưng Engagement kém

analysis_table = df.groupby(["PayZone","Performance Score"]).agg({
    "Engagement Score":["mean","median","count"]
}).reset_index()
# Làm bảng đẹp hơn 
analysis_table.columns = ["PayZone","Performance Score","Avg_Engagement","Median_Engagement","Employee_Count"]
print("--- BẢNG PHÂN TÍCH TỔNG HỢP 3 CHỈ TIÊU ---")
print(analysis_table)
# Insight – KPI 6:
# - Nhóm PIP tại Zone A có Avg Engagement > Median → còn động lực cải thiện
# - Nhóm Exceeds tại Zone A có Avg < Median → dấu hiệu phân hóa nội bộ
# - Hàm ý: Lương cao không đảm bảo gắn kết đồng đều



# KPI 7: Engagement Skew & Detractor Analysis
# Ý nghĩa:
# - Xác định nhóm nhân sự kéo tụt Engagement
# - Phát hiện rủi ro ẩn trong từng PayZone × Performance
print("Danh sách cột thực tế trong file:", df.columns.tolist())
def analyze_group_impact(df, zone, performance):
    group = df[
        (df["PayZone"] == zone) &
        (df["Performance Score"] == performance)
    ] 
    if group.empty:
        print(f"(!) Không có dữ liệu cho nhóm {zone} - {performance}")
        return
    n = len(group)
    avg = group["Engagement Score"].mean()
    median =group["Engagement Score"].median()
    std_dev = group["Engagement Score"].std()

    # Phân tích tỷ lệ các mức điểm ( giả sử thang điểm 1-5)
    score_counts = group["Engagement Score"].value_counts(normalize=True).sort_index()*100

    # xác định nhóm kéo lùi (Detractors) - Những người có điểm thấp hơn trung vị
    detractors = group[group["Engagement Score"] < median]
    detractor_pct = (len(detractors) / n) * 100

    # In kết quả phân tích 
    print(f"=== Phân tích nhóm :{zone} | HIỆU SUẤT:{performance} ===")
    print(f"Số lượng nhân sự: {n} người")
    print(f"Chỉ số: Trung bình = {avg:.3f} | Trung vị = {median:.0f}")

    if avg < median:
        print(f"Cảnh báo: Trung bình THẤP HƠN trung vị. Nhóm đang bị lệch trái(Negative SKew).")
        print(f"Nguyên nhân: có {len(detractors)} nhân viên ({detractor_pct:.1f}%) có mức gắn kết thấp kéo điểm số xuống")
    else:
        print(f"TRẠNG THÁI: Trung bình ổn định so với trung vị")

    print(f"Chi tiết phân bổ điểm số (%):")
    for score,pct in score_counts.items():
        print(f" - Điểm {score}:{pct:.1f}%")
        
        
    print("-" * 50)
# 1. Danh sách chuẩn (Đã khớp với dữ liệu thực tế)
zones = ["Zone A", "Zone B", "Zone C"]
perf_scores = ["Exceeds", "Fully Meets", "Needs Improvement", "PIP"]

# 2. Chuẩn hóa dữ liệu trước khi chạy để loại bỏ khoảng trắng thừa
df["PayZone"] = df["PayZone"].astype(str).str.strip()
df["Performance Score"] = df["Performance Score"].astype(str).str.strip()

# 3. Vòng lặp thực thi
for z in zones:
    print(f"\n>>> ĐANG PHÂN TÍCH VÙNG LƯƠNG {z} <<<")
    for p in perf_scores:
        # Gọi hàm analyze_group_impact đã định nghĩa của bạn
        analyze_group_impact(df, z, p)

# Phân tích chi tiết về chỉ số này
show_value = df["Satisfaction Score"]
nhom_hailong = df.groupby("PayZone")["Satisfaction Score"].mean()
tong_hailong = df["Satisfaction Score"].sum()
nhom_hailong_pct  = (df.groupby("PayZone")["Satisfaction Score"].sum() / tong_hailong)*100
print(nhom_hailong_pct)
# thống kê mô tả chi tiết 
# Thay vì chỉ tính mean, ta tính tính thêm Median và Std để xem độ biến đôngj
payzone_stats = df.groupby("PayZone")["Satisfaction Score"].agg(["mean","median","std","count"]).reset_index()

# 2 tính % đóng góp của mỗi zone vào tổng diểm hài lòng
payzone_stats["pct_total_score"] = (df.groupby("PayZone")["Satisfaction Score"].sum().values / tong_hailong)*100

print("--- Thống kê hài lòng theo PayZone ---")
# 3 phân tích mức ảnh hưởng của performance Score
# sắp xếp thứ tự ảnh hưởng


# bảng chéo: Trung bình điểm hài lòng theo cả PayZone
impact_analysis = df.pivot_table(index="Performance Score",
                                 columns="PayZone",
                                 values="Satisfaction Score",
                                 aggfunc="mean")

print("\n--- Điểm hài lòng trung bình theo hiệu suất và vùng lương ---")
print(impact_analysis)
overall_std = df["Satisfaction Score"].std()
print(f"Độ phân tán tổng thể (Std Dev): {overall_std:.2f}")


# KPI 8: Satisfaction Score by PayZone
# Ý nghĩa:
# - Đánh giá mức độ hài lòng theo vùng lương
# - Phát hiện PayZone có rủi ro hài lòng thấp

# Trực quan hóa (tùy chọn nhưng rất quan trọng trong phân tích)
plt.figure(figsize=(10,6))
sns.boxplot(x="PayZone",y="Satisfaction Score", data=df, palette="Set2")
plt.title("Phân bổ điểm hài lòng theo PayZone")
plt.show()
 
# KPI 9: Low Satisfaction Rate by PayZone
# KPI 10: Satisfaction Distribution by PayZone × Performance
# Ý nghĩa:
# - Phân tích mức độ hài lòng thấp theo PayZone & Performance
# - Xác định nhóm có nguy cơ nghỉ việc / giảm hiệu suất

# 1.Tính số lượng và % nhân viên theo PayZone
zone_counts = df["PayZone"].value_counts().reset_index()
zone_counts.columns = ["PayZone","Count"]
zone_counts["Percentage"] = (zone_counts["Count"] / len(df)) * 100

# 2. Tính % nhân viên Hài thấp ( ví dụ score <= 2) theo từng nhóm
# Giả sử Satisfaction Score từ 1 đến 5
low_sat = df[df["Satisfaction Score"] <= 2].groupby("PayZone").size() / df.groupby("PayZone").size() *100

print("--- Cơ cấu nhân sự theo zone ---")
print(low_sat)
# với tỷ lệ thấp hơn 2 thấp nhất ở nhóm này ta có thể thấy nằm chủ yếu ở nhóm Zone A có chỉ số Hài lòng thấp 
# giờ chúng ta sẽ phân tích chi tiết chỉ số này theo mức hiệu xuất và mức độ hài lòng để thấy rõ vấn đề
# Zone A theo nhóm hiệu xuất và mức độ hài lòng  

# gom nhóm để phân tích 
# Tạo bảng pivot table để dễ quan sát 
pivot_report = pd.pivot_table(
    df,
    values="Employee ID",
    index=["PayZone","Performance Score"],
    columns="Satisfaction Score",
    aggfunc="count",
    fill_value=0
)
# Tính tổng số lượng nhân viên cho mỗi nhóm(Hàng)
pivot_report["Total_Employees"] = pivot_report.sum(axis=1)

# 3 Tính tỷ lệ phần trăm cho từng mức hài lòng 
# ta lấy từng cột (1-5) chia cho cột total_Employees
pivot_percent = pivot_report.iloc[:,0:5].div(pivot_report["Total_Employees"],axis=0)*100
pivot_percent_formatted = pivot_percent.round(1).astype(str) + "%"
# Làm tròn chữ số lên 1 chữ số 

# In ra kết quả 
print("--- Báo cáo phân nhóm chi tiết ---")
print(pivot_report)

print("\n--- Bảng 2: Tỷ lệ phần trăm hài lòng trong mỗi nhóm")
print(pivot_percent_formatted)
# === VISUALIZATION - KPI 10 ===
fig, ax = plt.subplots(figsize=(12,6))
sns.heatmap(
    pivot_percent,
    annot=True,
    fmt=".1f",
    cmap="YlGnBu",
    linewidths=0.5,
    linecolor="white",
    ax=ax
)
ax.set_title("KPI 10 - Satisfaction Distribution by PayZone x Performance Score (%)")
ax.set_xlabel("Satisfaction Score")
ax.set_ylabel("PayZone x Performance")


plt.tight_layout()
# =========================================================
# KPI EXTENSION – WORKFORCE EFFICIENCY & FINANCIAL RISK
# ---------------------------------------------------------
# Objective:
# - Combine Performance & Salary into efficiency_ratio
# - Segment workforce into High ROI / Balanced / High Risk
# - Identify hidden financial and retention risks
#
# Note:
# This is NOT a core KPI, but a synthesis layer
# built on top of KPI 1–10 for executive decision-making
# =========================================================

# Đọc file bỏ qua quotechar để Pandas có thể tách cột dựa trên dấu phẩy bên trong ngoặc kép
df_2 = pd.read_csv(
    "HR_phantich_luong.csv",
    sep=",",
    engine="python",
    quoting=3 # csv.QUOTE_NONE
).apply(lambda x: x.str.replace('"', '').str.strip() if x.dtype == "object" else x)

# Làm sạch tên cột và chuyển đổi kiểu dữ liệu số
df_2.columns = df_2.columns.str.replace('"', '').str.replace("'", "").str.strip()
numeric_cols = ["so_luong_nv", "avg_performance_point", "efficiency_ratio"]
for col in numeric_cols:
    if col in df_2.columns:
        df_2[col] = pd.to_numeric(df_2[col], errors='coerce')

print(df_2.head())
 
# Step 1 – Workforce Value Segmentation
# Classify employees based on performance-to-cost efficiency
# 1 gom nhóm giá trị cao (segmentation)
# Nhóm giá trị cao (high Value): hiệu suất cao, chi phí thấp (ration cao)
# Nhóm rủi ro (low value): hiệu suất thấp chi phí cao (ratio thấp)
df_2["Value_Group"] = np.select(
    [
        df_2["efficiency_ratio"] >= 2.0,
        df_2["efficiency_ratio"].between(1.0, 2.0)
    ],
    [
        "Giá trị cao (High ROI)",
        "Giá trị ổn định"
    ],
    default="Giá trị thấp / rủi ro (High Cost)"
)
print("--- Thống kê theo nhóm giá trị")
summary = df_2.groupby("Value_Group").agg({
    "so_luong_nv": "sum",
    "avg_performance_point": "mean",
    "efficiency_ratio": "mean"
}).reset_index()
print(summary)

# 2. Hàm dự báo rủi ro (Đã sửa lỗi cú pháp chuỗi f-string)
# Cấu hình để hiện rõ nội dung, không bị dấu "..."
# Xóa bỏ giới hạn độ rộng của từng ô (để hiện hết chữ trong risk_forecast)
pd.set_option('display.max_colwidth', None)

# Hiện toàn bộ các cột, không bỏ bớt cột nào ở giữa
pd.set_option('display.max_columns', None)

# Hiện toàn bộ các dòng (nếu bảng dài, nó sẽ không hiện dấu ...)
pd.set_option('display.max_rows', None)

# Ép bảng hiển thị trên một dòng dài, không tự động xuống dòng (tránh bị vỡ bảng)
pd.set_option('display.expand_frame_repr', False)

# Step 2 – Risk Forecasting
# Detect budget risk (low efficiency) and retention risk (high efficiency)
df_2["risk_forecast"] = "ổn định"
df_2.loc[df_2["efficiency_ratio"] < 1.0, "risk_forecast"] = \
    "Rủi ro cao: Thâm hụt ngân sách do hiệu quả thấp"

df_2.loc[df_2["efficiency_ratio"] > 2.5, "risk_forecast"] = \
    "Rủi ro chảy máu chất xám: lương thấp so với năng lực"
# Step 3 – Visualization
# Compare workforce efficiency and risk structure across PayZones
# 3. Vẽ biểu đồ mô tả thực trạng 
plt.figure(figsize=(12,6))

# Biểu đồ cột thể hiện tương quan hiệu suất 
sns.barplot(
    data=df_2,
    x="PayZone",
    y="efficiency_ratio",
    hue="Value_Group",
    palette="viridis")
plt.axhline(1.0, linestyle="--", color="red", label="Điểm hòa vốn (ratio = 1)")
plt.title("Workforce Efficiency & Risk Segmentation by PayZone", fontsize=14)
plt.ylabel("Efficiency Ratio (Performance / Cost)")
plt.legend(bbox_to_anchor=(1.05,1), loc="upper left")
plt.tight_layout()
plt.show()
# Xuất bảng phân tích rủi ro hiện rõ chư
print("\n--- BẢNG PHÂN TÍCH RỦI RO CHI TIẾT ---")
print(df_2[["PayZone", "avg_performance_point", "efficiency_ratio", "risk_forecast"]])

# =========================================================
# WORKFORCE ANALYSIS BY AGE GROUP
# ---------------------------------------------------------
# Objective:
# - Analyze workforce structure and performance by age group
# - Identify risk of turnover, promotion potential, and retention issues
# - Support HR strategic planning and succession management
# =========================================================

# Load aggregated HR dataset by age group
df_3 = pd.read_csv("PT_Tuoi.csv",sep=",")
print(df_3)

# ---------------------------------------------------------
# Utility Function:
# Calculate internal workforce distribution (%) within each age group
# This helps identify dominant performance segments per age cohort
# --------------------------------------------------------- 
def process_group_stats(df_group):
    total_nv = df_group["so_luong_nv"].sum()
    df_group["percentage_nv"] = round((df_group["so_luong_nv"] / total_nv) * 100,2)  
    return df_group

# ---------------------------------------------------------
# Age Group 1: Startup / Early Career (18–25)
# Focus:
# - Identify turnover risk among young talents
# - Detect early burnout or disengagement signals
# ---------------------------------------------------------
def evaluate_turnover_risk(row):
    # High turnover risk:
    # - High performers (Exceeds) with very high efficiency_ratio
    #   → performance significantly exceeds compensation
    if row["PerformanceScore"] == "Exceeds" and row["efficiency_ratio"] > 2.0:
        return "Rủi ro nghỉ việc cao (Nhân tài cần điều chỉnh lương ngay)"
    # Workforce pressure risk:
    # - Low or underperforming employees in early career stage
    elif row["PerformanceScore"] in ["PIP","Needs Improvement"]:
        return "Rủi ro từ bỏ cao (Áp lực công việc)"
    return "ổn định"

df_khoi_nghiep = df_3[df_3["Age_group"] == "Nhóm Khởi nghiệp"].copy()
df_khoi_nghiep = process_group_stats(df_khoi_nghiep)
df_khoi_nghiep["Danh_gia_rui_ro"] = df_khoi_nghiep.apply(evaluate_turnover_risk, axis=1)

# ---------------------------------------------------------
# Age Group 2: Growth / Acceleration Stage (25–35)
# Focus:
# - Identify promotion readiness
# - Build leadership pipeline and succession candidates
# ---------------------------------------------------------
def predict_promotion_potentital(row):
    # High promotion readiness:
    # - Sustained high performance with optimal cost-efficiency 
    if row["PerformanceScore"] == "Exceeds" and row["efficiency_ratio"] >= 1.8:
        return "Sẵn sàng thăng tiến (High Potential)"
    
    # Medium-term successor candidates
    elif row["PerformanceScore"] == "Fully Meets" and row["efficiency_ratio"] > 1.5:
        return "Tiềm năng kế thừa"
    return "Cần bồi dưỡng thêm"

 
df_but_pha = df_3[df_3["Age_group"] == "Nhóm Bứt phá"].copy()
df_but_pha = process_group_stats(df_but_pha)
df_but_pha["Du_bao_thang_tien"] = df_but_pha.apply(predict_promotion_potentital,axis=1)

# ---------------------------------------------------------
# Age Group 3: Advisor / Core Workforce (36–55)
# Focus:
# - Retention of key contributors
# - Identify skill stagnation or capacity erosion risks
# ---------------------------------------------------------
def advisor_volatility(row):
    # Key retention targets:
    # - Experienced employees with consistently high performance 
    if row["PerformanceScore"] == "Exceeds":
        return "Trọng tâm giữ chân (Key Person)"
    
    # Capability erosion risk:
    # - Medium to low performers at senior age bands
    elif row["PerformanceScore"] in ["Needs Improvement","PIP"]:
        return "Nguy cơ thâm hụt năng lực" 
    return "Duy trì ổn định"

df_co_van = df_3[df_3["Age_group"] == "Nhóm Cố vấn"].copy()
df_co_van = process_group_stats(df_co_van)
df_co_van["Bien_dong_nhan_su"] = df_co_van.apply(advisor_volatility,axis=1)
  
# ---------------------------------------------------------
# Age Group 4: Leadership / Management (55+)
# Focus:
# - Leadership retention and succession risk
# - Detect burnout or external headhunting exposure
# ---------------------------------------------------------
def leadership_engagement(row):
    # Leadership attrition risk:
    # - Very high contribution but under-compensated leadership
    if row["PerformanceScore"] == "Exceeds" and row["efficiency_ratio"] >= 2.5:
        return "Nguy cơ rời bỏ (burnout hoặc săn đầu người)"
    
    # Replacement requirement:
    elif row["PerformanceScore"] == "PIP":
        return "Cần thay thế vị trí quản trị nhân sự"
    return "gắn bó bền vững"

df_quan_tri = df_3[df_3["Age_group"] == "Nhóm Quản trị"].copy()
df_quan_tri = process_group_stats(df_quan_tri)
df_quan_tri["Du_bao_gan_bo"] = df_quan_tri.apply(leadership_engagement,axis=1)

 
# ---------------------------------------------------------
# Output Summary Tables for Insight Validation
# These tables support qualitative insights in the HR report
# ---------------------------------------------------------
print("--- 1. Nhóm khời nghiệp ---")
print(df_khoi_nghiep[["PerformanceScore","percentage_nv","efficiency_ratio","Danh_gia_rui_ro"]])

print("\n --- 2. NHóm bứt phá ---")
print(df_but_pha[["PerformanceScore","percentage_nv","efficiency_ratio","Du_bao_thang_tien"]])  

print("\n --- 3. Nhóm cố vấn ---")
print(df_co_van[["PerformanceScore","percentage_nv","efficiency_ratio","Bien_dong_nhan_su"]])

print("\n --- 4. Nhóm quản trị ---")  
print(df_quan_tri[["PerformanceScore","percentage_nv","efficiency_ratio","Du_bao_gan_bo"]])

# ================= HEATMAP: Efficiency Ratio =================
# Insight tổng hợp: Hiệu quả chi phí theo Nhóm tuổi × Hiệu suất
heatmap_data = df_3.pivot_table(
    index="Age_group",
    columns="PerformanceScore",
    values="efficiency_ratio",
    aggfunc="mean"
)

plt.figure(figsize=(10,6))
sns.heatmap(
    heatmap_data,
    annot=True,
    fmt=".2f",
    cmap="RdYlGn",
    linewidths=0.5
)
plt.title("Heatmap - Efficiency Ratio theo nhóm tuổi & Hiệu suất")
plt.ylabel("Nhóm tuổi")
plt.xlabel("Mức độ hoàn thành")
plt.tight_layout()
plt.show()

# 2 Biểu đồ 1: Phân bố số lượng nhân viên theo nhóm tuổi và hiệu suất
import plotly.io as pio
pio.renderers.default = "browser"   # mở trực tiếp bằng trình duyệt ngoài

fig1 = px.bar(
    df_3,
    x="Age_group",
    y="so_luong_nv",
    color="PerformanceScore",
    title="Phân bố số lượng nhân viên theo nhóm tuổi & Mức độ hoàn thành",
    barmode="group",
    text_auto=True
)
fig1.show()

# 3. Biểu đồ 2: Xu hướng hiệu quả
df_trend = df_3.groupby("Age_group").agg({
    "efficiency_ratio":"mean",
    "so_luong_nv":"sum"
}).reset_index().sort_values(by="efficiency_ratio", ascending=False)

fig2 = px.line(
    df_trend,
    x="Age_group",
    y="efficiency_ratio",
    markers=True,
    title="Xu hướng chỉ số hiệu quả (Efficiency Ratio) trung bình theo Nhóm tuổi",
    hover_data=["so_luong_nv"]
)
fig2.update_traces(line_color="red", line_width=3)
fig2.show()

# Phân tích nhanh
print("--- PHÂN TÍCH NHANH ---")
top_eff = df_trend.iloc[0]
print(f"1. Nhóm có hiệu quả tiềm năng nhất: {top_eff['Age_group']} ({top_eff['efficiency_ratio']:.2f})")
co_van_nv = df_3.loc[df_3["Age_group"]=="Nhóm Cố vấn", "so_luong_nv"].sum()
print(f"2. Nhóm cố vấn có quy mô nhân sự lớn nhất ({co_van_nv} người), cần tập trung tối ưu nhóm này")

# ---------------------------------------------------------
# Performance-Based Attrition Analysis
# Objective:
# - Analyze workforce structure by Performance Score
# - Detect attrition concentration by performance level
# - Evaluate retention risk across performance tiers
# ---------------------------------------------------------
# Step 1: Load processed performance dataset
df_4 = pd.read_csv("nv_hieusuat.csv",sep=",")
print(df_4)
# Step 2: Reshape data for stacked bar visualization
# Index: Performance Score
# Columns: Employee Status (Active / Terminated)
# Values: Percentage within each performance group
pivot_df = df_4.pivot(index="PerformanceScore",
                      columns="EmployeeStatus",
                      values="phan_tram_theo_nhom")
print(pivot_df.sum(axis=1))

# Step 3: Reorder performance levels (High → Low)
order = ["Exceeds","Fully Meets","Needs Improvement","PIP"]
pivot_df = pivot_df.reindex(order)

# Step 4: Visualize internal attrition structure by performance tier
# This chart shows the proportion of Active vs Terminated
# within each performance category 
# ---------------------------------------------------------
# Step 4: Add percentage labels directly inside stacked bars
pivot_df = pivot_df.reindex(columns=["Active","Terminated"], fill_value=0)
pivot_df = pivot_df.fillna(0)

ax = pivot_df.plot(kind="bar",
                   stacked=True,
                   figsize=(10,6),
                   color=["#2ecc71","#e74c3c"], # màu xanh cho active, đỏ cho Terminated
                   width=0.7)

# Purpose:
# - Make internal attrition intensity visually clear
# - Help compare Active vs Terminated proportion inside each performance tier
# - Avoid misinterpretation when reading stacked structure
# --------------------------------------------------------- 
for p in ax.patches:
    width, height = p.get_width(), p.get_height()
    x, y = p.get_xy()
    if height > 0:
        ax.text(x + width/2,
                y + height/2,
                f"{height:.1f}%",
                ha="center",
                va="center",
                color="white",
                fontweight="bold")
        
# ---------------------------------------------------------
# Step 5: Final formatting for Intensity Chart
# This chart represents:
# - Attrition Intensity (within-group risk)
# - Internal structural instability by performance level
# ---------------------------------------------------------
plt.title("Tỷ lệ % Trạng thái nhân viên theo nhóm hiệu suất",fontsize=14,pad=20)
plt.xlabel("Nhóm Performance Score", fontsize=12)
plt.ylabel("Phần trăm (%)",fontsize=12)
plt.xticks(rotation=0) # Để chữ nằm ngang
plt.legend(title="trạng thái", bbox_to_anchor=(1.05,1),loc="upper left")

plt.tight_layout()
plt.show()

# ---------------------------------------------------------
# Step 6: Calculate Total Workforce Size
# Purpose:
# - Establish baseline to measure overall organizational loss
# - Required for Attrition Impact calculation
# ---------------------------------------------------------
total_all_employees = df_4["so_luong_nv"].sum()
print(f"Tổng số nhân viên toàn công ty: {total_all_employees}")

# ---------------------------------------------------------
# Step 7: Filter Terminated Employees
# Purpose:
# - Isolate workforce loss group
# - Prepare dataset for Impact analysis
# ---------------------------------------------------------
df_terminated = df_4[df_4["EmployeeStatus"].str.strip() == "Terminated"].copy()

# ---------------------------------------------------------
# Step 8: Validate termination data availability
# Avoid silent analytical error if filtering fails
# ---------------------------------------------------------
if df_terminated.empty:
    print("Vẫn không tìm thấy dữ liệu Terminated. Hãy kiểm tra lại tên cột hoặc giá trị thực tế.")
else:
    # ---------------------------------------------------------
    # Step 9: Calculate Attrition Impact
    # Formula:
    # Terminated in group / Total company workforce
    #
    # This measures:
    # - Organizational loss impact
    # - Contribution of each performance tier to total attrition
    # ---------------------------------------------------------
    df_terminated["pct_tren_tong"] = (
        df_terminated["so_luong_nv"] / total_all_employees
        ) * 100

# Attrition Impact - Contribution to Total Workforce Loss
# ---------------------------------------------------------
# Step 10: Prepare ordered performance structure for Impact visualization
# ---------------------------------------------------------
df_terminated["PerformanceScore"] = pd.Categorical(
    df_terminated["PerformanceScore"].str.strip(),
    categories=order, 
    ordered=True
)
df_terminated = df_terminated.sort_values("PerformanceScore")


# ---------------------------------------------------------
# Step 11: Visualize Attrition Impact
# This chart answers:
# - Which performance tier contributes most to total workforce loss?
# - Where does organizational attrition pressure truly concentrate?
# --------------------------------------------------------- 
plt.figure(figsize=(8,6))


plt.bar(
    df_terminated["PerformanceScore"],
    df_terminated["pct_tren_tong"]
)


# ---------------------------------------------------------
# Step 12: Add impact percentage labels
# Ensure clear differentiation from Intensity chart
# ---------------------------------------------------------
for i, value in enumerate(df_terminated["pct_tren_tong"]):
    plt.text(i,  value/2, f"{value:.2f}%",ha="center",va="center")

plt.title("Attrition Impact by Performance Level\n(% Contribution to Total Workforce)", fontsize=13)
plt.xlabel("Performance Score")
plt.ylabel("Percentage of Total Workforce (%)")
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()

# ---------------------------------------------------------
# Step 13: Display supporting data table
# Used for precise numerical interpretation in written insight
# ---------------------------------------------------------
print("\nBảng tỷ lệ nhân viên nghỉ theo tổng nhân sự:")
pd.options.display.float_format = "{:.2f}".format
print(df_terminated[["PerformanceScore","so_luong_nv","pct_tren_tong"]])
# phân tích theo tỷ lệ tự nguyện

# ---------------------------------------------------------
# SECTION 1 – DATA LOADING & STRUCTURE VALIDATION
# Objective:
# - Analyze attrition pattern within Exceeds performance group
# - Identify compensation-risk imbalance across PayZones
# ---------------------------------------------------------

df_exceeds = pd.read_csv("Nhom_tu_nguyen.csv",sep=",")
print(df_exceeds)
# Nhóm theo số nhân viên đã nghỉ, payzone ,nhóm tuổi 
# Loại bỏ ký tự % 
if not df_exceeds.empty:
    print(f"Giá trị Engagement đầu tiên: {df_exceeds['avg_engagement_nghi_viec'].iloc[0]}")

# Hoặc in trực tiếp dtype
print(df_exceeds["avg_engagement_nghi_viec"].dtype)

# Xử lý an toàn 
if df_exceeds["ty_le_nghi_viec_pct"].dtype == "object":
    df_exceeds["ty_le_nghi_viec_pct"] = (
        df_exceeds["ty_le_nghi_viec_pct"]
        .str.replace("%","")
        .str.replace(",",".")
        .astype(float)
)
# ---------------------------------------------------------
# SECTION 2 – ATTRITION STRUCTURE ANALYSIS
# Analyze attrition concentration by:
# - PayZone
# - Age Group
# KPI:
# - Total Exceeds employees
# - Total attrition count
# - Median attrition rate per segment
# ---------------------------------------------------------

nhom_luong_nghi = (
    df_exceeds
    .groupby(["PayZone","Age_group"]).
    agg({
        "tong_nv_xuat_sac":"sum",
        "ty_le_nghi_viec_pct":"median",
        "so_nv_da_nghi":"sum",
        })
        .reset_index()
        .sort_values("ty_le_nghi_viec_pct",ascending=False)
)
print(nhom_luong_nghi)
# ---------------------------------------------------------
# SECTION 3 – PERFORMANCE TO COMPENSATION EFFICIENCY
# Objective:
# - Convert PayZone into compensation intensity scale
# - Estimate performance-to-pay ratio
# - Detect potential value leakage segments
# ---------------------------------------------------------

he_so_luong  = {
    "Zone A" : 3,
    "Zone B" : 2,
    "Zone C" : 1
}
# 2 tạo cột mới trên cột PayZone 
nhom_luong_nghi["he_so_luong"] = nhom_luong_nghi["PayZone"].map(he_so_luong) 
# hiệu xuất 
nhom_luong_nghi["hệ số exceeds"] = 4
nhom_luong_nghi["hiệu suất/lương"] = nhom_luong_nghi["hệ số exceeds"]/nhom_luong_nghi["he_so_luong"]
print(nhom_luong_nghi)
# Phân tích theo cụm 3 nhóm 1
print(nhom_luong_nghi.head(3))
                             
# ---------------------------------------------------------
# SECTION 4 – PREDICTIVE MODELING
# Objective:
# - Estimate drivers of attrition rate
# - Measure relative impact of:
#     + Compensation level
#     + Engagement score
#     + Satisfaction score
# Model:
# - Random Forest Regressor
# - Feature Importance analysis
# ---------------------------------------------------------
df_model = df_exceeds.copy()

zone_map = {"Zone A": 3, "Zone B": 2, "Zone C": 1}
df_model["He_so_Zone"] = df_model["PayZone"].map(zone_map)

# Chọn các biến đầu vào và biến mục tiêu
features_rf = ["He_so_Zone", "avg_engagement_nghi_viec", "avg_satisfaction_nghi_viec"]
target = "ty_le_nghi_viec_pct"

# Chuẩn hóa kiểu dữ liệu
for col in [target, 'avg_engagement_nghi_viec', 'avg_satisfaction_nghi_viec']:
    if df_model[col].dtype == 'object':
        df_model[col] = df_model[col].str.replace(',', '.').astype(float)

X = df_model[features_rf].fillna(0)

y = df_model[target]
y = y.fillna(y.mean())

# 3 Xây dựng mô hình ( dùng random Forest để  đạt độ chính xác cao)
# với dữ liệu nhỏ, chúng ta dùng n_estimators thấp để tránh quá tải
# Train / Test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
model_rf = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model_rf.fit(X_train, y_train)

# Đánh giá 
y_pred = model_rf.predict(X_test)

r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print("R2 Score:", round(r2,3))
print("MAE:", round(mae, 3))

# --- TÍNH TOÁN ĐỘ QUAN TRỌNG (Cần thêm bước này) ---
importances = model_rf.feature_importances_

importance_df = pd.DataFrame({
    "Chỉ số": features_rf,
    "Mức độ ảnh hưởng (%)": importances * 100
}).sort_values(by="Mức độ ảnh hưởng (%)", ascending=False)

print("\nFeature Importance:")
print(importance_df)
# Dự báo cho từng kịch bản
# 4. GIẢ LẬP KỊCH BẢN TỐI ƯU ĐỂ LOẠI BỎ CẢNH BÁO
# Giả sử ta tăng đồng thời cả 3 chỉ số lên mức cao
optimal_scenario = pd.DataFrame([[3, 4.5, 4.5]], columns=features_rf)
predicted_rate = model_rf.predict(optimal_scenario)

print(df_model[features_rf].max())

# Mô hình dự báo mức độ ảnh hưởng của các nhân tố đến tỷ lệ nghỉ việc 
# ==========================================================
# 1. LOAD DATA
# ========================================================== 
df_anhhuong = pd.read_csv("PT_nghiviec_dachieu.csv",sep=",")
print("Kích thước dataset:",df_anhhuong.shape)
print(df_anhhuong.head())
# ==========================================================
# 2. CLEAN PERCENT COLUMNS (AN TOÀN)
# ==========================================================
pct_cols = ["phan_tram_tong_nhan_su","ty_le_nghi_viec_noi_bo_pct"]

for col in pct_cols:
    # Bước A: Ép kiểu về string để xử lý sạch dấu phẩy (nếu có)
    if df_anhhuong[col].dtype == 'object':
        df_anhhuong[col] = df_anhhuong[col].str.replace(',', '.').astype(float)
    
   # 2. Chia đồng loạt cho 100 để đưa về đơn vị thập phân chính xác
    # (Không dùng điều kiện if x > 1 để tránh sót các số nhỏ như 0.57)
    if df_anhhuong[col].max() > 1:
        df_anhhuong[col] = df_anhhuong[col] / 100.0
    
   # 3. Cấu hình hiển thị 4 chữ số thập phân để kiểm tra
pd.set_option("display.float_format", "{:.4f}".format)

print("Kết quả chính xác tuyệt đối:")
print(df_anhhuong[pct_cols].head())
print(df_anhhuong) 

# ==========================================================
# 3. ENCODE CATEGORICAL VARIABLES
# ==========================================================
zone_map = {"Zone A": 3, "Zone B": 2, "Zone C": 1}
perf_map = {"Exceeds":4, "Fully Meets":3, "Needs Improvement":2, "PIP":1}

df_anhhuong["PayZone_Num"] = df_anhhuong["PayZone"].map(zone_map)
df_anhhuong["Perf_Num"] = df_anhhuong["PerformanceScore"].map(perf_map)
 
# Giữ bản copy để vẽ biểu đồ sau 
df_plot = df_anhhuong.copy()

# Nếu muốn đưa Age_group vào model
df_anhhuong = pd.get_dummies(df_anhhuong, columns=["Age_group"], drop_first=True)

# ==========================================================
# 4. BUILD FEATURE MATRIX
# ==========================================================
features_xgb = [
    "PayZone_Num",
    "Perf_Num",
    "avg_engagement_nghi_viec",
    "avg_satisfaction_nghi_viec"
]

# Thêm Age dummy nếu có
features_xgb += [col for col in df_anhhuong.columns if col.startswith("Age_group_")]

X = df_anhhuong[features_xgb].fillna(df_anhhuong[features_xgb].mean())
y = df_anhhuong["ty_le_nghi_viec_noi_bo_pct"]

# ==========================================================
# 5. TRAIN / TEST SPLIT
# ==========================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ==========================================================
# 6. TRAIN MODEL
# ==========================================================
model_xgb = xgb.XGBRegressor(
    n_estimators=200,
    max_depth=3,         # Giới hạn độ sâu để bắt quy luật chung, không học vẹt từng dòng 
    learning_rate=0.05,  # học rất chậm để đạt độ chính xác cao nhất 
    subsample=0.8,       # ngẫu nhiên hóa dữ liệu theo dòng
    colsample_bytree=0.8, # ngẫu nhiên hóa dữ liệu cột 
    random_state=42
)
model_xgb.fit(X_train, y_train)


# ==========================================================
# 7. EVALUATION
# ==========================================================

y_pred = model_xgb.predict(X_test)

r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print("\n==== MODEL PERFORMANCE ====")
print("R2:", round(r2, 4))
print("MAE:", round(mae, 4))


# ==========================================================
# 8. FEATURE IMPORTANCE
# ========================================================== 
importances = model_xgb.feature_importances_

# Tạo DataFrame để quản lý 
importances_df = pd.DataFrame({
    "Nhân tố (Features)":features_xgb,
    "Trọng số ảnh hưởng (%)": importances * 100
}).sort_values(by="Trọng số ảnh hưởng (%)", ascending=False)

print("\n====== FEATURE IMPORTANCE ======")
print(importances_df.to_string(index=False))

# ==========================================================
# 9. SHAP ANALYSIS
# ==========================================================
# Lượng hóa mức độ ảnh hưởng 
explainer = shap.TreeExplainer(model_xgb)
shap_values = explainer.shap_values(X_test)

plt.figure()
shap.summary_plot(shap_values, X_test)

# ==========================================================
# 10. AGE GROUP VISUALIZATION (DESCRIPTIVE)
# ==========================================================
plt.figure(figsize=(10,6))

age_order = sorted(df_plot["Age_group"].unique())

df_plot["ty_le_nghi_viec_display"] = df_plot["ty_le_nghi_viec_noi_bo_pct"] * 100

ax = sns.barplot(
    data=df_plot,
    x="Age_group",
    y="ty_le_nghi_viec_display",
    order=age_order
)

mean_val = (df_plot["ty_le_nghi_viec_noi_bo_pct"] * 100).mean()

plt.axhline(mean_val, linestyle="--",color="red")
plt.title("Tỷ lệ nghỉ việc theo tuổi")
plt.ylabel("Tỷ lệ nghỉ việc (%)")
plt.tight_layout()
plt.show()