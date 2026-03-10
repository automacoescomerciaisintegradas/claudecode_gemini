import React, { useState } from 'react';
import { Sidebar } from './Sidebar';
import { KanbanBoard } from './KanbanBoard';
import { AgentTerminals } from './AgentTerminals';
import { AgentsView } from './AgentsView';
import { CreateTaskModal } from './CreateTaskModal';
import { TaskDetailPanel } from './TaskDetailPanel';
import { useAppStore } from '../store/appStore';

type View = 'kanban' | 'terminals' | 'agents' | 'insights' | 'git' | 'settings';

const App: React.FC = () => {
  const [currentView, setCurrentView] = useState<View>('kanban');
  const { isCreatingTask, selectedTaskId } = useAppStore();

  const renderView = () => {
    switch (currentView) {
      case 'kanban':
        return <KanbanBoard />;
      case 'terminals':
        return <AgentTerminals />;
      case 'agents':
        return <AgentsView />;
      case 'insights':
        return (
          <div className="h-full flex items-center justify-center bg-dark-900 text-gray-400">
            <div className="text-center">
              <h2 className="text-xl font-semibold mb-2">Em Desenvolvimento</h2>
              <p className="text-sm">A visão de Insights estará disponível em breve</p>
            </div>
          </div>
        );
      case 'git':
        return (
          <div className="h-full flex items-center justify-center bg-dark-900 text-gray-400">
            <div className="text-center">
              <h2 className="text-xl font-semibold mb-2">Em Desenvolvimento</h2>
              <p className="text-sm">A visão de Git estará disponível em breve</p>
            </div>
          </div>
        );
      case 'settings':
        return (
          <div className="h-full flex items-center justify-center bg-dark-900 text-gray-400">
            <div className="text-center">
              <h2 className="text-xl font-semibold mb-2">Em Desenvolvimento</h2>
              <p className="text-sm">As configurações estarão disponíveis em breve</p>
            </div>
          </div>
        );
      default:
        return <KanbanBoard />;
    }
  };

  return (
    <div className="flex h-screen bg-dark-900 overflow-hidden">
      {/* Sidebar */}
      <Sidebar currentView={currentView} onViewChange={setCurrentView} />

      {/* Main Content */}
      <main className="flex-1 overflow-hidden">
        {renderView()}
      </main>

      {/* Modals */}
      {isCreatingTask && (
        <CreateTaskModal onClose={() => useAppStore.getState().setCreatingTask(false)} />
      )}

      {selectedTaskId && (
        <TaskDetailPanel
          taskId={selectedTaskId}
          onClose={() => useAppStore.getState().setSelectedTask(undefined)}
        />
      )}
    </div>
  );
};

export default App;
