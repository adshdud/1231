import streamlit as st
from database import get_database_connection
from config import booth_lst
import sms

def show_customer_interface():
    st.header("고객용 인터페이스")
    booth_number = st.selectbox("예약하실 부스를 선택해주세요", range(len(booth_lst)), format_func=lambda x: booth_lst[x])
    show_reservation_form(booth_number)

def show_reservation_form(booth_number):
    st.title(booth_lst[booth_number])
    st.header("예약하기")
    st.divider()

    name = st.text_input("이름")
    phone = st.text_input("전화번호")

    submit = st.button("예약 제출")
    st.divider()

    if submit:
        process_reservation(name, phone, booth_number)

def process_reservation(name, phone, booth_number):
    conn = get_database_connection()
    cursor = conn.cursor()
    booth_n = booth_lst[booth_number]

    cursor.execute(
        "SELECT COUNT(*) FROM reservations WHERE booth = ? AND phone = ?",
        (booth_n, phone),
    )
    existing_reservation_count = cursor.fetchone()[0]

    if existing_reservation_count > 0:
        st.warning("이미 해당 부스에 예약이 존재합니다. 중복 예약은 허용되지 않습니다.")
    else:
        cursor.execute(
            "SELECT last_order_number FROM order_sequence WHERE booth =?", (booth_n,)
        )
        last_order_number = cursor.fetchone()[0]

        order_number = f"{booth_lst[booth_number]} {str(last_order_number + 1).zfill(2)}번"

        cursor.execute(
            "INSERT INTO reservations (name, phone, booth, order_number) VALUES (?, ?, ?, ?)",
            (name, phone, booth_lst[booth_number], order_number),
        )

        last_order_number += 1
        cursor.execute(
            "UPDATE order_sequence SET last_order_number = ? WHERE booth =?",
            (last_order_number, booth_lst[booth_number]),
        )

        conn.commit()
        conn.close()

        st.success(f"예약 완료! 순서는 {order_number} 입니다.")
        send_confirmation_sms(phone, booth_lst[booth_number], last_order_number)

    st.divider()
    st.text('프로그램 관련 문의사항 01022619433')

def send_confirmation_sms(phone, booth, order_number):
    receiver_lst = [phone]
    message = f"{booth} 예약번호는 {order_number}입니다."
    sms.send_sms(receivers=receiver_lst, message=message)
    