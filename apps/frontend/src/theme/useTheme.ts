import { useState, useEffect } from 'react';
import { ColorTheme, Mode, ThemeConfig } from './types';

const THEME_STORAGE_KEY = 'cleudocode_theme_config';

export const useTheme = () => {
  const [config, setConfig] = useState<ThemeConfig>(() => {
    const saved = localStorage.getItem(THEME_STORAGE_KEY);
    return saved ? JSON.parse(saved) : { theme: 'default', mode: 'dark' };
  });

  useEffect(() => {
    localStorage.setItem(THEME_STORAGE_KEY, JSON.stringify(config));
    
    // Aplicar classes ao documento para Tailwind
    const root = window.document.documentElement;
    
    // Remover temas antigos
    root.classList.forEach(cls => {
      if (cls.startsWith('theme-') || cls === 'dark' || cls === 'light') {
        root.classList.remove(cls);
      }
    });

    root.classList.add(`theme-${config.theme}`);
    root.classList.add(config.mode);
    
    // Atualizar meta theme-color se necessário
  }, [config]);

  const setTheme = (theme: ColorTheme) => setConfig(prev => ({ ...prev, theme }));
  const setMode = (mode: Mode) => setConfig(prev => ({ ...prev, mode }));
  const toggleMode = () => setConfig(prev => ({ ...prev, mode: prev.mode === 'light' ? 'dark' : 'light' }));

  return {
    ...config,
    setTheme,
    setMode,
    toggleMode
  };
};
