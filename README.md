# Financial Fraud Detection Using Machine Learning

A Django-based web application designed to detect financial fraud in skewed transaction data using ensemble Machine Learning algorithms (Value-at-Risk concepts, SVM, K-Nearest Neighbors, Decision Tree, Voting Classifier, and Gradient Boosting).

## Table of Contents
- [Architecture & Features](#architecture--features)
- [Machine Learning Models](#machine-learning-models)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Database Setup](#database-setup)
- [Environment Configuration](#environment-configuration)
- [Running the Server](#running-the-server)
- [License](#license)

---

## Architecture & Features

The system consists of two primary portals:

1. **Remote User Portal**:
   - Account Registration & Secure Authentication (Password Hashing).
   - Profile Management.
   - Transaction Fraud Prediction interface.

2. **Service Provider (Admin) Portal**:
   - Secure Admin Authentication.
   - View registered remote users.
   - View predicted fraud transactions and export reports to Excel.
   - Train and evaluate ML model accuracy & detection ratios.
   - Interactive visual charts (Ratio and Accuracy metrics).

---

## Machine Learning Models

The application trains and evaluates multiple classification models:
- **Linear Support Vector Classifier (LinearSVC)**
- **K-Nearest Neighbors (KNN)**
- **Decision Tree Classifier (DTC)**
- **Gradient Boosting Classifier (GBC)**
- **Ensemble Voting Classifier**

---

## Project Structure

```
Financial_Fraud_Detection/
├── Database/
│   └── financial_fraud_detection.sql   # Database schema & import script
├── financial_fraud_detection/          # Django Project Root
│   ├── Datasets.csv                    # Training dataset for ML models
│   ├── Remote_User/                    # Remote User App
│   ├── Service_Provider/               # Admin / Service Provider App
│   ├── Template/                       # HTML Templates & Static Assets
│   ├── financial_fraud_detection/      # Django Settings & URLs
│   └── manage.py                       # Django CLI entry point
├── .env.example                        # Environment variables template
├── .gitignore                          # Git ignore configuration
├── README.md                           # Project documentation
└── requirements.txt                    # Python package dependencies
```

---

## Prerequisites

- **XAMPP** (Apache + MySQL) — [Download XAMPP](https://www.apachefriends.org/)
- **Anaconda** — [Download Anaconda](https://www.anaconda.com/download)
- **Python 3.7.4** (via Anaconda conda environment)

---

## Database Setup

1. Open **XAMPP Control Panel** and start **Apache** and **MySQL**.
2. Click **Admin** next to MySQL to open **phpMyAdmin**.
3. In phpMyAdmin, click **Import**, then **Choose File**.
4. Navigate to the project folder and select:
   ```
   Database/financial_fraud_detection.sql
   ```
5. Click **Go** to import the database.

---

## Installation & Setup

Open **Anaconda Prompt** and run the following commands:

### Step 1 — Create a Conda Environment with Python 3.7.4
```bash
conda create -n p374 python==3.7.4
```
Type `Y` and press Enter when prompted.

### Step 2 — Activate the Environment
```bash
conda activate p374
```

### Step 3 — Navigate to the Project Directory
```bash
cd path\to\Financial_Fraud_Detection\financial_fraud_detection
```
*(Replace with the actual path where `manage.py` is located)*

### Step 4 — Install Required Packages
```bash
pip install "django>=3.0,<4.0"
pip install pymysql
pip install openpyxl
pip install pandas
pip install scikit-learn
pip install xlwt
pip install python-dotenv
```

> **Tip:** After each `pip install`, you can verify with `python manage.py runserver` to catch any remaining missing packages early.

---

## Environment Configuration

1. Copy `.env.example` to a new file named `.env` in the project root:
   ```bash
   copy .env.example .env
   ```
2. Open `.env` and update if needed (XAMPP MySQL defaults should work out of the box):
   ```
   DB_USER=root
   DB_PASSWORD=          # Leave blank for XAMPP default
   DB_HOST=127.0.0.1
   DB_PORT=3306
   ```

---

## Running the Server

```bash
python manage.py runserver
```

Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

**Default Admin Login:**
- Username: `Admin`
- Password: `Admin`

---

## License

This project is open-source and available under the [Apache-2.0 License](LICENSE).
