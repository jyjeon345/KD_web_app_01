import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

# 1. 페이지 설정: 워드프레스 900px 폭에 최적화
st.set_page_config(page_title="Kd Analyzer", layout="wide")

# CSS: 아스트라 테마와 어울리도록 폰트 및 여백 조정
st.markdown("""
    <style>
    /* 기본 폰트를 시스템 산세리프(Astra 기본값)로 설정 */
    html, body, [class*="css"] { font-family: "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    .block-container { padding-top: 1rem; padding-bottom: 0rem; max-width: 900px; }
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; }
    header {visibility: hidden;} 
    footer {visibility: hidden;} 
    </style>
    """, unsafe_allow_html=True) # <- 'html'로 고쳐주세요!

# 2. 사이드바 설정
st.sidebar.header("📊 Data Input")
x_raw = st.sidebar.text_area("Conc. (X)", "0, 0.5, 1, 2, 5, 10, 20, 50, 100")
y_raw = st.sidebar.text_area("Signal (Y)", "0, 0.12, 0.21, 0.38, 0.62, 0.81, 0.92, 0.98, 1.02")

def binding_model(x, Bmax, Kd):
    return (Bmax * x) / (Kd + x)

if st.sidebar.button("Analyze Now"):
    try:
        x = np.array([float(i.strip()) for i in x_raw.split(",")])
        y = np.array([float(i.strip()) for i in y_raw.split(",")])

        # 피팅 및 R-square 계산
        popt, _ = curve_fit(binding_model, x, y, p0=[max(y), np.median(x)])
        bmax_fit, kd_fit = popt
        y_pred = binding_model(x, *popt)
        r_squared = r2_score(y, y_pred)

        # 3. 결과 레이아웃: 수치를 3열로 배치하여 공간 절약
        m1, m2, m3 = st.columns(3)
        m1.metric("Kd (Affinity)", f"{kd_fit:.4f}")
        m2.metric("Bmax", f"{bmax_fit:.4f}")
        m3.metric("R² (Fit Quality)", f"{r_squared:.3f}")

        # 4. 그래프 레이아웃: 가로폭 900px에 최적화된 가로세로비
        fig, ax = plt.subplots(figsize=(8, 3.8)) # 가로로 더 길게
        ax.scatter(x, y, color='#2c3e50', s=60, label='Data', zorder=3)
        
        x_fit = np.linspace(0, max(x), 200)
        ax.plot(x_fit, binding_model(x_fit, *popt), color='#e74c3c', lw=2.5, label='Fit Curve')
        
        ax.set_xlabel("Concentration", fontsize=10)
        ax.set_ylabel("Response", fontsize=10)
        ax.tick_params(labelsize=9)
        ax.grid(True, linestyle=':', alpha=0.7)
        ax.legend(fontsize=9)
        
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.write("⬅️ 왼쪽 바에 데이터를 입력하고 분석 버튼을 눌러주세요.")

