import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";
import BudgetInsights from "../components/BudgetInsights";

export default function Budgets() {

    const [budgets, setBudgets] = useState<any[]>([]);
    const [category, setCategory] = useState("");
    const [limit, setLimit] = useState("");

    useEffect(() => {
        loadBudgets();
    }, []);

    async function loadBudgets() {
        const response = await api.get("/budgets");
        setBudgets(response.data);
    }

    async function saveBudget() {
        await api.post("/budgets", {
            category,
            monthly_limit: limit
        });

        loadBudgets();
        setCategory("");
        setLimit("");
        window.dispatchEvent(new CustomEvent("budget-updated")
    );
    }

    return (
        <div className="max-w-6xl mx-auto px-6 py-8">

            {/* HEADER */}
            <div className="flex items-center justify-between mb-8">
                <h1 className="text-3xl font-bold">
                    Monthly Budgets
                </h1>

                <Link
                    to="/"
                    className="px-4 py-2 rounded-lg border border-slate-300 hover:bg-slate-100 transition"
                >
                    ← Back to Dashboard
                </Link>
            </div>


            {/* TOP GRID */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-10">


                {/* LEFT: CREATE BUDGET */}
                <div className="bg-white border border-slate-200 rounded-2xl shadow-sm h-[520px] p-6 flex flex-col">

                    <h2 className="text-xl font-semibold mb-4 text-center">
                        Create Monthly Budget
                    </h2>

                    <div className="flex-1 overflow-y-auto space-y-4">

                        <select
                            value={category}
                            onChange={(e) => setCategory(e.target.value)}
                            className="w-full border p-3 rounded-lg bg-white"
                        >
                            <option value="">Select category</option>
                            <option value="Food">Food</option>
                            <option value="Fuel">Fuel</option>
                            <option value="Shopping">Shopping</option>
                            <option value="Groceries">Groceries</option>
                            <option value="Travel">Travel</option>
                            <option value="Entertainment">Entertainment</option>
                            <option value="Lifestyle">Lifestyle</option>
                            <option value="Utilities">Utilities</option>
                            <option value="Healthcare">Healthcare</option>
                            <option value="Other">Other</option>
                        </select>

                        <input
                            placeholder="Monthly limit (e.g. 500)"
                            value={limit}
                            onChange={(e) => setLimit(e.target.value)}
                            className="w-full border p-3 rounded-lg"
                        />

                        <button
                            onClick={saveBudget}
                            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-medium"
                        >
                            Save Budget
                        </button>

                    </div>
                </div>


                {/* RIGHT: AI INSIGHTS */}
                <div className="bg-white border border-slate-200 rounded-2xl shadow-sm h-[520px] overflow-y-auto  flex flex-col">

                    <h2 className="text-xl font-semibold mb-4 sticky top-0 z-50 bg-white px-6 pt-6 pb-4 -mt-px">
                        🤖 AI Budget Insights
                    </h2>

                    {/* IMPORTANT: NO SCROLL HERE */}
                    <div className="flex-1 px-6">
                        <BudgetInsights />
                    </div>

                </div>

            </div>


            {/* BOTTOM: BUDGET LIST */}
            <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">

                <div className="p-5 border-b font-semibold text-lg">
                    Existing Budgets
                </div>

                {budgets.length === 0 ? (
                    <div className="p-8 text-center text-slate-500">
                        No budgets created yet.
                    </div>
                ) : (
                    budgets.map((budget: any) => (
                        <div
                            key={budget.id}
                            className="p-4 border-b flex justify-between items-center"
                        >
                            <span className="font-medium">
                                {budget.category}
                            </span>

                            <span className="text-blue-600 font-semibold">
                                ${budget.monthly_limit}
                            </span>
                        </div>
                    ))
                )}

            </div>

        </div>
    );
}