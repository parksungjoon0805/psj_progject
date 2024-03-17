## 대출 가능 필드를 추가
## 각 도서의 대출 여부를 추적하여 중복 대출을 방지하고, 반납 시 다시 대출할 수 있도록 하기위해

import csv

# CSV 파일 경로 설정
csv_file = 'books.csv'

# 추가할 값 설정
new_value = '대출가능'

# 열려 있는 CSV 파일에 값 추가하기
with open(csv_file, 'r', newline='', encoding='utf-8-sig') as infile:
    reader = csv.reader(infile)
    rows = list(reader)

    # 동일한 값을 추가할 열 선택
    col_index = 8  # 예를 들어 I열에 해당하는 열

    for row in rows:
        row[col_index] = new_value

# 결과를 동일한 파일에 저장
with open(csv_file, 'w', newline='', encoding='utf-8-sig') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(rows)

print(f'CSV 파일에 값 "{new_value}"가 추가되었습니다.')