import { useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom"; // 1. Added Link and useNavigate
import api from "../services/api";
import ReceiptExplorer from "../components/ReceiptExplorer";

export default function ReceiptDetails() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [receipt, setReceipt] = useState<any>(null);

    useEffect(() => {
        loadReceipt();
    }, [id]); // Added dependency to re-run if URL changes

    async function loadReceipt() {
        const response = await api.get(`/expenses/${id}`);
        setReceipt(response.data);
    }

    if (!receipt) return <p className="p-8 text-center text-slate-500">Loading...</p>;

    return (
        <div className="max-w-6xl mx-auto p-8 relative">
            
            {/* Top Bar Header Area with Back button and Close button */}
            <div className="flex items-center justify-between mb-6">
                <Link 
                    to="/" 
                    className="inline-flex items-center gap-2 text-sm font-medium text-slate-600 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 px-4 py-2 rounded-lg transition-colors"
                >
                    ← Back to Dashboard
                </Link>
            </div>

            <h1 className="text-3xl font-bold text-slate-800">
                {receipt.merchant_name}
            </h1>

            {/* Details Box */}
            <div className="bg-white p-6 rounded-xl shadow border border-slate-100 mt-6 space-y-3">
                <p className="text-slate-600 text-sm">
                    <strong className="text-slate-800 font-semibold">Amount:</strong> ${receipt.amount}
                </p>
                <p className="text-slate-600 text-sm">
                    <strong className="text-slate-800 font-semibold">Category:</strong> {receipt.category}
                </p>
                <p className="text-slate-600 text-sm">
                    <strong className="text-slate-800 font-semibold">Date:</strong> {receipt.expense_date}
                </p>
            </div>

            {/* OCR Box - Height capped at 200px */}
            <div className="bg-white p-6 rounded-xl shadow border border-slate-100 mt-6">
                <h2 className="text-xl font-bold mb-4 text-slate-800">
                    OCR Text
                </h2>
                <pre className="whitespace-pre-wrap bg-slate-50 p-4 rounded-xl text-xs text-slate-600 max-h-[200px] overflow-y-auto border border-slate-100">
                    {receipt.raw_receipt_text || "No OCR raw text extracted."}
                </pre>
            </div>

            {/* Explorer Component */}
            <div className="mt-6">
                <ReceiptExplorer expenseId={receipt.id} />
            </div>

        </div>
    );
}
