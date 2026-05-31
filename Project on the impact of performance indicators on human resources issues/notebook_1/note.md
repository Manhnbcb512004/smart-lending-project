Strategic HR Analytics & Workforce Optimization
Executive Summary

This project delivers a comprehensive HR Analytics and Workforce Optimization framework designed to evaluate employee performance, compensation efficiency, engagement, satisfaction, workforce sustainability, and attrition risk.
The analysis combines descriptive analytics, workforce segmentation, financial efficiency evaluation, and machine learning modeling to identify hidden organizational risks and optimize human capital strategy.

The project analyzes 2,845 employees across multiple salary zones, performance levels, workforce age groups, and employment statuses.
Key findings reveal a significant imbalance between compensation allocation and workforce value creation, particularly among high-cost leadership segments and high-performing low-salary employees vulnerable to attrition.

In addition to traditional HR KPI analysis, the project integrates predictive modeling using Random Forest and XGBoost to identify key attrition drivers and quantify the impact of employee satisfaction, engagement, compensation structure, and workforce demographics on employee turnover behavior.

The project ultimately provides strategic recommendations for:

Workforce optimization
Retention strategy
Compensation restructuring
Succession planning
Employee engagement improvement
Financial risk reduction
Business Objectives

The project aims to solve several critical workforce management problems:

Analyze workforce performance distribution across salary zones.
Identify compensation inefficiencies and workforce ROI imbalance.
Evaluate employee engagement and satisfaction trends.
Detect workforce aging and succession risks.
Measure attrition intensity and organizational turnover impact.
Predict employee turnover using machine learning models.
Quantify the impact of emotional and demographic factors on attrition.
Support strategic HR decision-making through data-driven insights.
Dataset Overview

The project integrates multiple HR-related datasets covering workforce demographics, compensation structure, employee performance, engagement, satisfaction, and attrition information.

Main Data Domains
Employee demographics
Workforce age segmentation
PayZone classification
PerformanceScore evaluation
Employee satisfaction survey
Employee engagement survey
Employee employment status
Attrition statistics
Workforce efficiency metrics
Key Variables
Variable	Description
PayZone	Salary classification (Zone A/B/C)
PerformanceScore	Employee performance category
EngagementSurvey	Employee engagement score
EmpSatisfaction	Employee satisfaction score
EmployeeStatus	Active / Terminated
Age_group	Workforce lifecycle segmentation
efficiency_ratio	Performance-to-cost efficiency metric
Workforce Segmentation Framework
1. PayZone Structure

The organization is segmented into three compensation zones:

Zone	Description
Zone A	High salary workforce
Zone B	Medium salary workforce
Zone C	Low salary workforce
2. Performance Framework
Performance Group	Meaning
Exceeds	Outstanding performance
Fully Meets	Stable operational workforce
Needs Improvement	Underperforming workforce
PIP	Critical performance risk group
3. Workforce Lifecycle Segmentation
Age Group	Description	Strategic Meaning
Nhóm thực tập sinh	Internship workforce	Early-stage talent pipeline
Nhóm Khởi nghiệp (18–25)	Startup workforce	Workforce entry & adaptation stage
Nhóm Bứt phá (25–35)	Breakthrough workforce	High growth & promotion potential
Nhóm Cố vấn (36–55)	Advisor workforce	Core operational & strategic workforce
Nhóm Quản trị (55+)	Leadership workforce	Senior leadership & organizational stability
Key Workforce Metrics
KPI	Key Result
Total Employees	2,845
Largest Workforce Segment	Leadership – Fully Meets
Highest Efficiency Ratio	Internship Workforce (3.0)
Largest Operational Workforce	Advisor Group
Highest Attrition Risk	PIP Workforce
Strongest Attrition Driver	Employee Satisfaction
Critical Workforce Risk	Aging workforce structure
Highest ROI Workforce	Zone C High Performers
HR KPI & Workforce Analytics
1. Performance & Compensation Analysis
KPI Coverage
KPI 1: Performance Distribution by PayZone
KPI 2: Exceeds Ratio by PayZone
KPI 3: Performance Mix across PayZones
Visualizations
Grouped Bar Chart
Stacked Bar Chart
Core Insights
Fully Meets employees dominate all salary zones (~76–81%).
Zone A shows only a marginal increase in Exceeds performance despite significantly higher salary allocation.
More than 44% of PIP employees belong to Zone A, revealing severe compensation inefficiency.
Nearly one-third of high-performing employees remain in Zone C, creating talent leakage risk.
Salary growth is not fully aligned with workforce contribution.
Strategic Risks
Compensation inflation
Leadership productivity stagnation
Talent underpayment
Workforce value imbalance
2. Engagement & Satisfaction Analysis
KPI Coverage
KPI 4: Engagement Score by PayZone
KPI 5: Engagement Deviation
KPI 6: Engagement by Salary × Performance Matrix
KPI 7: Detractor Analysis
KPI 8: Satisfaction Distribution
KPI 9: Low Satisfaction Rate
KPI 10: Satisfaction Heatmap
Visualizations
Boxplot
Heatmap
Core Insights
Zone A employees display the highest emotional polarization.
High salary does not guarantee employee satisfaction.
PIP employees in Zone A show critically low satisfaction levels (~2.2).
Exceeds employees in low salary zones report higher emotional stability than some high-paid employees.
Emotional burnout becomes more visible among leadership-level employees.
Strategic Risks
Burnout risk
Leadership disengagement
Emotional attrition
Toxic workforce pockets
3. Workforce Efficiency & Financial Risk
KPI Coverage
Efficiency Ratio
Workforce ROI Segmentation
Workforce Financial Risk
Visualization
ROI Bar Chart with Break-even Line
Core Insights
Zone C contains the highest ROI workforce with efficiency ratios approaching 3.0.
Zone A contains high-cost low-efficiency workforce segments below break-even threshold.
Several leadership-level positions generate limited operational return relative to compensation cost.
Workforce value creation is unevenly distributed across compensation zones.
Strategic Risks
Salary budget inefficiency
Financial workforce burden
Workforce ROI imbalance
Compensation allocation distortion
4. Age-Based Workforce Strategy
Workforce Groups
Internship Workforce
Startup Workforce
Breakthrough Workforce
Advisor Workforce
Leadership Workforce
Visualizations
Efficiency Heatmap
Interactive Grouped Bar Chart
Workforce Efficiency Trend Line
Core Insights
The organization displays an aging workforce structure.
Leadership and Advisor groups dominate workforce volume.
Internship pipeline remains critically underdeveloped.
Workforce efficiency drops sharply after internship stage.
Breakthrough workforce faces the highest external recruitment pressure.
Advisor workforce represents the operational backbone of the company.
Strategic Risks
Succession crisis
Knowledge gap risk
Weak talent pipeline
Workforce sustainability concerns
5. Attrition & Turnover Analysis
KPI Coverage
Attrition Intensity
Attrition Impact
Performance-based Attrition
Visualizations
Stacked Bar Chart
Attrition Contribution Chart
Core Insights
PIP employees show the highest attrition intensity (~20.9%).
Exceeds employees also display concerning attrition levels (~11.6%).
Fully Meets employees contribute the largest share of total workforce loss (~10.86%).
Breakthrough workforce shows elevated turnover pressure due to market competition.
Attrition is strongly influenced by emotional experience rather than demographic structure alone.
Strategic Risks
Regrettable attrition
Talent leakage
Operational instability
Workforce continuity disruption
Machine Learning & Predictive Modeling
1. Random Forest Attrition Prediction
Objective

Predict turnover risk using workforce emotional and compensation indicators.

Features
PayZone
Employee Engagement
Employee Satisfaction
Evaluation Metrics
Metric	Result
R² Score	0.068
MAE	4.189
Key Findings
Employee engagement contributes ~35.6% to attrition prediction.
Employee satisfaction contributes ~34.6%.
Compensation zone contributes ~29.8%.
Emotional indicators outperform compensation variables.
2. XGBoost Workforce Impact Modeling
Objective

Analyze multi-dimensional workforce attrition drivers.

Features
PayZone
PerformanceScore
Age Groups
Satisfaction
Engagement
Evaluation Metrics
Metric	Result
R² Score	0.747
MAE	0.0433
Explainable AI (XAI)
SHAP Summary Plot
Feature Importance Analysis
Key Findings
Feature	Influence (%)
Satisfaction	25.93%
Advisor Workforce	16.13%
Performance Level	14.61%
Startup Workforce	12.93%
Internship Workforce	9.29%
Engagement	8.67%
PayZone	8.39%
Strategic Interpretation
Emotional experience is the strongest turnover driver.
Workforce age matters less than employee satisfaction and engagement.
Workforce stability depends heavily on emotional retention factors rather than salary alone.
Strategic Business Insights
Critical Organizational Findings
1. Workforce Aging Risk

