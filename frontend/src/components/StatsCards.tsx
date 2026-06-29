export default function StatsCards(
  { stats }
) {

  return (
    <div className="grid grid-cols-4 gap-4 mb-8">
      <div className="bg-white rounded-xl shadow p-4">
        <h3>Total Spending</h3>
        <p className="text-2xl font-bold">${stats.total_spending}</p>
      </div>

      <div className="bg-white rounded-xl shadow p-4">
         <h3>Expenses</h3>
        <p className="text-2xl font-bold">{stats.total_expenses}</p>
      </div>

      <div className="bg-white rounded-xl shadow p-4">
        <h3>Average</h3>
        <p className="text-2xl font-bold">${stats.average_expense}</p>
      </div>

      <div className="bg-white rounded-xl shadow p-4">
        <h3> Top Category</h3>

        <p className="text-2xl font-bold"> {stats.top_category} </p>
      </div>
    </div>
  );
}