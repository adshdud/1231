import streamlit as st
from database import get_database_connection
from config import booth_lst, admin_password
import sms
from datetime import datetime

def show_manager_interface():
    st.header("부스 관리자용 인터페이스")
    page = st.sidebar.selectbox("페이지 선택", ["부스 관리", "부스 생성"])

    if page == "부스 관리":
        booth_number = st.selectbox("관리하실 부스를 선택해주세요", range(len(booth_lst)), format_func=lambda x: booth_lst[x])
        show_reservations(booth_number)
    elif page == "부스 생성":
        show_add_booth_form()

def show_reservations(booth_number):
    send_time = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
    st.title("부스 관리 시스템")
    st.header("예약 목록")

    conn = get_database_connection()
    cursor = conn.cursor()

    booth_n = booth_lst[booth_number]
    cursor.execute(
        "SELECT id, name, phone, booth, order_number FROM reservations WHERE booth=?",
        (booth_n,),
    )
    reservations = cursor.fetchall()

    for reservation in reservations:
        display_reservation(reservation, send_time)

    conn.close()

def display_reservation(reservation, send_time):
    if f"approved_{reservation[0]}" not in st.session_state:
        st.session_state[f"approved_{reservation[0]}"] = False

    if st.session_state[f"approved_{reservation[0]}"]:
        st.markdown(
            f'<span style="text-decoration: line-through;">'
            f"ID: {reservation[0]}, 이름: {reservation[1]}, 전화번호: {reservation[2]}, 음식: {reservation[3]}, 순서: {reservation[4]},문자 발송 시간 : {send_time} "
            f"</span>",
            unsafe_allow_html=True,
        )
    else:
        st.text(
            f"순서: {reservation[4]},  이름: {reservation[1]}, 전화번호: {reservation[2]}, 음식: {reservation[3]}, ID: {reservation[0]}"
        )
    
    agree_b = st.checkbox(f"{reservation[4]} 예약 :blue[승인]")            
    if agree_b:
        approve_reservation(reservation)
    
    diagree_b = st.checkbox(f"{reservation[4]} 예약 :red[취소]")
    if diagree_b:
        cancel_reservation(reservation)
        
    st.divider()

def approve_reservation(reservation):
    send_time = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
    receiver_lst = [reservation[2]]
    message = f"{reservation[1]}님 5분 안에 {reservation[4]} 방문해주세요"
    sms.send_sms(receivers=receiver_lst, message=message)
    st.session_state[f"approved_{reservation[0]}"] = True
    st.success(f"{reservation[1]}님의 예약(ID: {reservation[0]})이 승인되었습니다.")

def cancel_reservation(reservation):
    send_time = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
    receiver_lst = [reservation[2]]
    message = f"{reservation[1]}님 {reservation[3]}이 마감되었습니다. 죄송합니다. "
    sms.send_sms(receivers=receiver_lst, message=message)
    st.session_state[f"approved_{reservation[0]}"] = True
    st.success(f"{reservation[1]}님의 예약(ID: {reservation[0]}) 이(가) 취소되었습니다.")

def show_add_booth_form():
    st.header("부스 추가")
    password = st.text_input("비밀번호를 입력하세요", type="password")
    
    if st.button("비밀번호 확인"):
        if password == admin_password:
            st.session_state['add_booth'] = True
            st.experimental_rerun()
        else:
            st.error("비밀번호가 틀렸습니다.")
    
    if st.session_state.get('add_booth'):
        add_booth_form()

def add_booth_form():
    st.header("부스 생성")
    booth_location = st.text_input("부스 위치")
    booth_name = st.text_input("부스 이름")
    
    if st.button("부스 추가하기"):
        add_booth_to_database(booth_location, booth_name)
        st.success("부스가 성공적으로 추가되었습니다.")
        
        # 부스 리스트에 추가
        booth_lst.append(f"{booth_location} : {booth_name}")
        st.session_state['add_booth'] = False
        st.experimental_rerun()

def add_booth_to_database(location, name):
    conn = get_database_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO order_sequence (booth, last_order_number) VALUES (?, 0)",
        (f"{location} : {name}",)
    )

    conn.commit()
    conn.close()
