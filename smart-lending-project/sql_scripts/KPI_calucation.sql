USE SmartLending_DB;

# Phân tích sơ bộ 
 SELECT * FROM Final_Scorecard_Data;
 -- chia nhóm DTI và tính tỷ lệ nợ xấu Default_Flag
SELECT
Default_Flag, 
     CASE 
         WHEN Debt_to_Income_Ratio <= 0.2 THEN 'Tỷ lệ thấp (dưới 20%)'   
         WHEN Debt_to_Income_Ratio <= 0.4 THEN 'Tỷ lệ trung bình (20-40%)'   
         WHEN Debt_to_Income_Ratio <= 0.6 THEN 'Tỷ lệ khá (40-60%)'
         ELSE 'Tỷ lệ cao (>60%)'
	 END AS  Nhom_DTI,
     COUNT(*) AS So_luong_khach_hang
FROM Final_Scorecard_Data 
GROUP BY Default_Flag, Nhom_DTI
ORDER BY Default_Flag, Nhom_DTI;
-- insight: Tổng số khách hàng nợ tốt thấp hơn nhiều ở cả 3 nhóm DTI
-- Với nhóm nợ tốt: Tỷ lệ nợ trên thu nhập ở nhóm khá và trung bình chiếm tỷ trọng lớn với số lượng khách hàng  gần gấp đôi nhóm tỷ lệ thấp
--- nguyên nhân có thể do Thu nhập của nhóm này k cao tuy nhiên vì vẫn giữ ở mức nợ tốt chứng tỏ kiểm soát đc tổng nợ tương đối ổn định và nhóm có tỷ lệ DTI thấp hơn có thể có mức thu nhập tốt hơn 
--- Nhóm nợ xấu cũng có cơ cấu tương tự nhóm nợ tốt  tuy nhiên tỷ trọng lại gần gấp đôi 
--- đòi hỏi doanh nghiệp cần chia nhỏ nhóm khách hàng để xem phân khúc đang chiếm tỷ trọng lớn nhất của nhóm nợ xấu và có tỷ số DTI tương đối cao  là phân khúc nào

-- Thu nhập trung bình nhóm nợ tốt so với nhóm nợ xấu ( SO SÁNH THU NHẬP )
SELECT 
     Default_Flag,
     AVG(Cleaned_Income) AS AVG_thunhap
FROM final_scorecard_data
GROUP BY Default_Flag;
-- insight 
-- Thu nhập của nhóm nợ xấu có xu hướng cao hơn nhóm nợ tốt 
-- điều này phản ánh nhóm có mức thu nhập  thấp hơn nhưng k nhiều  có tỷ lệ nợ xấu cao , trả chậm hơn yêu cầu -- chiếm dụng vốn tương đối cần siết các khoản vay và áp mức vay giới hạn để k mất vốn chiếm dụng 
--- nhóm nợ tốt có thu nhập cao hơn nhưng cũng k quá vượt trội nhóm này cần có nhiểu mức vay ưu đãi hơn , xét các khách hàng nhiều lần trả đúng hẹn với mức vay tốt hơn 
--- Percentile (phân vị) sắp xếp thu nhập theo nhóm ( PHÂN VỊ ) 
WITH Income_Ranked AS (
    SELECT 
		Default_Flag,
        Cleaned_Income,
        PERCENT_RANK () OVER (PARTITION BY Default_Flag ORDER BY Cleaned_Income) AS p_rank
	FROM final_scorecard_data
)
SELECT 
	Default_Flag,
    -- Lấy giá trị thu nhập gần mức 25%, 50%, 75% nhất
    MIN(CASE WHEN p_rank >= 0.25 THEN Cleaned_Income END) AS P_25,
    MIN(CASE WHEN p_rank >= 0.50 THEN Cleaned_Income END) AS P_median,
    MIN(CASE WHEN p_rank >= 0.75 THEN Cleaned_Income END ) AS P_75
