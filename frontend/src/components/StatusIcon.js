import React from 'react';

export default function StatusIcon({ status }) {
  const map = {
    sent: '✓',
    delivered: '✓✓',
    read: '✓✓'
  }
  const color = status === 'read' ? 'text-blue-500' : 'text-gray-500'
  return <span className={`ml-1 ${color}`}>{map[status]}</span>
}