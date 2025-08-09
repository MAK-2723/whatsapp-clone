import React, {useEffect, useState } from 'react';
import { fetchMessages } from '../services/api';
import MessageBubble from "./MessageBubble";
import SendMessage from "./SendMessage";

export default function ChatWindow({wa_id}) {
    const [messages, setMessages]= useState([]);

    useEffect(() => {
        async function load() {
            const data = await fetchMessages(wa_id);
            setMessages(data);
        }
        load();
    }, [wa_id]);

    return (
        <div className="w-2/3 flex flex-col bg-chat-pattern">
            <div className="flex-1 p-4 overflow-y-auto space-y-3">
                {messages.map((msg,index)=> <MessageBubble key={index} message={msg}/>)}
            </div>
            <SendMessage wa_id={wa_id} reload={() => fetchMessages(wa_id).then(setMessages)}/>
        </div>
    );
}