The company heavily depends on Advisor and Leadership workforce groups while maintaining a critically weak internship pipeline.

2. Compensation Misalignment

High salary allocation does not consistently produce high workforce performance.

3. Emotional Attrition Risk

Employee satisfaction and engagement outperform salary as predictors of turnover behavior.

4. Talent Leakage Risk

High-performing employees in low salary zones are vulnerable to external recruitment pressure.

5. Operational Dependency Risk

The organization relies heavily on Fully Meets employees for operational continuity.

Strategic Recommendations
Workforce Strategy
Build stronger internship and management trainee pipelines.
Develop succession planning programs for leadership continuity.
Reduce dependency on aging workforce groups.
Compensation Strategy
Redesign compensation based on performance contribution.
Accelerate salary review for high-performing low-cost employees.
Reduce high-cost low-efficiency workforce allocation.
Employee Experience Strategy
Implement continuous engagement monitoring.
Improve leadership emotional management.
Develop burnout prevention initiatives.
Retention Strategy
Launch retention programs for Exceeds employees.
Conduct Stay Interviews for high-performing workforce segments.
Build personalized career development pathways.
Analytics & Technology Strategy
Expand predictive HR analytics capabilities.
Integrate real-time HR dashboards.
Deploy explainable AI monitoring for attrition prediction.
Technology Stack
Category	Tools
Programming	Python
Data Analysis	Pandas, NumPy
Visualization	Matplotlib, Seaborn, Plotly
Machine Learning	Scikit-learn, XGBoost
Explainable AI	SHAP
Environment	Jupyter Notebook
Project Outcomes
Built a strategic HR KPI framework.
Developed workforce efficiency segmentation.
Identified critical attrition drivers.
Built predictive workforce attrition models.
Integrated explainable AI into HR analytics.
Generated strategic workforce optimization recommendations.
Combined business analytics with machine learning interpretation.
Future Improvements
Deploy interactive HR dashboard.
Integrate Power BI/Tableau reporting.
Add real-time workforce monitoring.
Expand predictive workforce modeling.
Implement survival analysis for attrition prediction.
Build automated workforce risk alert systems.
Conclusion

This project demonstrates how HR Analytics can evolve from descriptive reporting into strategic workforce intelligence.
By combining workforce segmentation, compensation analysis, emotional experience evaluation, and predictive machine learning models, the project provides a data-driven framework for optimizing workforce sustainability, reducing attrition risk, and improving organizational efficiency.

The analysis highlights that workforce stability is driven not only by compensation, but more importantly by employee satisfaction, engagement, workforce lifecycle management, and strategic talent allocation.



2. Executive Summary
# Executive Summary

Dự án “HR Analytics & Workforce Optimization” được xây dựng nhằm phân tích hiệu quả sử dụng nguồn lực nhân sự, tối ưu hóa chiến lược phân bổ lương thưởng và dự báo rủi ro nghỉ việc trong doanh nghiệp thông qua Data Analytics kết hợp Machine Learning.

Dự án tập trung khai thác mối quan hệ giữa PayZone (vùng lương), Performance Score (mức độ hoàn thành công việc), Engagement Score (mức độ gắn kết), Satisfaction Score (mức độ hài lòng), Age Group (nhóm tuổi) và Attrition (nghỉ việc) để xác định các điểm mất cân đối trong cấu trúc nhân sự và hiệu quả đầu tư quỹ lương.

Thông qua hệ thống KPI đa chiều, dự án phát hiện nhiều vấn đề quản trị quan trọng:
- Nhóm nhân sự lương thấp (Zone C) tạo ra Efficiency Ratio cao nhất nhưng lại tồn tại nguy cơ chảy máu chất xám.
- Một bộ phận nhân sự lương cao (Zone A) có hiệu suất thấp hơn kỳ vọng, tạo ra rủi ro chi phí nhân sự.
- Satisfaction và Engagement có ảnh hưởng mạnh hơn yếu tố độ tuổi trong việc dự báo nghỉ việc.
- Nhóm Fully Meets tuy ổn định nhưng lại đóng góp tỷ trọng lớn nhất vào tổng số nhân sự nghỉ việc do quy mô quá lớn.
- Cấu trúc nhân sự hiện tại có xu hướng “già hóa”, phụ thuộc mạnh vào nhóm Cố vấn và Quản trị.

Dự án sử dụng hệ thống trực quan hóa dữ liệu bằng Seaborn, Matplotlib và Plotly để phân tích:
- Hiệu suất theo vùng lương.
- Ma trận hài lòng & gắn kết.
- Workforce Efficiency.
- Attrition Impact.
- Phân tích chiến lược theo nhóm tuổi.

Ngoài phân tích mô tả, dự án còn triển khai 2 mô hình Machine Learning:
- Random Forest Regressor: dự báo tỷ lệ nghỉ việc dựa trên Satisfaction, Engagement và hệ số vùng lương.
- XGBoost Regressor: phân tích đa chiều tác động của vùng lương, độ tuổi và hiệu suất đến rủi ro nghỉ việc.

Mô hình XGBoost đạt:
- R2 Score: 0.747
- MAE: 0.0433

Kết quả từ Explainable AI (SHAP & Feature Importance) cho thấy:
- Satisfaction Score là yếu tố ảnh hưởng mạnh nhất đến quyết định nghỉ việc.
- Các yếu tố cảm xúc và trải nghiệm nhân sự có tác động lớn hơn các yếu tố nhân khẩu học đơn thuần.

Dự án hướng tới xây dựng một framework HR Analytics có khả năng hỗ trợ:
- Workforce Optimization
- Compensation Strategy
- Retention Planning
- Attrition Prediction
- Explainable HR Decision-Making

3. Business Objectives
# Business Objectives

Dự án được xây dựng nhằm giải quyết các bài toán chiến lược trong quản trị nhân sự và tối ưu hóa hiệu quả vận hành doanh nghiệp thông qua dữ liệu.

## Core Objectives

### 1. Phân tích hiệu quả sử dụng nguồn lực nhân sự
- Đánh giá mức độ tương quan giữa chi phí lương và hiệu suất lao động.
- Xác định các nhóm nhân sự tạo ra giá trị cao (High ROI) và các nhóm có nguy cơ gây thất thoát chi phí.

### 2. Phát hiện rủi ro nghỉ việc (Attrition Risk)
- Phân tích tỷ lệ nghỉ việc theo:
  - vùng lương (PayZone)
  - nhóm hiệu suất
  - nhóm tuổi
  - mức độ hài lòng và gắn kết
- Xác định các nhóm nhân sự có nguy cơ “chảy máu chất xám”.

### 3. Đánh giá mức độ hài lòng & gắn kết nhân sự
- Đo lường Satisfaction Score và Engagement Score theo nhiều chiều dữ liệu.
- Xác định các nhóm “Detractors” kéo giảm chất lượng môi trường làm việc.
- Phân tích sự mất cân đối tâm lý giữa các vùng lương.

### 4. Tối ưu hóa chiến lược phân bổ lương thưởng
- Đánh giá tính hiệu quả của hệ thống PayZone hiện tại.
- Xác định các trường hợp:
  - High Cost – Low Performance
  - Low Cost – High Performance
- Hỗ trợ doanh nghiệp tái cấu trúc quỹ lương theo hướng hiệu quả hơn.

### 5. Phân tích cấu trúc nhân sự theo vòng đời nghề nghiệp
- Đánh giá hiệu suất và rủi ro nhân sự theo từng nhóm tuổi:
  - Khởi nghiệp (18–25)
  - Bứt phá (25–35)
  - Cố vấn (36–55)
  - Quản trị (55+)
- Phát hiện xu hướng “già hóa” nguồn lực và rủi ro đứt gãy đội ngũ kế thừa.

### 6. Ứng dụng Machine Learning vào dự báo nhân sự
- Xây dựng mô hình dự báo nghỉ việc bằng Random Forest và XGBoost.
- Đánh giá mức độ ảnh hưởng của:
  - Satisfaction
  - Engagement
  - PayZone
  - Performance
  - Age Group
- Triển khai Explainable AI nhằm giải thích quyết định mô hình một cách minh bạch.

