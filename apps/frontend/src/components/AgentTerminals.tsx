import React from 'react';
import { AgentTerminal } from './AgentTerminal';
import { useAppStore } from '../store/appStore';
import { Plus, Terminal as TerminalIcon, X } from 'lucide-react';

interface AgentTerminalsProps {
  className?: string;
}

export const AgentTerminals: React.FC<AgentTerminalsProps> = ({ className = '' }) => {
  const { 
    terminalSessionIds, 
    getTerminalSession, 
    activeTerminalId, 
    setActiveTerminal, 
    addTerminalSession,
    removeTerminalSession
  } = useAppStore();

  const handleAddTerminal = () => {
    const { agents } = useAppStore.getState();
    const firstAgent = Object.values(agents)[0];
    
    if (firstAgent) {
      addTerminalSession({
        agentId: firstAgent.id,
        agentName: firstAgent.name,
        isActive: true,
      });
    } else {
      // Criar terminal genérico
      addTerminalSession({
        agentId: 'default',
        agentName: 'Terminal',
        isActive: true,
      });
    }
  };

  const handleCloseAll = () => {
    terminalSessionIds.forEach((id) => {
       removeTerminalSession(id);
    });
  };

  return (
    <div className={`flex flex-col h-full bg-dark-900 ${className}`}>
      {/* Terminals Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-dark-700">
        <div className="flex items-center gap-2">
          <TerminalIcon className="w-5 h-5 text-primary-400" />
          <h3 className="font-semibold text-white">Terminais de Agente</h3>
          <span className="bg-dark-700 text-gray-400 text-xs px-2 py-0.5 rounded-full">
            {terminalSessionIds.length}
          </span>
        </div>
        
        <div className="flex items-center gap-2">
          <button
            onClick={handleAddTerminal}
            className="flex items-center gap-1 bg-primary-600 hover:bg-primary-700 text-white px-3 py-1.5 rounded-lg text-sm transition-colors"
          >
            <Plus className="w-4 h-4" />
            Novo Terminal
          </button>
          
          {terminalSessionIds.length > 0 && (
            <button
              onClick={handleCloseAll}
              className="p-2 hover:bg-dark-700 rounded-lg transition-colors"
              title="Fechar todos"
            >
              <X className="w-4 h-4 text-gray-400" />
            </button>
          )}
        </div>
      </div>

      {/* Terminals Grid */}
      <div className="flex-1 overflow-auto p-4">
        {terminalSessionIds.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-gray-500">
            <TerminalIcon className="w-12 h-12 mb-4 opacity-20" />
            <p className="text-sm">Nenhum terminal ativo</p>
            <p className="text-xs mt-1">Clique em "Novo Terminal" para criar</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 h-full">
            {terminalSessionIds.map((sessionId) => {
              const session = getTerminalSession(sessionId);
              if (!session) return null;

              return (
                <div
                  key={sessionId}
                  className={`rounded-lg overflow-hidden border-2 transition-colors ${
                    activeTerminalId === sessionId
                      ? 'border-primary-500'
                      : 'border-dark-700 hover:border-dark-600'
                  }`}
                  onClick={() => setActiveTerminal(sessionId)}
                >
                  <AgentTerminal 
                    sessionId={sessionId} 
                    onClose={() => removeTerminalSession(sessionId)} 
                  />
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};
