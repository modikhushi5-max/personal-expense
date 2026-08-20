# 💰 Personal Expense Manager (Smart Expense Analyzer)

A modern, full-featured **Personal Expense Manager** providing both an interactive **Streamlit Web UI** and a terminal-based **CLI application**, built with a modular, tested Python architecture and lightweight local JSON persistence.

---

## 📌 1. Problem Statement

In daily life, individuals struggle to monitor their day-to-day expenditures across multiple categories such as food, travel, shopping, utilities, and healthcare. 

- **Lack of Visibility**: Without a structured tracking tool, people often experience unexpected budget deficits at the end of the month.
- **Cumbersome Manual Logging**: Traditional paper ledgers or raw spreadsheets are inconvenient and prone to errors.
- **Complex & Paid Alternatives**: Commercial finance apps often require paid subscriptions, mandatory cloud account creation, or compromise privacy by reading sensitive SMS data.

There is a strong need for a **free, privacy-friendly, easy-to-use, and visually rich personal expense tracking solution** with zero setup friction.

---

## 🎯 2. Objectives

- **Effortless Expense Logging**: Allow users to record daily transactions quickly with date, category, description, and amount.
- **Zero-Cost & Local Persistence**: Store data securely on the local system using standard JSON without external database dependencies.
- **Strict Data Validation**: Prevent corrupt or invalid data entries (such as invalid dates, negative amounts, or blank descriptions).
- **Interactive Visual Analytics**: Deliver intuitive visual representations (Plotly Donut & Bar charts, KPI metric cards) to help users make smarter spending decisions.
- **Dual Interface**: Offer a modern Web Dashboard (Streamlit) for visual tracking and a lightweight Terminal CLI (main.py) for command-line users.

---

## 🌟 3. Key Features

### 📊 Modern Financial Dashboard
- **4 KPI Metric Cards**: Total Spending, Transaction Count, Average Expense, and Highest Single Expense.
- **Interactive Plotly Visualizations**:
  - **Category Spending Donut Chart**: Clear percentage shares (%), hover tooltips, and center total.
  - **Category Distribution Bar Chart**: Exact amount labels in Indian Rupees (₹) sorted by highest spending.
- **Recent Transactions Ledger**: Instant view of the 5 most recent transactions.

### ➕ Add Expense
- Clean form with calendar date selector (DD-MM-YYYY), standardized category dropdown, description input, and amount field.
- Auto-generates sequential unique IDs (E001, E002, ...).
- Real-time validation checks before saving.

### 📋 View Expenses & CSV Export
- Clean tabular view of all recorded expenses.
- Currency formatted in Indian Rupees (₹1,250.00).
- One-click **CSV Download** (expenses.csv) for external spreadsheet use.

### 🔍 Search Expenses
- Case-insensitive keyword search matching across descriptions and category names.
- Instant search results with matching item count.

### ⚡ Filter & Sort
- Filter transactions by category (Food, Travel, Shopping, Education, Entertainment, Health, Other).
- Sort transactions by monetary amount in **Ascending** (Lowest to Highest) or **Descending** (Highest to Lowest) order.

### ✏️ Update Expense
- Select any existing transaction from a dropdown.
- Form pre-populates with existing data for easy editing.
- Fully validated updates applied directly through the backend.

### 🗑️ Delete Expense
- Select any transaction to view a preview card.
- Requires explicit confirmation to prevent accidental deletion.

### 📈 Summary & Analytics
- Complete aggregate metrics: Total Spending, Transaction Count, Average Expense, Top Spending Category, and Highest/Lowest transactions.
- Category breakdown table displaying transaction counts, amount totals, and percentage shares (%).

---

## 🛠️ 4. Technologies Used

| Technology | Purpose |
|---|---|
| **Python 3.9+** | Core programming language |
| **Streamlit** | Modern Web UI framework |
| **Plotly Express & Graph Objects** | Interactive charts, donut distributions, and bar graphs |
| **Pandas** | Data structuring, filtering, and CSV export |
| **Matplotlib** | Supplementary plotting utility |
| **JSON** | Local persistent file storage (data/expenses.json) |
| **Unittest & Mock** | Automated testing and I/O isolation |

