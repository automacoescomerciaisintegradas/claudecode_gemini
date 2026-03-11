import React from 'react';
import { cn } from '../lib/utils';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input: React.FC<InputProps> = ({
  label,
  error,
  className,
  ...props
}) => {
  return (
    <div className="space-y-1.5">
      {label && (
        <label className="block text-xs font-bold text-gray-400 uppercase tracking-widest ml-1">
          {label}
        </label>
      )}
      <input
        className={cn(
          'w-full bg-dark-900 border border-dark-700 rounded-xl px-4 py-2.5 text-white placeholder-gray-600 transition-all duration-200 outline-none',
          'focus:border-primary-500/50 focus:ring-4 focus:ring-primary-500/10',
          'disabled:opacity-50 disabled:bg-dark-950 disabled:cursor-not-allowed',
          error ? 'border-red-500/50 focus:border-red-500' : '',
          className
        )}
        {...props}
      />
      {error && (
        <p className="text-xs text-red-400 ml-1 mt-1 font-medium italic">
          {error}
        </p>
      )}
    </div>
  );
};
