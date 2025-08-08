import React from 'react';

type Props = {
  messages: { role: string; content: string }[];
};

export default function ChatWindow({ messages }: Props) {
  return (
    <div className="chat-window">
      {messages.map((m, i) => (
        <div key={i} className={m.role}>
          <b>{m.role}: </b>{m.content}
        </div>
      ))}
    </div>
  );
}
