import { app, BrowserWindow, ipcMain } from 'electron';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

let mainWindow: BrowserWindow | null = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1024,
    minHeight: 768,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      preload: path.join(__dirname, 'preload.js'),
    },
    icon: path.join(__dirname, '../frontend/icons/icon.png'),
    titleBarStyle: 'default',
    frame: true,
  });

  // Carregar app
  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:3000');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, '../frontend/dist/index.html'));
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// IPC Handlers para comunicação com o backend Python
ipcMain.handle('run-task', async (event, taskData) => {
  // Executar tarefa no backend Python
  const { spawn } = await import('child_process');
  
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['run.py', '--title', taskData.title]);
    
    let output = '';
    let error = '';
    
    pythonProcess.stdout.on('data', (data) => {
      output += data.toString();
      mainWindow?.webContents.send('task-output', data.toString());
    });
    
    pythonProcess.stderr.on('data', (data) => {
      error += data.toString();
    });
    
    pythonProcess.on('close', (code) => {
      if (code === 0) {
        resolve({ success: true, output });
      } else {
        reject(new Error(error || 'Erro na execução'));
      }
    });
  });
});

ipcMain.handle('get-tasks', async () => {
  // Retornar lista de tarefas do backend
  return [];
});

ipcMain.handle('get-agent-status', async () => {
  // Retornar status dos agentes
  return {
    agents: [
      { name: 'PlanningAgent', state: 'idle' },
      { name: 'CodingAgent', state: 'idle' },
      { name: 'QAAgent', state: 'idle' },
      { name: 'MergeAgent', state: 'idle' },
    ],
  };
});
