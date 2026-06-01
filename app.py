import streamlit as st
import plotly.graph_objects as px
import plotly.express as px_exp
import pandas as pd
import numpy as np

# 1. CẤU HÌNH TRANG & GIAO DIỆN (DARK MODE NEON STYLE)
st.set_page_config(
    page_title="Merchant Onboarding Performance App",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS để đè giao diện phẳng lì thành giao diện App cao cấp
st.markdown("""
    <style>
    body { background-color: #0e1117; color: #ecf0f1; }
    .stApp { background-color: #0b0d12; }
    [data-testid="stSidebar"] { background-color: #11151c; border-right: 1px solid #1e293b; }
    div.metric-card {
        background-color: #161b22;
        border: 1px solid #21262d;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        text-align: center;
    }
    div.metric-card h3 { color: #8b5cf6; margin: 0 0 10px 0; font-size: 16px; font-weight: 600; text-transform: uppercase; }
    div.metric-card p { color: #ffffff; margin: 0; font-size: 28px; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

# 2. GIẢ LẬP DATA SỐ LIỆU (Sau này kết nối trực tiếp với Google Sheets API)
@st.cache_data
def load_funnel_data():
    return pd.DataFrame({
        "Bước": ["Hồ sơ tạo mới", "HTKD duyệt", "VHSP duyệt", "Cấu hình", "Giao việc", "Triển khai thành công"],
        "SL": [1200, 1050, 920, 810, 750, 680]
    })

@st.cache_data
def load_backlog_data():
    return pd.DataFrame({
        "Trạng thái": ["Chờ HTKD", "Chờ BSHS", "Chờ VHSP", "Chờ cấu hình", "Chờ giao việc", "Chờ VNNG nhận", "Chờ triển khai", "Chờ nghiệm thu"],
        "Số lượng tồn": [45, 30, 25, 15, 10, 20, 55, 12]
    })

# 3. SIDEBAR DI CHUYỂN GIỮA CÁC PHẦN (MENU APP)
st.sidebar.title("⚡ NAVIGATION")
menu = st.sidebar.radio(
    "Chọn Chức năng Báo cáo:",
    [
        "I. Tổng quan (Executive Summary)",
        "II. Phễu Chuyển đổi (Onboarding Funnel)",
        "III. Tồn đọng (Backlog)",
        "IV. Tuổi hồ sơ (Aging)",
        "V. Hiệu suất & SLA",
        "VI. Chất lượng hồ sơ & Lỗi",
        "VII. Quản lý đối tác VNNG",
        "VIII. Trung tâm cảnh báo (Alert)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔄 Trạng thái kết nối")
st.sidebar.success("Đang đồng bộ trực tuyến với Google Sheets")
if st.sidebar.button("F5 - Làm mới số liệu"):
    st.rerun()

# 4. XỬ LÝ HIỂN THỊ TỪNG TRANG APP THEO LỰA CHỌN
# ----------------------------------------------------------------------
if menu == "I. Tổng quan (Executive Summary)":
    st.title("📊 TỔNG QUAN HIỆU SUẤT HÀNG NGÀY")
    st.markdown("---")
    
    # Hàng KPI Đầu tiên (Volume)
    cols = st.columns(6)
    kpis = [
        ("Tạo mới hôm nay", "45", cols[0]),
        ("Hoàn thành hôm nay", "38", cols[1]),
        ("Đang xử lý", "212", cols[2]),
        ("Tồn cuối ngày", "184", cols[3]),
        ("Quá SLA", "14", cols[4]),
        ("Merchant Thành công", "680", cols[5])
    ]
    for title, val, col in kpis:
        with col:
            st.markdown(f'<div class="metric-card"><h3>{title}</h3><p>{val}</p></div>', unsafe_allow_html=True)
            
    st.markdown("### 📈 Xu hướng 30 ngày qua (Trend)")
    chart_data = pd.DataFrame(
        np.random.randint(30, 60, size=(30, 3)),
        columns=['Hồ sơ tạo mới', 'Hồ sơ hoàn thành', 'Hồ sơ tồn']
    )
    st.line_chart(chart_data, color=["#6366f1", "#4ade80", "#f43f5e"])

# ----------------------------------------------------------------------
elif menu == "II. Phễu Chuyển đổi (Onboarding Funnel)":
    st.title("🎯 PHỄU CHUYỂN ĐỔI ONBOARDING MERCHANT")
    st.markdown("---")
    
    df_funnel = load_funnel_data()
    
    # Vẽ đồ thị phễu dạng phễu xịn của Plotly (Interactive)
    fig = px.funnel(
        df_funnel, x='SL', y='Bước',
        color_discrete_sequence=['#8b5cf6'],
        title="Phễu chuyển đổi toàn quy trình Onboarding"
    )
    fig.update_layout(template="plotly_dark", paper_bgcolor="#0b0d12", plot_bgcolor="#0b0d12")
    st.plotly_chart(fig, use_container_width=True)
    
    # Conversion từng bước & End-to-End
    st.markdown("### 📐 Chỉ số Chuyển đổi chi tiết")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Chuyển đổi từng bước (Step-by-Step Conversion):**")
        st.code("""
        - Khai báo → HTKD: 87.5%
        - HTKD → VHSP: 87.6%
        - VHSP → Cấu hình: 88.0%
        - Cấu hình → Giao việc: 92.5%
        - Giao việc → Triển khai thành công: 90.6%
        """, language="yaml")
    with col2:
        st.markdown("**Hiệu suất tổng quy trình (End-to-End):**")
        st.metric(label="Tỷ lệ Tạo hồ sơ → Triển khai thành công", value="56.6%", delta="+2.3% so với tháng trước")

# ----------------------------------------------------------------------
elif menu == "III. Tồn đọng (Backlog)":
    st.title("📦 QUẢN LÝ TỒN ĐỌNG (BACKLOG ANALYSIS)")
    st.markdown("---")
    
    df_backlog = load_backlog_data()
    
    col1, col2 = st.columns([6, 4])
    with col1:
        st.markdown("### Tồn theo trạng thái")
        st.dataframe(df_backlog, use_container_width=True, hide_index=True)
    with col2:
        st.markdown("### Tỷ trọng tồn (Donut Chart)")
        fig_donut = px_exp.pie(df_backlog, values='Số lượng tồn', names='Trạng thái', hole=0.5, color_discrete_sequence=px_exp.colors.sequential.Purples_r)
        fig_donut.update_layout(template="plotly_dark", paper_bgcolor="#0b0d12")
        st.plotly_chart(fig_donut, use_container_width=True)

# ----------------------------------------------------------------------
elif menu == "IV. Tuổi hồ sơ (Aging)":
    st.title("⏳ THEO DÕI TUỔI HỒ SƠ (AGING REPORT)")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Aging Toàn bộ")
        st.bar_chart(pd.DataFrame({"SL": [50, 40, 30, 15, 8]}, index=["0-1 ngày", "2-3 ngày", "4-7 ngày", "8-15 ngày", ">15 ngày"]), color="#8b5cf6")
    with col2:
        st.subheader("Aging BSHS")
        st.bar_chart(pd.DataFrame({"SL": [20, 15, 8, 2]}, index=["0-1 ngày", "2-3 ngày", "4-7 ngày", ">7 ngày"]), color="#3b82f6")
    with col3:
        st.subheader("Aging Triển khai")
        st.bar_chart(pd.DataFrame({"SL": [35, 22, 12, 5]}, index=["0-1 ngày", "2-3 ngày", "4-7 ngày", ">7 ngày"]), color="#ec4899")

# ----------------------------------------------------------------------
elif menu == "V. Hiệu suất & SLA":
    st.title("⏱️ HIỆU SUẤT XỬ LÝ & SLA TỪNG CÔNG ĐOẠN")
    st.markdown("---")
    
    st.markdown("### Leadtime Toàn Quy Trình (Ngày tạo → Triển khai thành công)")
    cols = st.columns(4)
    cols[0].metric("Median (Trung vị)", "3.2 Ngày")
    cols[1].metric("P90", "5.8 Ngày")
    cols[2].metric("Average (Trung bình)", "3.5 Ngày")
    cols[3].metric("Max (Lâu nhất)", "18.2 Ngày")
    
    st.markdown("### Chi tiết SLA từng công đoạn")
    sla_data = pd.DataFrame({
        "Công đoạn": ["HTKD", "VHSP", "Cấu hình", "Giao việc", "Triển khai"],
        "Median (h)": [4, 6, 2, 1, 24],
        "P90 (h)": [8, 12, 4, 2, 48],
        "% Đạt SLA": ["95.2%", "91.8%", "98.5%", "99.1%", "86.4%"]
    })
    st.table(sla_data)

# ----------------------------------------------------------------------
elif menu == "VI. Chất lượng hồ sơ & Lỗi":
    st.title("🎯 QUẢN LÝ CHẤT LƯỢNG HỒ SƠ (QLDV)")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### First Pass Yield (Tỷ lệ Đạt ngay lần đầu)")
        fig_pie = px_exp.pie(values=[75, 25], names=["Pass lần đầu", "Phải BSHS / Từ chối"], color_discrete_sequence=["#10b981", "#ef4444"])
        st.plotly_chart(fig_pie, use_container_width=True)
    with col2:
        st.markdown("### Chỉ số BSHS (Bổ sung hồ sơ)")
        st.markdown("""
        - **Tỷ lệ hồ sơ lỗi cần BSHS:** 21.4%
        - **Số lần BSHS Trung bình / Hồ sơ:** 1.4 lần
        - **Hồ sơ hiện đang ở trạng thái BSHS:** 32 Hồ sơ
        - **Tỷ lệ Khôi phục (Recovery Rate):** 94.2%
        """)

# ----------------------------------------------------------------------
elif menu == "VII. Quản lý Đối tác VNNG":
    st.title("🤝 HIỆU SUẤT ĐỐI TÁC TRIỂN KHAI VNNG")
    st.markdown("---")
    
    cols = st.columns(4)
    cols[0].metric("Job giao hôm nay", "28")
    cols[1].metric("Job hoàn thành hôm nay", "24")
    cols[2].metric("Job Pending", "5")
    cols[3].metric("Job Tồn", "42")
    
    st.markdown("### Hiệu suất theo nhân viên triển khai")
    nv_data = pd.DataFrame({
        "Nhân viên": ["VNNG_TuanNV", "VNNG_HoangAM", "VNNG_LinhPhan", "VNNG_DuyNguyen"],
        "Số job đã nhận": [15, 12, 10, 5],
        "% Đạt SLA": ["93.3%", "100%", "80.0%", "100%"]
    })
    st.dataframe(nv_data, use_container_width=True, hide_index=True)

# ----------------------------------------------------------------------
elif menu == "VIII. Trung tâm cảnh báo (Alert)":
    st.title("🚨 TRUNG TÂM CẢNH BÁO TỒN LÂU / QUÁ SLA")
    st.markdown("---")
    
    st.subheader("🔴 Top 5 hồ sơ tồn lâu nhất")
    st.table(pd.DataFrame({
        "Mã HS": ["HS-9982", "HS-9811", "HS-9762", "HS-9710", "HS-9655"],
        "Merchant": ["Công ty Cổ phần Thương mại Alpha", "Hộ kinh doanh Nguyễn Văn A", "Cửa hàng Thời trang Venus", "Công ty TNHH Beta Việt Nam", "Nhà thuốc số 10"],
        "Trạng thái": ["Chờ triển khai", "Chờ BSHS", "Chờ VHSP", "Chờ cấu hình", "Chờ triển khai"],
        "Số ngày tồn": [19, 16, 14, 12, 11]
    }))
    
    st.subheader("⚠️ Hồ sơ đang quá hạn SLA")
    st.table(pd.DataFrame({
        "Mã HS": ["HS-1022", "HS-1029"],
        "Merchant": ["Quán ăn ngon 3 miền", "Coffee House chi nhánh 2"],
        "SLA Quy định": ["24 giờ", "4 giờ"],
        "Thời gian thực tế hiện tại": ["36 giờ", "7.5 giờ"]
    }))
