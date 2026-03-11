import React from 'react';
import { KanbanColumn } from './KanbanColumn';
import { useAppStore, KANBAN_COLUMNS } from '../store/appStore';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import { Plus, Settings, RefreshCw } from 'lucide-react';
import { Button } from './index';
import { motion } from 'framer-motion';

export const KanbanBoard: React.FC = () => {
  const { setCreatingTask } = useAppStore();

  const handleNewTask = () => {
    setCreatingTask(true);
  };

  return (
    <DndProvider backend={HTML5Backend}>
      <motion.div 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="h-full flex flex-col bg-dark-900"
      >
        {/* Board Header */}
        <div className="flex items-center justify-between p-6 bg-dark-950/20 backdrop-blur-md border-b border-dark-700 h-[73px]">
          <div>
            <h1 className="text-xl font-black text-white tracking-tight">
               PLANEJAMENTO <span className="text-primary-500 font-medium">DE SPRINT</span>
            </h1>
          </div>
          
          <div className="flex items-center gap-2">
            <Button
              onClick={handleNewTask}
              variant="primary"
              size="sm"
              className="font-black uppercase tracking-widest text-[10px]"
            >
              <Plus className="w-3.5 h-3.5 mr-1" />
              Nova Tarefa
            </Button>
            
            <div className="h-4 w-[1px] bg-dark-700 mx-2" />

            <Button variant="ghost" size="sm" className="p-2">
              <RefreshCw className="w-4 h-4 text-gray-400" />
            </Button>
            
            <Button variant="ghost" size="sm" className="p-2">
              <Settings className="w-4 h-4 text-gray-400" />
            </Button>
          </div>
        </div>

        {/* Board Columns */}
        <div className="flex-1 overflow-x-auto overflow-y-hidden p-6 no-scrollbar">
          <motion.div 
            layout
            className="flex gap-6 h-full min-w-max"
          >
            {KANBAN_COLUMNS.map((column) => (
              <KanbanColumn key={column.id} column={column} />
            ))}
          </motion.div>
        </div>
      </motion.div>
    </DndProvider>
  );
};

