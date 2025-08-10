import React, {useEffect, useState } from 'react';
import { fetchMessages } from '../services/api';
import MessageBubble from "./MessageBubble";
import SendMessageForm from "./SendMessage";

export default function ChatWindow({conversation_id}) {
    const [messages, setMessages]= useState([]);

    const load= async() => {
        const data = await fetchMessages(conversation_id);
        setMessages(data);
    };
    
    useEffect(() => {
        load();
    }, [conversation_id]);

    return (
        <div className="w-2/3 flex flex-col bg-chat-pattern">
            <div className="flex-1 p-4 overflow-y-auto space-y-3">
                {messages.map((msg, index) => {
                    <MessageBubble key={msg._id || index} message={msg} isSender={msg.name === 'You'} />
                })}
            </div>
            <SendMessageForm conversation_id={conversation_id} reload={load}/>
        </div>
    );
}

