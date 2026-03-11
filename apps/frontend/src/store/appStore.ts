import { create } from 'zustand';
import { Task, TaskStatus, Agent, AgentState, TerminalSession, TerminalLine, Spec } from '../types';
import { v4 as uuidv4 } from 'uuid';
import { format } from 'date-fns';

// Definição das colunas do Kanban
export const KANBAN_COLUMNS = [
  { id: 'pending', title: 'Pendentes', status: 'pending' as TaskStatus, color: 'bg-gray-500', icon: '📋' },
  { id: 'planning', title: 'Planejamento', status: 'planning' as TaskStatus, color: 'bg-blue-500', icon: '📝' },
  { id: 'coding', title: 'Codificação', status: 'coding' as TaskStatus, color: 'bg-yellow-500', icon: '💻' },
  { id: 'qa', title: 'QA', status: 'qa' as TaskStatus, color: 'bg-purple-500', icon: '🔍' },
  { id: 'merge', title: 'Merge', status: 'merge' as TaskStatus, color: 'bg-orange-500', icon: '🔀' },
  { id: 'completed', title: 'Concluídos', status: 'completed' as TaskStatus, color: 'bg-green-500', icon: '✅' },
  { id: 'failed', title: 'Falhados', status: 'failed' as TaskStatus, color: 'bg-red-500', icon: '❌' },
];

const INITIAL_AGENTS: Record<string, Agent> = {
  'planning-id': {
    id: 'planning-id',
    name: 'Planning Agent',
    type: 'planning',
    state: 'idle',
    createdAt: new Date().toISOString(),
    history: [],
  },
  'coding-id': {
    id: 'coding-id',
    name: 'Coding Agent',
    type: 'coding',
    state: 'idle',
    createdAt: new Date().toISOString(),
    history: [],
  },
  'qa-id': {
    id: 'qa-id',
    name: 'QA Agent',
    type: 'qa',
    state: 'idle',
    createdAt: new Date().toISOString(),
    history: [],
  },
  'merge-id': {
    id: 'merge-id',
    name: 'Merge Agent',
    type: 'merge',
    state: 'idle',
    createdAt: new Date().toISOString(),
    history: [],
  },
  'lara-id': {
    id: 'lara-id',
    name: 'Lara ExecAssist',
    type: 'executive' as any,
    state: 'idle',
    createdAt: new Date().toISOString(),
    history: [],
  },
};

interface AppState {
  // Tasks
  tasks: Record<string, Task>;
  taskIds: string[];
  
  // Agents
  agents: Record<string, Agent>;
  agentIds: string[];
  
  // Terminal Sessions
  terminalSessions: Record<string, TerminalSession>;
  terminalSessionIds: string[];
  activeTerminalId?: string;
  
  // Specs
  specs: Record<string, Spec>;
  specIds: string[];
  
  // UI State
  selectedTaskId?: string;
  isCreatingTask: boolean;
  sidebarOpen: boolean;
  currentView: 'kanban' | 'terminals' | 'agents' | 'insights' | 'git' | 'settings';
  
  // Actions
  addTask: (task: Partial<Task>) => string;
  updateTask: (id: string, updates: Partial<Task>) => void;
  updateTaskStatus: (id: string, status: TaskStatus) => void;
  deleteTask: (id: string) => void;
  getTask: (id: string) => Task | undefined;
  getTasksByStatus: (status: TaskStatus) => Task[];
  
  addAgent: (agent: Partial<Agent>) => void;
  updateAgent: (id: string, updates: Partial<Agent>) => void;
  updateAgentState: (id: string, state: AgentState) => void;
  getAgent: (id: string) => Agent | undefined;
  
  addTerminalSession: (session: Partial<TerminalSession>) => string;
  addTerminalLine: (sessionId: string, line: Omit<TerminalLine, 'id' | 'timestamp'>) => void;
  setActiveTerminal: (id: string | undefined) => void;
  removeTerminalSession: (id: string) => void;
  getTerminalSession: (id: string) => TerminalSession | undefined;
  
  addSpec: (spec: Partial<Spec>) => void;
  updateSpec: (id: string, updates: Partial<Spec>) => void;
  getSpec: (id: string) => Spec | undefined;
  
  setSelectedTask: (id: string | undefined) => void;
  setCreatingTask: (isCreating: boolean) => void;
  toggleSidebar: () => void;
  setCurrentView: (view: 'kanban' | 'terminals' | 'agents' | 'insights' | 'git' | 'settings') => void;
}

