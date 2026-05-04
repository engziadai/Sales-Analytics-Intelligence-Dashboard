
# 📊 Sales Analytics Intelligence Dashboard

A professional end-to-end data engineering and visualization project. This repository contains a complete pipeline to clean raw sales data and host an interactive intelligence dashboard using Streamlit.

## 🚀 Live Demo
Check out the live dashboard here: [Live Dashboard Link](https://sales-analytics-intelligence-dashboard-pygr5mpwhgwjqu7appafel.streamlit.app/)

## 📁 Repository Structure
- `dashboard.py`: The main Streamlit application script.
- `cleaning.py`: Python script for data preprocessing and standardization.
- `Dashboard_Dataset_After.csv`: Cleaned dataset used by the dashboard.
- `requirements.txt`: Essential libraries for Streamlit Cloud deployment.
- `README.md`: Project documentation and setup guide.

## 💻 Local Setup & Installation

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/your-username/Sales-Analytics-Intelligence-Dashboard.git](https://github.com/your-username/Sales-Analytics-Intelligence-Dashboard.git)
   cd Sales-Analytics-Intelligence-Dashboard
   ```

2. **Create a Virtual Environment** (Optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Data Path**:
   Ensure `Dashboard_Dataset_After.csv` is in the root directory before launching.

5. **Run the Dashboard**:
   ```bash
   streamlit run dashboard.py
   ```

## 🛠️ Technologies Used
- **Python 3.10+**
- **Pandas**: For data manipulation and cleaning.
- **Streamlit**: For the interactive web interface.
- **Altair**: For advanced data visualizations.
- **Plotly**: For supplemental interactive charting.
