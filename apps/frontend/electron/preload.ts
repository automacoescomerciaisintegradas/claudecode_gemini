import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('electron', {
  runTask: (taskData: any) => ipcRenderer.invoke('run-task', taskData),
  getTasks: () => ipcRenderer.invoke('get-tasks'),
  getAgentStatus: () => ipcRenderer.invoke('get-agent-status'),
  onTaskOutput: (callback: (data: string) => void) => {
    ipcRenderer.on('task-output', (event, data) => callback(data));
  },
  removeTaskOutputListener: (callback: (data: string) => void) => {
    ipcRenderer.removeListener('task-output', callback);
  },
});