FROM Income_Ranked
GROUP BY Default_Flag;
--- Insight 
--- Mô hình chung ở cả 2 nhóm nợ tốt và nợ xấu tỷ lệ thu nhập đều có xu hướng tăng theo phân vị 
--- tuy nhiên ở mỗi mức phân vị đều có cơ cấu khác nhau 
--- Nhóm 25% tỷ trọng nợ tốt cao hơn điều này chứng tỏ ở mức thu nhập thấp tỷ trọng nợ xấu vẫn thấp hơn nợ tốt 
--- điều này có thể giải thích đc vì với thu nhập thấp người tiêu dùng sẽ e dè hơn trong việc bỏ tiền cũng sẽ có tâm lý sợ k trả đc nợ 
--- Với nhóm thu nhập bình quân (Median) thì đã có sự thay  đổi rõ rệt chỉ số nợ xấu đã kéo gần hơn nợ tốt điều này chứng tỏ người tiêu dùng bắt đầu mua nhiều hơn 
--- với mức thu nhập 75% tỷ lệ vẫn ở mức vẫn sát nhau nhưng nợ xấu cũng k chiếm ưu thế có thể người tiêu dùng 1 kiểm soát nợ tốt k phát sinh nhiều khoản nợ , hoặc thu nhập biến thiên theo chiều hướng tích cực
--- Cách giải quyết với thu nhập ở mức trung bình nhóm nợ xấu đang kéo gần nhóm nợ tốt chứng tỏ thu nhập k phải chỉ tiêu ảnh hưởng chính đến nợ xấu có thể do người tiêu dùng k kiểm soát đc tổng nợ 
--- Biện pháp đè xuất với 2 nhóm 25 và 75 % với  thu nhập nhóm nợ tốt cơ cấu cao hơn nợ xấu đây là cơ cấu ổn và phù hợp nếu an toàn có thể lập vùng an toàn giới hạn khách hàng k vay quá  mức cho phép 
--- với nhóm thu nhập trung bình nợ xấu đang có tỷ trọng tiến gần về nợ tốt yêu cầu nhóm này cần 1 kiểm soát  tốt tổng nợ , trả nợ đúng hẹn có thể trả dần     
-- Phân tích PTI (Payment_to_Income / Loan_to_Income) ( PHÂN TÍCH PTI )
SELECT 
     Default_Flag,
     ROUND((AVG(Loan_Amount / Cleaned_Income)),4) AS Loan_to_Income
FROM final_scorecard_data
WHERE Cleaned_Income  <> 0 
GROUP BY Default_Flag;
--- insight 
--- Với chỉ số Loan to income nhóm nợ xấu đang chiếm tỷ lệ cao hơn có thể đến từ việc phê duyệt số tiền cho vay lớn hơn khả năng chi trả dẫn tới tỷ lệ loan to income nhóm nợ xấu lớn hơn vì k đủ khả năng dẫn tới chậm 
--- biện pháp để tránh việc này phân tích kỹ khả năng chi trả và mức tối đa có thể cho vay 
SELECT * FROM final_scorecard_data;


--- Phần 2 
--- Tính sơ bộ và khái quát các chỉ số quan  trọng min, max, avg, media
-- 1. Tính Min, Max, Average và Median của Credit Score theo nhóm Nợ tốt/Nợ xấu
WITH ranked_scores  AS ( 
    SELECT 
		Default_Flag,
		Credit_Score,
        ROW_NUMBER() OVER (PARTITION BY Default_Flag ORDER BY Credit_Score) AS row_num,
        COUNT(*) OVER (PARTITION BY Default_Flag) AS total_count
	FROM final_scorecard_data
),
median_extracted AS (
	SELECT 
        Default_Flag,
        AVG(credit_score) AS median_score 
	FROM ranked_scores
    WHERE row_num IN (FLOOR((total_count + 1) / 2), CEIL((total_count + 1) / 2)) 
    GROUP  BY Default_Flag
)
SELECT 
    t1.Default_Flag,
    COUNT(*) AS total_customers,
    MIN(t1.Credit_Score) AS min_score,
    MAX(t1.Credit_Score) AS max_score,
    ROUND(AVG(t1.Credit_Score),2) AS avg_score,
    ROUND(t2.median_score,2) AS median_score
