// src/components/ContactList.jsx
import { useEffect, useState } from "react"
import { getContacts } from "../services/api"

export default function ContactList({ onSelect }) {
  const [contacts, setContacts] = useState([])

  useEffect(() => {
    async function loadContacts() {
      const res = await getContacts()
      setContacts(res.data)
    }
    loadContacts()
  }, [])

    return (
      <ul className="space-y-4">
        {contacts.map((contact, idx) => (
          <li key={idx}
           onClick={() => onSelect(contact.name)}
           className="flex justify-between items-center bg-white p-4 rounded-xl shadow-sm border"
           >

            <span className="font-medium">{contact.name}</span>
            <span className={`text-white text-sm px-3 py-1 rounded-full ${contact.color}`}>
              {contact.tag}
            </span>
          </li>
        ))}
      </ul>
    )
  }
