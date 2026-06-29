import { useEffect, useState } from "react";
import api from "../services/api";

export default function BudgetInsights() {

    const [data, setData] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        load();
        function handleBudgetUpdated() {
        load();
    }

    window.addEventListener(
        "budget-updated",
        handleBudgetUpdated
    );

    return () => {
        window.removeEventListener(
            "budget-updated",
            handleBudgetUpdated
        );
    };
    }, []);

    async function load() {
        try {
            const res = await api.get("/budgets/insights");
            setData(res.data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    }

    if (loading) {
        return (
            <div className="text-sm text-gray-500">
                Loading insights...
            </div>
        );
    }

    return (
       
        <div className="h-full overflow-y-auto pr-2 space-y-4">

            {data.map((item, idx) => (
                <div
                    key={idx}
                    className="bg-slate-50 border border-slate-200 rounded-xl p-4"
                >

                    <div className="flex justify-between mb-2">
                        <h3 className="font-semibold">
                            {item.category}
                        </h3>

                        <span className="text-xs text-slate-500">
                            ${item.spent} / ${item.budget}
                        </span>
                    </div>

                    <p className="text-sm text-slate-700 leading-snug">
                        🤖 {item.insight}
                    </p>

                </div>
            ))}

        </div>
    );
}