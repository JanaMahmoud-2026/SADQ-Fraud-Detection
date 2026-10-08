import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="SADQ Fraud Detection", page_icon="🛡️", layout="wide")

st.title("🛡️ SADQ - Fraud Detection System")
st.markdown("### نظام كشف الاحتيال المالي الذكي")

st.sidebar.header("⚙️ الإعدادات")
threshold = st.sidebar.slider("حد الاحتيال (Threshold)", 0.0, 1.0, 0.5)

st.sidebar.markdown("---")
st.sidebar.info("المشروع: SADQ-Fraud-Detection\nBy: Jana Mahmoud")

tab1, tab2, tab3 = st.tabs(["🔍 كشف مباشر", "📂 فحص ملف", "📊 عن المشروع"])

with tab1:
    st.subheader("إدخال عملية جديدة")
    col1, col2 = st.columns(2)
    with col1:
        amount = st.number_input("المبلغ (Amount)", min_value=0.0, value=1500.0)
        time = st.number_input("الوقت (Time)", min_value=0, value=120)
        v1 = st.slider("V1", -5.0, 5.0, 0.5)
        v2 = st.slider("V2", -5.0, 5.0, -0.3)
    with col2:
        v3 = st.slider("V3", -5.0, 5.0, 1.2)
        v4 = st.slider("V4", -5.0, 5.0, -1.0)
        v14 = st.slider("V14", -5.0, 5.0, -2.5)
        v17 = st.slider("V17", -5.0, 5.0, -1.5)

    # Simple SADQ Logic Simulation
    risk_score = (abs(v14) + abs(v17) + abs(v1) + (amount/10000)) / 4
    is_fraud = risk_score > threshold

    if st.button("🚀 افحص العملية", type="primary", use_container_width=True):
        if is_fraud:
            st.error(f"🚨 عملية مشبوهة! Risk Score: {risk_score:.2f}")
            st.progress(min(risk_score,1.0))
            st.markdown("**التوصية:** إيقاف العملية ومراجعة يدوية")
        else:
            st.success(f"✅ عملية سليمة - Risk Score: {risk_score:.2f}")
            st.progress(min(risk_score,1.0))

with tab2:
    st.subheader("رفع ملف CSV للفحص")
    file = st.file_uploader("ارفعي ملف transactions.csv", type=["csv"])
    if file:
        df = pd.read_csv(file)
        st.dataframe(df.head())
        # Simulate prediction
        df['Fraud_Score'] = np.random.uniform(0,1, len(df))
        df['Prediction'] = df['Fraud_Score'].apply(lambda x: 'Fraud' if x > threshold else 'Normal')
        st.bar_chart(df['Prediction'].value_counts())
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 تحميل النتائج", csv, "results.csv", "text/csv")

with tab3:
    st.markdown("""
    **SADQ Fraud Detection**
    - مشروع تخرج لكشف الاحتيال باستخدام تعلم الآلة
    - الموديل: XGBoost + Isolation Forest
    - الدقة المستهدفة: 99.2%
    - المطورة: Jana Mahmoud - 2026
    """)