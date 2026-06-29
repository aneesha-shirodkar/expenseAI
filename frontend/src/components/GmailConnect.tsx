import { useEffect, useState } from "react";
import { FiMail, FiRefreshCw } from "react-icons/fi";
import api from "../services/api";

type Props = {
    collapsed: boolean;
};

export default function GmailConnect({
    collapsed,
}: Props) {

    const [connected, setConnected] =
        useState(false);

    const [email, setEmail] =
        useState("");

    const [loading, setLoading] =
        useState(true);

        const [lastSync, setLastSync] =
    useState<string | null>(null);

    const[syncing, setSyncing] = useState(false);

const [totalImported, setTotalImported] =
    useState(0);

    useEffect(() => {
        loadStatus();
    }, []);

    async function loadStatus() {

        try {

            const response =
                await api.get("/gmail/status");

            setConnected(
                response.data.connected
            );

            setEmail(
                response.data.email || ""
            );
             setLastSync(
            response.data.last_sync
        );

        setTotalImported(
            response.data.total_imported || 0
        );

        } catch (error) {

            console.error(error);

        } finally {

            setLoading(false);

        }
    }

    async function connect() {

        const response =
            await api.get("/gmail/connect");

        window.location.href =
            response.data.url;
    }

    async function syncReceipts() {
        setSyncing(true)
       const response= await api.post("/gmail/sync");

        //alert("Receipts synced successfully");
        console.log(response)
        setTotalImported(response.data.imported || 0);
        setSyncing(false)
        window.dispatchEvent( new CustomEvent("receipts-synced"));
    }

    if (loading) {
        return null;
    }

    return (

        <div className="border-t border-slate-800 p-3">

            {!connected ? (

                <button
                    onClick={connect}
                    className="
                        w-full
                        flex
                        items-center
                        gap-3
                        p-3
                        rounded-xl
                        hover:bg-slate-800
                        transition
                    "
                >

                    <FiMail size={20} />

                    {!collapsed && (
                        <span>
                            Connect Gmail
                        </span>
                    )}

                </button>

            ) : (

                <div className="space-y-2">

                    <div
                        className="
                            flex
                            items-center
                            gap-3
                            p-3
                            rounded-xl
                            bg-slate-900
                        "
                    >

                        <FiMail
                            size={20}
                            className="text-green-400"
                        />

                        {!collapsed && (

                            <div className="min-w-0">

                                <p
                                    className="
                                        text-sm
                                        font-medium
                                        truncate
                                    "
                                >
                                    Gmail Connected
                                </p>

                                <p
                                    className="
                                        text-xs
                                        text-slate-400
                                        truncate
                                    "
                                >
                                    {email}
                                </p>
                                 <p
                                    className="
                                        text-xs
                                        text-slate-400
                                        truncate
                                    "
                                >
                                    Imported : {totalImported} 
                                </p>
                                {lastSync && (

                    <p
                        className="
                            text-[11px]
                            text-slate-500
                        "
                    >
                        Last sync:{" "}
                        {new Date(
                            lastSync
                        ).toLocaleString()}
                    </p>)}


                            </div>

                        )}

                    </div>

                    {!collapsed && (

                        <button
                            onClick={syncReceipts}
                            className="
                                w-full
                                flex
                                items-center
                                justify-center
                                gap-2
                                bg-blue-600
                                hover:bg-blue-700
                                py-2
                                rounded-lg
                                text-sm
                            "
                        >

                            <FiRefreshCw />

                          { syncing ?(<p>Syncing...</p>) : <p>Sync Receipts </p>}  

                        </button>

                    )}

                </div>

            )}

        </div>

    );
}