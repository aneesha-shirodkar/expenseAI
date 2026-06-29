import { useState } from "react";
import api from "../services/api";

export default function ChatWidget() {

    const [message, setMessage] =
        useState("");

    const [answer, setAnswer] =
        useState("");

    async function askQuestion() {

        const response =
            await api.post(
                "/chat",
                {
                    message
                }
            );

        setAnswer(
            response.data.answer
        );
    }

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
                🤖 Ask Your Expenses
            </h2>

            <input

                value={message}

                onChange={
                    e =>
                    setMessage(
                        e.target.value
                    )
                }

                placeholder="
                How much did I spend on food?
                "

                className="
                w-full
                border
                p-3
                rounded
                "

            />

            <button

                onClick={askQuestion}

                className="
                mt-4
                bg-blue-600
                text-white
                px-4
                py-2
                rounded
                "

            >

                Ask

            </button>

            {

                answer && (

                    <div
                        className="
                        mt-4
                        p-4
                        bg-gray-100
                        rounded
                        "
                    >

                        {answer}

                    </div>

                )

            }

        </div>

    );
}