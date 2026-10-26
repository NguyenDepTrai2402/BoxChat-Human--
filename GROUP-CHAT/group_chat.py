import streamlit as st
from google import genai
from google.genai import types

# --- CẤU HÌNH API KEY MIỄN PHÍ TỪ GOOGLE AI STUDIO ---
API_KEY = "AQ.Ab8RN6JPBO7BZq7rUVqivM4M3p7uoZtrRkxrem26F3Ug_KbnVQ"
client = genai.Client(api_key=API_KEY)

st.set_page_config(page_title="Group Chat 3 Anh Em", page_icon="💬")
st.title("💬 Phòng Họp: Nguyễn & 2 Đệ AI")

# Khởi tạo lịch sử chat chung của cả group
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "Coder", "avatar": "🧑‍💻", "content": "Chào sếp Nguyễn, nay có kèo code gì quăng vô đây em xử cho!"},
        {"role": "Reviewer", "avatar": "🕵️", "content": "Để tao chống mắt lên coi m code có ra hồn kh nha thằng kia =)))"}
    ]

# Hiển thị toàn bộ tin nhắn trong box chat
if "cdmessages" not in st.session_state:
    st.session_state.cdmessages = []
for msg in st.session_state.cdmessages:
    with st.chat_message(msg["role"], avatar=msg["avatar"]):
        st.markdown(f"**{msg['role']}**: {msg['content']}")

# Hàm gom lịch sử chat để AI hiểu ngữ cảnh 3 người đang nói gì
def get_chat_context():
    context = "Đây là cuộc trò chuyện trong 1 group chat gồm 3 người: Sếp Nguyễn (User), Coder và Reviewer.\nLịch sử chat:\n"
    for m in st.session_state.messages[-10:]: # Lấy 10 tin gần nhất
        context += f"{m['role']}: {m['content']}\n\n"
    return context

# Khung nhập tin nhắn của mày
if user_input := st.chat_input("Nhắn gì đó vào group..."):
    # 1. Hiện tin nhắn của mày
    st.session_state.messages.append({"role": "Sếp Nguyễn", "avatar": "👑", "content": user_input})
    with st.chat_message("Sếp Nguyễn", avatar="👑"):
        st.markdown(f"**Sếp Nguyễn**: {user_input}")

    # 2. Tới lượt thằng Coder (AI 1) trả lời
    with st.chat_message("Coder", avatar="🧑‍💻"):
        with st.spinner("Thằng Coder đang gõ phím..."):
            prompt_coder = get_chat_context() + "\nHãy đóng vai Coder (nói chuyện kiểu bạn bè miền Nam tự nhiên, xưng tao-mày với Reviewer và gọi Nguyễn là đại ca/ní). Trả lời tin nhắn mới nhất và viết code nếu được yêu cầu."
            res_coder = client.models.generate_content(
                model="gemini-flash-latest",
                contents=prompt_coder
            )
            coder_reply = res_coder.text
            st.markdown(f"**Coder**: {coder_reply}")
            st.session_state.messages.append({"role": "Coder", "avatar": "🧑‍💻", "content": coder_reply})

    # 3. Tới lượt thằng Reviewer (AI 2) nhảy vào tiếp chuyện/bắt lỗi
    with st.chat_message("Reviewer", avatar="🕵️"):
        with st.spinner("Thằng Reviewer đang soi lỗi..."):
            prompt_reviewer = get_chat_context() + "\nHãy đóng vai Reviewer (tính tình khó ở, hay cà khịa thằng Coder, nói chuyện ngắn gọn, soi kỹ đoạn trả lời/code của thằng Coder vừa nhắn ở trên xem có lỗi hay tối ưu được gì không rồi báo cáo cho Nguyễn)."
            res_reviewer = client.models.generate_content(
                model="gemini-flash-latest",
                contents=prompt_reviewer
            )
            reviewer_reply = res_reviewer.text
            st.markdown(f"**Reviewer**: {reviewer_reply}")
            st.session_state.messages.append({"role": "Reviewer", "avatar": "🕵️", "content": reviewer_reply})