import { useState,useRef } from "react";
import api from "../services/api";

export default function UploadReceipt({onUploadSuccess}) {

    const [loading, setLoading] =
        useState(false);

    const [result, setResult] =
        useState(null);

    const [duplicate, setDuplicate] = useState(false);   
    const fileInputRef = useRef(null);

    async function upload(
        event
    ) {

        const file =
            event.target.files[0];

        if(!file)
            return;

        const formData =
            new FormData();

        formData.append(
            "file",
            file
        );

        setLoading(true);

        try {

            const response =
                await api.post(
                    "/receipts/process",
                    formData
                );

            setResult(
                response.data
            );
            setDuplicate(response.data.duplicate)
            onUploadSuccess?.();

             setTimeout(() => {
                setResult(null);
                setDuplicate(false);
                if (fileInputRef.current) {
                    fileInputRef.current.value = ""; 
                }
            }, 5000); 

        } finally {

            setLoading(false);

        }
    }

    return (

        <div
            className="
            bg-white
            shadow
            rounded-xl
            p-8 mb-4
            "
        >

            <h2
                className="
                text-xl
                font-bold
                mb-4
                "
            >
                Upload Receipt
            </h2>

            <input
    type="file"
    onChange={upload}
    ref={fileInputRef}
    className="
    block w-full text-sm text-slate-500
    file:mr-4 file:py-2.5 file:px-4
    file:rounded-lg file:border-0
    file:text-sm file:font-semibold
    file:bg-blue-50 file:text-blue-700
    hover:file:bg-blue-100
    cursor-pointer
    "
/>

            {
                loading &&
                <p>
                    Processing...
                </p>
            }
        { duplicate && (

        <div className="bg-yellow-100 border border-yellow-400 text-yellow-800 p-4 rounded-xl mt-4 " >

            ⚠ Duplicate receipt detected!! Below are the details:
        </div>)}
        {
                result  &&

                <div
                    className="
                    mt-4
                    border
                    rounded
                    p-4
                    "
                >

                    <p>
                        Merchant:
                        {result.merchant_name}
                    </p>

                    <p>
                        Amount:
                        ${result.amount}
                    </p>

                    <p>
                        Category:
                        {result.category}
                    </p>

                </div>
            }

        </div>
    );
}