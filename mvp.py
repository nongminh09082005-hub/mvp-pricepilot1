import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

st.set_page_config(page_title="PricePilot", layout="wide", page_icon="🔧")

# ====================== STYLE & POPPINS FONT ======================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif !important;
    }

    .main-title {
        font-size:42px;
        font-weight:700;
        text-align:center;
        margin-bottom:10px;
    }

    h1, h2, h3, h4 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600;
    }

    .stButton>button {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 500;
    }

    p, label, li {
        font-family: 'Poppins', sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)

# ====================== STYLE ======================
st.markdown("""
<style>
.main-title {
    font-size:42px;
    font-weight:700;
    text-align:center;
    margin-bottom:10px;
}
.sub-title {
    font-size:18px;
    text-align:center;
    color:#555;
    margin-bottom:30px;
}
.card {
    padding:25px;
    border-radius:12px;
    background:#f9f9f9;
    margin-top:15px;
}

    /* ================== GET STARTED BUTTON - MẠNH HƠN ================== */
    .small-btn {
        text-align: center !important;
        margin-top: 40px;
        width: 100%;
    }

    .small-btn button, 
    .stButton button, 
    button[data-baseweb="button"] {
        background-color: #008735 !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 14px 40px !important;
        font-size: 18px !important;
        margin: 0 auto !important;
        display: block !important;
        box-shadow: 0 4px 12px rgba(0, 135, 53, 0.4) !important;
    }

    .small-btn button:hover, 
    .stButton button:hover {
        background-color: #00CC00 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ====================== SESSION ======================
if "page" not in st.session_state:
    st.session_state.page = "intro"

# ====================== INTRO PAGE ======================
if st.session_state.page == "intro":

    st.markdown('<div class="main-title">PricePilot</div>', unsafe_allow_html=True)

    
    st.markdown("""
    ### PricePilot là công cụ mô phỏng định giá thông minh dành cho doanh nghiệp gia công cơ khí. Công cụ giúp bạn dễ dàng phân tích tác động của việc thay đổi giá bán đến lợi nhuận, sản lượng và rủi ro.
Bạn sẽ nhận được giá bán tối ưu và mức tăng giá khuyến nghị, lợi nhuận hiện tại & dự báo sau khi tăng giá, điểm hòa vốn, các chiến lược giá phù hợp (Aggressive, Balanced, Conservative), cùng những insight sâu sắc để bảo vệ lợi nhuận mà vẫn giữ được sức cạnh tranh trên thị trường.
    """)

    st.markdown('<div class="small-btn">', unsafe_allow_html=True)
    if st.button("Get Started"):
        st.session_state.page = "input"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ====================== INPUT PAGE ======================
elif st.session_state.page == "input":

    st.title("")

    with st.sidebar:

        st.header("Nguyên vật liệu")

        material = st.selectbox(
            "Chọn vật liệu",
            [
                "Thép - 29,825,172 VNĐ/tấn",
                "Inox - 84,000,000 VNĐ/tấn",
                "Nhôm - 93,255,906 VNĐ/tấn",
                "Đồng - 358,625,259 VNĐ/tấn"
            ]
        )

        material_price = {
            "Thép - 29,825,172 VNĐ/tấn": 29825172,
            "Inox - 84,000,000 VNĐ/tấn": 84000000,
            "Nhôm - 93,255,906 VNĐ/tấn": 93255906,
            "Đồng - 358,625,259 VNĐ/tấn": 358625259
        }

        tons = st.number_input("Sản lượng (tấn/tháng)", value=120)

        st.header("Chi phí")

        workers = st.number_input("Số công nhân", value=25)
        salary = st.number_input("Lương (VNĐ/tháng)", value=9000000)

        electricity_year = st.number_input("Điện + mặt bằng (VNĐ/năm)", value=600000000)
        maintenance_year = st.number_input("Bảo trì (VNĐ/năm)", value=300000000)
        machine_value = st.number_input("Giá trị máy (VNĐ)", value=3000000000)
        machine_life = st.number_input("Tuổi thọ (năm)", value=8)

        st.header("Kinh doanh")

        margin = st.slider("Margin (%)", 0, 60, 20)
        win_rate = st.slider("Win rate (%)", 0, 100, 35)
        orders = st.number_input("Số đơn/tháng", value=45)

        st.header("Thị trường")

        elasticity = st.slider("Elasticity", 0.5, 2.0, 1.2)
        industry_growth = st.slider("Tăng trưởng ngành (%)", 0, 15, 7)
        income_growth = st.slider("Tăng trưởng nhu cầu (%)", 0, 10, 5)
        inflation = st.slider("Lạm phát (%)", 0, 10, 4)

        if st.button("Run Simulation"):
            st.session_state.page = "loading"
            st.session_state.inputs = locals()
            st.rerun()

# ====================== LOADING ======================
elif st.session_state.page == "loading":

    st.title("Đang phân tích...")

    progress = st.progress(0)
    status = st.empty()

    for i in range(100):
        progress.progress(i + 1)

        if i < 30:
            status.text("Đang tính chi phí...")
        elif i < 60:
            status.text("Đang mô phỏng giá...")
        else:
            status.text("Đang tối ưu chiến lược...")

        time.sleep(0.02)

    st.session_state.page = "result"
    st.rerun()

# ====================== RESULT ======================
elif st.session_state.page == "result":

    inputs = st.session_state.inputs

    # ================= BASELINE =================
    mat_cost = inputs["material_price"][inputs["material"]] * inputs["tons"]
    labor_cost = inputs["workers"] * inputs["salary"]

    electricity_month = inputs["electricity_year"] / 12
    maintenance_month = inputs["maintenance_year"] / 12
    depreciation = inputs["machine_value"] / (inputs["machine_life"] * 12)

    fixed_cost = electricity_month + maintenance_month + depreciation
    total_cost = mat_cost + labor_cost + fixed_cost

    real_orders = inputs["orders"] * (inputs["win_rate"] / 100)
    cost_per_order = total_cost / max(real_orders, 1)

    base_price = cost_per_order / (1 - inputs["margin"] / 100)
    base_profit = (base_price - cost_per_order) * real_orders

    # ================= SIMULATION =================
    results = []

    for inc in range(0, 21, 2):

        demand_change = (
            inputs["industry_growth"]/100 +
            inputs["income_growth"]/100 -
            inputs["elasticity"] * (inc/100)
        )

        new_orders = real_orders * (1 + demand_change)

        new_cost = cost_per_order * (1 + inputs["inflation"]/100)
        new_price = base_price * (1 + inc/100)

        new_profit = (new_price - new_cost) * max(new_orders, 0)

        results.append({
            "Increase %": inc,
            "Orders": new_orders,
            "Profit": new_profit
        })

    df = pd.DataFrame(results)

    # ================= DISPLAY =================
    st.success("Phân tích hoàn tất")

  # ================= PHẦN HIỂN THỊ BASE PRICE  =================
    st.markdown("### Khuyến nghị giá gia công hiện tại")
    st.metric(
        label="**Giá base hiện tại (per order)**", 
        value=f"{base_price:,.0f} VNĐ"
    )

    best = df.loc[df["Profit"].idxmax()]

    col1, col2, col3 = st.columns(3)
    col1.metric("Profit hiện tại", f"{base_profit:,.0f}")
    col2.metric("Profit max", f"{best['Profit']:,.0f}")
    col3.metric("Optimal price", f"{best['Increase %']}%")

    fig = px.line(df, x="Increase %", y="Profit", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # ================= RECOMMENDATION =================
    st.header("Recommendation")

    col1, col2, col3 = st.columns(3)

    # Aggressive
    with col1:
        st.markdown("### 🔴 Aggressive")
        st.write(f"""
        **Tăng {best['Increase %']}%**

        👉 Tối đa hóa lợi nhuận  
        👉 Chấp nhận rủi ro giảm sản lượng  
        👉 Phù hợp khi:
        - Nhu cầu mạnh
        - Khách hàng ít nhạy giá
        """)

    # Balanced
    with col2:
        balanced_df = df[(df["Increase %"] <= 12)]

        if not balanced_df.empty:
            bal = balanced_df.loc[balanced_df["Profit"].idxmax()]

            st.markdown("### 🟡 Balanced")
            st.write(f"""
            **Tăng {bal['Increase %']}%**

            👉 Cân bằng giữa volume & margin  
            👉 Giảm rủi ro mất khách  
            👉 Phù hợp khi:
            - Thị trường cạnh tranh
            - Muốn tăng lợi nhuận nhưng vẫn giữ khách
            """)

    # Conservative
    with col3:
        st.markdown("### 🟢 Conservative")
        st.write("""
        **Tăng 0–5%**

        👉 Giữ ổn định sản lượng  
        👉 Rủi ro thấp nhất  
        👉 Phù hợp khi:
        - Khách hàng rất nhạy giá
        - Doanh nghiệp cần dòng tiền ổn định
        """)

    # ================= INSIGHT =================
    st.header("Insight")

    st.write(f"""
    - Khi bạn tăng giá → margin tăng nhưng số đơn giảm  
    - Khi bạn giảm giá → số đơn tăng nhưng margin giảm  

    👉 Điểm tối ưu hiện tại là **{best['Increase %']}%** vì đây là điểm:
    - Lợi nhuận cao nhất
    - Trade-off tốt nhất giữa volume và margin

    📌 Nếu Elasticity cao → nên tăng giá ít  
    📌 Nếu thị trường tăng trưởng mạnh → có thể tăng giá nhiều hơn  
    """)

   
    if st.button("Thử lại"):
        st.session_state.page = "input"
        st.rerun()