---

## ⚙️ 5. Installation & Setup Instructions

### Prerequisites
- Python 3.9 or higher installed.

### Setup Steps
1. Open your terminal or PowerShell and navigate to the project directory:
   `ash
   cd C:\python\smart-expense
   `
2. (Optional) Create and activate a virtual environment:
   `ash
   python -m venv venv
   .\venv\Scripts\activate
   `
3. Install required dependencies:
   `ash
   pip install -r requirements.txt
   `

---

## 🚀 6. How to Run the Project

### Option A: Launch Streamlit Web UI (Recommended)
`ash
python -m streamlit run app.py
`
*The web dashboard will automatically open in your default browser at **http://localhost:8501**.*

### Option B: Launch Terminal CLI Menu
`ash
python main.py
`

---

## 📁 7. Project Structure

`
smart-expense/
├── app.py                      # Streamlit Web UI Application (Frontend)
├── main.py                     # Terminal Command-Line Interface (CLI)
├── expense_manager.py          # Central ExpenseManager Business Logic
├── models.py                   # Expense Data Model (OOP Class)
├── storage.py                  # Local JSON Storage & Persistence Layer
├── validators.py               # Input Validation Module
├── requirements.txt            # Python Project Dependencies
├── README.md                   # Complete Project Documentation
├── PROJECT_REPORT.md           # In-Depth Technical Project Report
│
├── .streamlit/
│   └── config.toml             # Custom Streamlit Theme Configuration
│
├── data/
│   └── expenses.json           # JSON Database File
│
├── tests/
│   └── test_expense_manager.py # Automated Unit Test Suite
│
└── screenshots/                # Application UI Screenshots
    ├── add_expense.png
    ├── expense_list.png
    ├── search.png
    └── summary.png
`

---

## 🧪 8. Testing Details

Automated unit tests are implemented using Python's standard unittest framework with unittest.mock to mock disk read/write operations.

### Run All Unit Tests:
`ash
python -m unittest tests.test_expense_manager -v
`

### Test Coverage:
1. 	est_add_expense: Validates record insertion and sequential ID generation (E001).
2. 	est_search_expense: Validates case-insensitive keyword search on description and category.
3. 	est_filter_by_category: Tests exact category filtering.
4. 	est_sort_by_amount: Tests ascending and descending order sorting.
5. 	est_update_expense: Validates in-place field updates.
6. 	est_delete_expense: Validates successful deletion of existing records.
7. 	est_get_summary: Verifies total calculation and category breakdown dictionaries.
8. 	est_delete_invalid_expense: Asserts graceful handling when deleting non-existent IDs.
9. 	est_update_invalid_expense: Asserts graceful handling when updating non-existent IDs.
10. 	est_empty_expenses: Validates correct responses when no expenses exist.

**Test Suite Result: Ran 10 tests in 0.008s -> OK (100% Passed)**

---

## ⚠️ 9. Limitations

- **Single-User Scope**: Designed for personal local usage without multi-user authentication.
- **File-Based Storage**: JSON storage is optimal for thousands of transactions but not designed for enterprise-scale datasets.
- **Single Currency**: Default currency is Indian Rupee (₹). Multi-currency conversion is not built-in.

---

## 🔮 10. Future Improvements

- **Monthly Budget Targets**: Set spending limits per category and receive alert badges when approaching thresholds.
- **Income & Savings Tracking**: Record income streams to calculate net savings rate.
- **Receipt OCR / Image Upload**: Scan physical receipts to auto-extract transaction details.
- **PDF Report Export**: Generate downloadable monthly financial summary PDF reports.
- **Database Migration**: Optional SQLite backend support for larger transaction volumes.

---

## 📄 License
Open source and completely free for personal and educational use.
