import React from 'react';

export default function MessageBubble({ message }) {
  const isSender= message.isSender || message.name === "you"; 
  return (
    <div className={`flex ${isSender ? 'justify-end' : 'justify-start'}`}>
      <div className="max-w-xs md:max-w-sm">
        {/* Show sender's name if not "You" */}
        {!isSender && (<div className="text-xs text-gray-500 mb-1">{message.name}</div>)}
        <div className={`p-3 rounded-lg shadow ${
            isSender ? 'bg-green-100 rounded-br-none': 'bg-white rounded-bl-none'}`}>
          <p className="text-sm">{message.text}</p>
          <div className="text-right text-xs text-gray-500 mt-1">
            {message.timestamp} {isSender && <StatusIcon status={message.status} />}
          </div>
        </div>
      </div>
    </div>
  );

}


