import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

# 1. 페이지 설정
st.set_page_config(page_title="Kd Analyzer", layout="wide")

# CSS: 워드프레스 환경에 맞춰 여백 최적화
st.markdown("""
    <style>
    /* 1. 메인 타이틀 (KD Analysis Tool) 크기 조절 */
    h1 {
        font-size: 1.8rem !important;  /* 기본값보다 작게 조절 */
        font-weight: 700 !important;
        color: #31333F !important;
        padding-bottom: 0.5rem !important;
    }

    /* 2. 소제목 (1. 데이터 입력, 2. 분석 결과) 크기 조절 */
    h3 {
        font-size: 1.3rem !important;  /* 타이틀보다 약간 작게 */
        margin-top: 1.5rem !important;
        color: #262730 !important;
    }

    /* 3. 입력창 라벨 (농도, 시그널 강도) 폰트 조절 */
    .stTextArea label p {
        font-size: 1rem !important;
        font-weight: 600 !important;
    }

    /* 기존 워드프레스 최적화 코드 유지 */
    html, body, [class*="css"] { font-family: sans-serif; }
    .block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 900px; }
    header {visibility: hidden;} 
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("🧪 KD Analysis Tool")

# 2. 메인 화면에 입력창 배치 (사이드바 대신)
st.subheader("1. 데이터 입력")
col_in1, col_in2 = st.columns(2)

with col_in1:
    x_raw = st.text_area("농도 (Concentrations, 쉼표 구분)", "0, 0.5, 1, 2, 5, 10, 20, 50, 100", height=80)
with col_in2:
    y_raw = st.text_area("시그널 강도 (Signals, 쉼표 구분)", "0, 0.12, 0.21, 0.38, 0.62, 0.81, 0.92, 0.98, 1.02", height=80)

analyze_btn = st.button("🚀 데이터 분석 시작", use_container_width=True)

st.divider()

# 3. 계산 및 결과 출력
def binding_model(x, Bmax, Kd):
    return (Bmax * x) / (Kd + x)

if analyze_btn:
    try:
        x = np.array([float(i.strip()) for i in x_raw.split(",")])
        y = np.array([float(i.strip()) for i in y_raw.split(",")])

        # 피팅 실행
        popt, _ = curve_fit(binding_model, x, y, p0=[max(y), np.median(x)])
        bmax_fit, kd_fit = popt
        r_squared = r2_score(y, binding_model(x, *popt))

        # 결과 수치 (3열 배치)
        st.subheader("2. 분석 결과")
        m1, m2, m3 = st.columns(3)
        m1.metric("KD (해리 상수)", f"{kd_fit:.4f}")
        m2.metric("Bmax (최대 결합)", f"{bmax_fit:.4f}")
        m3.metric("R² (정확도)", f"{r_squared:.3f}")

        # 그래프 출력
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.scatter(x, y, color='#2c3e50', s=80, label='Measured Data', zorder=3)
        x_fit = np.linspace(0, max(x), 200)
        ax.plot(x_fit, binding_model(x_fit, *popt), color='#e74c3c', lw=3, label='Best Fit Curve')
        
        ax.set_xlabel("Concentration")
        ax.set_ylabel("Response")
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend()
        
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)

    except Exception as e:
        st.error(f"입력 데이터를 확인해 주세요: {e}")
else:
    st.info("위의 입력창에 데이터를 넣고 버튼을 누르면 그래프가 여기에 나타납니다.")


