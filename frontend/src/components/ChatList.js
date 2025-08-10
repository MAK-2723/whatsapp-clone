import React from 'react';

export default function ChatList({ chats, onSelect }) {
    return (
        <div className="w-1/3 min-w-[320px] border-r border-gray-200 overflow-y-auto bg-gray-50">
            {chats.length === 0 && (<div className="p-4 text-gray-500">No chats available</div>)}
            {chats.map(chat => (
                <div key={chat.conversation_id} onClick={() => onSelect(chat.conversation_id)} className="p-4 cursor-pointer hover:bg-gray-200 transition-colors flex items-center gap-3">
                    <img src="https://i.pravatar.cc/40" alt="Avatar" className="rounded-full w-10 h-10"/>
                    <div className="flex flex-col overflow-hidden">
                        <div className="font-semibold text-md truncate">{chat.name || chat.wa_id}</div>
                        <div className="text-sm text-gray-600 truncate">{chat.last_msg || 'No messages yet'}</div>
                    </div>
                </div>
            ))}
        </div>
    );
}
