import { useState } from "react";
import { NavLink } from "react-router-dom";

import {
    FiHome,
    FiDollarSign,
    FiChevronLeft,
    FiChevronRight,
} from "react-icons/fi";

import GmailConnect from "./GmailConnect";

type Props = {
    gmailConnected: boolean;

};

export default function Sidebar({
    gmailConnected,
}: Props) {

    const [collapsed, setCollapsed] =
        useState(false);
    const linkClass = ({ isActive }: { isActive: boolean }) => `
        flex items-center gap-3 p-3 rounded-xl transition-all duration-200
        ${isActive 
            ? 'bg-slate-800 text-white font-semibold shadow-sm' // Active state: noticeably lighter or highlighted
            : 'text-slate-400 hover:bg-slate-900/50 hover:text-white' // Inactive state
        }
    `;

    return (

        <aside
            className={`
                bg-slate-950
                text-white
                min-h-screen
                transition-all
                duration-300
                flex
                flex-col
                
                ${collapsed ? "w-20" : "w-64"}
            `}
        >

            {/* TOP SECTION */}
            <div>

                {/* HEADER */}
                <div
                    className="
                        p-6
                        flex
                        items-center
                        justify-between
                    "
                >

                    {!collapsed && (

                        <h1
                            className="
                                text-2xl
                                font-bold
                            "
                        >
                            ExpenseAI
                        </h1>

                    )}

                    <button
                        onClick={() =>
                            setCollapsed(
                                !collapsed
                            )
                        }
                        className="
                            p-2
                            rounded-lg
                            hover:bg-slate-800
                        "
                    >

                        {collapsed
                            ? <FiChevronRight />
                            : <FiChevronLeft />
                        }

                    </button>

                </div>


                {/* NAVIGATION */}
                <nav
                    className="
                        mt-6
                        px-3
                        space-y-2
                    "
                >

                    <NavLink
                        to="/"
                        className={linkClass}>

                        <FiHome size={20} />

                        {!collapsed &&
                            "Dashboard"}

                    </NavLink>


                    <NavLink
                        to="/budgets"
                        className={linkClass}>  
                    

                        <FiDollarSign
                            size={20}
                        />

                        {!collapsed &&
                            "Budgets"}

                    </NavLink>

                </nav>

            </div>


            {/* BOTTOM SECTION */}
            <GmailConnect
                collapsed={collapsed}

            />

        </aside>

    );

}