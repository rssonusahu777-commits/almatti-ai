"use client";

import { useState } from "react";

export default function Home() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState<any[]>([]);

  const sendMessage = async () => {
    if (!message) return;

    const res = await fetch("https://almatti-ai.onrender.com/api/chats", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: message,
      }),
    });

    const data = await res.json();

    // Add message to chat UI
    setChat([...chat, { user: message,bot: data.reply  }]);

    setMessage("");
  };

  return (
    <div style={{ padding: "20px", maxWidth: "600px", margin: "auto" }}>
      <h2>Almatti AI Chat</h2>

      {/* Chat Messages */}
      <div style={{ marginBottom: "20px" }}>
        {chat.map((c, i) => (
          <div key={i}>
            <p><b>You:</b> {c.user}</p>
            <p><b>AI:</b> {c.bot}</p>
            <hr />
          </div>
        ))}
      </div>

      {/* Input */}
      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message..."
        style={{ width: "100%", padding: "10px" }}
      />

      <button onClick={sendMessage} style={{ marginTop: "10px" }}>
        Send
      </button>
    </div>
  );
}