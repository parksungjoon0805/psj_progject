import csv
import streamlit as st
from datetime import datetime

# CSV 파일 경로 설정
BOOKS_FILE = 'reduced_data.csv'
LOANS_FILE = 'output.csv'

# CSV 파일 헤더
BOOKS_HEADER = ['도서관명', '자료실', '등록번호', '서명', '저자', '출판사', '대출상태']
LOANS_HEADER = ['User ID', 'Book ID', '대출일', '반납일']

# 세션 상태 변수 초기화
if 'loaded_books' not in st.session_state:
    st.session_state.loaded_books = []

if 'loaded_loans' not in st.session_state:
    st.session_state.loaded_loans = []

# 도서 정보 불러오기
def load_books():
    # 세션 상태에 loaded_books가 없거나 비어있는 경우 실행
    if not st.session_state.loaded_books:
        # CSV 파일을 읽어와서 세션 상태에 저장하는 부분
        with open(BOOKS_FILE, 'r', newline='', encoding='utf-8-sig') as csvfile: # newline='' 은 줄바꿈을 하지 않음
            reader = csv.DictReader(csvfile)  # CSV 파일을 딕셔너리 형태로 읽기 위한 reader 객체 생성
            # 각 도서에 대출상태를 추가하여 리스트로 변환하여 loaded_books에 저장
            books = [{**book, '대출상태': '대출가능'} for book in reader]
            st.session_state.loaded_books = books  # 세션 상태의 loaded_books에 로드한 도서 정보 저장
    # 함수가 호출될 때마다 세션 상태의 loaded_books 반환
    return st.session_state.loaded_books

# 대출 정보 불러오기
def load_loans():
    # 세션 상태에 loaded_loans가 없거나 비어있는 경우 실행
    if not st.session_state.loaded_loans:
        # CSV 파일을 읽어와서 세션 상태에 저장하는 부분
        with open(LOANS_FILE, 'r', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)  # CSV 파일을 딕셔너리 형태로 읽기 위한 reader 객체 생성
            st.session_state.loaded_loans = list(reader)  # CSV 파일의 내용을 리스트로 변환하여 세션 상태에 저장
    # 함수가 호출될 때마다 세션 상태의 loaded_loans 반환
    return st.session_state.loaded_loans

# 도서 정보 저장하기
def save_books(books):
    # CSV 파일을 쓰기 모드로 열고 utf-8-sig 인코딩을 사용하여 파일에 데이터를 저장합니다.
    with open(BOOKS_FILE, 'w', newline='', encoding='utf-8-sig') as csvfile:
        # CSV 파일에 딕셔너리를 기록하기 위한 DictWriter 객체를 생성합니다.
        writer = csv.DictWriter(csvfile, fieldnames=BOOKS_HEADER)
        # CSV 파일의 헤더를 쓰기 위해 writeheader() 메서드를 호출합니다. 
        writer.writeheader()
        # books 리스트에 있는 모든 딕셔너리를 CSV 파일에 기록합니다.
        writer.writerows(books)

# 대출 정보 저장하기
def save_loans(loans):
    # CSV 파일을 쓰기 모드로 열고 utf-8-sig 인코딩을 사용하여 파일에 데이터를 저장합니다.
    with open(LOANS_FILE, 'w', newline='', encoding='utf-8-sig') as csvfile:
        # CSV 파일에 딕셔너리를 기록하기 위한 DictWriter 객체를 생성합니다.
        writer = csv.DictWriter(csvfile, fieldnames=LOANS_HEADER)
        # CSV 파일의 헤더를 쓰기 위해 writeheader() 메서드를 호출합니다.
        writer.writeheader()
        # loans 리스트에 있는 모든 딕셔너리를 CSV 파일에 기록합니다.
        writer.writerows(loans)

# 도서 추가하기
def add_book(library, room, reg_no, title, author, publisher):
    # 이미 로드된 도서 정보를 가져옴
    books = load_books()
    
    # 새로운 도서 정보를 딕셔너리 형태로 생성하여 리스트에 추가
    new_book = {'도서관명': library, '자료실': room, '등록번호': reg_no, '서명': title, '저자': author,
                '출판사': publisher, '대출상태': '대출가능'}
    # books 딕셔너리에 new_book 딕셔너리 추가
    books.append(new_book) 
    
    # 업데이트된 도서 정보를 CSV 파일에 저장
    save_books(books)
    
    # 세션 상태에 업데이트된 도서 정보를 저장
    st.session_state.loaded_books = books
    
    # 사용자에게 성공 메시지를 출력
    st.success(f'도서 "{title}"이(가) 추가되었습니다.')

    
