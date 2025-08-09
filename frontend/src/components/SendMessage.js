import React, { useState } from 'react';
import { sendMessage } from '../services/api';

export default function sendMessage({wa_id, reload}) {
    const [text, setText] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        await sendMessage({ wa_id, text, name: "You", timestamp: new Date().toISOString(), status: "sent"});
        setText('');
        reload();
    };

    return (
        <form onSubmit={handleSubmit} className="flex items-center gap-2 p-3 border-t bg-white">
            <input
            className="flex-1 p-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-green-500"
            placeholder="Type a message"
            value={text}
            onChange={e => setText(e.target.value)}
            />
            <button className="px-4 py-4 bg-green-500 hover:bg-green-600 text-white rounded-full">Send</button>
        </form>
    );
}