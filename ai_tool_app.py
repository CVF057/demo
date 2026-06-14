"""
AI 工具选型器 — Streamlit Web App
面试作品：为公司三个业务场景（赛车模拟器 / 艺术空间 / 商业活动）快速匹配最佳 AI 工具
"""

import streamlit as st
import pandas as pd
from pathlib import Path

# ── 页面配置 ──────────────────────────────────────────
st.set_page_config(
    page_title="AI 工具选型器",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 自定义样式 ──────────────────────────────────────────
st.markdown("""
<style>
    /* 全局 */
    .main { padding-top: 1rem; }

    /* 指标卡片 */
    .metric-row {
        display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1.5rem;
    }
    .metric-card {
        flex: 1; min-width: 140px; padding: 1rem 1.2rem;
        border-radius: 12px; background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
        border: 1px solid #e0e0e0;
    }
    .metric-card .number { font-size: 2rem; font-weight: 700; color: #1a1a1a; }
    .metric-card .label { font-size: 0.85rem; color: #666; margin-top: 0.25rem; }

    /* 工具卡片 */
    .tool-card {
        padding: 1.2rem 1.5rem; border-radius: 12px;
        border: 1px solid #e8e8e8; margin-bottom: 0.8rem;
        background: white; transition: box-shadow 0.2s;
    }
    .tool-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.08); }
    .tool-card .header { display: flex; justify-content: space-between; align-items: flex-start; }
    .tool-card .name { font-size: 1.15rem; font-weight: 700; color: #1a1a1a; }
    .tool-card .category-tag {
        font-size: 0.75rem; padding: 2px 10px; border-radius: 20px;
        background: #eef2ff; color: #4f46e5; white-space: nowrap;
    }
    .tool-card .desc { font-size: 0.9rem; color: #444; margin: 0.5rem 0; }
    .tool-card .meta { display: flex; gap: 1.5rem; flex-wrap: wrap; font-size: 0.8rem; color: #888; }
    .tool-card .scenario-box {
        margin-top: 0.6rem; padding: 0.5rem 0.8rem; border-radius: 8px;
        background: #fafafa; font-size: 0.82rem; color: #555;
        border-left: 3px solid #4f46e5;
    }

    /* 星星 */
    .stars { color: #f59e0b; font-size: 0.9rem; }
    .stars .dim { color: #d0d0d0; }

    /* 场景按钮 */
    .scenario-active { font-weight: 700 !important; }

    /* 价格标签 */
    .price-free { color: #059669; font-weight: 600; }
    .price-paid { color: #d97706; }

    /* 响应式 */
    @media (max-width: 768px) {
        .metric-row { flex-direction: column; }
        .tool-card .header { flex-direction: column; gap: 0.3rem; }
    }
</style>
""", unsafe_allow_html=True)


# ── 数据加载 ──────────────────────────────────────────
@st.cache_data
def load_data():
    csv_path = Path(__file__).parent / "AI工具库.csv"
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    # 清理列名空格
    df.columns = df.columns.str.strip()
    # 填充空值
    df = df.fillna("")
    return df

df = load_data()

# 提取所有唯一值用于筛选
all_categories = sorted(df["分类"].unique().tolist())
all_difficulties = ["低", "中", "高"]
all_prices = df["价格（月费）"].unique().tolist()

# 三个场景列名
SCENARIOS = {
    "🏎️ 赛车模拟器": "🏎️赛车模拟器",
    "🎨 艺术空间": "🎨艺术空间",
    "💼 商业活动": "💼商业活动",
}


# ── 侧边栏 — 筛选器 ────────────────────────────────────
with st.sidebar:
    st.title("🛠️ AI 工具选型器")
    st.caption("为公司业务场景快速匹配合适的 AI 工具")
    st.divider()

    # 场景筛选（大按钮）
    st.subheader("📌 业务场景")
    selected_scenario = st.radio(
        "按场景筛选工具（单选）",
        options=["全部场景"] + list(SCENARIOS.keys()),
        index=0,
    )

    st.divider()

    # 分类筛选
    st.subheader("📂 工具分类")
    selected_categories = st.multiselect(
        "按分类筛选",
        options=all_categories,
        default=[],
        placeholder="全部类别",
    )

    # 难度筛选
    st.subheader("📊 上手难度")
    selected_difficulty = st.select_slider(
        "按难度筛选",
        options=["全部"] + all_difficulties,
        value="全部",
    )

    # 价格筛选
    st.subheader("💰 价格")
    show_free_only = st.checkbox("只显示免费工具", value=False)

    # 搜索
    st.subheader("🔍 搜索")
    search_query = st.text_input("搜索工具名或功能", placeholder="输入关键词...")

    st.divider()
    st.caption(f"共收录 {len(df)} 款 AI 工具")
    st.caption("数据更新：2026-06-13")


# ── 数据筛选 ──────────────────────────────────────────
filtered_df = df.copy()

# 场景筛选
if selected_scenario != "全部场景":
    scenario_col = SCENARIOS[selected_scenario]
    filtered_df = filtered_df[filtered_df[scenario_col].str.strip() != ""]

# 分类筛选
if selected_categories:
    filtered_df = filtered_df[filtered_df["分类"].isin(selected_categories)]

# 难度筛选
if selected_difficulty != "全部":
    filtered_df = filtered_df[filtered_df["上手难度"] == selected_difficulty]

# 免费
if show_free_only:
    filtered_df = filtered_df[filtered_df["价格（月费）"].str.contains("免费", na=False)]

# 搜索
if search_query:
    mask = (
        filtered_df["工具名"].str.contains(search_query, case=False, na=False)
        | filtered_df["功能简述"].str.contains(search_query, case=False, na=False)
        | filtered_df["分类"].str.contains(search_query, case=False, na=False)
    )
    filtered_df = filtered_df[mask]


# ── 主页面 ────────────────────────────────────────────

# ── 顶部指标 ──
st.markdown("### 📊 概览")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    with st.container(border=True):
        st.metric("收录工具", f"{len(df)} 款")
with col2:
    n_free = len(df[df["价格（月费）"].str.contains("免费", na=False)])
    with st.container(border=True):
        st.metric("免费工具", f"{n_free} 款")
with col3:
    with st.container(border=True):
        st.metric("覆盖分类", f"{len(all_categories)} 类")
with col4:
    with st.container(border=True):
        st.metric("覆盖场景", "3 个")
with col5:
    with st.container(border=True):
        st.metric("当前筛选", f"{len(filtered_df)} 款")

st.divider()

# ── 场景快捷入口（若未选择场景） ──
if selected_scenario == "全部场景":
    st.markdown("### 🎯 按业务场景快速筛选")
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.markdown("#### 🏎️ 赛车模拟器")
            st.caption("赛事战报、选手数据、成绩榜单、社媒宣发、客服咨询")
    with c2:
        with st.container(border=True):
            st.markdown("#### 🎨 艺术空间")
            st.caption("展览海报、艺术家介绍、展品讲解Bot、展览文档、数据报告")
    with c3:
        with st.container(border=True):
            st.markdown("#### 💼 商业活动")
            st.caption("活动方案、邀约函、主持串词、物料设计、合规流程、复盘报告")
    st.caption("👆 在左侧边栏选择一个场景，即可筛选该场景的专属工具")
    st.divider()

# ── 工具列表 ──
st.markdown(f"### 🧰 工具列表 ({len(filtered_df)} 款)")

if len(filtered_df) == 0:
    st.info("没有匹配的工具，请调整筛选条件。")
else:
    # 按推荐指数排序（高星在前）
    star_order = {"⭐⭐⭐⭐⭐": 5, "⭐⭐⭐⭐": 4, "⭐⭐⭐": 3}
    display_df = filtered_df.copy()
    display_df["排序"] = display_df["推荐指数"].map(star_order).fillna(0)
    display_df = display_df.sort_values("排序", ascending=False)

    for _, row in display_df.iterrows():
        name = row["工具名"]
        category = row["分类"]
        desc = row["功能简述"]
        price = row["价格（月费）"]
        rating = row["推荐指数"]
        difficulty = row["上手难度"]
        alt = row["替代工具"]
        link = row["官方链接"]
        note = row["备注"]

        # 构建三个场景的使用说明
        scenario_texts = []
        for label, col_name in SCENARIOS.items():
            val = row[col_name].strip()
            if val:
                scenario_texts.append(f"**{label}**：{val}")

        # 难度颜色
        diff_color = {"低": "#059669", "中": "#d97706", "高": "#dc2626"}
        diff_bg = {"低": "#ecfdf5", "中": "#fef3c7", "高": "#fef2f2"}
        d_color = diff_color.get(difficulty, "#888")
        d_bg = diff_bg.get(difficulty, "#f5f5f5")

        # 价格样式
        is_free = "免费" in price
        price_class = "price-free" if is_free else "price-paid"

        # ── 渲染卡片 ──
        with st.container():
            st.markdown(f"""
            <div class="tool-card">
                <div class="header">
                    <div>
                        <span class="name">{name}</span>
                        <span class="stars">{rating}</span>
                    </div>
                    <span class="category-tag">{category}</span>
                </div>
                <div class="desc">{desc}</div>
                <div class="meta">
                    <span>💰 <span class="{price_class}">{price}</span></span>
                    <span>📊 上手：<span style="color:{d_color};background:{d_bg};padding:1px 8px;border-radius:10px;">{difficulty}</span></span>
                    {f"<span>🔄 替代：{alt}</span>" if alt else ""}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # 场景使用详情（可折叠）
            if scenario_texts:
                with st.expander(f"查看「{name}」在三个业务场景中的用法", expanded=False):
                    for s_text in scenario_texts:
                        st.markdown(f"""
                        <div class="scenario-box">{s_text}</div>
                        """, unsafe_allow_html=True)
                    c1, c2 = st.columns([1, 3])
                    with c1:
                        if link:
                            st.link_button("🔗 访问官网", link)
                    with c2:
                        if note:
                            st.caption(f"📝 {note}")

            # 如果当前已选场景，高亮显示该场景的用法
            if selected_scenario != "全部场景":
                scenario_col_name = SCENARIOS[selected_scenario]
                scenario_val = row[scenario_col_name].strip()
                if scenario_val:
                    st.markdown(f"""
                    <div class="scenario-box" style="border-left-color:#f59e0b;background:#fffbeb;">
                        <strong>🎯 {selected_scenario}用法：</strong>{scenario_val}
                    </div>
                    """, unsafe_allow_html=True)

# ── 底部 ──
st.divider()
st.caption("🛠️ AI 工具选型器 · 面试作品 · 2026-06-13")
st.caption("数据持续更新中，每周新增 3-5 款工具")