### 7. Hỗ trợ ra quyết định quản trị chiến lược
Dự án hướng tới xây dựng một hệ thống HR Analytics có khả năng hỗ trợ:
- Workforce Optimization
- Compensation Efficiency
- Retention Strategy
- Talent Management
- Predictive HR Analytics
- Explainable HR Decision-Making


# Dataset Overview

Dự án sử dụng nhiều nguồn dữ liệu nhân sự được chuẩn hóa và liên kết nhằm phục vụ phân tích đa chiều về hiệu suất lao động, mức độ hài lòng, gắn kết nhân sự và dự báo nghỉ việc.

## Dataset Sources

Các dataset chính được sử dụng trong dự án:

| Dataset | Mục đích |
|---|---|
| Cleaned_HR_Data_Analysis.csv | Dataset tổng hợp phục vụ phân tích KPI |
| pjhieusuat.csv | Dữ liệu hiệu suất nhân sự |
| HR_phantich_luong.csv | Dữ liệu vùng lương & chi phí nhân sự |
| PT_Tuoi.csv | Phân nhóm nhân sự theo độ tuổi |
| nv_hieusuat.csv | Dataset phục vụ phân tích attrition & machine learning |

---

## Dataset Scale

### Tổng quy mô dữ liệu
- Tổng số nhân viên: **2,845**
- Nhiều bảng dữ liệu liên kết phục vụ:
  - KPI Dashboard
  - Workforce Analytics
  - Attrition Analysis
  - Machine Learning

### Đặc điểm dữ liệu
Dữ liệu bao gồm:
- dữ liệu định tính (categorical)
- dữ liệu định lượng (numerical)
- dữ liệu hành vi nhân sự
- dữ liệu hiệu suất
- dữ liệu nghỉ việc
- dữ liệu mức độ hài lòng & gắn kết

---

# Core Variables Structure

## 1. Employee Demographics
Các biến mô tả thông tin nhân sự:
- Age
- Age Group
- Department
- Position
- Workforce Lifecycle Segment

### Workforce Lifecycle Segments
| Nhóm tuổi | Ý nghĩa |
|---|---|
| Nhóm thực tập sinh | Giai đoạn thử việc / pipeline đầu vào |
| Nhóm Khởi nghiệp (18–25) | Giai đoạn hình thành năng lực |
| Nhóm Bứt phá (25–35) | Giai đoạn tăng trưởng & cạnh tranh |
| Nhóm Cố vấn (36–55) | Nhóm chuyên môn cốt lõi |
| Nhóm Quản trị (55+) | Nhóm lãnh đạo & quản trị chiến lược |

---

## 2. Compensation & PayZone Variables

Các biến liên quan đến chi phí nhân sự:
- Salary
- PayZone
- Compensation Segment
- Salary Coefficient

### PayZone Structure
| PayZone | Ý nghĩa |
|---|---|
| Zone A | Nhóm lương cao |
| Zone B | Nhóm lương trung bình |
| Zone C | Nhóm lương thấp |

---

## 3. Performance Variables

Các biến phản ánh mức độ hoàn thành công việc:
- PerformanceScore
- Performance Point
- Efficiency Ratio
- ROI Workforce Metrics

### Performance Categories
| PerformanceScore | Ý nghĩa |
|---|---|
| Exceeds | Vượt kỳ vọng |
| Fully Meets | Hoàn thành tốt |
| Needs Improvement | Cần cải thiện |
| PIP | Hiệu suất thấp / diện theo dõi |

---

## 4. Employee Experience Variables

Các biến phản ánh trải nghiệm nhân sự:
- Engagement Score
- Satisfaction Score
- Employee Experience Metrics
- Detractor Indicators

### Analytical Objectives
Các biến này được sử dụng để:
- đo lường mức độ gắn kết
- phát hiện nhóm bất mãn (Detractors)
- phân tích rủi ro nghỉ việc
- đánh giá chất lượng môi trường làm việc

---

## 5. Attrition Variables

Các biến phục vụ phân tích nghỉ việc:
- EmployeeStatus
- Attrition Rate
- Internal Turnover Ratio
- Attrition Impact Contribution

### Employee Status
| Status | Ý nghĩa |
|---|---|
| Active | Nhân viên đang làm việc |
| Terminated | Nhân viên đã nghỉ việc |

---

## 6. Machine Learning Variables

Các biến được sử dụng trong mô hình dự báo:
- He_so_Zone
- avg_engagement_nghi_viec
- avg_satisfaction_nghi_viec
- Performance Encoding
- Age Group Encoding
- Attrition Rate

### ML Objectives
- dự báo rủi ro nghỉ việc
- xác định yếu tố ảnh hưởng mạnh nhất
- giải thích mô hình bằng SHAP
- hỗ trợ ra quyết định nhân sự


# Workforce Segmentation Framework

Dự án xây dựng một hệ thống phân khúc nguồn lực nhân sự đa chiều nhằm đánh giá:
- hiệu quả lao động
- mức độ hài lòng
- rủi ro nghỉ việc
- hiệu quả sử dụng quỹ lương
- tiềm năng phát triển nhân sự

Framework này đóng vai trò là nền tảng cốt lõi cho toàn bộ hệ thống KPI và mô hình Machine Learning trong dự án.

---

# 1. PayZone Segmentation Framework

Hệ thống PayZone được sử dụng để phân loại nhân sự theo mức chi phí lương và chiến lược đãi ngộ của doanh nghiệp.

| PayZone | Đặc điểm |
|---|---|
| Zone A | Nhóm lương cao – thường là nhân sự cấp cao hoặc chuyên môn quan trọng |
| Zone B | Nhóm lương trung bình – lực lượng vận hành ổn định |
| Zone C | Nhóm lương thấp – nhân sự trẻ hoặc nhóm tối ưu chi phí |

## Strategic Meaning
Framework này giúp:
- đánh giá hiệu quả đầu tư quỹ lương
- phát hiện nhóm High Cost – Low Performance
- xác định khu vực có nguy cơ “chảy máu chất xám”
- tối ưu chiến lược compensation

---

# 2. Performance Segmentation Framework

Nhân sự được phân loại theo mức độ hoàn thành công việc nhằm phục vụ:
- KPI Analytics
- Efficiency Analysis
- Attrition Prediction
- Workforce Optimization

| Performance Group | Ý nghĩa |
|---|---|
| Exceeds | Nhóm vượt kỳ vọng |
| Fully Meets | Nhóm hoàn thành ổn định |
| Needs Improvement | Nhóm cần cải thiện |
| PIP | Nhóm hiệu suất thấp / diện theo dõi |

## Strategic Meaning
Framework hiệu suất giúp doanh nghiệp:
- xác định nhóm nhân tài chiến lược
- phát hiện nhóm gây thất thoát hiệu quả
- đánh giá chất lượng vận hành tổng thể
- xây dựng hệ thống thưởng/phạt hợp lý

---

# 3. Workforce Lifecycle Framework (Age Segmentation)

Dự án phân tích nhân sự theo vòng đời nghề nghiệp nhằm đánh giá:
- tiềm năng phát triển
- mức độ ổn định
- nguy cơ nghỉ việc
- vai trò chiến lược của từng nhóm tuổi

---

## 3.1 Nhóm thực tập sinh
### Vai trò
- Pipeline đầu vào
- Nguồn lực kế cận dài hạn

### Đặc điểm
- Quy mô nhỏ
- Efficiency Ratio rất cao
- Chi phí thấp
- Động lực phát triển lớn

### Strategic Risk
- Thiếu hụt pipeline kế thừa
- Rủi ro già hóa workforce trong dài hạn

---

## 3.2 Nhóm Khởi nghiệp (18–25)

### Vai trò
- Giai đoạn hình thành năng lực
- Workforce trẻ

### Đặc điểm
- Khả năng thích nghi cao
- Hiệu suất ổn định
- Rủi ro nghỉ việc tương đối lớn

### Strategic Risk
- Dễ burnout
- Dễ dịch chuyển sang doanh nghiệp khác

---

## 3.3 Nhóm Bứt phá (25–35)

### Vai trò
- Workforce tăng trưởng chính
- Nhóm cạnh tranh mạnh nhất trên thị trường lao động

### Đặc điểm
- Tiềm năng thăng tiến cao
- Chịu áp lực KPI lớn
- Attrition Risk cao

### Strategic Risk
- Headhunt Risk
- Talent Leakage
- Career Plateau

---

## 3.4 Nhóm Cố vấn (36–55)

