import { useState } from "react";

import api from "../services/api";


type Props = {

    expenseId: number;

};


export default function ReceiptExplorer({

    expenseId

}: Props) {

    const [question, setQuestion] =
        useState("");

    const [answer, setAnswer] =
        useState("");

    const [loading, setLoading] =
        useState(false);


    async function askQuestion() {

        setLoading(true);

        const response = await api.post(

            `/receipt-chat/${expenseId}`,

            {
                question
            }

        );

        setAnswer(
            response.data.answer
        );

        setLoading(false);
    }


    return (

        <div
            className="
                bg-white
                p-6
                rounded-xl
                shadow
                mt-6
            "
        >

            <h2
                className="
                    text-xl
                    font-bold
                    mb-4
                "
            >

                🧾 Receipt Explorer

            </h2>

            <input

                value={question}

                onChange={
                    e =>
                    setQuestion(
                        e.target.value
                    )
                }

                placeholder="
                Did I buy dairy products?
                "

                className="
                    border
                    w-full
                    p-3
                    rounded
                "

            />

            <button

                onClick={askQuestion}

                disabled={loading}

                className="
                    mt-4
                    bg-green-600
                    text-white
                    px-4
                    py-2
                    rounded
                "

            >

                {

                    loading
                        ? "Thinking..."
                        : "Ask"

                }

            </button>

            {

                answer && (

                    <div
                        className="
                            mt-4
                            p-4
                            bg-gray-50
                            rounded
                            whitespace-pre-wrap
                        "
                    >

                        🤖 {answer}

                    </div>

                )

            }

        </div>

    );
}