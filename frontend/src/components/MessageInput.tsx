import React, { useState } from 'react';

type Props = { onSend: (text: string) => void };

export default function MessageInput({ onSend }: Props) {
  const [input, setInput] = useState('');
  const handleSend = () => {
    if (!input.trim()) return;
    onSend(input);
    setInput('');
  };
  return (
    <div className="message-input">
      <input
        type="text"
        value={input}
        placeholder="Frag etwas..."
        onChange={e => setInput(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && handleSend()}
      />
      <button onClick={handleSend}>Senden</button>
    </div>
  );
}
