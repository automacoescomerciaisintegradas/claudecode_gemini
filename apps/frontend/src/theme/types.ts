export type Mode = 'light' | 'dark';

export type ColorTheme = 'default' | 'dusk' | 'lime' | 'ocean' | 'retro' | 'neo' | 'forest';

export interface ThemePreviewColors {
  primary: string;
  secondary: string;
  accent: string;
  background: string;
}

export interface ColorThemeDefinition {
  id: ColorTheme;
  name: string;
  preview: ThemePreviewColors;
}

export interface ThemeConfig {
  theme: ColorTheme;
  mode: Mode;
}
