import StyleSummaryCard from '../components/StyleSummaryCard'
import ContactList from '../components/ContactList'

export default function Home() {
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

      <div>
        <h2 className="text-2xl font-semibold mb-4">💬 Recent Conversations</h2>
        <ContactList />
      </div>
    </div>
  )
}
