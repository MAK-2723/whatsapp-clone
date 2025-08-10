import React, {useEffect, useState } from 'react';
import { fetchMessages } from '../services/api';
import MessageBubble from "./MessageBubble";
import SendMessageForm from "./SendMessage";

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
                {messages.map((msg, index) => {
                    const showName = index === 0 || messages[index - 1].wa_id !== msg.wa_id;
                    return (
                        <div key={index}>
                            {showName && (
                                <div className="text-xs font-bold text-gray-600 mb-1">
                                    {msg.name}
                                </div>
                            )}
                            <MessageBubble key={index} message={msg} isSender={msg.name === 'You'} />
                        </div>
                    );
                })}
            </div>
            <SendMessageForm conversation_id={wa_id} reload={() => fetchMessages(conversation_id).then(setMessages)}/>
        </div>
    );

}






