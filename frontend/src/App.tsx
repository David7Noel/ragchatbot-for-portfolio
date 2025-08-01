import React, { useState } from 'react';
import ChatWindow from './components/ChatWindow';
import MessageInput from './components/MessageInput';
import './App.css';

function App() {
  const [messages, setMessages] = useState<{role: string; content: string;}[]>([]);

  const sendMessage = async (content: string) => {
    const userMsg = { role: 'user', content };
    setMessages(prev => [...prev, userMsg]);
    // später: call your backend
    // const resp = await sendQuery(...)
    // setMessages(prev => [...prev, { role: 'assistant', content: resp.answer }]);
  };

  return (
    <div className="app">
      <h1>RAG‑Chatbot & Portfolio</h1>
      <ChatWindow messages={messages} />
      <MessageInput onSend={sendMessage} />
    </div>
  );
}

export default App;
