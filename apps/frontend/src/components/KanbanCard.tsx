import React from 'react';
import { Task } from '../types';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import { Clock, AlertCircle, CheckCircle, FileText, MoreHorizontal } from 'lucide-react';
import { motion } from 'framer-motion';
import { Card, Badge, AvatarGroup, Avatar } from './index';
import { cn } from '../lib/utils';

interface KanbanCardProps {
  task: Task;
  onClick: () => void;
  onNativeDragStart?: (e: React.DragEvent) => void;
}

export const KanbanCard: React.FC<KanbanCardProps> = ({ task, onClick, onNativeDragStart }) => {
  const getStatusColor = (status: Task['status']) => {
    const colors = {
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

  const getPriorityIcon = () => {
    if (task.errors.length > 0) {
      return <AlertCircle className="w-4 h-4 text-red-500" />;
    }
    if (task.status === 'completed') {
      return <CheckCircle className="w-4 h-4 text-green-500" />;
    }
    return <Clock className="w-4 h-4 text-gray-500" />;
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      whileHover={{ y: -4, transition: { duration: 0.2 } }}
      whileTap={{ scale: 0.98 }}
    >
      <div
        draggable
        onDragStart={onNativeDragStart}
        onClick={onClick}
        className="cursor-grab active:cursor-grabbing group h-full"
      >
      <Card 
        className={cn(
          "relative border-dark-700/50 hover:border-primary-500/30 hover:shadow-[0_10px_30px_rgba(0,0,0,0.5)] transition-all",
          "before:absolute before:left-0 before:top-4 before:bottom-4 before:w-1 before:rounded-r-full",
          getStatusColor(task.status).replace('bg-', 'before:bg-')
        )}
        noPadding
      >
        <div className="p-4 space-y-4">
          <div className="flex items-start justify-between gap-3">
             <div className="space-y-1 flex-1">
                <div className="flex items-center gap-2">
                   <Badge variant="outline" className="text-[8px] font-black uppercase tracking-widest px-1">
                      TASK-{task.id.slice(0, 4)}
                   </Badge>
                   {task.progress === 100 && (
                      <Badge variant="success" className="px-1">PRONTO</Badge>
                   )}
                </div>
                <h4 className="font-bold text-white text-sm leading-tight group-hover:text-primary-400 transition-colors">
                  {task.title}
                </h4>
             </div>
             <button className="text-gray-600 hover:text-white transition-colors">
                <MoreHorizontal className="w-4 h-4" />
             </button>
          </div>

          {task.description && (
            <p className="text-gray-500 text-xs line-clamp-2 leading-relaxed italic">
              {task.description}
            </p>
          )}

          <div className="pt-2 flex items-center justify-between border-t border-dark-700/30">
            <div className="flex items-center gap-3">
               <span className="flex items-center gap-1.5 text-[10px] font-bold text-gray-500">
                  <FileText className="w-3 h-3 text-primary-500/50" />
                  {task.requirements.length}
               </span>
               <span className="flex items-center gap-1.5 text-[10px] font-bold text-gray-500">
                  {getPriorityIcon()}
                  {format(new Date(task.createdAt), 'dd MMM', { locale: ptBR })}
               </span>
            </div>
            
            <AvatarGroup>
               <Avatar name="AI" size="xs" className="border-dark-800" />
               <Avatar name="System" size="xs" className="border-dark-800 bg-primary-900/50" />
            </AvatarGroup>
          </div>
        </div>

        {task.progress > 0 && task.progress < 100 && (
          <div className="absolute bottom-0 left-0 w-full h-1 bg-dark-900">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${task.progress}%` }}
              className="bg-primary-500 h-full shadow-[0_0_10px_rgba(14,165,233,0.5)]"
            />
          </div>
        )}
      </Card>
      </div>
    </motion.div>
  );
};

