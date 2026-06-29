type Props = {
    insights: string[];
};

export default function InsightsCard({
    insights
}: Props) {

    if (!insights.length) {
        return null;
    }
    console.log(insights)

    return (

        <div
            className="
            bg-white
            shadow-md
            rounded-xl
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
                🤖 AI Spending Insights
            </h2>

            {

                insights.map(
                    (
                        insight,
                        index
                    ) => (

                        <div
                            key={index}
                            className="
                            mb-3
                            p-3
                            bg-gray-50
                            rounded-lg
                            border
                            "
                        >

                            {insight}

                        </div>

                    )
                )

            }

        </div>

    );
}