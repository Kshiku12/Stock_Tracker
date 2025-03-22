import { useEffect, useState } from "react";
import { fetchStockData } from "../api";

function Dashboard() {
  const [stocks, setStocks] = useState([]);
  
  useEffect(() => {
    fetchStockData()
      .then((data) => {
        console.log("📢 Fetched Stock Data:", data);
        // Add this to check the exact structure of your data
        console.log("Data type:", typeof data);
        console.log("Is array:", Array.isArray(data));
        
        setStocks(Array.isArray(data) ? data : [data]);
      })
      .catch((error) => console.error("❌ Error fetching stock data:", error));
  }, []);
  
  return (
    <div style={{ padding: "20px" }}>
      <h2>📊 Stock Dashboard</h2>
      
      {stocks.length > 0 ? (
        <ul style={{ listStyle: "none", padding: 0 }}>
          {stocks.map((stock, index) => {
            // Log each stock to see its structure
            console.log(`Rendering stock ${index}:`, stock);
            
            return (
              <li
                // Use a guaranteed unique key combining index and ticker if available
                key={`stock-${index}-${stock.ticker || ""}`}
                style={{
                  marginBottom: "15px",
                  borderBottom: "1px solid #ccc",
                  paddingBottom: "10px",
                }}
              >
                <div>
                  <strong>{stock.ticker ? stock.ticker.toUpperCase() : "N/A"}</strong> - {stock.name || "Unknown"}
                </div>
                <div>
                  <span style={{ fontWeight: "bold" }}>Price:</span> {stock.price !== undefined ? stock.price : "N/A"} INR
                </div>
                <div>
                  <span style={{ fontWeight: "bold" }}>Market Cap:</span> {stock.market_cap !== undefined ? stock.market_cap.toLocaleString() : "N/A"}
                </div>
              </li>
            );
          })}
        </ul>
      ) : (
        <p>⚠️ Loading stocks... (Check console for logs)</p>
      )}
    </div>
  );
}

export default Dashboard;