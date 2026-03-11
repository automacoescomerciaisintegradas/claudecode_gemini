import React, { useEffect, useRef } from 'react';
import { Terminal } from '@xterm/xterm';
import { FitAddon } from '@xterm/addon-fit';
import '@xterm/xterm/css/xterm.css';
import { useAppStore } from '../store/appStore';
import { X, Maximize2, Minimize2 } from 'lucide-react';

interface AgentTerminalProps {
  sessionId: string;
  onClose?: () => void;
}

export const AgentTerminal: React.FC<AgentTerminalProps> = ({ sessionId, onClose }) => {
  const terminalRef = useRef<HTMLDivElement>(null);
  const terminalInstance = useRef<Terminal | null>(null);
  const fitAddon = useRef<FitAddon | null>(null);
  
  const { getTerminalSession, addTerminalLine, removeTerminalSession, setActiveTerminal } = useAppStore();
  const session = getTerminalSession(sessionId);

  useEffect(() => {
    if (!terminalRef.current || !session) return;

    // Configurar terminal
    const term = new Terminal({
      cursorBlink: true,
      fontSize: 14,
      fontFamily: 'JetBrains Mono, monospace',
      theme: {
        background: '#0f172a',
        foreground: '#e2e8f0',
        cursor: '#0ea5e9',
        cursorAccent: '#0f172a',
        selection: 'rgba(14, 165, 233, 0.3)',
        black: '#1e293b',
        red: '#ef4444',
        green: '#22c55e',
        yellow: '#eab308',
        blue: '#3b82f6',
        magenta: '#a855f7',
        cyan: '#06b6d4',
        white: '#f1f5f9',
        brightBlack: '#475569',
        brightRed: '#f87171',
        brightGreen: '#4ade80',
        brightYellow: '#facc15',
        brightBlue: '#60a5fa',
        brightMagenta: '#c084fc',
        brightCyan: '#22d3ee',
        brightWhite: '#ffffff',
      },
      scrollback: 10000,
    });

    const fit = new FitAddon();
    term.loadAddon(fit);
    term.open(terminalRef.current);
    fit.fit();

    terminalInstance.current = term;
    fitAddon.current = fit;

    // Escrever output existente
    session.output.forEach((line) => {
      const color = line.type === 'error' ? '\x1b[31m' : 
                    line.type === 'input' ? '\x1b[36m' : 
                    line.type === 'system' ? '\x1b[33m' : '';
      const reset = '\x1b[0m';
      term.writeln(`${color}${line.content}${reset}`);
    });

    // WebSocket - Conectar ao backend
    const ws = new WebSocket(`ws://localhost:8000/ws/terminal/${sessionId}`);
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      addTerminalLine(sessionId, {
        type: data.type,
        content: data.content
      });
    };

    ws.onopen = () => {
      addTerminalLine(sessionId, { type: 'system', content: '>>> Conexão estabelecida com o servidor de agentes.' });
    };

    ws.onerror = () => {
      addTerminalLine(sessionId, { type: 'error', content: '>>> Erro na conexão com o servidor.' });
    };

    ws.onclose = () => {
      addTerminalLine(sessionId, { type: 'system', content: '>>> Conexão encerrada.' });
    };

    // Handler para entrada do usuário (digitação)
    term.onData((data) => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(data);
      }
    });

    // Listener para novo output no store (para atualizar o xterm)
    const unsubscribe = useAppStore.subscribe(
      (state) => state.terminalSessions[sessionId],
      (newSession) => {
        if (newSession && terminalInstance.current) {
          const lastLine = newSession.output[newSession.output.length - 1];
          if (lastLine) {
            const color = lastLine.type === 'error' ? '\x1b[31m' : 
                          lastLine.type === 'input' ? '\x1b[36m' : 
                          lastLine.type === 'system' ? '\x1b[33m' : 
                          lastLine.type === 'success' ? '\x1b[32m' : '';
            const reset = '\x1b[0m';
            
            // Para inputs (echo), usamos write para não pular linha
            if (lastLine.type === 'input') {
              terminalInstance.current.write(`${color}${lastLine.content}${reset}`);
            } else {
              terminalInstance.current.writeln(`${color}${lastLine.content}${reset}`);
            }
          }
        }
      }
    );

    // Resize handler
    const handleResize = () => fitAddon.current?.fit();
    window.addEventListener('resize', handleResize);

    return () => {
      unsubscribe();
      ws.close();
      window.removeEventListener('resize', handleResize);
      term.dispose();
    };
  }, [sessionId, session, addTerminalLine]);

  useEffect(() => {
    if (fitAddon.current) {
      setTimeout(() => fitAddon.current?.fit(), 100);
    }
  }, []);

  if (!session) {
    return null;
  }

  return (
    <div className="flex flex-col h-full bg-dark-900 rounded-lg overflow-hidden border border-dark-700">
      {/* Terminal Header */}
      <div className="flex items-center justify-between px-4 py-2 bg-dark-800 border-b border-dark-700">
        <div className="flex items-center gap-2">
          <div className="flex gap-1.5">
            <div className="w-3 h-3 rounded-full bg-red-500" />
            <div className="w-3 h-3 rounded-full bg-yellow-500" />
            <div className="w-3 h-3 rounded-full bg-green-500" />
          </div>
          <span className="text-gray-400 text-sm ml-2">
            {session.agentName}
            {session.taskId && ` - ${session.taskId.slice(0, 8)}`}
          </span>
        </div>
        
        <div className="flex items-center gap-2">
          <button
            onClick={() => setActiveTerminal(sessionId)}
            className="p-1 hover:bg-dark-700 rounded transition-colors"
            title="Maximizar"
          >
            <Maximize2 className="w-4 h-4 text-gray-400" />
          </button>
          {onClose && (
            <button
              onClick={() => {
                removeTerminalSession(sessionId);
                onClose();
              }}
              className="p-1 hover:bg-red-500/20 rounded transition-colors"
              title="Fechar"
            >
              <X className="w-4 h-4 text-gray-400 hover:text-red-400" />
            </button>
          )}
        </div>
      </div>

      {/* Terminal Body */}
      <div ref={terminalRef} className="flex-1 overflow-hidden" />
    </div>
  );
};
