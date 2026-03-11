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
import { ThemeSelector } from '../theme/ThemeSelector';
import { cn } from '../lib/utils';
import { motion } from 'framer-motion';

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
    <motion.div
      initial={false}
      animate={{ width: sidebarOpen ? 256 : 64 }}
      className={cn(
        "h-full bg-dark-900 border-r border-dark-700 flex flex-col z-30 transition-colors duration-300",
        "shadow-[10px_0_30px_rgba(0,0,0,0.3)]"
      )}
    >
      <div className="flex flex-col h-full overflow-hidden">
        {/* Logo Section */}
        <div className="p-4 border-b border-dark-700 flex items-center justify-between h-[73px]">
          {sidebarOpen && (
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex items-center gap-3 overflow-hidden"
            >
              <div className="p-1.5 bg-primary-600 rounded-lg shadow-lg shadow-primary-900/20">
                <Cpu className="w-6 h-6 text-white" />
              </div>
              <span className="font-black text-xl text-white tracking-tighter uppercase">
                Cleudo<span className="text-primary-500">Code</span>
              </span>
            </motion.div>
          )}
          {!sidebarOpen && (
             <div className="mx-auto p-1.5 bg-primary-600 rounded-lg shadow-lg shadow-primary-900/20">
                <Cpu className="w-5 h-5 text-white" />
             </div>
          )}
        </div>

        {/* Menu Navigation */}
        <nav className="flex-1 p-3 space-y-1.5 overflow-y-auto no-scrollbar pt-6">
          {menuItems.map((item) => (
            <button
              key={item.id}
              onClick={() => onViewChange(item.id)}
              className={cn(
                "group w-full flex items-center gap-3 px-3 py-3 rounded-xl transition-all relative overflow-hidden",
                currentView === item.id
                  ? 'bg-primary-600/10 text-primary-400'
                  : 'text-gray-500 hover:bg-dark-800 hover:text-white'
              )}
            >
              {currentView === item.id && (
                <motion.div 
                  layoutId="sidebar-active"
                  className="absolute left-0 w-1 h-6 bg-primary-500 rounded-r-full"
                />
              )}
              
              <item.icon className={cn(
                "w-5 h-5 flex-shrink-0 transition-transform duration-300",
                currentView === item.id ? "scale-110" : "group-hover:scale-110"
              )} />
              
              {sidebarOpen && (
                <motion.div 
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="flex flex-1 items-center justify-between overflow-hidden"
                >
                  <span className="text-sm font-bold tracking-tight">{item.label}</span>
                  {item.badge !== null && item.badge > 0 && (
                    <span className="bg-primary-500 text-white text-[10px] font-black px-1.5 py-0.5 rounded-md min-w-[20px] text-center">
                      {item.badge}
                    </span>
                  )}
                </motion.div>
              )}
            </button>
          ))}
        </nav>

        {/* Theme & Status Section */}
        <div className="p-4 border-t border-dark-700 bg-dark-950/20 space-y-4">
          <div className={cn("flex items-center", sidebarOpen ? "justify-between" : "justify-center")}>
            <ThemeSelector />
            {sidebarOpen && (
              <button
                onClick={toggleSidebar}
                className="p-2 hover:bg-dark-700 rounded-lg text-gray-500 hover:text-white transition-colors"
                title="Fechar Sidebar"
              >
                <ChevronLeft className="w-5 h-5" />
              </button>
            )}
          </div>

          {!sidebarOpen && (
            <button
              onClick={toggleSidebar}
              className="mx-auto p-2 hover:bg-dark-700 rounded-lg text-gray-500 hover:text-white transition-colors flex"
            >
              <ChevronRight className="w-5 h-5" />
            </button>
          )}

          {sidebarOpen && (
            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-dark-800/50 border border-dark-700 rounded-xl p-3 space-y-2"
            >
              <div className="flex items-center justify-between text-[10px] font-black uppercase tracking-widest">
                <span className="text-gray-500 uppercase">Status do Sistema</span>
                <span className="text-green-500 flex items-center gap-1">
                   <div className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse" />
                   Online
                </span>
              </div>
              <div className="h-1 w-full bg-dark-700 rounded-full overflow-hidden">
                <motion.div 
                  initial={{ width: 0 }}
                  animate={{ width: '100%' }}
                  transition={{ duration: 1.5 }}
                  className="h-full bg-gradient-to-r from-primary-600 to-primary-400" 
                />
              </div>
            </motion.div>
          )}
        </div>
      </div>
    </motion.div>
  );
};

