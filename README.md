# Financial Fraud Detection Using Machine Learning

A Django-based web application designed to detect financial fraud in skewed transaction data using ensemble Machine Learning algorithms (Value-at-Risk concepts, SVM, K-Nearest Neighbors, Decision Tree, Voting Classifier, and Gradient Boosting).

## Table of Contents
- [Architecture & Features](#architecture--features)
- [Machine Learning Models](#machine-learning-models)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Environment Configuration](#environment-configuration)
- [Database Setup](#database-setup)
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
│   └── financial_fraud_detection.sql   # Database dump script
├── financial_fraud_detection/          # Django Project Root
│   ├── Datasets.csv                    # Training dataset
│   ├── Remote_User/                    # Remote User App
│   ├── Service_Provider/               # Admin App
│   ├── Template/                       # HTML & Static Templates
│   ├── financial_fraud_detection/      # Django Settings & URLs
│   └── manage.py                       # Django CLI tool
├── .env.example                        # Environment variables template
├── .gitignore                          # Git ignore configuration
├── README.md                           # Documentation
└── requirements.txt                    # Project dependencies
```

---

## Prerequisites

- **Python**: 3.7 or higher
- **MySQL / MariaDB**: Server installed locally (or XAMPP/WAMP)

---

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Financial_Fraud_Detection.git
   cd Financial_Fraud_Detection
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Environment Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Update `.env` with your actual secret key, admin credentials, and database settings.

---

## Database Setup

1. Create a MySQL database named `financial_fraud_detection`:
   ```sql
   CREATE DATABASE financial_fraud_detection;
   ```
2. Import the provided SQL dump:
   ```bash
   mysql -u root -p financial_fraud_detection < Database/financial_fraud_detection.sql
   ```
3. Run Django migrations (if needed):
   ```bash
   cd financial_fraud_detection
   python manage.py migrate
   ```

---

## Running the Server

1. Navigate to the Django application directory:
   ```bash
   cd financial_fraud_detection
   ```
2. Start the development server:
   ```bash
   python manage.py runserver
   ```
3. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000/
   ```

---

## License

This project is open-source and available under the [MIT License](LICENSE).