### Vai trò
- Nhóm chuyên môn cốt lõi
- Backbone Workforce

### Đặc điểm
- Quy mô lớn
- Đóng vai trò ổn định vận hành
- Knowledge Holder

### Strategic Risk
- Knowledge Gap
- Workforce Aging
- Risk Concentration

---

## 3.5 Nhóm Quản trị (55+)

### Vai trò
- Leadership Workforce
- Strategic Decision Layer

### Đặc điểm
- Kinh nghiệm quản trị cao
- Ảnh hưởng lớn đến văn hóa tổ chức
- Quy mô nhân sự rất lớn

### Strategic Risk
- Succession Planning Risk
- Leadership Dependency
- Retirement Wave Risk

---

# 4. Workforce Value Segmentation

Ngoài phân loại truyền thống, dự án còn xây dựng framework phân đoạn giá trị nguồn lực theo Efficiency Ratio.

| Segment | Ý nghĩa |
|---|---|
| High ROI | Nhóm tạo giá trị vượt trội |
| Stable Workforce | Nhóm vận hành ổn định |
| High Cost / Low Efficiency | Nhóm có nguy cơ gây thất thoát ngân sách |

## Strategic Meaning
Framework này hỗ trợ:
- Workforce Optimization
- Budget Allocation
- HR Cost Control
- Retention Strategy
- Talent Prioritization

---

# 5. Strategic Purpose of the Framework

Toàn bộ hệ thống segmentation trong dự án được thiết kế nhằm:
- liên kết dữ liệu nhân sự với hiệu quả tài chính
- chuyển đổi HR Analytics từ descriptive sang strategic analytics
- hỗ trợ Predictive Workforce Management
- tăng khả năng Explainable HR Decision-Making
- xây dựng nền tảng cho AI-driven HR Strategy


# Key Workforce Metrics

Dự án xây dựng hệ thống KPI tổng hợp nhằm đo lường:
- hiệu quả nguồn lực nhân sự
- chất lượng workforce
- mức độ ổn định vận hành
- rủi ro nghỉ việc
- hiệu quả sử dụng quỹ lương

Các chỉ số dưới đây đóng vai trò là “Strategic Workforce Indicators” cho toàn bộ hệ thống phân tích.

---

## Core Workforce Metrics

| Metrics | Value | Strategic Meaning |
|---|---|---|
| Total Employees | 2,845 | Quy mô tổng workforce |
| Largest Workforce Group | Nhóm Quản trị – Fully Meets (943 nhân sự) | Workforce già hóa & phụ thuộc leadership |
| Second Largest Workforce Group | Nhóm Cố vấn – Fully Meets (680 nhân sự) | Backbone vận hành doanh nghiệp |
| Highest Efficiency Ratio | Nhóm thực tập sinh (3.00) | Low-cost high-efficiency workforce |
| Highest Stable Efficiency Group | Nhóm Khởi nghiệp – Fully Meets (2.44) | Workforce trẻ có khả năng tối ưu chi phí |
| Largest Attrition Contributor | Fully Meets (10.86%) | Backbone workforce loss |
| Highest Attrition Rate | PIP (20.93%) | Workforce instability |
| Regrettable Attrition | Exceeds (11.56%) | Talent leakage risk |
| Strongest Attrition Driver | Satisfaction Score | Emotional attrition signal |
| Most Critical Workforce Risk | Workforce Aging | Succession & knowledge gap risk |

---

# Workforce Structure Snapshot

## Workforce Composition
Cấu trúc workforce hiện tại cho thấy:
- doanh nghiệp đang phụ thuộc mạnh vào nhóm:
  - Cố vấn (36–55)
  - Quản trị (55+)
- trong khi pipeline nhân sự trẻ còn khá mỏng.

### Strategic Implication
Điều này tạo ra:
- rủi ro già hóa workforce
- leadership dependency
- succession planning risk
- knowledge concentration risk

---

# Workforce Efficiency Snapshot

## High ROI Workforce
Các nhóm tạo ra Efficiency Ratio cao:
- Nhóm thực tập sinh
- Nhóm Khởi nghiệp
- Zone C Workforce

### Strategic Meaning
Đây là:
- nhóm tối ưu chi phí tốt nhất
- có tiềm năng tăng trưởng cao
- phù hợp chiến lược long-term workforce investment

---

## High Cost Workforce Risk
Một bộ phận workforce tại:
- Zone A
- nhóm hiệu suất thấp
đang tạo ra:
- Efficiency Ratio dưới break-even level.

### Strategic Meaning
Điều này phản ánh:
- salary allocation inefficiency
- compensation mismatch
- low-return payroll spending

---

# Employee Experience Snapshot

## Engagement & Satisfaction Signals

Kết quả phân tích cho thấy:
- Satisfaction và Engagement có tác động mạnh hơn tuổi tác trong việc dự báo nghỉ việc.
- Một số nhóm leadership salary cao có mức Satisfaction thấp hơn kỳ vọng.

### Strategic Meaning
Đây là tín hiệu của:
- burnout risk
- emotional disengagement
- leadership dissatisfaction
- silent attrition risk

---

# Attrition Snapshot

## Workforce Loss Pattern

### Nhóm nghỉ việc lớn nhất:
- Fully Meets Workforce

### Nhóm có tỷ lệ nghỉ việc cao:
- PIP
- nhóm Bứt phá
- một phần workforce Exceeds

### Strategic Meaning
Doanh nghiệp đang:
- mất workforce vận hành cốt lõi
- tồn tại risk về talent leakage
- chưa tối ưu retention strategy cho nhóm high performer

---

# Predictive HR Analytics Snapshot

## Machine Learning Results

### Random Forest
- Phân tích ảnh hưởng:
  - Satisfaction
  - Engagement
  - PayZone
đến tỷ lệ nghỉ việc.

### XGBoost
Kết quả mô hình:
- R2 Score: 0.747
- MAE: 0.0433

### Most Influential Features
| Feature | Impact |
|---|---|
| Satisfaction Score | Cao nhất |
| Age Group – Cố vấn | Tác động mạnh |
| Performance Score | Ảnh hưởng lớn |
| Engagement Score | Ảnh hưởng đáng kể |

### Strategic Meaning
Quyết định nghỉ việc:
- mang tính cảm xúc nhiều hơn demographic factors
- chịu ảnh hưởng mạnh bởi employee experience
- liên quan trực tiếp đến workforce engagement quality

# HR KPI & Workforce Analytics

Dự án xây dựng hệ thống KPI đa chiều nhằm phân tích:
- hiệu suất workforce
- hiệu quả sử dụng quỹ lương
- mức độ hài lòng & gắn kết
- rủi ro nghỉ việc
- hiệu quả vận hành nguồn lực nhân sự

Hệ thống KPI được thiết kế theo hướng:
- business-driven analytics
- workforce economics
- strategic HR analytics
- predictive workforce management

---

# 7.1 Performance & Compensation Analysis

## KPI Framework

### KPI 1
Performance Distribution by PayZone (%)
- Phân bổ hiệu suất theo vùng lương.

### KPI 2
Exceeds Ratio by PayZone
- Tỷ lệ nhân sự vượt kỳ vọng theo từng vùng lương.

### KPI 3
Performance Mix across PayZones
- Cơ cấu vùng lương trong từng nhóm hiệu suất.

---

## Visualizations

📊 Grouped Bar Chart (Seaborn)

📊 Stacked Bar Chart (% Labels)

---

## Core Business Insights

### Compensation Inefficiency
Nhóm Zone A có mức lương cao nhất nhưng tỷ lệ Exceeds không tạo ra khoảng cách lớn so với Zone C.

### High Salary ≠ High Performance
Một bộ phận workforce lương cao:
- chỉ đạt Fully Meets
- hoặc rơi vào nhóm hiệu suất thấp.

### Talent Imbalance
Một phần nhân sự Exceeds lại tập trung tại Zone C:
- tạo ra rủi ro chảy máu chất xám
- phản ánh salary-performance mismatch.

### Payroll Allocation Risk
Ngân sách lương đang bị phân bổ chưa tối ưu:
- high-cost low-return workforce
- low-cost high-efficiency workforce.

---

# 7.2 Engagement & Satisfaction Analysis

## KPI Framework

### KPI 4 & 5
Engagement Metrics
- Điểm gắn kết trung bình.
- Độ lệch gắn kết theo vùng lương.

### KPI 6 & 7
Drill-down & Detractor Analysis
- Phân tích nhóm kéo thấp Engagement.

