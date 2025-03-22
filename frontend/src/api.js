const API_BASE_URL = "http://127.0.0.1:5000"; // Flask Backend URL

// Test API Connection
export async function testBackend() {
    try {
        const response = await fetch(`${API_BASE_URL}/stock/test`); // Modify endpoint if needed
        const data = await response.json();
        return data.message;
    } catch (error) {
        console.error("Error connecting to backend:", error);
        return "Backend connection failed";
    }
}

// Fetch Stocks Data
export async function fetchStockData() {
    try {
        const response = await fetch("http://127.0.0.1:5000/stock/all");
        const data = await response.json();

        // Ensure data is an array
        return Array.isArray(data) ? data : [data]; 
    } catch (error) {
        console.error("Error fetching stock data:", error);
        return [];
    }
}


// Handle Login
export async function loginUser(credentials) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(credentials),
        });
        return await response.json();
    } catch (error) {
        console.error("Login error:", error);
        return { error: "Login failed" };
    }
}

// Fetch Transactions
export async function fetchTransactions() {
    try {
        const response = await fetch(`${API_BASE_URL}/transactions/all`);
        return await response.json();
    } catch (error) {
        console.error("Error fetching transactions:", error);
        return [];
    }
}
