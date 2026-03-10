// Tipos globais do Electron
interface Window {
  electron: {
    runTask: (taskData: TaskData) => Promise<TaskResult>;
    getTasks: () => Promise<Task[]>;
    getAgentStatus: () => Promise<AgentStatusResponse>;
    onTaskOutput: (callback: (data: string) => void) => void;
    removeTaskOutputListener: (callback: (data: string) => void) => void;
  };
}

// Tipos de Tarefa
export interface Task {
  id: string;
  title: string;
  description: string;
  status: TaskStatus;
  requirements: string[];
  constraints: string[];
  acceptanceCriteria: string[];
  createdAt: string;
  updatedAt: string;
  assignedAgent?: string;
  progress: number;
  artifacts: string[];
  errors: string[];
}

export type TaskStatus = 
  | 'pending'
  | 'planning'
  | 'coding'
  | 'qa'
  | 'merge'
  | 'completed'
  | 'failed'
  | 'cancelled';

export interface TaskData {
  title: string;
  description?: string;
  requirements?: string[];
  constraints?: string[];
  acceptanceCriteria?: string[];
}

export interface TaskResult {
  success: boolean;
  output: string;
  errors?: string[];
  artifacts?: string[];
  metadata?: Record<string, any>;
}

// Tipos de Agente
export interface Agent {
  id: string;
  name: string;
  type: AgentType;
  state: AgentState;
  currentTaskId?: string;
  createdAt: string;
  history: AgentEvent[];
}

export type AgentType = 
  | 'planning'
  | 'coding'
  | 'qa'
  | 'merge'
  | 'orchestrator';

export type AgentState = 
  | 'idle'
  | 'planning'
  | 'executing'
  | 'waiting'
  | 'validating'
  | 'completed'
  | 'failed'
  | 'cancelled';

export interface AgentEvent {
  timestamp: string;
  event: string;
  action?: string;
  details?: Record<string, any>;
}

export interface AgentStatusResponse {
  agents: Array<{
    name: string;
    state: AgentState;
    currentTask?: string;
  }>;
}

// Tipos do Kanban
export interface KanbanColumn {
  id: string;
  title: string;
  status: TaskStatus;
  color: string;
  icon: string;
}

export interface KanbanState {
  columns: KanbanColumn[];
  tasks: Record<string, Task>;
  taskOrder: Record<string, string[]>;
}

// Tipos do Terminal
export interface TerminalSession {
  id: string;
  agentId: string;
  agentName: string;
  taskId?: string;
  output: TerminalLine[];
  isActive: boolean;
  createdAt: string;
}

export interface TerminalLine {
  id: string;
  type: 'input' | 'output' | 'error' | 'system';
  content: string;
  timestamp: string;
}

// Tipos de Contexto
export interface TaskContext {
  task_id: string;
  title: string;
  description: string;
  requirements: string[];
  constraints: string[];
  acceptance_criteria: string[];
  related_files?: string[];
  worktree_path?: string;
  branch_name?: string;
  metadata?: Record<string, any>;
}

// Tipos de Configuração
export interface AppConfig {
  maxParallelAgents: number;
  agentTimeoutMinutes: number;
  defaultModel: string;
  mainBranch: string;
  autoCommit: boolean;
  runTests: boolean;
  runLinting: boolean;
  runTypeCheck: boolean;
  enableMemoryLayer: boolean;
  enableAutoMerge: boolean;
}

// Tipos de Memory Layer
export interface MemoryLayer {
  totalTasks: number;
  successRate: number;
  commonIssues: Array<{
    issue: string;
    count: number;
  }>;
  optimizations: string[];
}

// Tipos de Especificação
export interface Spec {
  id: string;
  title: string;
  description: string;
  requirements: string[];
  constraints: string[];
  acceptanceCriteria: string[];
  status: TaskStatus;
  createdAt: string;
  updatedAt: string;
  result?: TaskResult;
}
