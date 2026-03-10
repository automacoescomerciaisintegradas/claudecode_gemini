import React from 'react';
import { KanbanColumn } from './KanbanColumn';
import { useAppStore, KANBAN_COLUMNS } from '../store/appStore';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import { Plus, Settings, RefreshCw } from 'lucide-react';

export const KanbanBoard: React.FC = () => {
  const { setCreatingTask } = useAppStore();

  const handleNewTask = () => {
    setCreatingTask(true);
  };

  return (
    <DndProvider backend={HTML5Backend}>
      <div className="h-full flex flex-col bg-dark-900">
        {/* Board Header */}
        <div className="flex items-center justify-between p-6 border-b border-dark-700">
          <div>
            <h1 className="text-2xl font-bold text-white mb-1">
              Quadro Kanban
            </h1>
            <p className="text-gray-400 text-sm">
              Gerenciamento visual de tarefas do planejamento até a conclusão
            </p>
          </div>
          
          <div className="flex items-center gap-3">
            <button
              onClick={handleNewTask}
              className="flex items-center gap-2 bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg transition-colors"
            >
              <Plus className="w-4 h-4" />
              Nova Tarefa
            </button>
            
            <button className="p-2 hover:bg-dark-700 rounded-lg transition-colors">
              <RefreshCw className="w-4 h-4 text-gray-400" />
            </button>
            
            <button className="p-2 hover:bg-dark-700 rounded-lg transition-colors">
              <Settings className="w-4 h-4 text-gray-400" />
            </button>
          </div>
        </div>

        {/* Board Columns */}
        <div className="flex-1 overflow-x-auto p-6">
          <div className="flex gap-4 h-full">
            {KANBAN_COLUMNS.map((column) => (
              <KanbanColumn key={column.id} column={column} />
            ))}
          </div>
        </div>
      </div>
    </DndProvider>
  );
};
