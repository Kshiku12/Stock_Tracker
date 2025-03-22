import { useEffect, useState } from "react";
import { fetchStockData  } from "./api";

function Dashboard() {
    const [stocks, setStocks] = useState([]);

    useEffect(() => {
        fetchStockData().then(setStocks);
    }, []);

    return (
        <div>
            <h2>Stock Dashboard</h2>
            {stocks.length > 0 ? (
                <ul>
                    {stocks.map((stock) => (
                        <li key={stock.symbol}>
                            {stock.symbol}: {stock.price} INR
                        </li>
                    ))}
                </ul>
            ) : (
                <p>Loading stocks...</p>
            )}
        </div>
    );
}

export default Dashboard;
