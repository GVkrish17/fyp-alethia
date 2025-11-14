import { useState } from 'react'
import StyleSummaryCard from '../components/StyleSummaryCard'
import ContactList from '../components/ContactList'
import InsightsPanel from '../components/InsightsPanel'

export default function Home() {
  const [selectedContact, setSelectedContact] = useState(null)

  return (
    <div className="min-h-screen bg-mistBlue px-6 py-10 text-charcoalGray">
      <h1 className="text-4xl font-bold mb-2 flex items-center gap-2">
        💬 Chat Behavior Dashboard
      </h1>
      <p className="text-slateGray text-lg mb-8">
        Your personalized relationship and tone assistant
      </p>

      <div className="mb-10">
        <h2 className="text-2xl font-semibold mb-4">🧍 Your Messaging Style</h2>
        <StyleSummaryCard />
      </div>

      <div className="mb-10">
        <h2 className="text-2xl font-semibold mb-4">💬 Recent Conversations</h2>
        <ContactList onSelect={setSelectedContact} />
      </div>

      {selectedContact && (
        <div>
          <h2 className="text-2xl font-semibold mb-4">
            📊 Insights for {selectedContact}
          </h2>
          <InsightsPanel contact={selectedContact} />
        </div>
      )}
    </div>
  )
}
