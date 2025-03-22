import React, { useEffect, useState } from "react";
import { fetchTransactions } from "../api.js"; // ✅ Use correct API function

function Transactions() {
    const [transactions, setTransactions] = useState([]);

    useEffect(() => {
        fetchTransactions()
            .then(setTransactions)
            .catch((error) => console.error("Error fetching transactions:", error));
    }, []);

    return (
        <div>
            <h2>Transaction History</h2>
            {transactions.length > 0 ? (
                <ul>
                    {transactions.map((txn, index) => (
                        <li key={index}>
                            {txn.type}: {txn.symbol} - {txn.quantity} shares at {txn.price} INR
                        </li>
                    ))}
                </ul>
            ) : (
                <p>Loading transactions...</p>
            )}
        </div>
    );
}

export default Transactions;
