import React from 'react';
import { cn } from '../lib/utils';

interface BadgeProps {
  variant?: 'default' | 'primary' | 'success' | 'warning' | 'error' | 'outline';
  className?: string;
  children: React.ReactNode;
}

export const Badge: React.FC<BadgeProps> = ({
  variant = 'default',
  className,
  children
}) => {
  const variants = {
    default: 'bg-dark-700 text-gray-400 border-dark-600',
    primary: 'bg-primary-500/10 text-primary-400 border-primary-500/20',
    success: 'bg-green-500/10 text-green-400 border-green-500/20',
    warning: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20',
    error: 'bg-red-500/10 text-red-400 border-red-500/20',
    outline: 'bg-transparent text-gray-400 border-dark-600',
  };

  return (
    <span
      className={cn(
        'inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold border',
        variants[variant],
        className
      )}
    >
      {children}
    </span>
  );
};
