import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

# 1. 페이지 설정 및 레이아웃 최적화
st.set_page_config(page_title="Kd Analyzer", layout="wide")

# CSS: h2~h4, 텍스트, 숫자의 일괄 균형 조정
st.markdown("""
    <style>
    /* 전체 기본 폰트 설정 */
    html, body, [class*="css"] { 
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; 
        line-height: 1.6;
    }
    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; max-width: 900px; }

    /* h2: 메인 타이틀 (기존 h1에서 변경) */
    h2 {
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        color: #1a1a1a !important;
        letter-spacing: -0.02em;
        margin-bottom: 1.2rem !important;
    }

    /* h3: 섹션 소제목 */
    h3 {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        color: #2c3e50 !important;
        margin-top: 1.8rem !important;
        border-left: 4px solid #1f77b4;
        padding-left: 12px !important;
    }

    /* h4: 강조 텍스트나 작은 제목 */
    h4 {
        font-size: 1.0rem !important;
        font-weight: 600 !important;
        color: #444 !important;
    }

    /* 일반 텍스트 및 라벨 */
    .stTextArea label p, .stMarkdown p, p {
        font-size: 0.95rem !important;
        font-weight: 400 !important;
        color: #555 !important;
    }

    /* 결과 숫자 (Metric Value) */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: #1f77b4 !important;
    }

    /* 결과 라벨 (Metric Label) */
    [data-testid="stMetricLabel"] p {
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        color: #777 !important;
    }

    header {visibility: hidden;} 
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 타이틀을 h2로 렌더링
st.header("🧪 Kd Analysis Tool")

# 2. 데이터 입력 섹션
st.subheader("1. 데이터 입력")
col_in1, col_in2 = st.columns(2)

with col_in1:
    x_raw = st.text_area("농도 (Concentrations, 쉼표 구분)", "0, 0.5, 1, 2, 5, 10, 20, 50, 100", height=100)
with col_in2:
    y_raw = st.text_area("시그널 강도 (Signals, 쉼표 구분)", "0, 0.12, 0.21, 0.38, 0.62, 0.81, 0.92, 0.98, 1.02", height=100)

analyze_btn = st.button("🚀 데이터 분석 및 그래프 생성", use_container_width=True)

st.divider()

# 3. 계산 및 시각화 로직 (Biotech KD 분석)
def binding_model(x, Bmax, Kd):
    return (Bmax * x) / (Kd + x)

if analyze_btn:
    try:
        x = np.array([float(i.strip()) for i in x_raw.split(",")])
        y = np.array([float(i.strip()) for i in y_raw.split(",")])

        popt, _ = curve_fit(binding_model, x, y, p0=[max(y), np.median(x)])
        bmax_fit, kd_fit = popt
        r_squared = r2_score(y, binding_model(x, *popt))

        # 결과 출력 섹션
        st.subheader("2. 분석 결과")
        m1, m2, m3 = st.columns(3)
        m1.metric("Kd (해리 상수)", f"{kd_fit:.4f}")
        m2.metric("Bmax (최대 결합)", f"{bmax_fit:.4f}")
        m3.metric("R² (피팅 정확도)", f"{r_squared:.3f}")

        # 그래프 디자인 최적화
        fig, ax = plt.subplots(figsize=(10, 4.2))
        ax.scatter(x, y, color='#2c3e50', s=80, label='Measured Data', zorder=3, alpha=0.8)
        
        x_fit = np.linspace(0, max(x), 200)
        ax.plot(x_fit, binding_model(x_fit, *popt), color='#e74c3c', lw=3, label='Best Fit Curve')
        
        ax.set_xlabel("Concentration", fontsize=10)
        ax.set_ylabel("Response", fontsize=10)
        ax.grid(True, linestyle=':', alpha=0.5)
        ax.legend()
        
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)

    except Exception as e:
        st.error(f"데이터 형식을 다시 확인해 주세요: {e}")
else:
    st.info("데이터를 입력하고 '분석 및 그래프 생성' 버튼을 클릭해 주세요.")