### KPI 8
Satisfaction Distribution

### KPI 9
Low Satisfaction Rate

### KPI 10
Satisfaction Matrix (PayZone × Performance)

---

## Visualizations

📊 Boxplot (Seaborn)

📊 Heatmap (Seaborn)

---

## Core Business Insights

### Burnout Risk
Nhóm salary cao tồn tại:
- độ phân tán Satisfaction lớn
- nhiều Detractor signals.

### Leadership Dissatisfaction
Một phần leadership workforce:
- nhận lương cao
- nhưng Satisfaction không tương xứng.

### Emotional Attrition Signals
Satisfaction & Engagement:
- là predictor mạnh của nghỉ việc
- có tác động lớn hơn yếu tố độ tuổi.

### Toxic Workforce Pattern
Nhóm:
- PIP × Zone A
- low engagement workforce
đang tạo ra vòng lặp:
low performance → dissatisfaction → attrition risk.

---

# 7.3 Workforce Efficiency & Financial Risk

## KPI Framework

### Efficiency Ratio
- Tỷ lệ Hiệu suất / Chi phí workforce.

### Workforce ROI Segmentation
Phân loại:
- High ROI
- Stable Workforce
- High Cost / Low Efficiency

---

## Visualizations

📊 ROI vs Break-even Bar Chart

---

## Core Business Insights

### High ROI Low-cost Workforce
Zone C và workforce trẻ:
- tạo ra Efficiency Ratio rất cao
- mang lại workforce leverage tốt.

### High-cost Low-efficiency Workforce
Một phần Zone A workforce:
- có ROI dưới break-even
- tạo ra payroll inefficiency.

### Salary Allocation Inefficiency
Cấu trúc compensation hiện tại:
- chưa phản ánh đúng giá trị tạo ra
- tồn tại salary-performance mismatch.

### Workforce Optimization Opportunity
Doanh nghiệp có khả năng:
- tái cấu trúc payroll allocation
- tối ưu workforce ROI
- tăng hiệu quả sử dụng ngân sách nhân sự.

---

# 7.4 Age-Based Workforce Strategy

## Workforce Lifecycle Groups

| Group | Age Range |
|---|---|
| Nhóm Khởi nghiệp | 18–25 |
| Nhóm Bứt phá | 25–35 |
| Nhóm Cố vấn | 36–55 |
| Nhóm Quản trị | 55+ |

---

## Visualizations

📊 Workforce Efficiency Heatmap

📊 Interactive Grouped Bar Chart (Plotly)

📊 Workforce Efficiency Trend Line (Plotly)

---

## Core Business Insights

### Workforce Aging
Cấu trúc workforce hiện tại:
- phụ thuộc mạnh vào nhóm Cố vấn & Quản trị.

### Succession Planning Risk
Pipeline kế thừa còn khá mỏng:
- đặc biệt ở nhóm thực tập sinh.

### Leadership Sustainability Risk
Leadership concentration quá lớn:
- tạo ra dependency risk.

### Promotion Potential
Nhóm Bứt phá:
- có tiềm năng kế thừa cao
- nhưng attrition risk cũng lớn.

### Knowledge Gap Risk
Nếu workforce senior rời đi đồng loạt:
- doanh nghiệp có thể mất:
  - operational knowledge
  - leadership continuity
  - mentoring capability.

---

# 7.5 Attrition & Turnover Analysis

## KPI Framework

### Attrition Intensity
- Tỷ lệ nghỉ việc theo nhóm hiệu suất.

### Attrition Impact
- Mức độ ảnh hưởng lên tổng workforce loss.

---

## Visualizations

📊 Stacked Bar Chart (Active vs Terminated)

📊 Contribution Bar Chart

---

## Core Business Insights

### Regrettable Attrition
Nhóm Exceeds:
- vẫn tồn tại tỷ lệ nghỉ việc đáng chú ý
- phản ánh talent retention issue.

### Backbone Workforce Loss
Nhóm Fully Meets:
- đóng góp phần lớn workforce loss
- do quy mô quá lớn.

### Talent Leakage
Một phần high performer workforce:
- chưa được giữ chân hiệu quả.

### Workforce Stability Risk
Attrition không chỉ đến từ low performer:
- mà còn xuất hiện ở nhóm core workforce.

### Retention Strategy Gap
Doanh nghiệp:
- đang làm tốt việc đào thải low performer
- nhưng chưa đủ mạnh trong retention strategy cho high-value workforce.


# Machine Learning & Predictive Modeling

Dự án không chỉ dừng lại ở descriptive analytics mà còn mở rộng sang predictive HR analytics nhằm:
- dự báo rủi ro nghỉ việc
- xác định các yếu tố ảnh hưởng mạnh nhất
- hỗ trợ strategic workforce planning
- tăng khả năng explainable decision-making trong quản trị nhân sự

Hai mô hình Machine Learning được triển khai:
- Random Forest Regressor
- XGBoost Regressor

---

# 8.1 Random Forest Model

## Objective

Mục tiêu của mô hình:
- dự báo tỷ lệ nghỉ việc của workforce
- phân tích mức độ ảnh hưởng của:
  - vùng lương
  - mức độ gắn kết
  - mức độ hài lòng

đến attrition behavior.

---

## Input Features

| Features |
|---|
| He_so_Zone |
| avg_engagement_nghi_viec |
| avg_satisfaction_nghi_viec |

---

## Model Architecture

| Model | Type |
|---|---|
| Random Forest Regressor | Ensemble Learning |

---

## Evaluation Metrics

| Metrics | Value |
|---|---|
| R² Score | 0.068 |
| MAE | 4.189 |

---

## Feature Importance

| Feature | Impact (%) |
|---|---|
| avg_engagement_nghi_viec | 35.61% |
| avg_satisfaction_nghi_viec | 34.59% |
| He_so_Zone | 29.80% |

---

## Core Findings

### Emotional Factors > Compensation Factors
Engagement và Satisfaction có ảnh hưởng mạnh hơn hệ số vùng lương trong việc dự báo nghỉ việc.

### Employee Experience Drives Attrition
Quyết định nghỉ việc mang tính:
- cảm xúc
- trải nghiệm
- mức độ gắn kết

nhiều hơn yếu tố chi phí đơn thuần.

### Salary Alone Cannot Retain Talent
Nhân sự:
- nhận lương cao
- nhưng Engagement thấp

vẫn có nguy cơ nghỉ việc lớn.

---

## Scenario Simulation

Mô hình được sử dụng để mô phỏng các kịch bản tối ưu workforce retention.

### Optimal Scenario Example
| Variables | Value |
|---|---|
| He_so_Zone | 3.00 |
| Engagement | 3.67 |
| Satisfaction | 4.00 |

### Business Meaning
Retention strategy hiệu quả cần:
- kết hợp compensation
- emotional engagement
- employee experience optimization

thay vì chỉ tăng lương đơn thuần.

---

# 8.2 XGBoost Attrition Model

## Objective

Mục tiêu mô hình:
- phân tích đa chiều các yếu tố gây nghỉ việc
- đánh giá tác động đồng thời của:
  - độ tuổi
  - vùng lương
  - hiệu suất
  - engagement
  - satisfaction

đến attrition behavior.

---

## Dataset Overview

| Metrics | Value |
|---|---|
| Dataset Size | (50, 9) |

---

## Input Features

| Features |
|---|
| PayZone_Num |
| Perf_Num |
| avg_engagement_nghi_viec |
| avg_satisfaction_nghi_viec |
| Age Group Dummies |

---

## Processing Pipeline

### Feature Engineering
- Encoding PayZone
- Encoding PerformanceScore
- Age Group Dummy Variables

### Model Optimization
- learning rate tuning
- subsample tuning
- multi-dimensional regression optimization

---

## Model Architecture

| Model | Type |
|---|---|
| XGBoost Regressor | Gradient Boosting |

---

## Evaluation Metrics

| Metrics | Value |
|---|---|
| R² Score | 0.747 |
| MAE | 0.0433 |

---

## Feature Importance

| Features | Impact (%) |
|---|---|
| avg_satisfaction_nghi_viec | 25.93% |
| Age_group_Nhóm Cố vấn | 16.13% |
| Perf_Num | 14.61% |
| Age_group_Nhóm Khởi nghiệp | 12.93% |
| Age_group_Thực tập sinh | 9.29% |
| avg_engagement_nghi_viec | 8.67% |
| PayZone_Num | 8.39% |
| Age_group_Nhóm Quản trị | 4.04% |

---

