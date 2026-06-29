import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    CartesianGrid,
    ResponsiveContainer
}
from "recharts";


type Props = {

    data: {
        month: string;
        amount: number;
    }[];

};


export default function MonthlyTrendChart(
    {
        data
    }: Props
) {

    return (

        <div
            className="
            bg-white
            rounded-xl
            shadow-md
            p-6
            mt-8
            "
        >

            <h2
                className="
                text-xl
                font-bold
                mb-4
                "
            >
                Monthly Spending Trend
            </h2>

            <ResponsiveContainer
                width="100%"
                height={300}
            >

                <LineChart
                    data={data}
                >

                    <CartesianGrid />

                    <XAxis
                        dataKey="month"
                    />

                    <YAxis />

                    <Tooltip />

                    <Line
                        type="monotone"
                        dataKey="amount"
                    />

                </LineChart>

            </ResponsiveContainer>

        </div>

    );

}