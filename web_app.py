import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

# 1. 페이지 설정
st.set_page_config(page_title="Kd Analyzer", layout="wide")

# CSS: 라벨 굵게(Bold) 및 왼쪽 맞춤(Left-align) 적용
st.markdown("""
    <style>
    /* 전체 레이아웃 */
    html, body, [class*="css"] { font-family: sans-serif; }
    .block-container { padding-top: 1rem; max-width: 900px; margin: 0 auto; }

    /* 타이틀 및 섹션 제목 (왼쪽 맞춤으로 통일) */
    h2 { font-size: 1.5rem !important; font-weight: 800 !important; text-align: left; margin-bottom: 1rem !important; }
    h3 { font-size: 1.15rem !important; font-weight: 700 !important; text-align: left; margin-top: 1.5rem !important; margin-bottom: 1rem !important; }

    /* 1. 입력창 라벨: 굵은 글씨 + 왼쪽 맞춤 */
    .stTextArea label p {
        font-size: 1rem !important;
        font-weight: 700 !important; /* 굵게 */
        text-align: left !important;  /* 왼쪽 맞춤 */
        color: #333 !important;
        margin-bottom: 8px !important;
        display: block !important;
    }

    /* 입력창 내부 숫자 디자인 (중앙 유지 또는 왼쪽 선택 가능 - 현재 중앙) */
    textarea {
        text-align: center !important;
        height: 52px !important; 
        min-height: 52px !important;
        padding-top: 15px !important; 
        background-color: #f0f2f6 !important;
        border-radius: 8px !important;
        border: 1px solid #d1d5db !important;
        resize: none;
    }

    /* 2. 분석 결과 라벨: 굵은 글씨 + 왼쪽 맞춤 */
    [data-testid="stMetricLabel"] p { 
        font-size: 0.9rem !important; 
        font-weight: 700 !important; /* 굵게 */
        text-align: left !important;  /* 왼쪽 맞춤 */
        color: #444 !important;
        margin-bottom: 5px !important;
    }

    /* 결과 수치(Value) 박스 레이아웃 조정 */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e1e4e8;
        border-radius: 10px;
        padding: 15px !important;
        display: flex;
        flex-direction: column;
        align-items: flex-start; /* 내부 요소 왼쪽 정렬 */
    }

    [data-testid="stMetricValue"] { 
        font-size: 1.6rem !important; 
        font-weight: 700 !important; 
        color: #1f77b4 !important;
        text-align: left !important;
    }

    /* 결과창 3열 강제 유지 */
    [data-testid="column"] { flex: 1 1 30% !important; min-width: 0 !important; }

    /* 버튼 디자인 */
    .stButton > button {
        background-color: #1f77b4 !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        padding: 0.6rem 2rem !important;
    }

    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.header("🧪 Kd Analysis Tool")

# 2. 데이터 입력 (1열 배치)
st.subheader("1. 데이터 입력")
x_raw = st.text_area("농도 (Concentrations, 쉼표 구분)", "0, 0.5, 1, 2, 5, 10, 20, 50, 100")
y_raw = st.text_area("시그널 강도 (Signals, 쉼표 구분)", "0, 0.12, 0.21, 0.38, 0.62, 0.81, 0.92, 0.98, 1.02")

analyze_btn = st.button("🚀 데이터 분석 및 그래프 생성", use_container_width=True)
st.divider()

# 3. 계산 및 시각화
def binding_model(x, Bmax, Kd):
    return (Bmax * x) / (Kd + x)

if analyze_btn:
    try:
        x = np.array([float(i.strip()) for i in x_raw.split(",")])
        y = np.array([float(i.strip()) for i in y_raw.split(",")])

        popt, _ = curve_fit(binding_model, x, y, p0=[max(y), np.median(x)])
        bmax_fit, kd_fit = popt
        r_squared = r2_score(y, binding_model(x, *popt))

        # 결과 출력 (라벨 왼쪽 맞춤 반영)
        st.subheader("2. 분석 결과")
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("Kd (해리 상수)", f"{kd_fit:.4f}")
        m_col2.metric("Bmax (최대 결합)", f"{bmax_fit:.4f}")
        m_col3.metric("R² (피팅 정확도)", f"{r_squared:.3f}")

        # 그래프 디자인
        fig, ax = plt.subplots(figsize=(10, 4.5))
        ax.scatter(x, y, color='#2c3e50', s=80, label='Measured Data', alpha=0.8)
        x_fit = np.linspace(0, max(x), 200)
        ax.plot(x_fit, binding_model(x_fit, *popt), color='#e74c3c', lw=3, label=f'Best Fit (Kd={kd_fit:.2f})')
        ax.set_xlabel("Concentration")
        ax.set_ylabel("Response")
        ax.grid(True, linestyle=':', alpha=0.5)
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)

    except Exception as e:
        st.error(f"오류 발생: {e}")
