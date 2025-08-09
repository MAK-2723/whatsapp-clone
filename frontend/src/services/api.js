const BASE = process.env.REACT_APP_API_URL || "https://localhost:8000";

export async function fetchConversations() {
    const res=await fetch(`${BASE}/conversations`);
    return res.json();
}

export async function fetchMessages(wa_id) {
    const res=await fetch(`${BASE}/messages/${wa_id}`);
    return res.json();
}

export async function sendMessage(data) {
    await fetch(`${BASE}/send`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
}
