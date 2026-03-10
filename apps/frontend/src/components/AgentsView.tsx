import React from 'react';
import { useAppStore } from '../store/appStore';
import { Cpu, Activity, Clock, CheckCircle } from 'lucide-react';

export const AgentsView: React.FC = () => {
  const { agents, agentIds } = useAppStore();

  const getAgentColor = (state: string) => {
    const colors: Record<string, string> = {
      idle: 'bg-gray-500',
      planning: 'bg-blue-500',
      executing: 'bg-yellow-500',
      waiting: 'bg-orange-500',
      validating: 'bg-purple-500',
      completed: 'bg-green-500',
      failed: 'bg-red-500',
      cancelled: 'bg-gray-500',
    };
    return colors[state] || 'bg-gray-500';
  };

  const getAgentIcon = (type: string) => {
    const icons: Record<string, string> = {
      planning: '📝',
      coding: '💻',
      qa: '🔍',
      merge: '🔀',
      orchestrator: '🎯',
    };
    return icons[type] || '🤖';
  };

  return (
    <div className="h-full bg-dark-900 p-6 overflow-y-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white mb-2">Agentes</h1>
        <p className="text-gray-400 text-sm">
          Gerencie e monitore os agentes autônomos do sistema
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div className="bg-dark-800 rounded-xl p-4 border border-dark-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary-500/20 rounded-lg">
              <Cpu className="w-5 h-5 text-primary-400" />
            </div>
            <div>
              <p className="text-gray-400 text-xs">Total de Agentes</p>
              <p className="text-white font-bold text-lg">{agentIds.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-dark-800 rounded-xl p-4 border border-dark-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-green-500/20 rounded-lg">
              <Activity className="w-5 h-5 text-green-400" />
            </div>
            <div>
              <p className="text-gray-400 text-xs">Agentes Ativos</p>
              <p className="text-white font-bold text-lg">
                {agentIds.filter(id => {
                  const agent = agents[id];
                  return agent && agent.state !== 'idle';
                }).length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-dark-800 rounded-xl p-4 border border-dark-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-500/20 rounded-lg">
              <Clock className="w-5 h-5 text-blue-400" />
            </div>
            <div>
              <p className="text-gray-400 text-xs">Em Espera</p>
              <p className="text-white font-bold text-lg">
                {agentIds.filter(id => {
                  const agent = agents[id];
                  return agent && agent.state === 'waiting';
                }).length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-dark-800 rounded-xl p-4 border border-dark-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-purple-500/20 rounded-lg">
              <CheckCircle className="w-5 h-5 text-purple-400" />
            </div>
            <div>
              <p className="text-gray-400 text-xs">Completados</p>
              <p className="text-white font-bold text-lg">
                {agentIds.filter(id => {
                  const agent = agents[id];
                  return agent && agent.state === 'completed';
                }).length}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Agents Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
        {agentIds.map((agentId) => {
          const agent = agents[agentId];
          if (!agent) return null;

          return (
            <div
              key={agentId}
              className="bg-dark-800 rounded-xl p-4 border border-dark-700 hover:border-dark-600 transition-colors"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{getAgentIcon(agent.type)}</span>
                  <div>
                    <h3 className="font-semibold text-white">{agent.name}</h3>
                    <p className="text-xs text-gray-400 capitalize">{agent.type}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <div className={`w-2 h-2 rounded-full ${getAgentColor(agent.state)} agent-pulse`} />
                  <span className="text-xs text-gray-400 capitalize">{agent.state}</span>
                </div>
              </div>

              {agent.currentTaskId && (
                <div className="bg-dark-900 rounded-lg p-3 mb-3">
                  <p className="text-xs text-gray-400 mb-1">Tarefa Atual</p>
                  <p className="text-sm text-white font-mono truncate">
                    {agent.currentTaskId}
                  </p>
                </div>
              )}

              <div className="flex items-center justify-between text-xs text-gray-500">
                <span>ID: {agent.id.slice(0, 8)}</span>
                <span>{new Date(agent.createdAt).toLocaleDateString()}</span>
              </div>
            </div>
          );
        })}

        {agentIds.length === 0 && (
          <div className="col-span-full flex flex-col items-center justify-center py-12 text-gray-500">
            <Cpu className="w-12 h-12 mb-4 opacity-20" />
            <p className="text-sm">Nenhum agente registrado</p>
            <p className="text-xs mt-1">Os agentes serão inicializados automaticamente</p>
          </div>
        )}
      </div>
    </div>
  );
};