FROM  final_scorecard_data t1 
JOIN median_extracted  t2 ON t1.Default_Flag = t2.Default_Flag
GROUP BY t1.Default_Flag, t2.median_score;
-- insight nhóm nợ xấu hơn gấp đôi nhóm nợ tốt 
-- điểm tín dụng thấp nhất cả 2 đều bằng nhau cho thấy là nợ xấu hay nợ tốt điểm mức k khác biệt cho thấy  khách hàng chưa phân hóa rõ rệt 
-- mức cao nhất cũng tương tự đều  k có sự phân hóa cho dù tổng số khách chênh lệch rất lớn 
--- về điểm trung bình có xu hướng cao hơn có thể đến từ nhóm nợ xấu có số khách hàng lớn hơn 
-- trung vị bằng nhau khoảng cách giữa các điểm đều tương tự 

--- Phân dải điểm tín dụng (Credit Score Binning) và Tính tỷ lệ nợ xấu (Bad Rate) 
-- 2. Phân nhóm điểm tín dụng và tính tỷ lệ nợ  xấu trên từng nhóm 
SELECT 
    CASE 
        WHEN Credit_Score < 500 THEN '1. Rất thấp (<500)'
        WHEN Credit_Score BETWEEN 500 AND 599 THEN '2. Thấp (500-599)'
        WHEN Credit_Score BETWEEN 600 AND 699 THEN '3. Trung bình (600-699)'
        WHEN Credit_Score BETWEEN 700 AND 799 THEN '4. Tốt (700-799)'
        ELSE '5. Xuất sắc (>=800)'
	END AS credit_score_tier,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Default_Flag  = 1 THEN 1 ELSE 0 END) AS bad_loans,
    ROUND(SUM(CASE WHEN Default_Flag = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS bad_rate_percentage
FROM final_scorecard_data
GROUP BY credit_score_tier
ORDER BY credit_score_tier;

-- chia nhóm để đi sâu hơn từng nhóm 
-- đầu tiên chỉ số credit score k dưới 600 k xuất hiện nhóm thấp và rất thấp uy tín của các Nhóm tương đối tốt 
-- cụ thể với Nhóm trung bình có số nợ xấu chiểm khoảng 3824 khách hàng cao thứ 2 nghĩa là có điểm tín dụng trung bình có tỷ lệ nợ xấu vẫn tương đối cao chiếm hơn 67% 
-- Nhóm này tuy giữ uy tín ở mức ổn định nhưng nợ xấu rất nhiều có thể do xuất hiện 1 hay nhiều lần có số nợ quá khả năng chi trả 
-- tiếp Nhóm có uy tín tốt Nhóm này có 5666 khách hàng chiếm số nợ xấu cao nhất 68.4 phần trăm ở mức uy tín cao nợ xấu có thể đến từ nhóm các cá nhân chiếm dụng vốn để kinh doanh khi chưa thể xoay vòng vốn để trả nợ kịp thời hoặc còn ở tài sản cố định 
-- với nhóm này cần đánh gía lại nguồn lực và tài sản cố định sở hữu để đánh giá lại năng lực trả nợ 
--- Nhóm có điểm xuất sắc luôn trả nợ đúng hẹn và đúng yêu cầu nhưng vẫn có nợ xấu chiếm 67.95% tương đối cao có thể nhóm này muốn tận dụng điểm tín dụng cao để duyệt khoản vay cao hơn nhưng đang lợi dụng kẽ hở này để chiếm dụng vốn 
--- PHÂN TÍCH CHÉO: CREDIT SCORE TIER VS PREVIOUS DEFAULTS
SELECT 
    CASE 
        WHEN Credit_Score BETWEEN 600 AND 699 THEN '3. Trung bình (600-699)'
        WHEN Credit_Score BETWEEN 700 AND 799 THEN '4. Tốt (700-799)'
        ELSE '5. Xuất sắc (>=800)' 
	END AS credit_score_tier,
        -- Phân loại chi tiết theo số lần vỡ nợ
    CASE 
        WHEN Previous_Defaults = 0 THEN '0 lần vỡ nợ'
        WHEN Previous_Defaults = 1 THEN '1 lần vỡ nợ'
        WHEN Previous_Defaults >= 2 THEN '>=2 lần vỡ nợ'
    END AS prior_default_history,
    COUNT(*) AS total_customer,
    SUM(CASE WHEN Default_Flag = 1 THEN 1 ELSE 0 END) AS bad_loans,
    SUM(CASE WHEN Default_Flag = 0 THEN 1 ELSE 0 END) AS good_loans,
    ROUND(SUM(CASE WHEN Default_Flag = 1 THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*),0), 2) AS bad_rate_percentage,

-- Tỷ trọng nợ xấu của nhóm trong tổng nợ xấu toàn bộ dữ liệu
    ROUND(SUM(CASE WHEN Default_Flag = 1 THEN 1 ELSE 0 END) * 100.0 /
          (SELECT SUM(CASE WHEN Default_Flag = 1 THEN 1 ELSE 0 END) FROM final_scorecard_data), 2) 
          AS bad_share_percentage
FROM final_scorecard_data
GROUP BY credit_score_tier, prior_default_history 
ORDER BY credit_score_tier ASC, prior_default_history DESC;
--- Insight với phần credit score phân tích chéo theo số lần vỡ nợ ở mức 0 1 2 
-- đầu tiên nhận thấy nợ xấu chỉ xuất hiện ở số lần vỡ nợ từ 1 lần trở nên ở cả 3 Nhóm credit score 
-- Phân hóa nhiếu nhất ở 2 nhóm có credit mức tốt và trung bình chiếm lần lượt hơn 35% và hơn 34% tổng nợ xấu 
-- Nhóm này cũng là 2 Nhóm có trên >= 2 lần vỡ nợ 
--- cũng ở mức này nhưng nhóm có 1 lần vỡ nợ ở nhóm credit này chỉ  chiếm hơn 12 và hơn 10 % 
-- Nhóm có credit xuất sắc có >=2 và 1 lần vỡ nợ đứng thấp hơn 5% và gần 2% tỷ lệ nơj xấu 
-- còn  nhóm 0 lần vỡ nợ hầu như k phát sinh nợ xấu  
--- điều này cho thấy thực tế Nhóm vỡ nợ nhiều có xác xuất phát sinh nợ xấu cao hơn tuy nhiên cũng cho thấy tất cả các nhóm đều xuất hiện nhóm 3 Nhóm credit cho thấy chỉ số này k quá ảnh hưởng đến chênh lệch 

 --- Phân tích chéo (Cross_Analysis): Tương quan giữa Uy tín (Credit Score) và đòn bẩy (LTI) 
SELECT 
    CASE 
        WHEN Credit_Score < 600 THEN '1. Very Low (<600)'
        WHEN Credit_Score BETWEEN 600 AND 650 THEN '2. Low-Mid (600-650)'
        WHEN Credit_Score BETWEEN 651 AND 700 THEN '3. Mid Score (651-700)'
        WHEN Credit_Score BETWEEN 751 AND 800 THEN '4. High Score (751-800)'
        WHEN Credit_Score > 800 THEN '5. Excellent (>800)'
        ELSE 'Other'
    END AS credit_profile,
    
    -- Tính LTI trung bình
    ROUND(AVG(Loan_Amount / Cleaned_Income), 4) AS avg_lti,
    ROUND(AVG(income), 2) AS avg_income,
    ROUND(SUM(CASE WHEN Default_Flag = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS bad_rate_percentage
FROM final_scorecard_data
GROUP BY credit_profile
ORDER BY avg_lti DESC;
--- insight cho phần mối quan hệ chéo giữa credit score và LTI (đòn bẩy) 
--- đều duy trì mức LTI < 1 giá trị Khoản nợ đều luôn nhỏ hơn  so với thu nhập 
-- đầu tiên ở mức credit 600 - 650 LTI đứng thứ 2 với 0.4126 với income đứng thứ nhất mức LTI , LTI cao cho thấu xu hướng nợ của nhóm này nhiều nhất 
-- nhưng mức thu thu nhập cũng là cao nhất tuy nhiên vẫn duy trì số nợ xấu hơn 67% 
-- tiếp mức từ 651 đến 700 mức LTI top  1 0.4142 nhưng mức thu nhập lại thâps nhất nợ xấu cũng chiếm hơn 67% như nhóm trên 
-- 2 Nhóm này có LTI cao nhất nhưng 1 nhóm thu nhập cao 1 nhóm thu nhập thấp nhưng tỷ lệ  nợ xấu lại bằng nhau chứng tỏ lý do LTI cao có thể đến từ 2 lý do khác nhau 
-- tiếp từ 751 đến 800 có LTI thấp nhất và income ở mức thứ 2 nhưng lại có tỷ lệ nợ xấu cao nhất với 68.21% 
-- Nhóm này tuy LTI thấp nhất tuy nhiên cungx chính là nhóm có khả năng chiếm dụng vốn cao nhất do thu nhập đứng thứ 2 
--  nhóm trên 800 có LTI đứng thứ 3 mức thu nhập cũng đứng thứ 3 tỷ lệ nợ xấu vẫn cao khoảng 67.94% vẫn tương đối cao nhưng thâps hơn nhóm trên 

--- gán số liệu cho Delinquency_Freq với poor = 3 , fair = 2 good = 1, excellent = 0 
-- Thêm cột mới để lưu Delinquency_Freq
ALTER TABLE final_scorecard_data ADD COLUMN Delinquency_Freq INT;

-- Gán số theo Payment_History ( Trả chậm hoặc trả muộn) 
UPDATE final_scorecard_data
SET Delinquency_Freq = CASE Payment_History
    WHEN 'POOR' THEN 3
    WHEN 'FAIR' THEN 2
    WHEN 'GOOD' THEN 1
    WHEN 'EXCELLENT' THEN 0
END;
--- thu nhập Loan_amunt / số Delinquency_Freq
SELECT 
    Delinquency_Freq,
    -- 1. Số lượng khách hàng trong từng nhóm số
    COUNT(*) AS total_customers,
    -- 2. Tổng giá trị khoản vay được giải ngân
    SUM(Loan_Amount) AS total_loan_value,
    -- 3. Giá trị khoản vay trung bình của mỗi nhóm
    ROUND(AVG(Loan_Amount), 2) AS avg_loan_value,
    -- 4. Tỷ trọng dư nợ của nhóm trên toàn hệ thống (%)
    ROUND(100.0 * SUM(Loan_Amount) / (SELECT SUM(Loan_Amount) FROM final_scorecard_data), 2) AS loan_share_percentage,
    -- 5. Tỷ lệ nợ xấu nội bộ nhóm (%)
    ROUND(100.0 * SUM(CASE WHEN Default_Flag = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS bad_rate_percentage
FROM final_scorecard_data
GROUP BY Delinquency_Freq
ORDER BY Delinquency_Freq ASC;

-- Phân tích (Previous_Defaults, Delinquency, Loan Purpose, Persistence Score)
-- Gom nhóm duy nhất: Rủi ro cao, Trung bình, Tốt, Xuất sắc
--- PHân tích rủi ro chung 
SELECT
  CASE
    -- Rủi ro cao: nhiều lần vỡ nợ hoặc delinquency cao
    WHEN Previous_Defaults >= 2 OR Delinquency_Freq = 3 THEN 'Rủi ro cao'
    -- Trung bình: 1 lần vỡ nợ hoặc delinquency trung bình
    WHEN Previous_Defaults = 1 OR Delinquency_Freq = 2 THEN 'Trung bình'
    -- Tốt: delinquency thấp (1)
    WHEN Delinquency_Freq = 1 THEN 'Tốt'
    -- Xuất sắc: không chậm trả, không vỡ nợ
    ELSE 'Xuất sắc'
  END AS risk_category,

  COUNT(*) AS n,
  SUM(CASE WHEN Default_Flag = 1 THEN 1 ELSE 0 END) AS bad_count,
  ROUND(100.0 * SUM(CASE WHEN Default_Flag = 1 THEN 1 ELSE 0 END) / NULLIF(COUNT(*),0), 2) AS bad_rate_percentage,
  ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM final_scorecard_data), 2) AS population_share_percentage
FROM final_scorecard_data
GROUP BY risk_category
ORDER BY bad_rate_percentage DESC;
-- Insight nhìn chung bảng này cho thấy nhóm có risk_category rủi ro cao chiếm đa số với 7734 khách hàng chiếm 63.15% trên tổng số khách hàng cơ cấu tương đối cao 
--- thể hiện chất lượng và uy  tín khách hàng suy giảm đáng kế tiềm ẩn rủi ro gây thâm hụt cho ngân hàng do chiếm dụng vốn quá nhiều vì nhóm này thường là nhóm có tỷ lệ vỡ nợ và tốc  độ trả nợ kém nhất 
-- tiếp theo tỷ lệ  nợ  xấu ở nhóm rủi ro cao luôn neo ở mức 86.86% Nhóm, cực cao cho thấy ngân hàng thâm hụt một khoản vốn rất lớn điều này có thể dẫn tới mất cân bằng tài chính và quá chình luân chuyển tiền 
-- Nhóm rủi ro trung bình với hệ số vỡ nợ = 1 và mức độ trễ hạn bằng 2  Nhóm này có số khách  hàng ít hơn rất nhiều chỉ  2510 khách hàng chiếm khoảng 20.49 khách hành tuy nhiên tỷ trọng nợ xấu chiếm 62.27% Nhóm cho thấy nhóm này đã kiểm soát tốt cơ cấu hơn giảm so với nhóm trên hơn 20% 
--- Nỗ lực của ngân hàng trong việc kiểm soát Nhóm nguy cơ trung bình tuy nhiên vấn đề này cũng tiềm tàng 1 rủi ro là việc ngân hàng có dấu hiệu bỏ nhóm rủi ro cao mà tập trung các nhóm có nguy cơ thấp trong ngắn hạn điều này có thể kiểm soát  cơ bản nguổn vốn nhưng trong dài hạn điều này có thể làm đòn bẩy tài chính đảo chiều bất lợi cho  ngân hàng 
--- minh chứng ở nhóm rủi ro tốt với mức vỡ nợ = 1 và trễ hạn = 1 với 1011 khách hàng chiếm 8.25% trên  tổng số 
--- và nhóm xuất sắc với mức vỡ nợ  = 0 và trễ hạn = 0 với 993 khách hàng chiếm 8.11% trên tổng số 
-- 2 Nhóm này đều k xuất hiện nợ xấu chứng minh  cho lập luận trên của tôi khi ngân hàng có khả năng đang bỏ quên nhóm cơ cấu cao nhất và rủi ro lớn nhất 
-- 2 Nhóm này đều k xuất hiện nợ xấu nhưng cơ cấu rất thấp chỉ khoảng hơn 16% thay vì dùng cách đó ta có thể chuyển đổi Nhóm rủi ro cao sang nhóm này bằng cách 
--- để hạn chế vỡ nợ giới hạn khoản nợ có thể vay và phân tích cơ cấu , nguổn thu nhập và giới hạn vay của khách hàng 
-- để hạn chế chả muộn có thể linh hoạt cho các khoản vay lớn để chia đợt trả nợ , khuyến khích trả nợ sớm với ưu đãi vay hấp dẫn hơn 
   
-- Phân tích riêng: Prior Defaults vs Risk Category ( rủi ro và trạng thái vỡ nợ)
SELECT
  CASE
    WHEN Previous_Defaults >= 2 OR Delinquency_Freq = 3 THEN 'Rủi ro cao'
    WHEN Previous_Defaults = 1 OR Delinquency_Freq = 2 THEN 'Trung bình'
    WHEN Delinquency_Freq = 1 THEN 'Tốt'
    ELSE 'Xuất sắc'
  END AS risk_category,
  CASE
    WHEN Previous_Defaults = 0 THEN '0 lần'
    WHEN Previous_Defaults = 1 THEN '1 lần'
    WHEN Previous_Defaults = 2 THEN '2 lần'
    WHEN Previous_Defaults = 3 THEN '3 lần'
    ELSE '>=4 lần'
  END AS prior_default_status,
  COUNT(*) AS n,
  SUM(CASE WHEN Default_Flag = 1 THEN 1 ELSE 0 END) AS bad_count,
  ROUND(100.0 * SUM(CASE WHEN Default_Flag = 1 THEN 1 ELSE 0 END) / NULLIF(COUNT(*),0), 2) AS bad_rate_percentage,
  ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM final_scorecard_data), 2) AS population_share_percentage
FROM final_scorecard_data
GROUP BY risk_category, prior_default_status
ORDER BY risk_category, bad_rate_percentage DESC;
-- insight nhìn chung với bảng này Nhóm rủi ro cao xuất hiện ở tất cả các trạng thái vỡ nợ điều này ban đầu có thể nhận  định trong số quyết định rủi ro cao nằm ở tốc độ thanh toans 
---  đầu tiên nhóm rủi ro cao về  cơ cấu khách hàng theo thứ tự từ cao xuống thấp là nhóm 2 lần (chiếm 17.21%  tổng số ) > nhóm >= 4 lần ( chiếm 17.08% tổng số )   > 3 lần ( chiếm 16.46% tổng số ) > nhóm 0 lần ( chiếm 8.3% tổng số  ) > nhóm 1 lần (chiếm 4.1 % tổng  số ) 
-- tỷ lệ nợ xấu  3 nhóm 2 , 3 và trên 4 lần đều duy trừ ở mức cực cao -- đây chính là ngưỡng hoàn toàn mất kiểm soát 
-- Nhóm 0 xuất hiện nợ xấu , nhóm 1 cơ cấu chiếm thấp nhưng cũng neo ở mức 100% 
--- đây  cho thấy mức nợ xấu doanh nghiệp luôn ở trạng thái phân hóa rõ 1 nhóm toàn nợ xấu 2  là nhóm k xuất hiện nhóm 0 và nhóm 1,2,3,4
--- điều này ảnh hưởng đáng kể đến việc đánh giá mức độ uy tín của khách hàng và quyết định tài chính có thể k đc chính xác 
--- Hơn nữa việc Nhóm chưa bao giờ vỡ nỡ nhưng lại nằm ở nhóm rủi ro cao cho thấy mức độ chậm trả luôn nằm ở mức 3 tuy k xuất hiện nợ xấu nhưng đây vẫn là nhóm rất đáng lưu tâm với 1016 khách hàng k hề nhỏ 
-- Phân tích riêng: Loan Purpose vs Risk Category
SELECT
  CASE
    WHEN Previous_Defaults >= 2 OR Delinquency_Freq = 3 THEN 'Rủi ro cao'
    WHEN Previous_Defaults = 1 OR Delinquency_Freq = 2 THEN 'Trung bình'
    WHEN Delinquency_Freq = 1 THEN 'Tốt'
    ELSE 'Xuất sắc'
  END AS risk_category,
  CASE
    WHEN Loan_Purpose IN ('BUSINESS','AUTO','HOME','PERSONAL') THEN Loan_Purpose
    ELSE 'OTHER'
  END AS loan_purpose_group,
  COUNT(*) AS n,
  SUM(CASE WHEN Default_Flag = 1 THEN 1 ELSE 0 END) AS bad_count,
  ROUND(100.0 * SUM(CASE WHEN Default_Flag = 1 THEN 1 ELSE 0 END) / NULLIF(COUNT(*),0), 2) AS bad_rate_percentage,
  ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM final_scorecard_data), 2) AS population_share_percentage
