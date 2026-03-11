import React from 'react';
import { KanbanCard } from './KanbanCard';
import { useAppStore, KANBAN_COLUMNS } from '../store/appStore';
import { Plus } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '../lib/utils';

interface KanbanColumnProps {
  column: typeof KANBAN_COLUMNS[0];
}

export const KanbanColumn: React.FC<KanbanColumnProps> = ({ column }) => {
  const { getTasksByStatus, setSelectedTask, setCreatingTask } = useAppStore();
  const tasks = getTasksByStatus(column.status);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const taskId = e.dataTransfer.getData('taskId');
    const newStatus = column.status;
    
    if (taskId) {
      const { updateTaskStatus } = useAppStore.getState();
      updateTaskStatus(taskId, newStatus);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDragStart = (e: React.DragEvent, taskId: string) => {
    e.dataTransfer.setData('taskId', taskId);
    e.dataTransfer.effectAllowed = 'move';
  };

  const handleAddTask = () => {
    setCreatingTask(true);
  };

  return (
    <motion.div
      layout
      className="flex-1 min-w-[320px] max-w-sm bg-dark-950/20 rounded-2xl p-4 flex flex-col border border-dark-700/50"
      onDrop={handleDrop}
      onDragOver={handleDragOver}
    >
      {/* Column Header */}
      <div className="flex items-center justify-between mb-6 px-1">
        <div className="flex items-center gap-3">
          <div className={cn("w-2 h-2 rounded-full", column.color.replace('bg-', 'bg-opacity-50 '))}>
             <div className={cn("w-full h-full rounded-full animate-pulse", column.color)} />
          </div>
          <h3 className="font-black text-[11px] text-gray-400 uppercase tracking-[0.2em]">{column.title}</h3>
          <span className="bg-dark-800 text-gray-500 text-[10px] font-black px-2 py-0.5 rounded-lg border border-dark-700">
            {tasks.length}
          </span>
        </div>
        <button
          onClick={handleAddTask}
          className="p-1.5 hover:bg-primary-500/10 rounded-lg transition-colors group"
          title="Adicionar tarefa"
        >
          <Plus className="w-4 h-4 text-gray-600 group-hover:text-primary-400" />
        </button>
      </div>

      {/* Tasks List */}
      <div className="flex-1 overflow-y-auto overflow-x-hidden no-scrollbar space-y-3 min-h-[200px]">
        <AnimatePresence mode="popLayout">
          {tasks.map((task) => (
            <KanbanCard
              key={task.id}
              task={task}
              onClick={() => setSelectedTask(task.id)}
              onNativeDragStart={(e) => handleDragStart(e, task.id)}
            />
          ))}
        </AnimatePresence>
        
        {tasks.length === 0 && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 0.5 }}
            className="flex-1 flex flex-col items-center justify-center text-gray-600 text-xs py-12 border-2 border-dashed border-dark-800 rounded-xl"
          >
            <div className="text-2xl mb-2 grayscale opacity-50">📋</div>
            Sem tarefas
          </motion.div>
        )}
      </div>
    </motion.div>
  );
};

