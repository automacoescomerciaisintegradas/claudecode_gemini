import React from 'react';
import { KanbanCard } from './KanbanCard';
import { useAppStore, KANBAN_COLUMNS } from '../store/appStore';
import { TaskStatus } from '../types';
import { Plus } from 'lucide-react';

interface KanbanColumnProps {
  column: typeof KANBAN_COLUMNS[0];
}

export const KanbanColumn: React.FC<KanbanColumnProps> = ({ column }) => {
  const { getTasksByStatus, setSelectedTask, setCreatingTask, addTask } = useAppStore();
  const tasks = getTasksByStatus(column.status);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const taskId = e.dataTransfer.getData('taskId');
    const newStatus = column.status;
    
    if (taskId) {
      // Atualizar status da tarefa
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
    <div
      className="flex-1 min-w-[280px] max-w-sm bg-dark-900 rounded-xl p-4 flex flex-col"
      onDrop={handleDrop}
      onDragOver={handleDragOver}
    >
      {/* Column Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <span className="text-xl">{column.icon}</span>
          <h3 className="font-semibold text-white">{column.title}</h3>
          <span className="bg-dark-700 text-gray-400 text-xs px-2 py-0.5 rounded-full">
            {tasks.length}
          </span>
        </div>
        <button
          onClick={handleAddTask}
          className="p-1 hover:bg-dark-700 rounded transition-colors"
          title="Adicionar tarefa"
        >
          <Plus className="w-4 h-4 text-gray-400" />
        </button>
      </div>

      {/* Tasks */}
      <div className="flex-1 overflow-y-auto max-h-[calc(100vh-250px)]">
        {tasks.map((task) => (
          <KanbanCard
            key={task.id}
            task={task}
            onClick={() => setSelectedTask(task.id)}
            onDragStart={(e) => handleDragStart(e, task.id)}
          />
        ))}
      </div>

      {/* Empty State */}
      {tasks.length === 0 && (
        <div className="flex-1 flex items-center justify-center text-gray-500 text-sm py-8">
          Nenhuma tarefa
        </div>
      )}
    </div>
  );
};
