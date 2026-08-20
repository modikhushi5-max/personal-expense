import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

from expense_manager import ExpenseManager
from validators import (
    validate_date,
    validate_amount,
    validate_text,
    validate_category
)

# Page configuration
st.set_page_config(
    page_title="Personal Expense Manager",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Allowed categories matching validators.py
ALLOWED_CATEGORIES = [
    "Food",
    "Travel",
    "Shopping",
    "Education",
    "Entertainment",
    "Health",
    "Other"
]

CATEGORY_ICONS = {
    "Food": "🍔 Food",
    "Travel": "✈️ Travel",
    "Shopping": "🛍️ Shopping",
    "Education": "📚 Education",
    "Entertainment": "🎬 Entertainment",
    "Health": "🏥 Health",
    "Other": "📦 Other"
}

# Modern Premium Color Palette (Fintech style)
CATEGORY_COLORS = {
    "Food": "#F97316",           # Vibrant Coral Orange
    "Travel": "#0EA5E9",         # Bright Sky Blue
    "Shopping": "#EC4899",       # Modern Pink/Rose
    "Education": "#6366F1",      # Indigo Accent
    "Entertainment": "#8B5CF6",  # Violet Purple
    "Health": "#10B981",         # Emerald Green
    "Other": "#64748B"           # Cool Slate
}

# Custom Premium CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
    }

    /* Top App Banner */
    .hero-banner {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%);
        border-radius: 16px;
        padding: 22px 28px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(67, 56, 202, 0.25);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .hero-banner h1 {
        color: #FFFFFF !important;
        font-size: 1.85rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-banner p {
        color: #C7D2FE;
        font-size: 0.95rem;
        margin: 4px 0 0 0;
    }

    /* Modern KPI Metric Cards */
    .metric-card-wrapper {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 18px 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .metric-card-wrapper:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 24px -4px rgba(15, 23, 42, 0.09);
        border-color: #CBD5E1;
    }
    .metric-card-accent-1 { border-top: 4px solid #4F46E5; }
    .metric-card-accent-2 { border-top: 4px solid #0EA5E9; }
    .metric-card-accent-3 { border-top: 4px solid #10B981; }
    .metric-card-accent-4 { border-top: 4px solid #F59E0B; }

    .metric-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 8px;
    }
    .metric-label {
        color: #64748B;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }
    .metric-icon-box {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
    }
    .icon-bg-1 { background: #EEF2FF; }
    .icon-bg-2 { background: #E0F2FE; }
    .icon-bg-3 { background: #ECFDF5; }
    .icon-bg-4 { background: #FEF3C7; }

    .metric-amount {
        color: #0F172A;
        font-size: 1.65rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
    }

    /* Content Box */
    .content-box {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
        margin-bottom: 20px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
    }
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #E2E8F0 !important;
    }

    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }

    h1, h2, h3 {
        color: #0F172A;
        font-weight: 700;
        letter-spacing: -0.3px;
    }
</style>
""", unsafe_allow_html=True)


def format_inr(amount):
    """Format float amount into Indian Rupee currency format (₹)."""
    return f"₹{float(amount):,.2f}"


def get_dataframe(expenses):
    """Convert list of expense dicts to formatted pandas DataFrame."""
    if not expenses:
        return pd.DataFrame(columns=["Expense ID", "Date", "Category", "Description", "Amount (₹)"])
    
    df = pd.DataFrame(expenses)
    df = df.rename(columns={
        "expense_id": "Expense ID",
        "date": "Date",
        "category": "Category",
        "description": "Description",
        "amount": "Amount (₹)"
    })
    return df[["Expense ID", "Date", "Category", "Description", "Amount (₹)"]]


def create_plotly_pie_chart(category_summary):
    """Create an interactive, clean Plotly Donut/Pie Chart with clear percentages and values."""
    categories = list(category_summary.keys())
    amounts = list(category_summary.values())
    total = sum(amounts)
    
    fig = px.pie(
        names=categories,
        values=amounts,
        hole=0.52,
        color=categories,
        color_discrete_map=CATEGORY_COLORS
    )
    fig.update_traces(
        textposition='inside',
        texttemplate='<b>%{label}</b><br>%{percent:.1%}',
        textfont=dict(size=13, color="#FFFFFF", family="Plus Jakarta Sans, sans-serif"),
        hovertemplate='<b>%{label}</b><br>Amount: <b>₹%{value:,.2f}</b><br>Share: <b>%{percent:.1%}</b><extra></extra>',
        marker=dict(line=dict(color='#FFFFFF', width=2.5))
    )
    fig.update_layout(
        title=dict(
            text=f"<b>Category Spending Share</b> (Total: {format_inr(total)})",
            x=0.5,
            xanchor="center",
            font=dict(size=15, color="#1E293B", family="Plus Jakarta Sans, sans-serif")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=50, b=30, l=20, r=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(size=12, color="#334155")
        ),
        height=420
    )
    return fig


def create_plotly_bar_chart(category_summary):
    """Create an interactive Plotly Bar Chart with clear currency formatting."""
    categories = list(category_summary.keys())
    amounts = list(category_summary.values())
    
    sorted_pairs = sorted(zip(categories, amounts), key=lambda x: x[1], reverse=True)
    cats_sorted = [p[0] for p in sorted_pairs]
    amts_sorted = [p[1] for p in sorted_pairs]
    
    fig = px.bar(
        x=cats_sorted,
        y=amts_sorted,
        color=cats_sorted,
        color_discrete_map=CATEGORY_COLORS,
        text=[f"₹{a:,.0f}" for a in amts_sorted],
        labels={"x": "Category", "y": "Amount (₹)"}
    )
    fig.update_traces(
        textposition="outside",
        textfont=dict(size=12, color="#0F172A", family="Plus Jakarta Sans, sans-serif"),
        hovertemplate="<b>Category:</b> %{x}<br><b>Amount:</b> ₹%{y:,.2f}<extra></extra>",
        marker=dict(line=dict(color="#FFFFFF", width=1.5), opacity=0.92)
    )
    fig.update_layout(
        title=dict(
            text="<b>Spending Breakdown by Category (₹)</b>",
            x=0.5,
            xanchor="center",
            font=dict(size=15, color="#1E293B", family="Plus Jakarta Sans, sans-serif")
        ),
        xaxis_title=None,
        yaxis_title="Total Amount (₹)",
        yaxis=dict(
            tickprefix="₹",
            tickformat=",.0f",
            gridcolor="#F1F5F9",
            zerolinecolor="#E2E8F0"
        ),
        xaxis=dict(
            gridcolor="rgba(0,0,0,0)"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=50, b=20, l=20, r=20),
        showlegend=False,
        height=420
    )
    return fig


def main():
    manager = ExpenseManager()
    all_expenses = manager.get_all_expenses()

    # Sidebar Navigation
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 10px 0 20px 0;">
            <div style="font-size: 2.2rem; margin-bottom: 5px;">💳</div>
            <div style="font-size: 1.25rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.5px;">ExpenseMaster</div>
            <div style="font-size: 0.8rem; color: #94A3B8;">Smart Financial Analytics</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

        menu = st.radio(
            "MAIN MENU",
            [
                "📊 Dashboard",
                "➕ Add Expense",
                "📋 View Expenses",
                "🔍 Search",
                "⚡ Filter & Sort",
                "✏️ Update Expense",
                "🗑️ Delete Expense",
                "📈 Summary"
            ],
            index=0
        )

        st.markdown("---")
        total_spent, _ = manager.get_summary()
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 14px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1);">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;">Total Spending</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: #38BDF8;">{format_inr(total_spent)}</div>
            <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">Transactions: <b style="color:#FFF;">{len(all_expenses)}</b></div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        st.caption("✨ Personal Expense Manager • v2.0")

    # -------------------------------------------------------------
    # 1. DASHBOARD
    # -------------------------------------------------------------
    if menu == "📊 Dashboard":
        st.markdown("""
        <div class="hero-banner">
            <div>
                <h1>📊 Financial Dashboard</h1>
                <p>Welcome back! Here is a real-time summary of your personal finances and transactions.</p>
            </div>
            <div style="font-size: 2.5rem; opacity: 0.85;">📈</div>
        </div>
        """, unsafe_allow_html=True)

        total_spending, category_summary = manager.get_summary()
        total_txns = len(all_expenses)
        avg_expense = (total_spending / total_txns) if total_txns > 0 else 0.0
        max_expense = max([e["amount"] for e in all_expenses]) if total_txns > 0 else 0.0

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-card-wrapper metric-card-accent-1">
                <div class="metric-header">
                    <div class="metric-label">Total Spending</div>
                    <div class="metric-icon-box icon-bg-1">💰</div>
                </div>
                <div class="metric-amount">{format_inr(total_spending)}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card-wrapper metric-card-accent-2">
                <div class="metric-header">
                    <div class="metric-label">Transactions</div>
                    <div class="metric-icon-box icon-bg-2">🧾</div>
                </div>
                <div class="metric-amount">{total_txns}</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card-wrapper metric-card-accent-3">
                <div class="metric-header">
                    <div class="metric-label">Avg. Expense</div>
                    <div class="metric-icon-box icon-bg-3">⚖️</div>
                </div>
                <div class="metric-amount">{format_inr(avg_expense)}</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="metric-card-wrapper metric-card-accent-4">
                <div class="metric-header">
                    <div class="metric-label">Highest Expense</div>
                    <div class="metric-icon-box icon-bg-4">🏆</div>
                </div>
                <div class="metric-amount">{format_inr(max_expense)}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if total_txns == 0:
            st.info("💡 No expenses recorded yet. Click on **'Add Expense'** in the sidebar to get started!")
            return

        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        col_left, col_right = st.columns([1, 1])

        with col_left:
            fig_donut = create_plotly_pie_chart(category_summary)
            st.plotly_chart(fig_donut, use_container_width=True)

        with col_right:
            fig_bar = create_plotly_bar_chart(category_summary)
            st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Recent Transactions
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.subheader("⏱️ Recent Transactions")
        recent_expenses = all_expenses[-5:][::-1]
        df_recent = get_dataframe(recent_expenses)
        df_recent_display = df_recent.copy()
        df_recent_display["Amount (₹)"] = df_recent_display["Amount (₹)"].apply(format_inr)
        st.dataframe(df_recent_display, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------
    # 2. ADD EXPENSE
    # -------------------------------------------------------------
    elif menu == "➕ Add Expense":
        st.title("➕ Add New Expense")
        st.markdown("Record a new personal expense transaction into the system.")

        with st.form("add_expense_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                input_date = st.date_input("Date", value=datetime.today())
                date_str = input_date.strftime("%d-%m-%Y")
                category = st.selectbox("Category", ALLOWED_CATEGORIES, format_func=lambda c: CATEGORY_ICONS.get(c, c))
            
            with col2:
                description = st.text_input("Description", placeholder="e.g. Grocery shopping, Flight tickets, Medicine...")
                amount = st.number_input("Amount (₹)", min_value=0.0, step=50.0, format="%.2f")

            submitted = st.form_submit_button("💳 Add Expense", use_container_width=True)

            if submitted:
                if not validate_date(date_str):
                    st.error("❌ Invalid date format. Must be DD-MM-YYYY.")
                elif not validate_category(category):
                    st.error("❌ Invalid category selected.")
                elif not validate_text(description):
                    st.error("❌ Description cannot be empty or whitespace only.")
                elif not validate_amount(amount):
                    st.error("❌ Amount must be a positive number greater than 0.")
                else:
                    expense_id = manager.add_expense(
                        date=date_str,
                        category=category.title(),
                        description=description.strip(),
                        amount=amount
                    )
                    st.success(f"✓ Expense added successfully! Generated ID: **{expense_id}**")
                    st.balloons()

    # -------------------------------------------------------------
    # 3. VIEW EXPENSES
    # -------------------------------------------------------------
    elif menu == "📋 View Expenses":
        st.title("📋 View All Expenses")
        st.markdown("Complete list of all recorded expenses.")

        if not all_expenses:
            st.info("No expenses recorded yet.")
        else:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"Showing **{len(all_expenses)}** recorded transaction(s)")
            with col2:
                df = get_dataframe(all_expenses)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name="expenses.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            df_display = df.copy()
            df_display["Amount (₹)"] = df_display["Amount (₹)"].apply(format_inr)
            st.dataframe(df_display, use_container_width=True, hide_index=True)

    # -------------------------------------------------------------
    # 4. SEARCH
    # -------------------------------------------------------------
    elif menu == "🔍 Search":
        st.title("🔍 Search Expenses")
        st.markdown("Search transactions by description keywords or category names.")

        search_query = st.text_input("Enter search keyword", placeholder="e.g. food, recharge, phone, medical...")

        if search_query.strip():
            results = manager.search_expenses(search_query.strip())
            st.markdown(f"Found **{len(results)}** matching result(s) for query: `\"{search_query}\"`")

            if results:
                df_results = get_dataframe(results)
                df_results_display = df_results.copy()
                df_results_display["Amount (₹)"] = df_results_display["Amount (₹)"].apply(format_inr)
                st.dataframe(df_results_display, use_container_width=True, hide_index=True)
            else:
                st.warning("No expenses match your search query.")
        else:
            st.info("Type a search keyword above to search through your expenses.")

    # -------------------------------------------------------------
    # 5. FILTER & SORT
    # -------------------------------------------------------------
    elif menu == "⚡ Filter & Sort":
        st.title("⚡ Filter & Sort Expenses")
        st.markdown("Filter transactions by category or sort them by amount.")

        col1, col2 = st.columns(2)
        with col1:
            category_filter = st.selectbox(
                "Filter by Category",
                ["All Categories"] + ALLOWED_CATEGORIES,
                format_func=lambda c: "🌐 All Categories" if c == "All Categories" else CATEGORY_ICONS.get(c, c)
            )

        with col2:
            sort_option = st.selectbox(
                "Sort by Amount",
                [
                    "Default Order",
                    "Lowest to Highest (Ascending)",
                    "Highest to Lowest (Descending)"
                ]
            )

        if category_filter != "All Categories":
            filtered_list = manager.filter_by_category(category_filter)
        else:
            filtered_list = manager.get_all_expenses()

        if sort_option == "Lowest to Highest (Ascending)":
            if category_filter == "All Categories":
                display_list = manager.sort_by_amount(descending=False)
            else:
                display_list = sorted(filtered_list, key=lambda x: x["amount"], reverse=False)
        elif sort_option == "Highest to Lowest (Descending)":
            if category_filter == "All Categories":
                display_list = manager.sort_by_amount(descending=True)
            else:
                display_list = sorted(filtered_list, key=lambda x: x["amount"], reverse=True)
        else:
            display_list = filtered_list

        st.markdown(f"Displaying **{len(display_list)}** transaction(s)")

        if display_list:
            df_filtered = get_dataframe(display_list)
            df_filtered_display = df_filtered.copy()
            df_filtered_display["Amount (₹)"] = df_filtered_display["Amount (₹)"].apply(format_inr)
            st.dataframe(df_filtered_display, use_container_width=True, hide_index=True)
        else:
            st.warning("No transactions found for the selected filter criteria.")

    # -------------------------------------------------------------
    # 6. UPDATE EXPENSE
    # -------------------------------------------------------------
    elif menu == "✏️ Update Expense":
        st.title("✏️ Update Expense")
        st.markdown("Modify the details of an existing expense record.")

        if not all_expenses:
            st.info("No expenses available to update.")
        else:
            expense_options = {
                f"{e['expense_id']} | {e['date']} | {e['category']} | {e['description']} ({format_inr(e['amount'])})": e["expense_id"]
                for e in all_expenses
            }
            
            selected_label = st.selectbox("Select Expense to Update", list(expense_options.keys()))
            selected_id = expense_options[selected_label]
            
            current_expense = next(e for e in all_expenses if e["expense_id"] == selected_id)

            try:
                current_date_obj = datetime.strptime(current_expense["date"], "%d-%m-%Y").date()
            except ValueError:
                current_date_obj = datetime.today().date()

            current_cat_index = (
                ALLOWED_CATEGORIES.index(current_expense["category"])
                if current_expense["category"] in ALLOWED_CATEGORIES
                else 0
            )

            with st.form("update_expense_form"):
                col1, col2 = st.columns(2)
                with col1:
                    new_date = st.date_input("New Date", value=current_date_obj)
                    new_date_str = new_date.strftime("%d-%m-%Y")
                    new_category = st.selectbox(
                        "New Category",
                        ALLOWED_CATEGORIES,
                        index=current_cat_index,
                        format_func=lambda c: CATEGORY_ICONS.get(c, c)
                    )
                with col2:
                    new_description = st.text_input("New Description", value=current_expense["description"])
                    new_amount = st.number_input(
                        "New Amount (₹)",
                        min_value=0.0,
                        value=float(current_expense["amount"]),
                        step=50.0,
                        format="%.2f"
                    )

                update_submitted = st.form_submit_button("💾 Save Changes", use_container_width=True)

                if update_submitted:
                    if not validate_date(new_date_str):
                        st.error("❌ Invalid date format.")
                    elif not validate_category(new_category):
                        st.error("❌ Invalid category.")
                    elif not validate_text(new_description):
                        st.error("❌ Description cannot be empty.")
                    elif not validate_amount(new_amount):
                        st.error("❌ Amount must be greater than 0.")
                    else:
                        success = manager.update_expense(
                            expense_id=selected_id,
                            date=new_date_str,
                            category=new_category.title(),
                            description=new_description.strip(),
                            amount=new_amount
                        )
                        if success:
                            st.success(f"✓ Expense **{selected_id}** updated successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to update expense. Expense ID not found.")

    # -------------------------------------------------------------
    # 7. DELETE EXPENSE
    # -------------------------------------------------------------
    elif menu == "🗑️ Delete Expense":
        st.title("🗑️ Delete Expense")
        st.markdown("Remove an unwanted expense entry from the database.")

        if not all_expenses:
            st.info("No expenses available to delete.")
        else:
            expense_options = {
                f"{e['expense_id']} | {e['date']} | {e['category']} | {e['description']} ({format_inr(e['amount'])})": e["expense_id"]
                for e in all_expenses
            }

            selected_label = st.selectbox("Select Expense to Delete", list(expense_options.keys()))
            selected_id = expense_options[selected_label]
            target_expense = next(e for e in all_expenses if e["expense_id"] == selected_id)

            st.warning(
                f"**Selected Record:**\n\n"
                f"- **ID:** `{target_expense['expense_id']}`\n"
                f"- **Date:** `{target_expense['date']}`\n"
                f"- **Category:** `{target_expense['category']}`\n"
                f"- **Description:** `{target_expense['description']}`\n"
                f"- **Amount:** `{format_inr(target_expense['amount'])}`"
            )

            confirm = st.checkbox("I confirm that I want to delete this expense record.")

            if st.button("🗑️ Permanently Delete Expense", type="primary", disabled=not confirm):
                success = manager.delete_expense(selected_id)
                if success:
                    st.success(f"✓ Expense **{selected_id}** deleted successfully.")
                    st.rerun()
                else:
                    st.error("❌ Failed to delete expense. Expense ID not found.")

    # -------------------------------------------------------------
    # 8. SUMMARY & ANALYTICS
    # -------------------------------------------------------------
    elif menu == "📈 Summary":
        st.title("📈 Expense Summary & Analytics")
        st.markdown("In-depth spending breakdown and statistics.")

        total_spending, category_summary = manager.get_summary()
        total_txns = len(all_expenses)

        if total_txns == 0:
            st.info("No expenses available for summary.")
            return

        avg_expense = total_spending / total_txns
        sorted_by_amt = sorted(all_expenses, key=lambda x: x["amount"])
        lowest_expense = sorted_by_amt[0]
        highest_expense = sorted_by_amt[-1]

        # Key Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Spending", format_inr(total_spending))
            st.metric("Number of Expenses", f"{total_txns}")
        with col2:
            st.metric("Average Expense", format_inr(avg_expense))
            st.metric("Highest Expense", f"{format_inr(highest_expense['amount'])} ({highest_expense['category']})")
        with col3:
            st.metric("Lowest Expense", f"{format_inr(lowest_expense['amount'])} ({lowest_expense['category']})")
            top_category = max(category_summary.items(), key=lambda x: x[1])[0] if category_summary else "N/A"
            st.metric("Top Spending Category", top_category)

        st.markdown("---")
        st.subheader("Category-wise Spending Breakdown")

        # Create Category breakdown DataFrame
        cat_data = []
        for cat, amt in category_summary.items():
            count = len([e for e in all_expenses if e["category"].lower() == cat.lower()])
            pct = (amt / total_spending * 100) if total_spending > 0 else 0
            cat_data.append({
                "Category": cat,
                "Transactions": count,
                "Total Amount (₹)": format_inr(amt),
                "Share (%)": f"{pct:.1f}%",
                "_raw_amt": amt
            })

        df_cat = pd.DataFrame(cat_data).sort_values(by="_raw_amt", ascending=False)
        st.dataframe(df_cat[["Category", "Transactions", "Total Amount (₹)", "Share (%)"]], use_container_width=True, hide_index=True)

        # Plotly Interactive Charts
        st.markdown("---")
        col_c1, col_c2 = st.columns(2)

        with col_c1:
            fig1 = create_plotly_pie_chart(category_summary)
            st.plotly_chart(fig1, use_container_width=True)

        with col_c2:
            fig2 = create_plotly_bar_chart(category_summary)
            st.plotly_chart(fig2, use_container_width=True)


if __name__ == "__main__":
    main()
