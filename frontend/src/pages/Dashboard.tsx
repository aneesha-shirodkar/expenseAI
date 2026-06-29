import { useEffect, useState } from "react";
import api from "../services/api";

import StatsCards from "../components/StatsCards";
import CategoryChart from "../components/CategoryChart";
import ExpenseTable from "../components/ExpenseTable";
import UploadReceipt from "./UploadReceipt";
import FilterBar from "../components/FilterBar";
import MonthlyTrendChart from "../components/MonthlyTrendChart";
import InsightsCard from "../components/InsightsCard";
import ChatWidget from "../components/ChatWidget";
import GmailConnect from "../components/GmailConnect";
import Sidebar from "../components/Sidebar";


type filter = { month?: string; category?: string; };
export default function Dashboard() {

  const [stats, setStats] = useState(null);
  const [summary, setSummary] = useState(null);
  const [expenses, setExpenses] = useState([]);
  const [month, setMonth] = useState("");
const [category, setCategory] = useState("");
const [trendData, setTrendData] = useState([]);
const [insights, setInsights] = useState<string[]>([]);

 useEffect(() => {
  loadDashboard();
}, [month, category]);

useEffect(() => {


    function handleReceiptsSynced() {
        loadDashboard();
    }

    window.addEventListener(
        "receipts-synced",
        handleReceiptsSynced
    );

    return () => {
        window.removeEventListener(
            "receipts-synced",
            handleReceiptsSynced
        );
    };

}, []);


  async function loadDashboard() {

  const params: filter = {};

  if (month) {
    params.month = month;
  }

  if (category) {
    params.category = category;
  }

  const currentYear = new Date().getFullYear();

  const [
    statsRes,
    summaryRes,
    expensesRes,
    trendRes,
    insightsRes
  ] = await Promise.all([
    api.get("/expenses/stats", { params }),
    api.get("/expenses/summary", { params }),
    api.get("/expenses", { params }),
    api.get("/expenses/monthly-trend",{params:{year: currentYear}}),
    api.get("/ai/insights")
  ]);

  setStats(statsRes.data);
  setSummary(summaryRes.data);
  setExpenses(expensesRes.data);
  setTrendData(trendRes.data);
  console.log(insightsRes.data.insights, insightsRes)
  setInsights(insightsRes.data.insights);

  

}
  

  return (

     
     <div className="flex bg-slate-100 min-h-screen ">

    <Sidebar  gmailConnected={true} />

        <main
            className="
                flex-1
                p-8
            "
        >
       <FilterBar
        month={month}
        setMonth={setMonth}
        category={category}
        setCategory={setCategory}
      />

      {stats &&
        <StatsCards
          stats={stats}
        />
      }

    <div className="grid md:grid-cols-2 gap-6">

        <UploadReceipt  onUploadSuccess={loadDashboard}/>
        <div className="grid md:grid-cols-2 gap-6 mt-6">
            {summary &&
             <CategoryChart summary={summary}/>
            }
        </div>
    </div>

    <MonthlyTrendChart data={trendData}/>

    <InsightsCard insights={insights}/>
    <ChatWidget />
     <div className="mt-8"><ExpenseTable expenses={expenses} /></div>
      </main>
    </div>
  );
}

   {/*  <div className="p-8">
       <div className="grid md:grid-cols-2 gap-6">
        <h1 className="text-3xl font-bold mt-4 mb-6">
        AI Expense Tracker 
        </h1>
        <div className="grid md:grid-cols-1 gap-6 ">
             <GmailConnect/>

        </div>
    </div> */}