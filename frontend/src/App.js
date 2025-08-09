import React, { useEffect, useState } from 'react';
import ChatList from './components/ChatList';
import ChatWindow from './components/ChatWindow';
import { fetchConversations } from './services/api';
import { io } from 'socket.io-client';

const socket=io("http://localhost:8000");

export default function App() {
    const [conversations, setConversations]=useState([]);
    const [activeChat, setActiveChat]=useState(null);
    
    const loadData= async () =>{
        const data = await fetchConversations();
        setConversations(data);
    };
    useEffect(() => {
        loadData();
        socket.on("connect", () => console.log("WebSocket connected"));
        socket.on("message", () => loadData());
        return () => socket.disconnect();
    }, []);

    return (
        <div className="felx h-screen bg-white text-gray-900 overflow-hidden">
            <ChatList chats={conversations} onSelect={setActiveChat} />
            {activeChat && <ChatWindow wa_id={activeChat}/>}
        </div>
    );
}