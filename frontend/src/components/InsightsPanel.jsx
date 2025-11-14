import { useEffect, useState } from "react"
import { getUserStyle, getChatMessages, runLLM } from "../services/api"


export default function InsightsPanel({ contact }) {
  const [style, setStyle] = useState(null)
  const [messages, setMessages] = useState([])
  const [toneStats, setToneStats] = useState({ positive: 0, neutral: 0, negative: 0 })
  const [llmSuggestion, setLlmSuggestion] = useState(null)
  const [loadingLLM, setLoadingLLM] = useState(false)

  useEffect(() => {
    async function loadInsights() {
      const styleRes = await getUserStyle(contact)
      setStyle(styleRes.data)

      const msgRes = await getChatMessages(contact, 100)
      setMessages(msgRes.data)

      const tones = { positive: 0, neutral: 0, negative: 0 }

      msgRes.data.forEach(msg => {
        if (!msg.text) return
        const text = msg.text.toLowerCase()
        if (text.includes("sad") || text.includes("angry") || text.includes("bad")) {
          tones.negative++
        } else if (text.includes("good") || text.includes("great") || text.includes("love")) {
          tones.positive++
        } else {
          tones.neutral++
        }
      })

      const total = tones.positive + tones.neutral + tones.negative
      setToneStats({
        positive: Math.round((tones.positive / total) * 100),
        neutral: Math.round((tones.neutral / total) * 100),
        negative: Math.round((tones.negative / total) * 100)
      })

      // 4️⃣ get AI suggestion from backend LLM
      setLoadingLLM(true)
      try {
        const llmRes = await runLLM({
          task: "reply",
          username: contact,
          messages: msgRes.data.map(m => m.text),
          style: styleRes.data
        })
        setLlmSuggestion(llmRes.data.result) // backend returns {type, result}
      } catch (err) {
        console.error("LLM request failed:", err)
        setLlmSuggestion("⚠️ Unable to fetch AI suggestion.")
      } finally {
        setLoadingLLM(false)
      }

    }

    loadInsights()
  }, [contact])
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {/* Tone Summary */}
      <div className="bg-white p-5 rounded-xl shadow border">
        <h3 className="text-oceanTeal font-semibold text-lg mb-2">Tone Snapshot</h3>
        <ul className="text-sm text-slateGray space-y-1">
          <li>😊 Positive: {toneStats.positive}%</li>
          <li>😐 Neutral: {toneStats.neutral}%</li>
          <li>😟 Negative: {toneStats.negative}%</li>
        </ul>
      </div>

      {/* Suggestions */}
      <div className="bg-white p-5 rounded-xl shadow border">
        <h3 className="text-softCoral font-semibold text-lg mb-2">💡 Suggestions</h3>
        <ul className="text-sm text-slateGray list-disc pl-4 space-y-1">
          {style?.summary.includes("short") && (
            <li>You tend to keep replies short — maybe expand when it’s emotional</li>
          )}
          {style?.summary.includes("lowercase") && (
            <li>Consider capitalizing for clarity in serious convos</li>
          )}
          {style?.summary.includes("emojis") && (
            <li>Keep using emojis — they add warmth and tone</li>
          )}
        </ul>

        {llmSuggestion && (
          <div className="mt-3 p-3 bg-emerald-50 border border-emerald-200 rounded-md text-slateGray text-sm">
            <p className="font-semibold text-emerald-700 mb-1">AI Suggested Reply</p>
            <p>{llmSuggestion}</p>
          </div>
        )}

        {loadingLLM && <p className="text-xs text-gray-400 mt-2">🤔 thinking...</p>}

      </div>

      {/* Placeholder for heatmap or chart */}
      <div className="bg-white p-5 rounded-xl shadow border">
        <h3 className="text-mutedRed font-semibold text-lg mb-2">🔥 Emotional Heatmap</h3>
        <p className="text-sm text-slateGray">Coming soon: Timeline of tone spikes 📈</p>
      </div>
    </div>
  )
}
