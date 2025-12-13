# 📊 Telecom Customer Churn Prediction

## 📌 Overview
Customer churn is a major challenge in the telecom industry, as retaining existing customers is more cost-effective than acquiring new ones.  
This project builds a **machine learning–based churn prediction system** to identify customers who are likely to discontinue services, helping telecom providers take proactive retention measures.

The notebook implements a complete **end-to-end ML pipeline**, including data exploration, preprocessing, class-imbalance handling, model training, and evaluation.

---

## 📂 Dataset
- **Dataset Name:** Telco Customer Churn  
- **File Used:** `WA_Fn-UseC_-Telco-Customer-Churn.csv`  
- **Description:**  
  Contains customer demographic details, account information, service usage patterns, and a target variable (`Churn`) indicating whether a customer has left the service.

---

## ⚙️ Technologies Used
- **Programming Language:** Python  
- **Libraries & Tools:**
  - Pandas, NumPy  
  - Matplotlib, Seaborn  
  - scikit-learn  
  - imbalanced-learn (SMOTE / SMOTEENN)  
  - Jupyter Notebook  

---

## 🔍 Project Workflow

### 1️⃣ Data Exploration
- Loaded and inspected the dataset  
- Checked for missing values and data types  
- Analyzed churn distribution to identify class imbalance  

---

### 2️⃣ Data Preprocessing
- Encoded categorical variables using **one-hot encoding**  
- Converted the target variable (`Churn`) into numerical form    

---

### 3️⃣ Exploratory Data Analysis (EDA)
- Studied churn behavior across:
  - Monthly charges  
  - Contract type  
  - Tenure  
  - Payment method  
- Used count plots and KDE plots for visualization  

---

### 4️⃣ Handling Class Imbalance
- Identified imbalance in churn vs. non-churn classes  
- Applied **SMOTE / SMOTEENN** to balance the dataset  
- Improved model recall for churned customers  

---

### 5️⃣ Model Training
Trained and evaluated multiple machine learning models: 
- Decision Tree  
- Random Forest   

---

### 6️⃣ Model Evaluation
Models were evaluated using:
- Accuracy  
- Precision  
- Recall  
- F1-Score  
- Confusion Matrix  

> Special focus was given to **Recall and F1-Score**, as missing a churned customer is costly.

---

## 📈 Key Insights
- Ensemble models performed better on imbalanced data  
- SMOTE-based resampling improved churn detection  
- Tenure, monthly charges, and contract type were strong churn indicators  

---