# 도서 대출하기
def borrow_book(user_id, book_id):
    # 이미 로드된 도서 정보를 가져옵니다.
    books = load_books()
    
    # 이미 로드된 대출 정보를 가져옵니다.
    loans = load_loans()
    
    # 사용자가 대출하려는 도서가 대출 가능한지 확인합니다.
    for book in books:
        if book['등록번호'] == book_id and book['대출상태'] == '대출가능':
            # 도서의 대출 상태를 '대출중'으로 변경합니다.
            book['대출상태'] = '대출중'
            
            # 변경된 도서 정보를 CSV 파일에 저장합니다.
            save_books(books)
            
            # 대출 목록에 새로운 대출 정보를 추가합니다.
            loans.append({'User ID': user_id, 'Book ID': book_id,
                          '대출일': datetime.now().strftime('%Y-%m-%d'), '반납일': ''})
            
            # 변경된 대출 정보를 CSV 파일에 저장합니다.
            save_loans(loans)
            
            # 사용자에게 성공 메시지를 출력합니다.
            st.success(f'사용자 {user_id}가 도서 {book_id}을(를) 대출했습니다.')
            
            # 함수를 종료하고 반환합니다.
            return
    
    # 모든 도서와 대출 정보를 확인했지만 해당 도서의 대출 정보를 찾을 수 없는 경우 사용자에게 경고 메시지를 출력합니다.
    st.warning('해당 도서는 이미 대출 중이거나 존재하지 않습니다.')


# 도서 반납하기
def return_book(user_id, book_id):
    # 이미 로드된 도서 정보를 가져옵니다.
    books = load_books()
    
    # 이미 로드된 대출 정보를 가져옵니다.
    loans = load_loans()
    
    # 현재 날짜를 가져옵니다.
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # 모든 도서를 순회하면서 대출중인 도서인지 확인합니다.
    for book in books:
        # 도서의 등록번호와 대출 상태를 확인합니다.
        if book['등록번호'] == book_id and book['대출상태'] == '대출중':
            # 도서의 대출 상태를 '대출가능'으로 변경합니다.
            book['대출상태'] = '대출가능'
            
            # 변경된 도서 정보를 CSV 파일에 저장합니다.
            save_books(books)
            
            # 대출 목록을 순회하면서 해당 도서의 대출 정보를 찾습니다.
            for loan in loans:
                # 도서 ID와 사용자 ID를 확인하여 해당 대출 정보를 찾습니다.
                if loan['Book ID'] == book_id and loan['User ID'] == user_id:
                    # 대출 반납일을 현재 날짜로 기록합니다.
                    loan['반납일'] = current_date
                    
                    # 변경된 대출 정보를 CSV 파일에 저장합니다.
                    save_loans(loans)
                    
                    # 사용자에게 성공 메시지를 출력합니다.
                    st.success(f'도서 {book_id}이(가) 반납되었습니다.')
                    
                    # 함수를 종료하고 반환합니다.
                    return
    
    # 모든 도서와 대출 정보를 확인했지만 해당 도서의 대출 정보를 찾을 수 없는 경우 사용자에게 경고 메시지를 출력합니다.
    st.warning('해당 도서는 대출 중이 아니거나 존재하지 않습니다.')


def main():
    st.sidebar.title('도서 대출 관리 시스템')
    menu_choice = st.sidebar.radio('메뉴를 선택하세요:', ['도서 정보', '도서 추가', '도서 대출', '도서 반납'])

    if menu_choice == '도서 정보':
        st.title('도서 정보')

        # 도서 검색 기능 구현
        search_query = st.text_input('도서 검색', placeholder='도서관 명, 책 이름, 자료실, 등록번호, 서명, 저자, 출판사')

        books = load_books()

        # 검색된 도서만 필터링
        filtered_books = []
        for book in books:
            if search_query.lower() in book['서명'].lower() or \
                search_query.lower() in book['자료실'].lower() or \
                search_query.lower() in book['도서관명'].lower() or \
                search_query.lower() in book['등록번호'].lower() or \
                search_query.lower() in book['저자'].lower() or \
                search_query.lower() in book['출판사'].lower():
                filtered_books.append(book)

        if not filtered_books:
            st.warning('찾으시는 정보가 없습니다.')
        else:
            # Pagination 설정
            items_per_page = 30
            total_items = len(filtered_books)
            total_pages = (total_items - 1) // items_per_page + 1

            # 페이지 번호 표시
            page_number = st.sidebar.selectbox('페이지 번호', range(1, total_pages + 1), index=0)

            start_idx = (page_number - 1) * items_per_page
            end_idx = min(start_idx + items_per_page, total_items)

            paged_books = filtered_books[start_idx:end_idx]

            st.write(paged_books)

            # 페이지 번호와 페이지 변경용 select box를 페이지의 하단에 배치
            col1, col2 = st.columns([3, 1])
            col1.text(f"페이지 번호: {page_number}/{total_pages}")
            with col2:
                st.write("")  

    elif menu_choice == '도서 추가':
        st.title('도서 추가')
        library = st.text_input('도서관명')
        room = st.text_input('자료실')
        reg_no = st.text_input('등록번호')
        title = st.text_input('서명')
        author = st.text_input('저자')
        publisher = st.text_input('출판사')

        if st.button('추가하기'):
            add_book(library, room, reg_no, title, author, publisher)

    elif menu_choice == '도서 대출':
        st.title('도서 대출')
        user_id = st.text_input('사용자 ID')
        book_id = st.text_input('도서 ID')

        if st.button('대출하기'):
            borrow_book(user_id, book_id)

    elif menu_choice == '도서 반납':
        st.title('도서 반납')
        user_id = st.text_input('사용자 ID')
        book_id = st.text_input('도서 ID')

        if st.button('반납하기'):
            return_book(user_id, book_id)

if __name__ == "__main__":
    main()