FROM final_scorecard_data
GROUP BY risk_category, loan_purpose_group
ORDER BY risk_category, bad_rate_percentage DESC;
-- insigh : nhìn chung tất cả các nhóm rủi ro đều tồn tại cả 4 nhóm nguyên nhân HOME (bất động sản ) , AUTO(mua ô tô tài sản cố định), BUSINESS(kinh doanh),PERSONAL(Mục đích cá nhân ) 
-- tuy k quá cụ thể nhưng 4 nhóm này đều cho thấy xu hướng mục đích ở 4 phương diện khác nhau là tài sản , tài sản cố định, tiêu dùng , và xoay vòng vốn 
--- phân tích từng nhóm rủi ro 
--- Nhóm rủi ro cao đều nằm trong top 4 có số lượng khách hàng đông nhất đều trên 1900 khách hàng chênh lệch giữa các mục đích chỉ giao động  ở mức vài chục người 
-- dẫn đầu là nhóm tài sản cố định và bất động sản đầu tư tổng cộng chiếm hơn 31% / tổng số khách hàng luôn duy  trì tỷ lệ nợ xấu cao với nhóm HOME là 87.6% và nhóm AUTO là 86.66% tương đương trên 1680 đến hơn 1700 khách hàng nợ xấu 
-- tôi cho rằng đây là nhóm nguy hiểm nhất vì là nợ xấu thứ nhất bất động sản đầu tư và tài sản cố định như AUTO là những tài sản có thể sinh lời và cho thuê cũng như có hao mòn việc chủ nhân có thể xử lý linh  hoạt có thể chiếm dụng 1 khoản vốn k hề nhỏ 
-- hơn nữa đây đều là 2 mục đích có giá  trị cao k hề nhỏ nếu chiếm dụng vốn lớn có thể đứt chuỗi vốn vì nhóm này đều 1 là vỡ nợ nhiều lần 2 là chậm trả nhiều lần 
--- NHóm kinh doanh và tiêu dùng cá nhân đứng ngay sau k chênh lệch quá nhiều nhưng nợ xấu cũng k hề thấp trong đó nhóm kinh doanh đạt 87.49%/Nhóm và tiêu dùng cá nhân đạt 85.71%/nhóm 
--- Nhóm kinh doanh đáng chú ý có khả năng xử dụng đòn bẩy tài chính để kinh doanh tuy nhiên để đánh giá đòn bẩy có hiệu quả hay k cần dựa vào thu nhập ( lợi nhuận cá nhân )
-- còn Nhóm tiêu dùng cá nhân có thể đánh giá thời điểm vay hoặc số người vay cùng 1 thời  điểm để có cái nhìn cụ thể tuy nhiên số khách hàng 2 nhóm này cộng lại cũng chiếm hơn 31% tổng số khách hàng là vùng nguy hiểm 
--- tiếp đến nhóm rủi ro trung bình cả 4 mục đích cũng nằm trong top 8 có số lượng khách đông nhất
--- đặc điểm chủ yếu tương tự nhóm trên k chênh lệch quá nhiều chỉ có nhóm AUTO thấp nhất chênh ít hơn các nhóm trên gần 100 người tỷ lệ nợ xấu giao động quanh mức 59%/Nhóm - 65%/Nhóm cơ cấu giảm đi rõ rệt so với nhóm trên hơn 20% 
--- thứ tự ưu tiên cũng có sự khác biệt bất động sản (HOME) vẫn chiếm ưu thế tuy nhiên cơ cấu nợ xấu là thấp nhất 4 nhóm mục đích chỉ khoảng 59.29% 
--- ghi nhận nhóm kinh doanh và cá nhân cao nhất 4 nhóm mục đích của nhóm rủi ro này với lần lượt 64.64%/ nhóm và 63.85%/nhóm chiếm dụng vốn vẫn rất lớn với kinh doanh điều này k phải quá tệ nhưng cần đánh giá năng lực trả nợ và hiệu quả của đòn bẩy tài chính 
--- điều đặc biệt nhất ở nhóm này chính là nhóm AUTO xuống thấp nhất có thể tài sản cố định như xe k còn là ưu tiên hoặc do chi phí bảo trì hoặc đặc thù nghề nghiệp k phù hợp tuy nhiên với mức nợ xấu 61.23%/nhóm vẫn cần cải thiện 
--- tiếp theo đến nhóm k xuất hiện nợ xấu 4 nhóm rủi ro ở mức (tốt và xuất sắc) phân bố k đều như 2 nhóm trên  
-- top  10 xuất hiện của rủi ro tốt ở 2 nhóm cá nhân và AUTO mỗi nhóm có khoảng 250-270 khách hàng 
-- top 12 xuất hiện lại của 2  xuất sắc với lần lượt 256 và 251 khách hàng với 2 nhóm cá nhân và AUTO 
-- việc xuất hiện nợ tốt ở các nhóm trên là do thứ nhất AUTO là mặt hàng có thể linh hoạt thu hồi vốn và vì có hao mòn nên giá trị khai thác có thể hơn giá trị tài sản 
-- tiêp vơí mục đích cá nhân có thể đến từ các khoản giá trị thấp có đủ khả năng chi trả 
-- top 14 xuất hiện nhóm tốt là kinh doanh và nhóm xuất sắc là HOME với lần lượt 246 và 245 khách hàng đây có thể là các hộ kinh doanh nhỏ hoặc chủ yếu là thanh lý tài sản cố định ngay chứ k phải cho thuê và thu hồi vốn 
-- top 16 xuẩt hiện nhóm tốt HOME và xuất sắc kinh doanh với lần lượt 242 và 241 khách hàng với lý do tương tự nhóm trên 
 
SELECT * FROM final_scorecard_data;
    
 




    
    


