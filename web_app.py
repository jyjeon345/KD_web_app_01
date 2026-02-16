import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

# 1. 페이지 설정
st.set_page_config(page_title="Kd Analyzer", layout="wide")

# CSS: 수직 정렬을 위한 스타일 추가
st.markdown("""
    <style>
    /* 전체 폰트 및 레이아웃 */
    html, body, [class*="css"] { font-family: sans-serif; }
    .block-container { padding-top: 1.5rem; max-width: 900px; }

    /* h2 타이틀 중앙 정렬 */
    h2 { font-size: 1.6rem !important; font-weight: 800 !important; text-align: center; margin-bottom: 1.5rem !important; }

    /* 1. 입력창 내부 '텍스트' 수직 중앙 정렬 */
    textarea {
        text-align: center !important;
        display: flex !important;
        align-items: center !important; /* 수직 중앙 */
        justify-content: center !important; /* 가로 중앙 */
        padding-top: 35px !important; /* 높이가 100px일 때 글자를 중앙으로 밀어내기 위한 조정 */
        line-height: 1.5 !important;
    }

    /* 2. 입력창 '라벨' 수직/가로 중앙 정렬 */
    .stTextArea label {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin-bottom: 10px !important;
    }

    /* 3. 결과 수치(Metric) 카드 내부 수직 정렬 */
    [data-testid="stMetric"] {
        display: flex;
        flex-direction: column;
        align-items: center; /* 가로 중앙 */
        justify-content: center; /* 세로 중앙 */
        text-align: center;
    }

    [data-testid="stMetricValue"] { font-size: 1.5rem !important; font-weight: 700 !important; line-height: 1.2 !important; }
    [data-testid="stMetricLabel"] p { font-size: 0.85rem !important; margin-bottom: 0 !important; }

    header {visibility: hidden;} 
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.header("🧪 Kd Analysis Tool")

# 2. 데이터 입력 섹션 (vertical_alignment="center" 적용)
st.subheader("1. 데이터 입력")
# 두 컬럼의 높이가 달라도 수직 중앙에 배치되도록 설정
col_in1, col_in2 = st.columns(2, vertical_alignment="center")

with col_in1:
    x_raw = st.text_area("농도 (Concentrations)", "0, 0.5, 1, 2, 5, 10, 20, 50, 100", height=100)
with col_in2:
    y_raw = st.text_area("시그널 강도 (Signals)", "0, 0.12, 0.21, 0.38, 0.62, 0.81, 0.92, 0.98, 1.02", height=100)

analyze_btn = st.button("🚀 데이터 분석 시작", use_container_width=True)

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

        # 결과 출력 섹션 (여기도 수직 중앙 정렬 적용)
        st.subheader("2. 분석 결과")
        m_col1, m_col2, m_col3 = st.columns(3, vertical_alignment="center")
        m_col1.metric("Kd (해리 상수)", f"{kd_fit:.4f}")
        m_col2.metric("Bmax (최대 결합)", f"{bmax_fit:.4f}")
        m_col3.metric("R² (피팅 정확도)", f"{r_squared:.3f}")

        # 그래프
        fig, ax = plt.subplots(figsize=(10, 4.2))
        ax.scatter(x, y, color='#2c3e50', s=80, label='Data', alpha=0.8)
        x_fit = np.linspace(0, max(x), 200)
        ax.plot(x_fit, binding_model(x_fit, *popt), color='#e74c3c', lw=3, label='Fit Curve')
        ax.grid(True, linestyle=':', alpha=0.5)
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)

    except Exception as e:
        st.error(f"오류 발생: {e}")
