import { useState, useRef, useEffect } from 'react'

export default function App() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hi! I am your car insurance specialist. Ask me anything about coverage, claims, premiums, or policy requirements.',
      toolUsed: null,
    },
  ])
  const [input, setInput] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)
  const bottomRef = useRef(null)

  // Auto scroll to bottom on new messages
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async () => {
    if (!input.trim() || isStreaming) return

    const userMessage = input.trim()
    setInput('')
    setIsStreaming(true)

    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: userMessage, toolUsed: null }])

    // Add empty assistant message that we will stream into
    setMessages(prev => [...prev, { role: 'assistant', content: '', toolUsed: null }])

    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage }),
      })

      const reader = response.body.getReader()
      const decoder = new TextDecoder()

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const text = decoder.decode(value)
        const lines = text.split('\n').filter(line => line.startsWith('data:'))

        for (const line of lines) {
          const raw = line.replace('data:', '').trim()
          if (!raw) continue

          try {
            const event = JSON.parse(raw)

            if (event.type === 'token') {
              // Append token to last assistant message
              setMessages(prev => {
                const updated = [...prev]
                updated[updated.length - 1] = {
                  ...updated[updated.length - 1],
                  content: updated[updated.length - 1].content + event.content,
                }
                return updated
              })
            }

            if (event.type === 'tool_use') {
              // Record which tool was used on the last assistant message
              setMessages(prev => {
                const updated = [...prev]
                updated[updated.length - 1] = {
                  ...updated[updated.length - 1],
                  toolUsed: event.tool,
                }
                return updated
              })
            }

            if (event.type === 'done') {
              setIsStreaming(false)
            }

            if (event.type === 'error') {
              setMessages(prev => {
                const updated = [...prev]
                updated[updated.length - 1] = {
                  ...updated[updated.length - 1],
                  content: 'Sorry, something went wrong. Please try again.',
                }
                return updated
              })
              setIsStreaming(false)
            }
          } catch {
            // Skip malformed events
          }
        }
      }
    } catch {
      setMessages(prev => {
        const updated = [...prev]
        updated[updated.length - 1] = {
          ...updated[updated.length - 1],
          content: 'Sorry, could not connect to the server. Please try again.',
        }
        return updated
      })
      setIsStreaming(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="container">
      <div className="header">
        <span>🚗</span>
        <h1>Car Insurance Specialist</h1>
      </div>

      <div className="chat-window">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <div className="bubble">
              {msg.content}
              {isStreaming && i === messages.length - 1 && msg.role === 'assistant' && (
                <span className="cursor">▋</span>
              )}
            </div>
            {msg.toolUsed && (
              <div className="tool-badge">
                🔧 Used: {msg.toolUsed.replace(/_/g, ' ')}
              </div>
            )}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <div className="input-bar">
        <textarea
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about car insurance..."
          disabled={isStreaming}
          rows={1}
        />
        <button onClick={sendMessage} disabled={isStreaming || !input.trim()}>
          {isStreaming ? '...' : 'Send'}
        </button>
      </div>
    </div>
  )
}