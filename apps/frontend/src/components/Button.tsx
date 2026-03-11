import React from 'react';
import { cn } from '../lib/utils';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'success' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  pill?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  className,
  variant = 'primary',
  size = 'md',
  pill = false,
  ...props
}) => {
  const variants = {
    primary: 'bg-primary-600 text-white hover:bg-primary-700 shadow-lg shadow-primary-900/20',
    secondary: 'bg-dark-700 text-gray-200 hover:bg-dark-600 border border-dark-600',
    ghost: 'bg-transparent text-gray-400 hover:bg-dark-700 hover:text-white',
    success: 'bg-green-600 text-white hover:bg-green-700 shadow-lg shadow-green-900/20',
    danger: 'bg-red-600 text-white hover:bg-red-700 shadow-lg shadow-red-900/20',
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-xs',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-3 text-base',
  };

  return (
    <button
      className={cn(
        'inline-flex items-center justify-center font-medium transition-all duration-200 active:scale-95 disabled:opacity-50 disabled:pointer-events-none',
        variants[variant],
        sizes[size],
        pill ? 'rounded-full' : 'rounded-lg',
        className
      )}
      {...props}
    />
  );
};
