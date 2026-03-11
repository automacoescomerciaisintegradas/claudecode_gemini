import React from 'react';
import { useTheme, COLOR_THEMES } from './index';
import { Sun, Moon, Palette, Check } from 'lucide-react';
import { cn } from '../lib/utils';
import { motion, AnimatePresence } from 'framer-motion';

export const ThemeSelector: React.FC = () => {
  const { theme, mode, setTheme, toggleMode } = useTheme();
  const [isOpen, setIsOpen] = React.useState(false);

  return (
    <div className="relative flex items-center gap-2">
      <button
        onClick={toggleMode}
        className="p-2 hover:bg-dark-700 rounded-lg transition-colors text-gray-400 hover:text-white"
        title={mode === 'dark' ? 'Mudar para luz' : 'Mudar para trevas'}
      >
        {mode === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
      </button>

      <div className="relative">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className={cn(
            "p-2 rounded-lg transition-all flex items-center gap-2",
            isOpen ? "bg-dark-700 text-white" : "text-gray-400 hover:bg-dark-700 hover:text-white"
          )}
        >
          <Palette className="w-5 h-5" />
          <span className="hidden sm:inline text-xs font-bold uppercase tracking-wider">
            {COLOR_THEMES.find(t => t.id === theme)?.name}
          </span>
        </button>

        <AnimatePresence>
          {isOpen && (
            <>
              <div 
                className="fixed inset-0 z-10" 
                onClick={() => setIsOpen(false)} 
              />
              <motion.div
                initial={{ opacity: 0, y: 10, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: 10, scale: 0.95 }}
                className="absolute right-0 mt-2 w-56 bg-dark-800 border border-dark-700 rounded-xl shadow-2xl z-20 p-2 overflow-hidden"
              >
                <div className="grid grid-cols-1 gap-1">
                  {COLOR_THEMES.map((t) => (
                    <button
                      key={t.id}
                      onClick={() => {
                        setTheme(t.id);
                        setIsOpen(false);
                      }}
                      className={cn(
                        "flex items-center gap-3 p-2 rounded-lg w-full transition-all",
                        theme === t.id 
                          ? "bg-primary-600/20 text-primary-400" 
                          : "hover:bg-dark-700 text-gray-400 hover:text-white"
                      )}
                    >
                      <div className="flex gap-1 shrink-0">
                        <div 
                          className="w-4 h-4 rounded-full border border-white/10" 
                          style={{ backgroundColor: t.preview.primary }} 
                        />
                        <div 
                          className="w-4 h-4 rounded-full border border-white/10" 
                          style={{ backgroundColor: t.preview.accent }} 
                        />
                      </div>
                      <span className="flex-1 text-left text-sm font-medium">{t.name}</span>
                      {theme === t.id && <Check className="w-4 h-4" />}
                    </button>
                  ))}
                </div>
              </motion.div>
            </>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};
