import { ChatKitProvider, Chat, ThreadList, Header } from "@openai/chatkit";
import "./App.css";

/**
 * Developer Onboarding Assistant
 * 
 * This ChatKit-based UI connects to the hosted multi-agent workflow
 * on Azure AI Foundry. Users can:
 * - Search for colleagues and team members
 * - Get personalized learning recommendations
 * - Request coding help and examples
 */
export default function App() {
  return (
    <ChatKitProvider endpoint="/chatkit">
      <div className="app-container">
        {/* Sidebar with thread history */}
        <aside className="sidebar">
          <div className="sidebar-header">
            <h1>💼 Developer Onboarding</h1>
            <p className="subtitle">Your AI Assistant for Getting Started</p>
          </div>
          <div className="thread-list-container">
            <ThreadList />
          </div>
          <div className="sidebar-footer">
            <p>Powered by Azure AI Foundry</p>
          </div>
        </aside>

        {/* Main chat area */}
        <main className="main-content">
          <Header />
          <Chat
            placeholder="Ask me anything! Try: 'Who should I connect with for learning Azure?' or 'Create a learning path for Kubernetes'"
          />
        </main>
      </div>
    </ChatKitProvider>
  );
}
