import React from 'react';
import { Task } from '../types';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { Clock, AlertCircle, CheckCircle, FileText } from 'lucide-react';

interface KanbanCardProps {
  task: Task;
  onClick: () => void;
  onDragStart?: (e: React.DragEvent) => void;
}

export const KanbanCard: React.FC<KanbanCardProps> = ({ task, onClick, onDragStart }) => {
  const getStatusColor = (status: Task['status']) => {
    const colors = {
      pending: 'border-gray-500',
      planning: 'border-blue-500',
      coding: 'border-yellow-500',
      qa: 'border-purple-500',
      merge: 'border-orange-500',
      completed: 'border-green-500',
      failed: 'border-red-500',
      cancelled: 'border-gray-500',
    };
    return colors[status] || 'border-gray-500';
  };

  const getPriorityIcon = () => {
    if (task.errors.length > 0) {
      return <AlertCircle className="w-4 h-4 text-red-500" />;
    }
    if (task.status === 'completed') {
      return <CheckCircle className="w-4 h-4 text-green-500" />;
    }
    return <Clock className="w-4 h-4 text-gray-400" />;
  };

  return (
    <div
      draggable
      onDragStart={onDragStart}
      onClick={onClick}
      className={`kanban-card bg-dark-800 border-l-4 ${getStatusColor(task.status)} rounded-lg p-4 mb-3 cursor-pointer hover:bg-dark-700 transition-all`}
    >
      <div className="flex items-start justify-between mb-2">
        <h4 className="font-semibold text-white text-sm line-clamp-2 flex-1">
          {task.title}
        </h4>
        {getPriorityIcon()}
      </div>

      {task.description && (
        <p className="text-gray-400 text-xs mb-3 line-clamp-2">
          {task.description}
        </p>
      )}

      <div className="flex items-center justify-between text-xs text-gray-500">
        <span className="flex items-center gap-1">
          <FileText className="w-3 h-3" />
          {task.requirements.length} req.
        </span>
        <span>
          {format(new Date(task.createdAt), 'dd MMM', { locale: ptBR })}
        </span>
      </div>

      {task.progress > 0 && (
        <div className="mt-3 w-full bg-dark-600 rounded-full h-1.5">
          <div
            className="bg-primary-500 h-1.5 rounded-full transition-all"
            style={{ width: `${task.progress}%` }}
          />
        </div>
      )}

      {task.artifacts.length > 0 && (
        <div className="mt-2 flex items-center gap-1 text-xs text-primary-400">
          <FileText className="w-3 h-3" />
          <span>{task.artifacts.length} arquivo(s)</span>
        </div>
      )}
    </div>
  );
};
