import streamlit as st
from customer_interface import show_customer_interface
from manager_interface import show_manager_interface
from database import initialize_database

def main():
    initialize_database()
    st.title("강원대학교사범대학부설고등학교 학술제 예약 시스템")
    
    page = st.sidebar.selectbox("페이지 선택", ["메인 페이지", "고객용 인터페이스", "부스 관리자용 인터페이스"])
    
    if page == "메인 페이지":
        show_main_page()
    elif page == "고객용 인터페이스":
        show_customer_interface()
    elif page == "부스 관리자용 인터페이스":
        show_manager_interface()

def show_main_page():
    st.header("환영합니다!")
    st.write("왼쪽 사이드바에서 원하는 인터페이스를 선택해주세요.")
    st.write("- 고객용 인터페이스: 예약을 원하시는 분은 이 옵션을 선택해주세요.")
    st.write("- 부스 관리자용 인터페이스: 부스 관리자분들은 이 옵션을 선택해주세요.")

if __name__ == "__main__":
    main()
