import { ColorThemeDefinition } from './types';

export const COLOR_THEMES: ColorThemeDefinition[] = [
  {
    id: 'default',
    name: 'Default',
    preview: { primary: '#3b82f6', secondary: '#1e293b', accent: '#0ea5e9', background: '#0f172a' }
  },
  {
    id: 'dusk',
    name: 'Dusk',
    preview: { primary: '#8b5cf6', secondary: '#1e1b4b', accent: '#d946ef', background: '#0c0a09' }
  },
  {
    id: 'lime',
    name: 'Lime',
    preview: { primary: '#84cc16', secondary: '#14532d', accent: '#a3e635', background: '#020617' }
  },
  {
    id: 'ocean',
    name: 'Ocean',
    preview: { primary: '#0891b2', secondary: '#164e63', accent: '#22d3ee', background: '#082f49' }
  },
  {
    id: 'retro',
    name: 'Retro',
    preview: { primary: '#f97316', secondary: '#431407', accent: '#fbbf24', background: '#1c1917' }
  },
  {
    id: 'neo',
    name: 'Neo',
    preview: { primary: '#ff00ff', secondary: '#1a1a1a', accent: '#00ffff', background: '#000000' }
  },
  {
    id: 'forest',
    name: 'Forest',
    preview: { primary: '#10b981', secondary: '#064e3b', accent: '#34d399', background: '#022c22' }
  }
];
