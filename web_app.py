import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# 1. 페이지 제목과 설명
st.set_page_config(page_title="Kd Analyzer", layout="wide")
st.title("🧪 Biomolecule Kd Calculation Tool")
st.markdown("농도별 시그널 데이터를 입력하여 **Kd(해리 상수)**를 구하세요.")

# 2. 사이드바 - 데이터 입력창
st.sidebar.header("Data Input")
x_raw = st.sidebar.text_area("Concentrations (X, comma separated)", "0, 0.5, 1, 2, 5, 10, 20, 50, 100")
y_raw = st.sidebar.text_area("Signal Intensity (Y, comma separated)", "0, 0.12, 0.21, 0.38, 0.62, 0.81, 0.92, 0.98, 1.02")

# 3. 계산 및 시각화 로직
if st.sidebar.button("Calculate & Plot"):
    try:
        x = np.array([float(i.strip()) for i in x_raw.split(",")])
        y = np.array([float(i.strip()) for i in y_raw.split(",")])

        def binding_model(x, Bmax, Kd):
            return (Bmax * x) / (Kd + x)

        popt, _ = curve_fit(binding_model, x, y, p0=[max(y), np.median(x)])
        bmax_fit, kd_fit = popt

        # 결과 보여주기
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"### Kd: {kd_fit:.4f}")
        with col2:
            st.info(f"### Bmax: {bmax_fit:.4f}")

        # 그래프 그리기
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(x, y, color='red', s=50, label='Actual Data')
        x_range = np.linspace(0, max(x), 100)
        ax.plot(x_range, binding_model(x_range, *popt), 'b-', label=f'Fit Line (Kd={kd_fit:.2f})')
        ax.set_xlabel("Concentration")
        ax.set_ylabel("Signal Intensity")
        ax.grid(True, alpha=0.3)
        ax.legend()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")

