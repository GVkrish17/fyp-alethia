export default function ContactList() {
    const contacts = [
      { name: "Amma", tag: "Active", color: "bg-sageGreen" },
      { name: "Alex", tag: "Tense", color: "bg-mutedRed" },
      { name: "John", tag: "Friendly", color: "bg-oceanTeal" },
    ]

    return (
      <ul className="space-y-4">
        {contacts.map((contact, idx) => (
          <li key={idx} className="flex justify-between items-center bg-white p-4 rounded-xl shadow-sm border">
            <span className="font-medium">{contact.name}</span>
            <span className={`text-white text-sm px-3 py-1 rounded-full ${contact.color}`}>
              {contact.tag}
            </span>
          </li>
        ))}
      </ul>
    )
  }
