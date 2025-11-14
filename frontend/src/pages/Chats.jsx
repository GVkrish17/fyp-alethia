import { useEffect, useState } from "react";

export default function HomePage() {
  const [chats, setChats] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/chats")
      .then(res => res.json())
      .then(data => setChats(data))
      .catch(err => console.error("Failed to fetch chats", err));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold mb-4">Your Telegram Chats</h1>
      <ul className="space-y-2">
        {chats.map(chat => (
          <li key={chat.chat_id} className="bg-white p-4 rounded shadow">
            <p><strong>Name:</strong> {chat.name}</p>
            <p><strong>Username:</strong> {chat.username || "N/A"}</p>
            <p><strong>ID:</strong> {chat.chat_id}</p>
            <p><strong>Type:</strong> {chat.type}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
