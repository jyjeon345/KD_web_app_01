import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

# 1. 페이지 설정
st.set_page_config(page_title="Kd Analyzer", layout="wide")

# CSS: 버튼 색상 및 시각적 균형 일괄 조정
st.markdown("""
    <style>
    /* 전체 레이아웃 */
    html, body, [class*="css"] { font-family: sans-serif; }
    .block-container { padding-top: 1.5rem; max-width: 900px; margin: 0 auto; }

    /* 타이틀 및 소제목 */
    h2 { font-size: 1.6rem !important; font-weight: 800 !important; text-align: center; margin-bottom: 1.5rem !important; }
    h3 { font-size: 1.2rem !important; font-weight: 700 !important; text-align: center; margin-top: 1.5rem !important; }

    /* 1. 입력창 디자인 (세로 1열) */
    textarea {
        text-align: center !important;
        height: 55px !important; 
        min-height: 55px !important;
        padding-top: 16px !important;
        font-size: 1.1rem !important;
        background-color: #f0f2f6 !important;
        border-radius: 10px !important;
        border: 1px solid #d1d5db !important;
        resize: none;
    }

    /* 2. 버튼 디자인 (색상 및 효과 추가) */
    .stButton > button {
        background-color: #1f77b4 !important; /* 메인 블루 색상 */
        color: white !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        padding: 0.6rem 2rem !important;
        border-radius: 10px !important;
        border: none !important;
        transition: all 0.3s ease-in-out !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
    }
    
    .stButton > button:hover {
        background-color: #155a8a !important; /* 호버 시 더 진한 색상 */
        box-shadow: 0 4px 12px rgba(31, 119, 180, 0.3) !important;
        transform: translateY(-1px);
    }

    /* 3. 분석 결과 (Metric) 가로 3열 강제 유지 */
    [data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important; }
    [data-testid="column"] { flex: 1 1 30% !important; min-width: 0 !important; }

    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #f0f2f6;
        border-radius: 10px;
        padding: 12px 5px !important;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    [data-testid="stMetricValue"] { font-size: 1.6rem !important; font-weight: 700 !important; color: #1f77b4 !important; }
    [data-testid="stMetricLabel"] p { font-size: 0.85rem !important; font-weight: 600 !important; color: #666 !important; }

    header {visibility: hidden;} 
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.header("🧪 Kd Analysis Tool")

# 2. 데이터 입력 섹션 (1열 구성)
st.subheader("1. 데이터 입력")

x_raw = st.text_area("농도 (Concentrations, 쉼표 구분)", "0, 0.5, 1, 2, 5, 10, 20, 50, 100")
y_raw = st.text_area("시그널 강도 (Signals, 쉼표 구분)", "0, 0.12, 0.21, 0.38, 0.62, 0.81, 0.92, 0.98, 1.02")

# 색상이 적용된 버튼
analyze_btn = st.button("🚀 데이터 분석 및 그래프 생성", use_container_width=True)

st.divider()

# 3. 계산 및 시각화 로직
def binding_model(x, Bmax, Kd):
    return (Bmax * x) / (Kd + x)

if analyze_btn:
    try:
        x = np.array([float(i.strip()) for i in x_raw.split(",")])
        y = np.array([float(i.strip()) for i in y_raw.split(",")])

        popt, _ = curve_fit(binding_model, x, y, p0=[max(y), np.median(x)])
        bmax_fit, kd_fit = popt
        r_squared = r2_score(y, binding_model(x, *popt))

        # 결과 출력 (가로 3열 유지)
        st.subheader("2. 분석 결과")
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("Kd (해리 상수)", f"{kd_fit:.4f}")
        m_col2.metric("Bmax (최대 결합)", f"{bmax_fit:.4f}")
        m_col3.metric("R² (피팅 정확도)", f"{r_squared:.3f}")

        # 그래프 디자인
        fig, ax = plt.subplots(figsize=(10, 4.2))
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
        st.error(f"데이터 형식을 다시 확인해 주세요: {e}")
else:
    st.info("데이터를 입력하고 '분석 및 그래프 생성' 버튼을 클릭해 주세요.")