## Explainable AI (XAI)

Mô hình sử dụng:
- Feature Importance
- SHAP Analysis

nhằm giải thích rõ:
- yếu tố nào ảnh hưởng mạnh nhất đến nghỉ việc
- mức độ tác động của từng biến
- hành vi workforce risk theo từng nhóm nhân sự

---

## SHAP Summary Plot

📊 SHAP Summary Plot

### Purpose
- trực quan hóa mức độ ảnh hưởng của từng feature
- giải thích logic dự báo của mô hình
- tăng tính minh bạch cho HR Analytics

---

## Core Findings

### Satisfaction Is The Strongest Attrition Driver
Satisfaction là biến có ảnh hưởng mạnh nhất trong toàn bộ mô hình.

### Emotional Signals Matter More Than Demographics
Các yếu tố:
- Satisfaction
- Engagement

quan trọng hơn:
- tuổi tác
- vùng lương

trong việc dự báo attrition.

### Workforce Lifecycle Still Matters
Nhóm:
- Cố vấn
- Khởi nghiệp

có tác động đáng kể đến workforce risk structure.

### Performance Is Strongly Related To Attrition
Performance Score:
- ảnh hưởng lớn đến khả năng nghỉ việc
- phản ánh pressure-risk relationship trong workforce.

### Explainable HR Analytics
Mô hình cho phép:
- HR hiểu lý do workforce nghỉ việc
- thay vì chỉ biết ai có khả năng nghỉ việc.

---

# Predictive HR Analytics Conclusion

Hai mô hình Machine Learning cho thấy:

- attrition không chỉ là vấn đề compensation
- workforce experience đóng vai trò quyết định
- emotional analytics quan trọng hơn demographic analytics
- predictive HR có thể hỗ trợ:
  - retention planning
  - workforce optimization
  - compensation strategy
  - talent management
  - strategic HR decision-making


# Strategic Business Insights

Dự án không chỉ tập trung vào phân tích dữ liệu nhân sự mà còn hướng tới việc chuyển đổi HR Analytics thành một công cụ hỗ trợ ra quyết định chiến lược cho doanh nghiệp.

Các insight dưới đây phản ánh những vấn đề cốt lõi về:
- workforce structure
- compensation efficiency
- talent retention
- organizational sustainability
- workforce economics

---

# 9.1 Workforce Aging Risk

## Key Findings

Cấu trúc workforce hiện tại có xu hướng “già hóa” rõ rệt:
- Nhóm Quản trị:
  - 943 nhân sự Fully Meets
- Nhóm Cố vấn:
  - 680 nhân sự Fully Meets

Trong khi:
- nhóm thực tập sinh chỉ có 2 nhân sự.

---

## Business Risk

Doanh nghiệp đang:
- phụ thuộc mạnh vào workforce senior
- thiếu pipeline kế thừa dài hạn.

Điều này tạo ra:
- succession planning risk
- leadership dependency
- knowledge concentration risk
- retirement wave risk

---

## Strategic Recommendation

Doanh nghiệp cần:
- mở rộng Management Trainee pipeline
- tăng đầu tư workforce trẻ
- xây dựng succession planning framework
- triển khai mentoring system giữa senior & junior workforce

---

# 9.2 Compensation Allocation Misalignment

## Key Findings

Dữ liệu cho thấy:
- Zone C workforce có Efficiency Ratio rất cao
- trong khi một phần Zone A workforce:
  - ROI thấp
  - hiệu suất chưa tương xứng với chi phí.

Ví dụ:
- High ROI tại Zone C đạt ratio ~3.0
- một số nhóm Zone A chỉ đạt ~0.5.

---

## Business Risk

Cấu trúc compensation hiện tại:
- chưa phản ánh đúng workforce value
- tồn tại salary-performance mismatch
- làm giảm payroll efficiency.

---

## Strategic Recommendation

Doanh nghiệp cần:
- chuyển sang pay-for-performance model
- tối ưu salary allocation
- tăng tốc promotion cho high performer tại Zone C
- giảm dependency vào high-cost low-efficiency workforce

---

# 9.3 Talent Leakage Risk

## Key Findings

Nhóm Exceeds:
- vẫn tồn tại tỷ lệ nghỉ việc đáng kể (~11.56%).

Đặc biệt:
- nhiều high performer nằm ở:
  - Zone C
  - nhóm Bứt phá
  - workforce trẻ

→ nhóm dễ bị headhunt nhất trên thị trường.

---

## Business Risk

Doanh nghiệp đang:
- giữ được workforce ổn định
- nhưng chưa giữ được workforce xuất sắc.

Điều này tạo ra:
- regrettable attrition
- talent leakage
- long-term innovation risk

---

## Strategic Recommendation

Cần:
- triển khai fast-track promotion
- xây dựng retention package riêng cho high performer
- áp dụng ESOP / performance bonus
- tăng career growth visibility cho workforce trẻ

---

# 9.4 Emotional Attrition Signals

## Key Findings

Machine Learning cho thấy:
- Satisfaction là attrition driver mạnh nhất.
- Engagement cũng có tác động lớn hơn:
  - PayZone
  - demographic variables.

---

## Business Meaning

Nhân sự:
- không chỉ nghỉ việc vì lương
- mà nghỉ việc vì:
  - burnout
  - disengagement
  - thiếu recognition
  - môi trường quản lý kém

---

## Strategic Recommendation

Doanh nghiệp cần:
- đo lường Engagement định kỳ
- triển khai Pulse Survey
- đào tạo leadership soft skills
- xây dựng employee experience framework

---

# 9.5 Backbone Workforce Attrition

## Key Findings

Nhóm Fully Meets:
- đóng góp 10.86% tổng attrition toàn công ty.

Dù:
- không phải high performer
- cũng không phải low performer

nhưng đây là:
- nhóm backbone workforce lớn nhất.

---

## Business Risk

Nếu backbone workforce rời đi hàng loạt:
- operational stability sẽ suy giảm mạnh
- workload pressure tăng cao
- retention cost tăng dần theo thời gian.

---

## Strategic Recommendation

Cần:
- tăng job rotation
- cải thiện career mobility
- tạo growth pathway cho workforce ổn định
- tránh workforce stagnation

---

# 9.6 Leadership Burnout & Dissatisfaction

## Key Findings

Một phần workforce:
- salary cao
- leadership position
- nhưng Satisfaction thấp hơn kỳ vọng.

Biểu hiện:
- dissatisfaction dispersion lớn
- nhiều detractor signals tại Zone A.

---

## Business Risk

Đây là:
- silent attrition risk
- leadership burnout signal
- cultural instability warning

---

## Strategic Recommendation

Doanh nghiệp cần:
- giảm administrative overload
- tăng leadership empowerment
- xây dựng executive well-being programs
- triển khai emotional leadership framework

---

# 9.7 Workforce Optimization Opportunity

## Strategic Opportunity

Dự án cho thấy doanh nghiệp có khả năng:
- tối ưu workforce ROI
- tái cấu trúc compensation
- giảm attrition cost
- cải thiện retention quality
- xây dựng predictive workforce system

---

## Long-term Strategic Direction

HR Analytics không nên chỉ dừng ở:
- reporting
- descriptive dashboards

mà cần chuyển sang:
- predictive HR analytics
- workforce intelligence
- explainable workforce decision-making
- AI-driven talent strategy

---

# Strategic Conclusion

Dự án chứng minh rằng:
- dữ liệu nhân sự có thể được chuyển hóa thành business intelligence
- workforce analytics có khả năng hỗ trợ strategic decision-making
- employee experience là yếu tố cốt lõi của organizational sustainability
- Machine Learning có thể trở thành nền tảng cho thế hệ HR Analytics hiện đại


# Strategic Recommendations

Dựa trên toàn bộ kết quả phân tích KPI, Workforce Analytics và Machine Learning, dự án đề xuất một số định hướng chiến lược nhằm:
- tối ưu hiệu quả workforce
- giảm attrition risk
- nâng cao ROI nhân sự
- tăng tính bền vững của tổ chức
- cải thiện chất lượng quản trị nhân lực dài hạn

---

# 10.1 Redesign Compensation Structure

## Current Problem

Cấu trúc lương hiện tại tồn tại:
- salary-performance mismatch
- high-cost low-efficiency workforce
- underpaid high performer workforce

Ví dụ:
- Zone C tạo ROI rất cao
- trong khi một phần Zone A có Efficiency Ratio dưới break-even.

---

## Strategic Direction