export const useAppStore = create<AppState>((set, get) => ({
  // Initial State
  tasks: {},
  taskIds: [],
  agents: INITIAL_AGENTS,
  agentIds: Object.keys(INITIAL_AGENTS),
  terminalSessions: {},
  terminalSessionIds: [],
  activeTerminalId: undefined,
  specs: {},
  specIds: [],
  selectedTaskId: undefined,
  isCreatingTask: false,
  sidebarOpen: true,
  currentView: 'kanban',
  
  // Task Actions
  addTask: (taskData) => {
    const id = uuidv4();
    const now = format(new Date(), "yyyy-MM-dd'T'HH:mm:ss");
    
    const task: Task = {
      id,
      title: taskData.title || 'Nova Tarefa',
      description: taskData.description || '',
      status: taskData.status || 'pending',
      requirements: taskData.requirements || [],
      constraints: taskData.constraints || [],
      acceptanceCriteria: taskData.acceptanceCriteria || [],
      createdAt: now,
      updatedAt: now,
      progress: taskData.progress || 0,
      artifacts: taskData.artifacts || [],
      errors: taskData.errors || [],
    };
    
    set((state) => ({
      tasks: { ...state.tasks, [id]: task },
      taskIds: [...state.taskIds, id],
    }));
    
    return id;
  },
  
  updateTask: (id, updates) => {
    set((state) => ({
      tasks: {
        ...state.tasks,
        [id]: {
          ...state.tasks[id],
          ...updates,
          updatedAt: format(new Date(), "yyyy-MM-dd'T'HH:mm:ss"),
        },
      },
    }));
  },
  
  updateTaskStatus: (id, status) => {
    const statusProgress: Record<TaskStatus, number> = {
      pending: 0,
      planning: 20,
      coding: 40,
      qa: 60,
      merge: 80,
      completed: 100,
      failed: 0,
      cancelled: 0,
    };
    
    get().updateTask(id, { 
      status, 
      progress: statusProgress[status] || 0 
    });
  },
  
  deleteTask: (id) => {
    set((state) => {
      const { [id]: removed, ...remaining } = state.tasks;
      return {
        tasks: remaining,
        taskIds: state.taskIds.filter((taskId) => taskId !== id),
      };
    });
  },
  
  getTask: (id) => get().tasks[id],
  
  getTasksByStatus: (status) => {
    return Object.values(get().tasks).filter((task) => task.status === status);
  },
  
  // Agent Actions
  addAgent: (agentData) => {
    const id = agentData.id || uuidv4();
    const now = format(new Date(), "yyyy-MM-dd'T'HH:mm:ss");
    
    const agent: Agent = {
      id,
      name: agentData.name || 'Agent',
      type: agentData.type || 'coding',
      state: agentData.state || 'idle',
      createdAt: now,
      history: [],
    };
    
    set((state) => ({
      agents: { ...state.agents, [id]: agent },
      agentIds: [...state.agentIds, id],
    }));
  },
  
  updateAgent: (id, updates) => {
    set((state) => ({
      agents: {
        ...state.agents,
        [id]: { ...state.agents[id], ...updates },
      },
    }));
  },
  
  updateAgentState: (id, state) => {
    get().updateAgent(id, { state });
  },
  
  getAgent: (id) => get().agents[id],
  
  // Terminal Actions
  addTerminalSession: (sessionData) => {
    const id = uuidv4();
    const now = format(new Date(), "yyyy-MM-dd'T'HH:mm:ss");
    
    const session: TerminalSession = {
      id,
      agentId: sessionData.agentId || '',
      agentName: sessionData.agentName || 'Agent',
      taskId: sessionData.taskId,
      output: sessionData.output || [],
      isActive: sessionData.isActive ?? false,
      createdAt: now,
    };
    
    set((state) => ({
      terminalSessions: { ...state.terminalSessions, [id]: session },
      terminalSessionIds: [...state.terminalSessionIds, id],
    }));
    
    return id;
  },
  
  addTerminalLine: (sessionId, lineData) => {
    set((state) => {
      const session = state.terminalSessions[sessionId];
      if (!session) return state;
      
      const line: TerminalLine = {
        id: uuidv4(),
        type: lineData.type,
        content: lineData.content,
        timestamp: format(new Date(), "yyyy-MM-dd'T'HH:mm:ss"),
      };
      
      return {
        terminalSessions: {
          ...state.terminalSessions,
          [sessionId]: {
            ...session,
            output: [...session.output, line],
          },
        },
      };
    });
  },
  
  setActiveTerminal: (id) => {
    set({ activeTerminalId: id });
  },
  
  removeTerminalSession: (id) => {
    set((state) => {
      const { [id]: removed, ...remaining } = state.terminalSessions;
      return {
        terminalSessions: remaining,
        terminalSessionIds: state.terminalSessionIds.filter((sid) => sid !== id),
        activeTerminalId: state.activeTerminalId === id ? undefined : state.activeTerminalId,
      };
    });
  },
  
  getTerminalSession: (id) => get().terminalSessions[id],
  
  // Spec Actions
  addSpec: (specData) => {
    const id = specData.id || uuidv4();
    const now = format(new Date(), "yyyy-MM-dd'T'HH:mm:ss");
    
    const spec: Spec = {
      id,
      title: specData.title || 'Nova Spec',
      description: specData.description || '',
      requirements: specData.requirements || [],
      constraints: specData.constraints || [],
      acceptanceCriteria: specData.acceptanceCriteria || [],
      status: specData.status || 'pending',
      createdAt: now,
      updatedAt: now,
    };
    
    set((state) => ({
      specs: { ...state.specs, [id]: spec },
      specIds: [...state.specIds, id],
    }));
  },
  
  updateSpec: (id, updates) => {
    set((state) => ({
      specs: {
        ...state.specs,
        [id]: {
          ...state.specs[id],
          ...updates,
          updatedAt: format(new Date(), "yyyy-MM-dd'T'HH:mm:ss"),
        },
      },
    }));
  },
  
  getSpec: (id) => get().specs[id],
  
  // UI Actions
  setSelectedTask: (id) => {
    set({ selectedTaskId: id });
  },
  
  setCreatingTask: (isCreating) => {
    set({ isCreatingTask: isCreating });
  },
  
  toggleSidebar: () => {
    set((state) => ({ sidebarOpen: !state.sidebarOpen }));
  },
  
  setCurrentView: (view: 'kanban' | 'terminals' | 'agents' | 'insights' | 'git' | 'settings') => {
    set({ currentView: view });
  },
}));
