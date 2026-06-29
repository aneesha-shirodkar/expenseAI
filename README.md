#  AI Expense Tracker

An AI-powered personal finance application that helps users track expenses, automate receipt processing, manage budgets, and receive intelligent financial insights using Azure OpenAI.

##  Features

###  Smart Receipt Processing

* Upload receipt images and automatically extract purchase information.
* AI-powered expense categorization (Groceries, Food, Travel, Shopping, Utilities, etc.).
* Duplicate receipt detection to prevent accidental double entries.
* View the original receipt content directly from the expense table.

### 📊 Interactive Dashboard

#### Spending Analytics

* Category-based spending pie chart.
* Monthly spending trend chart.
* Month and category filters across the dashboard.

#### Ask Your Expenses

Natural-language queries such as:

* "How much did I spend at Costco?"
* "How much did I spend on groceries this month?"
* "What was my largest expense in June?"

The system returns aggregated results using AI-assisted analysis.

### 🔍 Expense Management

* Search and filter expenses by:

  * Month
  * Category
  * Date
* View receipt details directly from the expense table.
* Access AI-powered receipt question answering from each expense.

### 🤖 Receipt Question & Answer

Users can ask questions about any uploaded receipt, including:

* "How much tax was charged?"
* "Did I buy any dairy products?"
* "What was the total spent on beverages?"
* "When was this purchase made?"

The AI analyzes the extracted receipt content and provides contextual answers.

### 📈 Spending Insights

* Generates concise AI insights comparing current month's spending against previous months.
* Identifies increases and decreases in category spending.
* Provides actionable recommendations in 2–3 sentences.

Example:

> "Your grocery spending increased by 18% compared to last month. Most of the increase came from bulk purchases. Consider reviewing recurring purchases to stay within budget."

### 💸 Budget Tracking

* Set monthly budgets for individual categories.
* Track budget usage and remaining balance.
* Receive AI-generated advice based on:

  * Budget amount
  * Current spending
  * Remaining days in the month
  * Overspending risk

Example:

> "You have used 90% of your Food budget with 8 days remaining. At your current spending rate, you may exceed your budget by approximately $65."

### 📧 Gmail Integration

* Secure Gmail OAuth authentication.
* Import receipts directly from email.
* Automatic synchronization of new receipt emails.
* Displays:

  * Number of emails scanned
  * Receipts imported
  * Duplicate receipts detected
  * Last synchronization status



---

## 🏗️ Tech Stack

### Frontend

* React
* TypeScript
* Tailwind CSS
* React Router
* Axios
* Chart.js

### Backend

* FastAPI
* SQLAlchemy
* PostgreSQL

### AI & Cloud

* Azure OpenAI - model gpt-4.1-mini
* Prompt Engineering
* OCR-based receipt extraction - Document intelligence
* Gmail OAuth 2.0

---

## 💡 Key Technical Highlights

* Full-stack application architecture.
* Real-world Azure OpenAI integration.
* AI-powered financial recommendations.
* Natural-language querying over expense data.
* Receipt understanding and question answering.
* Duplicate detection mechanisms.
* Modular service-based backend design.
* Responsive dashboard interface.

---

## Future Improvements

* Real-time notifications for overspending.
* Predictive budget forecasting.
* Recurring expense detection.
* Multi-user support.
* Mobile application integration.
* Background Gmail synchronization jobs

## Future Improvement: Architecture Migration & Automation

* Cloud Migration: Transition the current local client and backend infrastructure to Azure Web Apps to ensure higher scalability and availability.
* Database Cloud Hosting: Migrate the local PostgreSQL database to a fully managed Azure instance.
* Automated Email Syncing:Implement Azure Functions as serverless background workers to automatically parse and sync incoming Gmail receipts directly to the cloud database.

### 📚 Documentation

You will find additional project resources in the docs/ folder, including:

* Demo video showcasing end-to-end walkthrough of the application.
* Screenshots of the dashboard, expense management, budget insights, Gmail integration, and AI insights.
* System architecture diagram illustrating the interaction between the frontend, backend, database, Gmail services, and Azure OpenAI components.