Doanh nghiệp cần:
- chuyển từ seniority-based pay sang performance-based pay
- áp dụng compensation structure linh hoạt hơn
- tối ưu salary allocation theo workforce value thực tế

---

## Recommended Actions

### Pay-for-Performance
- tăng tỷ trọng thưởng hiệu suất
- giảm dependency vào fixed salary growth

### Fast-track Salary Review
Cho phép:
- high performer
- workforce trẻ
- talent nhóm Exceeds

được tăng lương nhanh hơn chu kỳ truyền thống.

### Compensation Benchmarking
- đối chiếu mức lương thị trường
- đặc biệt với nhóm:
  - Bứt phá
  - Exceeds
  - Zone C workforce

---

# 10.2 Succession Planning Strategy

## Current Problem

Workforce structure hiện tại:
- phụ thuộc mạnh vào nhóm:
  - Cố vấn
  - Quản trị
- pipeline kế thừa còn mỏng.

---

## Business Risk

Nếu workforce senior rời đi:
- doanh nghiệp có nguy cơ:
  - mất knowledge base
  - leadership continuity
  - mentoring capability

---

## Strategic Direction

Xây dựng:
- long-term succession planning framework
- workforce transition roadmap

---

## Recommended Actions

### Management Trainee Program
Mở rộng:
- trainee hiring
- fresher recruitment
- graduate development pipeline

### Mentoring Framework
Triển khai:
- senior-to-junior mentoring
- leadership shadowing
- knowledge transfer programs

### Leadership Pipeline Development
Xây dựng:
- talent pool
- internal successor mapping
- promotion readiness tracking

---

# 10.3 Retention & Talent Management

## Current Problem

Nhóm Exceeds:
- vẫn có attrition đáng kể
- đặc biệt ở workforce trẻ và Zone C.

---

## Strategic Direction

Doanh nghiệp cần:
- chuyển từ “retention đại trà”
sang:
- strategic talent retention.

---

## Recommended Actions

### Stay Interview Program
Thực hiện:
- phỏng vấn giữ chân nhân tài
- workforce sentiment analysis

### Retention Package
Áp dụng:
- ESOP
- performance bonus
- flexible benefit
- accelerated promotion

### Career Visibility
Tăng:
- transparency trong promotion path
- visibility về career growth

---

# 10.4 Workforce Efficiency Optimization

## Current Problem

Một phần workforce:
- salary cao
- nhưng ROI thấp
- efficiency dưới break-even level.

---

## Strategic Direction

Tối ưu:
- workforce allocation
- payroll efficiency
- organizational productivity

---

## Recommended Actions

### Workforce Rebalancing
- dịch chuyển talent hiệu quả cao lên vị trí chiến lược
- giảm dependency vào low-efficiency workforce

### Early Warning System
Xây dựng dashboard cảnh báo:
- Efficiency Ratio < 0.8
- high attrition probability
- burnout signals

### Workforce ROI Monitoring
Theo dõi:
- ROI theo phòng ban
- ROI theo nhóm tuổi
- ROI theo PayZone

---

# 10.5 Engagement & Satisfaction Monitoring

## Current Problem

Machine Learning cho thấy:
- Satisfaction & Engagement
là:
- attrition drivers mạnh nhất.

---

## Strategic Direction

Doanh nghiệp cần:
- quản trị employee experience
như một KPI chiến lược.

---

## Recommended Actions

### Pulse Survey System
Đo lường:
- Satisfaction
- Engagement
- Emotional Workforce Signals

theo chu kỳ hàng tháng/quý.

### Leadership Soft Skills Training
Đào tạo:
- emotional leadership
- communication
- coaching mindset
- employee empathy

### Burnout Prevention Program
Triển khai:
- workload balancing
- flexible working
- executive well-being support

---

# 10.6 Workforce Stability & Organizational Sustainability

## Strategic Direction

HR Analytics cần trở thành:
- strategic business function
thay vì:
- reporting support function.

---

## Recommended Actions

### Predictive HR Dashboard
Xây dựng:
- predictive attrition dashboard
- workforce risk monitoring system
- explainable workforce analytics

### AI-driven Workforce Planning
Ứng dụng:
- Machine Learning
- predictive modeling
- workforce forecasting

vào:
- manpower planning
- retention planning
- workforce optimization

### Data-driven HR Decision Making
Chuyển đổi:
- HR intuition
thành:
- HR intelligence & analytics-driven strategy

---

# Strategic Recommendation Summary

| Strategic Area | Key Direction |
|---|---|
| Compensation | Pay-for-performance |
| Retention | Talent-focused retention |
| Workforce Planning | Succession pipeline |
| HR Analytics | Predictive workforce analytics |
| Employee Experience | Engagement-centered strategy |
| Workforce Efficiency | ROI optimization |
| Leadership Strategy | Burnout prevention & empowerment |

---

# Final Strategic Perspective

Dự án cho thấy:
- workforce data có thể trở thành strategic asset
- HR Analytics có khả năng hỗ trợ business transformation
- employee experience là nền tảng của organizational sustainability
- predictive HR sẽ là xu hướng cốt lõi trong quản trị nhân sự hiện đại


# Technology Stack

Dự án được xây dựng bằng hệ sinh thái Python Data Analytics & Machine Learning nhằm:
- xử lý dữ liệu nhân sự quy mô lớn
- trực quan hóa KPI
- phân tích workforce behavior
- triển khai predictive HR analytics
- giải thích mô hình Machine Learning

---

# Core Programming Language

| Technology | Purpose |
|---|---|
| Python | Ngôn ngữ chính cho toàn bộ dự án |

---

# Data Processing & Analysis

| Library | Purpose |
|---|---|
| Pandas | Data cleaning, transformation, KPI aggregation |
| NumPy | Tính toán số học & xử lý dữ liệu |
| Datetime | Xử lý dữ liệu thời gian |
| Collections | Hỗ trợ thống kê & grouping logic |

---

# Data Visualization

| Library | Purpose |
|---|---|
| Matplotlib | Visualization framework |
| Seaborn | Statistical visualization & HR charts |
| Plotly | Interactive workforce dashboard |

---

# Machine Learning & Predictive Analytics

| Library | Purpose |
|---|---|
| Scikit-learn | Random Forest, preprocessing, evaluation metrics |
| XGBoost | Advanced predictive modeling |
| SHAP | Explainable AI & feature impact analysis |

---

# Machine Learning Techniques

## Supervised Learning
- Random Forest Regressor
- XGBoost Regressor

---

## Feature Engineering
- Encoding categorical variables
- Dummy variable creation
- Workforce segmentation
- PayZone transformation

---

## Model Evaluation
- R² Score
- Mean Absolute Error (MAE)
- Feature Importance Analysis

---

# Explainable AI (XAI)

Dự án triển khai:
- SHAP Summary Plot
- Feature Importance

nhằm:
- giải thích logic dự báo
- tăng khả năng interpretability
- hỗ trợ explainable workforce analytics

---

# Visualization Techniques

| Visualization | Usage |
|---|---|
| Grouped Bar Chart | Performance distribution |
| Stacked Bar Chart | Workforce composition |
| Boxplot | Satisfaction distribution |
| Heatmap | Workforce intensity matrix |
| Trend Line | Efficiency trends |
| Interactive Plotly Charts | Workforce exploration |
| SHAP Plot | Explainable AI |

---

# HR Analytics Techniques

## Workforce Analytics
- Workforce segmentation
- Attrition analysis
- Compensation analysis
- Employee experience analytics

---

## Predictive HR Analytics
- Attrition prediction
- Workforce risk scoring
- Engagement impact analysis
- Satisfaction-driven retention modeling

---

# Development Environment

| Tool | Purpose |
|---|---|
| Jupyter Notebook | Data exploration & modeling |
| VS Code | Development environment |
| CSV Data Sources | Workforce datasets |

---

# Technical Capabilities Demonstrated

## Data Analytics
- Data Cleaning
- Exploratory Data Analysis (EDA)
- KPI Engineering
- Workforce Metrics Design

---

## Business Analytics
- HR KPI Analysis
- Workforce Risk Assessment
- Strategic Workforce Insights
- Organizational Analytics

---

## Machine Learning
- Predictive Modeling
- Explainable AI
- Feature Importance Analysis
- Workforce Forecasting

---

# Technical Conclusion

Dự án thể hiện khả năng:
- kết hợp Business Analytics & Machine Learning
- triển khai HR Analytics end-to-end
- xây dựng predictive workforce system
- chuyển đổi workforce data thành strategic business intelligence


