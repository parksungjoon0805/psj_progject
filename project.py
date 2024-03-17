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
    if not st.session_state.loaded_books:
        with open(BOOKS_FILE, 'r', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            # 각 도서에 대출상태 초기화
            books = [{**book, '대출상태': '대출가능'} for book in reader]
            st.session_state.loaded_books = books
    return st.session_state.loaded_books

# 대출 정보 불러오기
def load_loans():
    if not st.session_state.loaded_loans:
        with open(LOANS_FILE, 'r', newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            st.session_state.loaded_loans = list(reader)
    return st.session_state.loaded_loans

# 도서 정보 저장하기
def save_books(books):
    with open(BOOKS_FILE, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=BOOKS_HEADER)
        writer.writeheader()
        writer.writerows(books)

# 대출 정보 저장하기
def save_loans(loans):
    with open(LOANS_FILE, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=LOANS_HEADER)
        writer.writeheader()
        writer.writerows(loans)

# 도서 추가하기
def add_book(library, room, reg_no, title, author, publisher):
    books = load_books()
    books.append({'도서관명': library, '자료실': room, '등록번호': reg_no, '서명': title, '저자': author,
                  '출판사': publisher, '대출상태': '대출가능'})
    save_books(books)
    st.session_state.loaded_books = books
    st.success(f'도서 "{title}"이(가) 추가되었습니다.')

# 도서 대출하기
def borrow_book(user_id, book_id):
    books = load_books()
    loans = load_loans()
    for book in books:
        if book['등록번호'] == book_id and book['대출상태'] == '대출가능':
            book['대출상태'] = '대출중'
            save_books(books)
            loans.append({'User ID': user_id, 'Book ID': book_id,
                          '대출일': datetime.now().strftime('%Y-%m-%d'), '반납일': ''})
            save_loans(loans)
            st.success(f'사용자 {user_id}가 도서 {book_id}을(를) 대출했습니다.')
            return
    st.warning('해당 도서는 이미 대출 중이거나 존재하지 않습니다.')

# 도서 반납하기
def return_book(user_id, book_id):
    books = load_books()
    loans = load_loans()
    current_date = datetime.now().strftime('%Y-%m-%d')  # 현재 날짜

    for book in books:
        if book['등록번호'] == book_id and book['대출상태'] == '대출중':
            book['대출상태'] = '대출가능'
            save_books(books)
            for loan in loans:
                if loan['Book ID'] == book_id and loan['User ID'] == user_id:
                    loan['반납일'] = current_date  # 반납일 기록
                    save_loans(loans)
                    st.success(f'도서 {book_id}이(가) 반납되었습니다.')
                    return
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
                search_query.lower() in book['도서관 명'].lower() or \
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
                st.write("")  # 비어 있는 공간을 만들어 select box를 우측 하단에 위치시킴

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
