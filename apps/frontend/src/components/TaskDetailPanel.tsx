import React from 'react';
import { useAppStore } from '../store/appStore';
import { Task } from '../types';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { X, CheckCircle, AlertCircle, Clock, FileText, Trash2 } from 'lucide-react';

interface TaskDetailPanelProps {
  taskId: string;
  onClose: () => void;
}

export const TaskDetailPanel: React.FC<TaskDetailPanelProps> = ({ taskId, onClose }) => {
  const { getTask, updateTask, deleteTask, setSelectedTask } = useAppStore();
  const task = getTask(taskId);

  if (!task) {
    return null;
  }

  const getStatusColor = (status: Task['status']) => {
    const colors: Record<Task['status'], string> = {
      pending: 'bg-gray-500',
      planning: 'bg-blue-500',
      coding: 'bg-yellow-500',
      qa: 'bg-purple-500',
      merge: 'bg-orange-500',
      completed: 'bg-green-500',
      failed: 'bg-red-500',
      cancelled: 'bg-gray-500',
    };
    return colors[status] || 'bg-gray-500';
  };

  const handleDelete = () => {
    if (confirm('Tem certeza que deseja excluir esta tarefa?')) {
      deleteTask(taskId);
      setSelectedTask(undefined);
      onClose();
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex justify-end">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Panel */}
      <div className="relative w-full max-w-md bg-dark-800 h-full overflow-y-auto border-l border-dark-700 shadow-2xl">
        {/* Header */}
        <div className="sticky top-0 bg-dark-800 border-b border-dark-700 p-6 flex items-start justify-between gap-4">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <span className={`${getStatusColor(task.status)} text-white text-xs px-2 py-0.5 rounded-full`}>
                {task.status.toUpperCase()}
              </span>
            </div>
            <h2 className="text-xl font-bold text-white">{task.title}</h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-dark-700 rounded-lg transition-colors flex-shrink-0"
          >
            <X className="w-5 h-5 text-gray-400" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Description */}
          {task.description && (
            <div>
              <h3 className="text-sm font-medium text-gray-400 mb-2">Descrição</h3>
              <p className="text-white text-sm">{task.description}</p>
            </div>
          )}

          {/* Progress */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-medium text-gray-400">Progresso</h3>
              <span className="text-white text-sm">{task.progress}%</span>
            </div>
            <div className="w-full bg-dark-700 rounded-full h-2">
              <div
                className="bg-primary-500 h-2 rounded-full transition-all"
                style={{ width: `${task.progress}%` }}
              />
            </div>
          </div>

          {/* Requirements */}
          {task.requirements.length > 0 && (
            <div>
              <h3 className="text-sm font-medium text-gray-400 mb-3 flex items-center gap-2">
                <FileText className="w-4 h-4" />
                Requisitos
              </h3>
              <ul className="space-y-2">
                {task.requirements.map((req, index) => (
                  <li key={index} className="flex items-start gap-2 text-sm text-white">
                    <span className="text-primary-400 mt-0.5">•</span>
                    {req}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Acceptance Criteria */}
          {task.acceptanceCriteria.length > 0 && (
            <div>
              <h3 className="text-sm font-medium text-gray-400 mb-3 flex items-center gap-2">
                <CheckCircle className="w-4 h-4" />
                Critérios de Aceitação
              </h3>
              <ul className="space-y-2">
                {task.acceptanceCriteria.map((criteria, index) => (
                  <li key={index} className="flex items-start gap-2 text-sm text-white">
                    <span className="text-green-400 mt-0.5">✓</span>
                    {criteria}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Errors */}
          {task.errors.length > 0 && (
            <div>
              <h3 className="text-sm font-medium text-gray-400 mb-3 flex items-center gap-2">
                <AlertCircle className="w-4 h-4" />
                Erros
              </h3>
              <ul className="space-y-2">
                {task.errors.map((error, index) => (
                  <li key={index} className="flex items-start gap-2 text-sm text-red-400">
                    <AlertCircle className="w-4 h-4 mt-0.5 flex-shrink-0" />
                    {error}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Artifacts */}
          {task.artifacts.length > 0 && (
            <div>
              <h3 className="text-sm font-medium text-gray-400 mb-3 flex items-center gap-2">
                <FileText className="w-4 h-4" />
                Arquivos Gerados
              </h3>
              <ul className="space-y-2">
                {task.artifacts.map((artifact, index) => (
                  <li key={index} className="text-sm text-primary-400 font-mono">
                    {artifact}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Metadata */}
          <div className="pt-4 border-t border-dark-700 space-y-2 text-xs text-gray-500">
            <div className="flex items-center gap-2">
              <Clock className="w-3 h-3" />
              Criado em: {format(new Date(task.createdAt), "dd 'de' MMMM 'de' yyyy 'às' HH:mm", { locale: ptBR })}
            </div>
            <div className="flex items-center gap-2">
              <Clock className="w-3 h-3" />
              Atualizado em: {format(new Date(task.updatedAt), "dd 'de' MMMM 'de' yyyy 'às' HH:mm", { locale: ptBR })}
            </div>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="sticky bottom-0 bg-dark-800 border-t border-dark-700 p-6 flex items-center justify-between">
          <button
            onClick={handleDelete}
            className="flex items-center gap-2 text-red-400 hover:text-red-300 transition-colors"
          >
            <Trash2 className="w-4 h-4" />
            Excluir
          </button>
          
          <button
            onClick={onClose}
            className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors"
          >
            Fechar
          </button>
        </div>
      </div>
    </div>
  );
};
