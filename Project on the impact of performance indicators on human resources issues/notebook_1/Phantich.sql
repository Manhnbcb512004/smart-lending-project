-- 1. Tạo Database
CREATE DATABASE IF NOT EXISTS project1;
USE project1;

-- 2. Tạo bảng HR_Data với các kiểu dữ liệu phù hợp
CREATE TABLE IF NOT EXISTS hr_data_analysis (
    `Employee ID` INT,
    `StartDate` VARCHAR(20),
    `Title` VARCHAR(100),
    `BusinessUnit` VARCHAR(50),
    `EmployeeStatus` VARCHAR(50),
    `EmployeeType` VARCHAR(50),
    `PayZone` VARCHAR(20),
    `EmployeeClassificationType` VARCHAR(50),
    `DepartmentType` VARCHAR(100),
    `Division` VARCHAR(100),
    `DOB` VARCHAR(20),
    `State` VARCHAR(10),
    `GenderCode` VARCHAR(20),
    `RaceDesc` VARCHAR(50),
    `MaritalDesc` VARCHAR(50),
    Performance_Score VARCHAR(50),
    `Current Employee Rating` INT,
    `Survey Date` VARCHAR(20),
    Engagement_Score INT,
    `Satisfaction Score` INT,
    `Work-Life Balance Score` INT,
    `Training Date` VARCHAR(20),
    `Training Program Name` VARCHAR(100),
    `Training Type` VARCHAR(50),
    `Training Outcome` VARCHAR(50),
    `Training Duration(Days)` INT,
    `Training Cost` DECIMAL(10,2),
    `Age` INT
);
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Cleaned_HR_Data_Analysis (1) - Cleaned_HR_Data_Analysis (1).csv.csv'
INTO TABLE hr_data_analysis
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

SELECT * FROM hr_data_analysis;
--- Hiệu suất 
SELECT 
    Employee_ID, 
    EmployeeStatus, 
    PayZone, 
    Performance_Score, 
    Engagement_Score, 
    Satisfaction_Score, 
    Age 
FROM hr_data_analysis
WHERE (Employee_ID BETWEEN 1001 AND 1735)
   OR (Employee_ID BETWEEN 3427 AND 4000)
ORDER BY Employee_ID;

-- Lương theo hiệu suất 
SELECT 
    PayZone,
    Performance_Score AS PerformanceScore,
    COUNT(*) AS so_luong_nv,
    -- Gán điểm chuẩn theo đúng file mẫu: Exceeds=4, Fully Meets=3, Needs=2, PIP=1
    CASE 
        WHEN Performance_Score = 'Exceeds' THEN 4.00
        WHEN Performance_Score = 'Fully Meets' THEN 3.00
        WHEN Performance_Score = 'Needs Improvement' THEN 2.00
        WHEN Performance_Score = 'PIP' THEN 1.00
    END AS avg_performance_point,
    -- Công thức tính Efficiency_ratio: Lấy điểm chuẩn chia cho trọng số vùng (A:3, B:2, C:1)
    CAST(
        (CASE 
            WHEN Performance_Score = 'Exceeds' THEN 4.00
            WHEN Performance_Score = 'Fully Meets' THEN 3.00
            WHEN Performance_Score = 'Needs Improvement' THEN 2.00
            WHEN Performance_Score = 'PIP' THEN 1.00
        END) / 
        (CASE 
            WHEN PayZone = 'Zone A' THEN 3.0
            WHEN PayZone = 'Zone B' THEN 2.0
            WHEN PayZone = 'Zone C' THEN 1.0
        END) 
    AS DECIMAL(10,2)) AS efficiency_ratio
FROM hr_data_analysis
GROUP BY PayZone, Performance_Score
ORDER BY 
    FIELD(PayZone, 'Zone A', 'Zone B', 'Zone C'),
    FIELD(Performance_Score, 'Exceeds', 'Fully Meets', 'Needs Improvement', 'PIP');
-- Nhóm tuổi 
WITH PhanLoaiNhanVien AS (
    SELECT 
        Age,
        CASE 
            WHEN Age < 18 THEN N'Nhóm thực tập sinh'
            WHEN Age BETWEEN 18 AND 25 THEN N'Nhóm Khởi nghiệp'
            WHEN Age BETWEEN 26 AND 35 THEN N'Nhóm Bứt phá'
            WHEN Age BETWEEN 36 AND 55 THEN N'Nhóm Cố vấn'
            WHEN Age > 55 THEN N'Nhóm Quản trị'
        END AS Age_group,
        CASE 
            WHEN Performance_Score = 'Exceeds' THEN 4
            WHEN Performance_Score = 'Fully Meets' THEN 3
            WHEN Performance_Score = 'Needs Improvement' THEN 2
            WHEN Performance_Score = 'PIP' THEN 1
        END AS avg_performance_point,
        Performance_Score AS PerformanceScore
    FROM  hr_data_analysis
    WHERE Performance_Score IN ('Exceeds', 'Fully Meets', 'Needs Improvement', 'PIP')
),
TongNhom AS (
    SELECT 
        Age_group,
        COUNT(*) AS total_in_group
    FROM PhanLoaiNhanVien
    GROUP BY Age_group
)
SELECT 
    p.Age_group,
    p.PerformanceScore,
    COUNT(*) AS so_luong_nv,
    p.avg_performance_point,
    ROUND(COUNT(*) * p.avg_performance_point * 1.0 / t.total_in_group, 2) AS efficiency_ratio
