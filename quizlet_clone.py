import random
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Quizlet IELTS", page_icon="📚", layout="centered"
)

st.title("📚 Ứng Dụng Ôn Thi Từ Vựng IELTS")


# Đọc file CSV chứa từ vựng
@st.cache_data
def load_data():
  try:
    df = pd.read_csv(
        "vocabulary.csv", header=None, names=["Word", "Definition"]
    )
    return df
  except Exception:
    return None


df = load_data()

if df is None or df.empty:
  st.error(
      "Không tìm thấy file `vocabulary.csv` hoặc file đang bị trống! T hãy kiểm"
      " tra lại file CSV trên GitHub nhé."
  )
else:
  # Khởi tạo trạng thái ngẫu nhiên từ vựng
  if "current_idx" not in st.session_state:
    st.session_state.current_idx = random.randint(0, len(df) - 1)
    st.session_state.show_def = False

  current_row = df.iloc[st.session_state.current_idx]
  word = current_row["Word"]
  definition = current_row["Definition"]

  st.markdown("### Từ vựng:")
  st.markdown(
      f"<h2 style='color: #29b6f6;'>{word}</h2>", unsafe_allow_html=True
  )

  if st.session_state.show_def:
    st.success(f"**Nghĩa:** {definition}")

  col1, col2 = st.columns(2)
  with col1:
    if not st.session_state.show_def:
      if st.button("🔍 Xem nghĩa", use_container_width=True):
        st.session_state.show_def = True
        st.rerun()
  with col2:
    if st.button("➡️ Từ tiếp theo", use_container_width=True):
      st.session_state.current_idx = random.randint(0, len(df) - 1)
      st.session_state.show_def = False
      st.rerun()