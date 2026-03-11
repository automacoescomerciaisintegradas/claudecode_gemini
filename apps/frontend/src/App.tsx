import React from 'react';
import { Sidebar } from './components/Sidebar';
import { KanbanBoard } from './components/KanbanBoard';
import { AgentTerminals } from './components/AgentTerminals';
import { AgentsView } from './components/AgentsView';
import { CreateTaskModal } from './components/CreateTaskModal';
import { TaskDetailPanel } from './components/TaskDetailPanel';
import { useAppStore } from './store/appStore';
import { useTheme } from './theme';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from './lib/utils';

const App: React.FC = () => {
  const { isCreatingTask, selectedTaskId, setCreatingTask, setSelectedTask, currentView, setCurrentView } = useAppStore();
  const { theme, mode } = useTheme();

  const renderView = () => {
    return (
      <AnimatePresence mode="wait">
        <motion.div
          key={currentView}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.2 }}
          className="h-full w-full"
        >
          {(() => {
            switch (currentView) {
              case 'kanban':
                return <KanbanBoard />;
              case 'terminals':
                return <AgentTerminals />;
              case 'agents':
                return <AgentsView />;
              case 'insights':
              case 'git':
              case 'settings':
                return (
                  <div className="h-full flex items-center justify-center bg-dark-900 text-gray-400">
                    <div className="text-center space-y-4">
                      <div className="w-16 h-16 bg-dark-800 rounded-2xl border border-dark-700 flex items-center justify-center mx-auto animate-pulse">
                         <div className="w-8 h-8 bg-primary-500/20 rounded-full" />
                      </div>
                      <div>
                        <h2 className="text-xl font-black text-white uppercase tracking-tighter">Em Desenvolvimento</h2>
                        <p className="text-sm font-medium text-gray-500">A visão de {currentView} estará disponível em breve</p>
                      </div>
                    </div>
                  </div>
                );
              default:
                return <KanbanBoard />;
            }
          })()}
        </motion.div>
      </AnimatePresence>
    );
  };

  return (
    <div className={cn(
      "flex h-screen overflow-hidden transition-colors duration-500",
      mode === 'dark' ? "bg-dark-950 text-white" : "bg-gray-50 text-dark-900",
      `theme-${theme}`
    )}>
      {/* Sidebar - Navigation */}
      <Sidebar currentView={currentView} onViewChange={setCurrentView} />

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col min-w-0 relative">
        <div className="flex-1 overflow-hidden relative">
           {renderView()}
        </div>
      </main>

      {/* Modals & Overlays */}
      <AnimatePresence>
        {isCreatingTask && (
          <CreateTaskModal onClose={() => setCreatingTask(false)} />
        )}

        {selectedTaskId && (
          <TaskDetailPanel
            taskId={selectedTaskId}
            onClose={() => setSelectedTask(undefined)}
          />
        )}
      </AnimatePresence>
    </div>
  );
};

export default App;
