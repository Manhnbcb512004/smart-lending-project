-- 1. Tạo Database mới
CREATE DATABASE IF NOT EXISTS SmartLending_DB;
USE SmartLending_DB;

-- 2. Xóa bảng nếu đã tồn tại để làm mới (Cẩn thận khi dùng)
DROP TABLE IF EXISTS lending_data;

CREATE TABLE lending_data (
    -- ID tự tăng (MySQL sẽ tự tạo, không có trong CSV)
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Nhân khẩu học
    Age INT,
    Gender VARCHAR(20),
    Education_Level VARCHAR(50), -- Khớp: Education Level
    Marital_Status VARCHAR(50),  -- Khớp: Marital Status
    
    -- Tài chính (Thứ tự khớp theo CSV)
    Income DECIMAL(15, 2),
    Credit_Score FLOAT,          -- Để FLOAT vì CSV có thể có .0
    Loan_Amount DECIMAL(15, 2),
    Loan_Purpose VARCHAR(50),
    Employment_Status VARCHAR(50),
    Years_at_Current_Job INT,
    Payment_History VARCHAR(50),
    Debt_to_Income_Ratio FLOAT,
    Assets_Value DECIMAL(15, 2),
    Number_of_Dependents FLOAT,  -- Để FLOAT trước vì CSV là 0.0, 1.0...
    
    -- Địa lý
    City VARCHAR(100),
    State VARCHAR(50),
    Country VARCHAR(100),
    
    -- Rủi ro
    Previous_Defaults FLOAT,     -- CSV là 2.0, 3.0...
    Marital_Status_Change INT,   -- Khớp: 0, 1, 2
    Risk_Rating VARCHAR(20),
    
    -- Thời gian hệ thống
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


TRUNCATE TABLE lending_data;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/financial_risk_assessment.csv'
INTO TABLE lending_data
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
-- Sử dụng biến tạm @ cho các cột hay bị trống dữ liệu
(Age, Gender, @Education_Level, @Marital_Status, @Income, @Credit_Score, @Loan_Amount, 
 @Loan_Purpose, @Employment_Status, Years_at_Current_Job, @Payment_History, 
 Debt_to_Income_Ratio, @Assets_Value, @Number_of_Dependents, City, State, 
 Country, @Previous_Defaults, Marital_Status_Change, Risk_Rating)
SET 
    -- Nếu biến trống ('') thì gán NULL, nếu có dữ liệu thì nạp vào
    Income = IF(@Income = '', NULL, @Income),
    Credit_Score = IF(@Credit_Score = '', NULL, @Credit_Score),
    Loan_Amount = IF(@Loan_Amount = '', NULL, @Loan_Amount),
    Assets_Value = IF(@Assets_Value = '', NULL, @Assets_Value),
    Number_of_Dependents = IF(@Number_of_Dependents = '', NULL, @Number_of_Dependents),
    Previous_Defaults = IF(@Previous_Defaults = '', NULL, @Previous_Defaults),
    
    -- Làm sạch khoảng trắng cho các cột chữ
    Education_Level = TRIM(@Education_Level),
    Marital_Status = TRIM(@Marital_Status),
    Loan_Purpose = TRIM(@Loan_Purpose),
    Employment_Status = TRIM(@Employment_Status),
    Payment_History = TRIM(@Payment_History);
 
 SELECT * FROM lending_data;
-- Clean data 
-- Kiểm tra số lượng giá trị NULL trong các cột trọng yếu
SELECT 
    COUNT(*) AS Total_Rows,
    SUM(CASE WHEN Income IS NULL THEN 1 ELSE 0 END) AS Missing_Income,
    SUM(CASE WHEN "Credit Score" IS NULL THEN 1 ELSE 0 END) AS Missing_CreditScore,
    SUM(CASE WHEN "Asset Value" IS NULL THEN 1 ELSE 0 END) AS Missing_Assets,
    SUM(CASE WHEN Age < 18 OR Age > 70 THEN 1 ELSE 0 END) AS Invalid_Age
FROM lending_data;
-- SCRIPT SQL làm sạch gọn gàng cho duy nhất INCOME  
CREATE TABLE Risk_Data_Final AS 
WITH Education_Avg AS (
    -- Tính thu nhập trung vị theo từng trình độ học vấn 
    SELECT 
        Education_Level,
        AVG(Income)  AS avg_income
     FROM lending_data
     WHERE Income IS NOT NULL
     GROUP BY Education_Level
)    
-- Kết hợp bảng gốc và bảng trung bình để làm sạch
SELECT 
    l.*, -- Lấy tất cả các cột cũ 
    -- Chỉ thay thế Income bằng giá trị trung bình của nhóm nếu bị NULL, còn lại giữ nguyên  
    COALESCE(l.Income, e.avg_income) AS Cleaned_Income,
    -- Tính toán lại DTI vì Income đã được điền mới(Loan Amount / Cleaned_Income)
    -- Dùng NULLIF để tránh lỗi chia cho 0
    ROUND(
		CAST(l.Loan_Amount AS DECIMAL(15,2)) / 
        NULLIF(COALESCE(l.Income, e.avg_income), 0),
4) AS Updated_DTI

FROM lending_data l
LEFT JOIN Education_Avg e ON l.Education_Level = e.Education_Level 
WHERE l.Age >= (l.Years_at_Current_Job + 18); -- Vẫn giữ nguyên bộ lọc tuổi tác 
-- Kiểm tra tính nhất quán 
-- xóa các dòng có số năm làm việc vô lý so với tuổi  
-- Giả định bắt đầu làm việc sớm nhất là từ 16 tuổi 
DELETE FROM Risk_Data_Final
WHERE Age < (Years_at_Current_Job + 16);

-- Quy  chuẩn hóa  dữ liệu định tính (Standardization)
UPDATE Risk_Data_Final
SET Payment_History = UPPER(TRIM(Payment_History)),
    Loan_Purpose = UPPER(TRIM(Loan_Purpose));
-- fix lỗi capping    
-- Bước 1: Tìm giá trị ngưỡng P95 cho Income và Loan_Amount
-- (Sử dụng LIMIT để lấy giá trị tại vị trí 95%) 

SET @p95_income = (
    SELECT Cleaned_Income
    FROM Risk_Data_Final
    ORDER BY Cleaned_Income ASC
    LIMIT 1 OFFSET 14250 -- 14250 là 95% của 15.000 dòng 
);

SET @p95_loan = (
    SELECT Loan_Amount
    FROM Risk_Data_Final
    ORDER BY Loan_Amount ASC 
	LIMIT 1 OFFSET 14250
);
-- Bước 2: cập nhật  (Capping) các giá trị vượt ngưỡng về mức p95
UPDATE Risk_Data_Final
SET 
    Cleaned_Income = CASE 
		WHEN Cleaned_Income > @p95_income THEN @p95_income
        ELSE Cleaned_Income
    END,
    Loan_Amount = CASE 
        WHEN Loan_Amount > @p95_loan THEN @o95_loan
        ELSE Loan_Amount
	END;
-- code feature engineering
CREATE TABLE Final_Scorecard_Data AS 
SELECT 
    *,
    -- 1.Tính lại DTI dựa trên dữ liệu đã Cleaned và capped
    -- Công thức:  Khoản vay / Thu thâp (Đã xử lý chia cho 0)
    ROUND(
        CAST(Loan_Amount AS DECIMAL(15,2)) / NULLIF(Cleaned_Income, 0),
	4) AS Final_DTI,
    
    -- 2. ordinal Encoding cho Education_Level (Chuyển chữ thành số có thứ tự
    -- Giúp mô hình hiểu được cấp bậc học vấn 
    CASE 
        WHEN UPPER(TRIM(Education_Level)) = 'HIGH SCHOOL' THEN 1
        WHEN UPPER(TRIM(Education_Level)) = 'BACHELOR' THEN 2
        WHEN UPPER(TRIM(Education_Level)) = 'MASTER' THEN 3
        WHEN UPPER(TRIM(Education_Level)) = 'PHD' THEN 4
        ELSE 0 
	END AS Education_Rank,
    
    -- 3. Tạo biến flag (Biến cờ) Cho nợ xấu quá khứ 
    CASE
        WHEN Previous_Defaults > 0 THEN 1
        ELSE 0
	END AS Has_Default_History,
    
    -- 4.Phân nhóm thâm niên công tác (Binning)
    CASE 
		WHEN Years_at_Current_Job < 2 THEN 'Junior'
        WHEN Years_at_Current_Job BETWEEN 2 AND 5 THEN 'Mid'
        WHEN Years_at_Current_Job > 5 THEN 'Senior'
        ELSE 'Unknow'
	END AS Job_Tenure_Group
    
FROM Risk_Data_Final;
-- KIỂM TRA     
SELECT 
     Education_Level, Education_Rank,
     Loan_Amount, Cleaned_Income, final_DTI
FROM Final_Scorecard_Data
LIMIt 10;
-- FIX LỖi 
-- Xóa bảng cũ nếu tồn tại để làm mới hoàn toàn
DROP TABLE IF EXISTS Final_Scorecard_Data;

CREATE TABLE Final_Scorecard_Data AS 
SELECT 
    l.*, -- Lấy tất cả cột từ bảng trước
    
    -- 1. Tạo cột Rank mới (Dùng tên khác để tránh trùng lặp)
    CASE 
        WHEN Education_Level LIKE 'High School%' THEN 1
        WHEN Education_Level LIKE 'Bachelor%' THEN 2
        WHEN Education_Level LIKE 'Master%' THEN 3
        WHEN Education_Level LIKE 'PhD%' THEN 4
        ELSE 0 
    END AS Education_Ordinal_Rank,

    -- 2. Tạo biến Flag cho nợ xấu (Nếu bảng trước chưa có)
    CASE 
        WHEN Previous_Defaults > 0 THEN 1 
        ELSE 0 
    END AS Default_Flag

FROM Risk_Data_Final l;
-- Final Touch
UPDATE Final_Scorecard_Data 
SET 
    -- 1. Nếu Updated_DTI bị NULL (do khoản vay trống), coi như bằng 0
    Updated_DTI = COALESCE(Updated_DTI, 0),
    
    -- 2. Nếu Previous_Defaults bị NULL, coi như khách chưa từng nợ xấu (= 0)
    Previous_Defaults = COALESCE(Previous_Defaults, 0),
    
    -- 3. Cập nhật lại Default_Flag cho những dòng vừa điền 0 ở trên
    Default_Flag = CASE WHEN Previous_Defaults > 0 THEN 1 ELSE 0 END;
UPDATE Final_Scorecard_Data 
SET 
    -- Xử lý nốt các ô Loan_Amount còn trống
    Loan_Amount = COALESCE(Loan_Amount, 0),
    
    -- Điền nốt Income nếu còn dòng nào sót (để tránh lỗi chia cho 0 sau này)
    Income = COALESCE(Income, 0),
    
    -- Đảm bảo Credit_Score không bị NULL (điền giá trị trung bình hoặc 0)
    Credit_Score = COALESCE(Credit_Score, 0);
  
SELECT * FROM Final_Scorecard_Data;
-- Xử lý nốt 2 giá trị còn lại 
UPDATE Final_Scorecard_Data
SET 
    -- 1. Xử lý giá trị tài sản:Điền bằng giá trị trung bình 
    Assets_Value = COALESCE(Assets_Value, (SElECT AVG(Assets_Value) FROM Risk_Data_Final)),
    
    -- 2. Xử lý số người phụ thuộc: Điền bằng 0
    Number_of_Dependents = COALESCE(Number_of_Dependents, 0),
    
    -- 3. Xử lý Marital_Status nếu có NULL (Điền 'Unknown')
    Marital_Status = COALESCE(Marital_Status, 'Unknown');
    
 SELECT * FROM  lending_data;
 --- clean Credit score 
 -- Tạo bảng tạm median theo nhóm học vấn
CREATE TEMPORARY TABLE median_scores AS
SELECT Education_Ordinal_Rank,
       AVG(Credit_Score) AS median_score
FROM (
    SELECT Education_Ordinal_Rank, Credit_Score
    FROM final_scorecard_data
    WHERE Credit_Score > 0
) t
GROUP BY Education_Ordinal_Rank;

-- Cập nhật Credit_Score = 0 bằng median theo nhóm
UPDATE final_scorecard_data c
JOIN median_scores m 
  ON c.Education_Ordinal_Rank = m.Education_Ordinal_Rank
SET c.Credit_Score = m.median_score
WHERE c.Credit_Score = 0;

SELECT 
Loan_Amount,
Cleaned_Income
FROM final_scorecard_data; 
  
 

 
 

   