# Project Outcomes

Dự án đã xây dựng thành công một hệ thống HR Analytics toàn diện kết hợp:
- Data Analytics
- Workforce Intelligence
- Predictive Modeling
- Explainable AI

nhằm hỗ trợ doanh nghiệp:
- tối ưu workforce efficiency
- giảm attrition risk
- nâng cao hiệu quả sử dụng quỹ lương
- cải thiện strategic HR decision-making

---

# 12.1 Workforce Analytics Outcomes

## Built End-to-End HR KPI Framework

Thiết kế hệ thống KPI đa chiều bao gồm:
- Performance Analytics
- Compensation Analysis
- Engagement Metrics
- Satisfaction Metrics
- Workforce ROI
- Attrition Analysis
- Workforce Lifecycle Analytics

Tổng hệ thống:
- 10+ KPI chiến lược
- nhiều lớp workforce segmentation
- multi-dimensional workforce analysis

---

## Identified Workforce Structure Risks

Phát hiện:
- workforce aging trend
- leadership dependency
- succession planning risk
- knowledge concentration risk

Thông qua:
- age-based workforce analysis
- workforce distribution analytics

---

## Identified Compensation Inefficiencies

Phân tích cho thấy:
- tồn tại salary-performance mismatch
- một phần workforce salary cao nhưng ROI thấp
- workforce trẻ tại Zone C có efficiency vượt trội

Từ đó:
- xác định opportunity tái cấu trúc compensation strategy

---

## Detected Talent Leakage Signals

Xác định:
- regrettable attrition trong nhóm Exceeds
- retention gap với workforce trẻ
- emotional disengagement risk

Thông qua:
- engagement analytics
- satisfaction analytics
- attrition analysis

---

# 12.2 Predictive HR Analytics Outcomes

## Developed Attrition Prediction Models

Triển khai:
- Random Forest Regressor
- XGBoost Regressor

nhằm:
- dự báo attrition behavior
- xác định workforce risk factors
- hỗ trợ predictive HR analytics

---

## Achieved Strong Predictive Performance

### XGBoost Results
| Metrics | Value |
|---|---|
| R² Score | 0.747 |
| MAE | 0.0433 |

Mô hình cho thấy:
- khả năng dự báo attrition tốt
- tính ổn định cao
- phù hợp workforce analytics use-case

---

## Built Explainable AI Framework

Triển khai:
- SHAP Analysis
- Feature Importance

nhằm:
- giải thích logic dự báo
- tăng interpretability
- hỗ trợ explainable HR decision-making

---

## Identified Core Attrition Drivers

Machine Learning xác định:
- Satisfaction
- Engagement
- Performance
- Age Group

là các yếu tố ảnh hưởng mạnh nhất đến attrition.

Insight quan trọng:
- employee experience có ảnh hưởng lớn hơn demographic variables.

---

# 12.3 Strategic Business Outcomes

## Converted HR Data into Business Intelligence

Dự án chuyển đổi:
- HR operational data
thành:
- strategic workforce intelligence

hỗ trợ:
- workforce planning
- retention strategy
- compensation optimization
- talent management

---

## Enabled Data-driven HR Decision Making

Hệ thống phân tích giúp:
- giảm dependency vào cảm tính
- tăng khả năng ra quyết định dựa trên dữ liệu
- hỗ trợ predictive workforce management

---

## Built Foundation for Predictive HR System

Dự án tạo nền tảng cho:
- AI-driven HR Analytics
- predictive workforce monitoring
- intelligent retention systems
- workforce forecasting

---

# Business Value Summary

| Strategic Area | Business Value |
|---|---|
| Workforce Analytics | Hiểu sâu cấu trúc workforce |
| Compensation Analytics | Tối ưu quỹ lương |
| Attrition Analytics | Giảm workforce loss |
| Predictive HR | Dự báo workforce risk |
| Explainable AI | Minh bạch hóa quyết định |
| Strategic HR | Hỗ trợ workforce planning |

---

# Final Outcome Perspective

Dự án chứng minh rằng:
- HR Analytics có thể trở thành strategic business function
- workforce data có khả năng tạo business intelligence thực tế
- Machine Learning có thể hỗ trợ workforce optimization
- employee experience là yếu tố cốt lõi của organizational sustainability


# Future Improvements

Dự án hiện tại tập trung vào:
- descriptive analytics
- workforce KPI analysis
- predictive attrition modeling

Trong tương lai, hệ thống có thể được mở rộng thành một nền tảng Workforce Intelligence hoàn chỉnh với khả năng:
- real-time analytics
- automated monitoring
- advanced forecasting
- interactive business intelligence

---

# 13.1 Interactive Dashboard Deployment

## Current Limitation

Các biểu đồ hiện tại:
- chủ yếu chạy trong notebook environment
- chưa có centralized analytics platform

---

## Future Direction

Triển khai:
- interactive HR dashboard
- executive workforce monitoring system

---

## Potential Technologies

| Technology | Purpose |
|---|---|
| Power BI | Executive HR dashboard |
| Tableau | Workforce visualization |
| Streamlit | Interactive Python dashboard |
| Plotly Dash | Real-time analytics app |

---

# 13.2 Real-time Workforce Monitoring

## Future Goal

Xây dựng:
- real-time HR monitoring system
- automated workforce alerts
- workforce risk detection engine

---

## Planned Features

### Early Warning Alerts
Cảnh báo khi:
- attrition probability tăng cao
- engagement giảm mạnh
- satisfaction xuống thấp
- Efficiency Ratio dưới break-even

---

### Workforce Risk Scoring
Tạo:
- employee risk score
- department risk index
- burnout probability tracking

---

# 13.3 Advanced Machine Learning Improvements

## Current Limitation

Mô hình hiện tại:
- tập trung vào regression-based attrition prediction
- chưa tối ưu hyperparameter chuyên sâu

---

## Future Direction

### Hyperparameter Optimization
Ứng dụng:
- Grid Search
- Random Search
- Bayesian Optimization

---

### Advanced Ensemble Learning
Mở rộng:
- LightGBM
- CatBoost
- Stacking Ensemble
- Blending Models

---

### Deep Learning Exploration
Nghiên cứu:
- Neural Networks
- Sequential Workforce Prediction
- Behavioral Pattern Modeling

---

# 13.4 Survival Analysis for Attrition Prediction

## Future Goal

Triển khai:
- Survival Analysis
- Time-to-Attrition Modeling

---

## Business Meaning

Không chỉ dự báo:
- ai sẽ nghỉ việc

mà còn dự báo:
- khi nào nhân sự có khả năng nghỉ việc

---

## Potential Techniques

| Technique | Purpose |
|---|---|
| Kaplan-Meier | Attrition timeline analysis |
| Cox Proportional Hazard Model | Workforce survival probability |
| Survival Regression | Time-to-exit forecasting |

---

# 13.5 Workforce Forecasting System

## Future Goal

Xây dựng hệ thống:
- workforce demand forecasting
- manpower planning prediction
- organizational growth simulation

---

## Planned Capabilities

### Workforce Supply Forecasting
Dự báo:
- workforce shortages
- talent gaps
- leadership succession risk

---

### Scenario Simulation
Mô phỏng:
- hiring strategy
- compensation restructuring
- retention policy impact

---

# 13.6 Advanced Explainable AI (XAI)

## Future Goal

Mở rộng khả năng:
- explainable workforce analytics
- transparent HR AI systems

---

## Potential Improvements

### Local Explainability
Ứng dụng:
- LIME
- SHAP force plots
- individual workforce explanation

---

### Fairness & Bias Detection
Phân tích:
- demographic bias
- compensation bias
- model fairness

---

# 13.7 Data Engineering & Automation

## Future Goal

Tự động hóa:
- HR data pipeline
- workforce ETL process
- analytics workflow

---

## Potential Technologies

| Technology | Purpose |
|---|---|
| SQL | Workforce database management |
| Airflow | Workflow automation |
| APIs | HR system integration |
| Cloud Storage | Workforce data centralization |

---

# Long-term Vision

Mục tiêu dài hạn:
- chuyển đổi dự án từ HR Analytics Project
thành:
- AI-driven Workforce Intelligence Platform

có khả năng:
- predictive workforce monitoring
- automated HR insights
- strategic workforce optimization
- real-time decision support

---

# Final Future Perspective

Dự án có tiềm năng phát triển thành:
- enterprise HR analytics system
- predictive workforce platform
- explainable HR AI solution
- intelligent workforce management ecosystem
 