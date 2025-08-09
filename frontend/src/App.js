import React, { useEffect, useState } from 'react';
import ChatList from './components/ChatList';
import ChatWindow from './components/ChatWindow';
import { fetchConversations } from './services/api';

export default function App() {
    const [conversations, setConversations]=useState([]);
    const [activeChat, setActiveChat]=useState(null);
    
    const loadData= async () =>{
        const data = await fetchConversations();
        setConversations(data);
    };
    useEffect(() => {
        loadData();
        const apiBASE= process.env.REACT_APP_API_URL || "http://localhost:8000";
        const urlObj= new URL(apiBASE);
        const wsProtocol= urlObj.protocol === "https:" ? "wss:" : "ws:";
        const wsUrl= `${wsProtocol}//${urlObj.host}/ws`;
        
        const ws= new WebSocket(wsUrl);

        ws.onopen= () => console.log("WebSocket connected");
        ws.onmessage= (event) => {
            if (event.data === "new_data") loadData();
        };
        ws.onerror= (err) => console.error("WebSocket error",err);
        return () => {
            ws.close();
        };
    }, []);

    return (
        <div className="flex h-screen bg-white text-gray-900 overflow-hidden">
            <ChatList chats={conversations} onSelect={setActiveChat} />
            {activeChat ? (
                <ChatWindow wa_id={activeChat}/>
            ) : (
                <div className="flex-1 flex items-center justify-center text-gray-500 bg-chat-pattern">Select a chat to start messaging</div>
            )}
        </div>
    );

}

