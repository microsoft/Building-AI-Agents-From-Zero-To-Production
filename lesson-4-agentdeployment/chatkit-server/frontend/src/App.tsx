import { ChatKit, useChatKit } from "@openai/chatkit-react";
import "./App.css";

const CHATKIT_API_URL = "/chatkit";
const CHATKIT_API_DOMAIN_KEY = "domain_pk_localhost_dev";

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
  const chatkit = useChatKit({
    api: {
      url: CHATKIT_API_URL,
      domainKey: CHATKIT_API_DOMAIN_KEY,
    },
    startScreen: {
      greeting:
        "Welcome to the Developer Onboarding Assistant! I'm here to help you get started on your journey. Ask me anything about finding colleagues, learning resources, or coding help.",
      prompts: [
        {
          label: "Find Team Members",
          prompt: "Who should I connect with for learning Azure?",
        },
        {
          label: "Learning Path",
          prompt: "Create a learning path for Kubernetes",
        },
        {
          label: "Coding Help",
          prompt: "Show me an example of a Python FastAPI server",
        },
        {
          label: "Getting Started",
          prompt: "What are the first things I should do as a new developer?",
        },
      ],
    },
    composer: {
      placeholder:
        "Ask me anything! Try: 'Who should I connect with for learning Azure?' or 'Create a learning path for Kubernetes'",
    },
  });

  return (
    <div className="app-container">
      {/* Sidebar with branding */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <h1>💼 Developer Onboarding</h1>
          <p className="subtitle">Your AI Assistant for Getting Started</p>
        </div>
        <div className="sidebar-content">
          <p className="help-text">
            I can help you with:
          </p>
          <ul className="help-list">
            <li>🔍 Finding colleagues and mentors</li>
            <li>📚 Learning recommendations</li>
            <li>💻 Coding examples and help</li>
            <li>🚀 Onboarding best practices</li>
          </ul>
        </div>
        <div className="sidebar-footer">
          <p>Powered by Azure AI Foundry</p>
        </div>
      </aside>

      {/* Main chat area */}
      <main className="main-content">
        <ChatKit control={chatkit.control} style={{ height: "100%" }} />
      </main>
    </div>
  );
}
