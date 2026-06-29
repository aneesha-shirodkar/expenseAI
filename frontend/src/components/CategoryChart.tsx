import {PieChart, Pie,Tooltip,Legend, Cell} from "recharts";

const COLORS = [
  "#3b82f6", // Blue (e.g., Groceries)
  "#10b981", // Green (e.g., Utilities)
  "#f59e0b", // Amber (e.g., Travel)
  "#ef4444", // Red (e.g., Entertainment)
  "#8b5cf6", // Purple
  "#ec4899", // Pink
  "#64748b"  // Slate (fallback)
];

export default function CategoryChart(
  { summary }
) {

  const data =
    Object.entries(
      summary.categories
    ).map(
      ([name, value]) => ({
        name,
        value
      })
    );

  return (
    <PieChart
      width={500}
      height={350} style={{marginBottom:"10px"}}
    >
      {/* <Pie
        data={data}
        dataKey="value"
        nameKey="name"
      /> */}
      <Pie
        data={data}
        dataKey="value"
        nameKey="name"
        cx="50%" // Centers the pie chart horizontally
        cy="50%" // Centers the pie chart vertically
        outerRadius={100} // Sizes the pie chart cleanly
        innerRadius={60}  // Optional: Makes it a modern Donut Chart! Set to 0 if you want a solid Pie.
        paddingAngle={3}  // Optional: Adds a tiny gap between slices
      >
         {/* 3. Map over data to assign a color cell to each slice */}
        {data.map((entry, index) => (
          <Cell 
            key={`cell-${index}`} 
            fill={COLORS[index % COLORS.length]} // Cycles colors if categories > palette size
          />
        ))}
      </Pie>

      {/* <Tooltip /> */}
       <Tooltip 
        contentStyle={{ 
          backgroundColor: '#fff', 
          borderRadius: '8px', 
          border: '1px solid #e2e8f0',
          boxShadow: '0 1px 3px 0 rgb(0 0 0 / 0.1)' 
        }} 
      />

      {/* <Legend /> */}
       <Legend verticalAlign="bottom" height={36} />
    </PieChart>
  );
}