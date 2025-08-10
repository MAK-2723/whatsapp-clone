const BASE = process.env.REACT_APP_API_URL || "https://localhost:8000";

export async function fetchConversations() {
    try {
        const res = await fetch(`${BASE}/conversations`);
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return await res.json();
    } catch (err) {
        console.error('Failed to fetch conversations:', err);
        return [];
    }
}

export async function fetchMessages(conversation_id) {
    const res=await fetch(`${BASE}/messages/${conversation_id}`);
    return res.json();
}

export async function sendMessage(data) {
    await fetch(`${BASE}/send`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
}
