import React from 'react';
import { cn } from '../lib/utils';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  noPadding?: boolean;
  hover?: boolean;
}

export const Card: React.FC<CardProps> = ({
  children,
  className,
  noPadding = false,
  hover = false
}) => {
  return (
    <div
      className={cn(
        'bg-dark-800 border border-dark-700 rounded-xl overflow-hidden scroll-smooth',
        !noPadding && 'p-4 sm:p-6',
        hover && 'hover:border-dark-600 hover:shadow-xl transition-all duration-300',
        className
      )}
    >
      {children}
    </div>
  );
};
