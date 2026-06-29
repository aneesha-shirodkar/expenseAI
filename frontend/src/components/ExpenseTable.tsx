import { Link } from "react-router-dom";
export default function ExpenseTable(
  { expenses }
) {

  return (
    <div className="overflow-hidden bg-white border border-slate-200 shadow-sm rounded-xl">

  <div className="px-6 py-4 border-b border-slate-200 bg-slate-50/50">
    <h3 className="font-semibold text-slate-800"> Receipts</h3>
  </div>
   <div className="overflow-x-auto">
    <table className="w-full text-sm text-left border-collapse text-slate-600">
      <thead className="text-xs uppercase bg-slate-50 text-slate-700 border-b border-slate-200">

      <tr>
        <th scope="col" className="px-6 py-3 font-semibold">Date</th>
        <th scope="col" className="px-6 py-3 font-semibold">Merchant</th>
        <th scope="col" className="px-6 py-3 font-semibold">Category</th>
        <th scope="col" className="px-6 py-3 font-semibold text-right">Amount</th>
      </tr>

      </thead>

      <tbody className="divide-y divide-slate-100">

      {
        expenses.map(
          expense => (
            <tr className="hover:bg-slate-50 transition-colors"
              key={expense.id}
            >
              <td className="px-6 py-4 font-medium text-slate-900">
                {
                  expense.expense_date
                }
              </td>

              <td className="px-6 py-4 font-medium text-slate-900">
                {
                  expense.merchant_name
                }
              </td>

              <td className="px-6 py-4">
                {
                  expense.category
                }
              </td>

              <td className="px-6 py-4 text-right font-semibold text-slate-900">
                $
                {
                  expense.amount
                }
              </td>
              <td>
                 <Link to={`/receipts/${expense.id}`} className="text-blue-600 hover:underline">View Receipt</Link>
              </td>
            </tr>
          )
        )
      }

      </tbody>
    </table>
       </div>
</div>
 
  );
}