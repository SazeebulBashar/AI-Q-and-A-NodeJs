import { useState, useRef, useEffect } from 'react'
import './App.css'

function NodeIcon() {
  return <img src="/nodejs-logo.png" alt="Node.js" className="node-icon" />
}

function SendIcon() {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M22 2L11 13" />
      <path d="M22 2L15 22L11 13L2 9L22 2Z" />
    </svg>
  )
}

function App() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! I am Node JS Guru. Ask me anything about Node.js!' },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  async function handleSend() {
    const query = input.trim()
    if (!query || loading) return

    setInput('')
    setMessages((prev) => [...prev, { role: 'user', content: query }])
    setLoading(true)

    try {
      const res = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      })
      const data = await res.json()
      setMessages((prev) => [...prev, { role: 'assistant', content: data.answer }])
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Something went wrong. Please try again.' },
      ])
    } finally {
      setLoading(false)
    }
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="chat-container">
      <div className="bg-glow" />

      <header className="chat-header">
        <div className="header-content">
          <div className="header-icon">
              <NodeIcon />
          </div>
          <div>
            <h1>Node JS Guru</h1>
            <p className="header-subtitle">Your AI assistant for Node.js</p>
          </div>
        </div>
      </header>

      <div className="messages-area">
        {messages.length === 1 && (
          <div className="welcome-suggestions">
            <p>Try asking:</p>
            <div className="suggestion-chips">
              {['What is Node.js?', 'How to create a server?', 'Explain Express.js', 'What is npm?'].map((s) => (
                <button key={s} className="chip" onClick={() => { setInput(s); document.querySelector('.input-wrapper input')?.focus() }}>
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role} ${i === messages.length - 1 ? 'message-enter' : ''}`}>
            {msg.role === 'assistant' && (
              <div className="avatar">
          <NodeIcon />
              </div>
            )}
            <div className="bubble">
              <div className="bubble-content">{msg.content}</div>
            </div>
          </div>
        ))}

        {loading && (
          <div className="message assistant">
            <div className="avatar">
                <NodeIcon />
            </div>
            <div className="bubble typing-bubble">
              <div className="typing-indicator">
                <span /><span /><span />
              </div>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <div className="input-area">
        <div className="input-wrapper">
          <input
            type="text"
            placeholder="Ask about Node.js..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={loading}
          />
          <button
            className={`send-btn ${input.trim() && !loading ? 'active' : ''}`}
            onClick={handleSend}
            disabled={loading || !input.trim()}
          >
            <SendIcon />
          </button>
        </div>
      </div>
    </div>
  )
}

export default App