FROM PhanLoaiNhanVien p
JOIN TongNhom t ON p.Age_group = t.Age_group
GROUP BY 
    p.Age_group, 
    p.PerformanceScore, 
    p.avg_performance_point,
    t.total_in_group
ORDER BY 
    CASE p.Age_group 
        WHEN N'Nhóm thực tập sinh' THEN 1
        WHEN N'Nhóm Khởi nghiệp' THEN 2
        WHEN N'Nhóm Bứt phá' THEN 3
        WHEN N'Nhóm Cố vấn' THEN 4
        WHEN N'Nhóm Quản trị' THEN 5
    END,
    p.avg_performance_point DESC;
--- Nhóm Tinh anh ( nghỉ việc )
WITH AgeTagged AS (
    -- Bước 1: Áp dụng mốc tuổi chuẩn từ file Phantich_theotuoi để đồng bộ Insight
    SELECT *,
        CASE 
            WHEN Age BETWEEN 18 AND 25 THEN 'Nhóm Khởi nghiệp'
            WHEN Age BETWEEN 26 AND 35 THEN 'Bứt phá'
            WHEN Age BETWEEN 36 AND 55 THEN 'Nhóm Cố vấn'
            ELSE 'Nhóm Quản trị'
        END AS Age_group
    FROM hr_data_analysis
    -- Lọc nhóm nhân sự đạt hiệu suất Xuất sắc
    WHERE Performance_Score = 'Exceeds'
)
-- Bước 2: Tổng hợp dữ liệu theo cấu trúc file nghiviec_nhomxs.csv
SELECT 
    Age_group,
    PayZone,
    COUNT(*) AS tong_nv_xuat_sac,
    SUM(CASE WHEN EmployeeStatus = 'Terminated' THEN 1 ELSE 0 END) AS so_nv_da_nghi,
    -- Tính tỷ lệ % nghỉ việc
    CAST(SUM(CASE WHEN EmployeeStatus = 'Terminated' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(10,2)) AS ty_le_nghi_viec_pct,
    -- Các chỉ số tương tác và hài lòng của nhóm đã nghỉ
    CAST(AVG(CASE WHEN EmployeeStatus = 'Terminated' THEN Engagement_Score ELSE NULL END) AS DECIMAL(10,2)) AS avg_engagement_nghi_viec,
    CAST(AVG(CASE WHEN EmployeeStatus = 'Terminated' THEN Satisfaction_Score ELSE NULL END) AS DECIMAL(10,2)) AS avg_satisfaction_nghi_viec
FROM AgeTagged
GROUP BY Age_group, PayZone
-- Bước 3: Chỉ giữ lại các nhóm có nhân viên nghỉ việc để tập trung phân tích rủi ro
HAVING so_nv_da_nghi > 0
-- Sắp xếp theo tỷ lệ nghỉ việc giảm dần để tìm ra các "điểm nóng" (Hotspots)
ORDER BY ty_le_nghi_viec_pct DESC;
-- Tỷ lệ nghỉ việc theo hiệu xuất 
SELECT 
    Performance_Score AS PerformanceScore,
    EmployeeStatus,
    COUNT(*) AS so_luong_nv,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY Performance_Score), 
        2
    ) AS phan_tram_theo_nhom
FROM hr_data_analysis
GROUP BY Performance_Score, EmployeeStatus
ORDER BY Performance_Score, EmployeeStatus;

--- nghỉ việc theo hiệu xuất và nhóm lương 
SELECT 
    CASE 
            WHEN Age < 18 THEN 'Nhóm thực tập sinh'
            WHEN Age BETWEEN 18 AND 25 THEN 'Nhóm Khởi nghiệp'
            WHEN Age BETWEEN 26 AND 35 THEN 'Nhóm Bứt phá'
            WHEN Age BETWEEN 36 AND 55 THEN 'Nhóm Cố vấn'
            ELSE 'Nhóm Quản trị'
    END AS Age_group,
    PayZone,
    Performance_Score AS PerformanceScore,
    COUNT(*) AS so_luong_nv,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM hr_data_analysis), 2) AS phan_tram_tong_nhan_su,
    SUM(CASE WHEN EmployeeStatus = 'Terminated' THEN 1 ELSE 0 END) AS so_nv_da_nghi,
    ROUND(
        SUM(CASE WHEN EmployeeStatus = 'Terminated' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS ty_le_nghi_viec_noi_bo_pct,
    ROUND(AVG(CASE WHEN EmployeeStatus = 'Terminated' THEN Engagement_Score END), 2) AS avg_engagement_nghi_viec,
    ROUND(AVG(CASE WHEN EmployeeStatus = 'Terminated' THEN Satisfaction_Score END), 2) AS avg_satisfaction_nghi_viec
FROM hr_data_analysis
GROUP BY Age_group, PayZone, Performance_Score
ORDER BY Age_group, PayZone, Performance_Score;

 


