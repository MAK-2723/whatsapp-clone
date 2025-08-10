import React from 'react';

export default function MessageBubble({ message }) {
  const isSender= message.name === "You"; 
  return (
    <div className={`flex ${isSender ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-xs md:max-w-sm p-3 rounded-lg shadow
        ${isSender ? 'bg-green-100 rounded-br-none' : 'bg-white rounded-bl-none'}`}>
        {!isSender && (
          <div className="text-xs font-semibold mb-1">{message.name}</div>
        )}
        <p className="text-sm">{message.text}</p>
        <div className="text-right text-xs text-gray-500 mt-1">
          {new Date(message.timestamp).toLocaleString()} 
          {isSender && <StatusIcon status={message.status} />}
        </div>
      </div>
    </div>
  );
}
