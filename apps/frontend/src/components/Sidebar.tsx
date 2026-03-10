import React from 'react';
import { useAppStore } from '../store/appStore';
import { 
  LayoutDashboard, 
  Terminal, 
  Cpu, 
  Settings, 
  GitBranch,
  BarChart3,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react';

interface SidebarProps {
  currentView: string;
  onViewChange: (view: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ currentView, onViewChange }) => {
  const { sidebarOpen, toggleSidebar, agents, tasks } = useAppStore();
  
  const taskCount = Object.keys(tasks).length;
  const activeAgents = Object.values(agents).filter(a => a.state !== 'idle').length;

  const menuItems = [
    { id: 'kanban', icon: LayoutDashboard, label: 'Quadro Kanban', badge: taskCount },
    { id: 'terminals', icon: Terminal, label: 'Terminais', badge: null },
    { id: 'agents', icon: Cpu, label: 'Agentes', badge: activeAgents },
    { id: 'insights', icon: BarChart3, label: 'Insights', badge: null },
    { id: 'git', icon: GitBranch, label: 'Git', badge: null },
    { id: 'settings', icon: Settings, label: 'Configurações', badge: null },
  ];

  return (
    <div
      className={`h-full bg-dark-900 border-r border-dark-700 transition-all duration-300 ${
        sidebarOpen ? 'w-64' : 'w-16'
      }`}
    >
      <div className="flex flex-col h-full">
        {/* Logo */}
        <div className="p-4 border-b border-dark-700 flex items-center justify-between">
          {sidebarOpen && (
            <div className="flex items-center gap-2">
              <Cpu className="w-6 h-6 text-primary-400" />
              <span className="font-bold text-white">Multi-Agent</span>
            </div>
          )}
          <button
            onClick={toggleSidebar}
            className="p-2 hover:bg-dark-700 rounded-lg transition-colors"
          >
            {sidebarOpen ? (
              <ChevronLeft className="w-4 h-4 text-gray-400" />
            ) : (
              <ChevronRight className="w-4 h-4 text-gray-400" />
            )}
          </button>
        </div>

        {/* Menu */}
        <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
          {menuItems.map((item) => (
            <button
              key={item.id}
              onClick={() => onViewChange(item.id)}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors ${
                currentView === item.id
                  ? 'bg-primary-600/20 text-primary-400'
                  : 'text-gray-400 hover:bg-dark-700 hover:text-white'
              }`}
            >
              <item.icon className="w-5 h-5 flex-shrink-0" />
              {sidebarOpen && (
                <>
                  <span className="flex-1 text-left text-sm">{item.label}</span>
                  {item.badge !== null && item.badge !== undefined && (
                    <span className="bg-dark-700 text-gray-400 text-xs px-2 py-0.5 rounded-full">
                      {item.badge}
                    </span>
                  )}
                </>
              )}
            </button>
          ))}
        </nav>

        {/* Status */}
        {sidebarOpen && (
          <div className="p-4 border-t border-dark-700">
            <div className="bg-dark-800 rounded-lg p-3 space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="text-gray-400">Agentes Ativos</span>
                <span className="text-white font-medium">{activeAgents}</span>
              </div>
              <div className="flex items-center justify-between text-xs">
                <span className="text-gray-400">Tarefas</span>
                <span className="text-white font-medium">{taskCount}</span>
              </div>
              <div className="pt-2 border-t border-dark-700">
                <div className="flex items-center gap-2 text-xs">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                  <span className="text-gray-400">Sistema Online</span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
