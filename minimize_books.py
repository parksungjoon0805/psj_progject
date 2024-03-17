## 받아온 csv 파일이 너무 커서 절반으로 자름

import pandas as pd

# 원본 CSV 파일 경로
input_file = 'books.csv'

# CSV 파일을 읽어 DataFrame으로 로드
df = pd.read_csv(input_file)

# DataFrame의 크기 확인
num_rows, num_cols = df.shape

# 데이터의 절반만 남기기 (반올림하여 홀수 행도 처리)
half_rows = num_rows // 2
df = df.iloc[:half_rows, :]

# 결과를 새로운 CSV 파일로 저장
output_file = 'reduced_data.csv'
df.to_csv(output_file, index=False)

print(f'Reduced data saved to {output_file}')