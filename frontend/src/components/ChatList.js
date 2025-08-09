import React from 'react';

export default function ChatList({chats, onSelect}) {
    return (
        <div className="w-1/3 min-w-[320px] border-r border-gray-200 overflow-y-auto bg-gray-50">
            {chats.map(chat => (
                <div key={chat._id} onClick={() => onSelect(chat._id)} className="p-4 cursor pointer hover:bg-gray-200 transition-colors">
                    <div className="font-semibold text-md">{chat._id}</div>
                    <div className="text-sm text-gray-600 truncate">{chat.last_msg}</div>
                    <img src="https://i.pravatar.cc/40" className="rounded-full w-10 h-10 mr-2"/>
                </div>
            ))}
        </div>
    );
}
