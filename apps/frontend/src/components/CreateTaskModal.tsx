import React, { useState } from 'react';
import { useAppStore } from '../store/appStore';
import { X } from 'lucide-react';

interface CreateTaskModalProps {
  onClose: () => void;
}

export const CreateTaskModal: React.FC<CreateTaskModalProps> = ({ onClose }) => {
  const { addTask, setCreatingTask } = useAppStore();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    requirements: [''],
    constraints: [''],
    acceptanceCriteria: [''],
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const task = {
      title: formData.title,
      description: formData.description,
      requirements: formData.requirements.filter(r => r.trim()),
      constraints: formData.constraints.filter(c => c.trim()),
      acceptanceCriteria: formData.acceptanceCriteria.filter(a => a.trim()),
    };

    addTask(task);
    setCreatingTask(false);
    onClose();
  };

  const addField = (field: keyof typeof formData) => {
    setFormData(prev => ({
      ...prev,
      [field]: [...prev[field], ''],
    }));
  };

  const updateField = (field: keyof typeof formData, index: number, value: string) => {
    setFormData(prev => ({
      ...prev,
      [field]: prev[field].map((item, i) => i === index ? value : item),
    }));
  };

  const removeField = (field: keyof typeof formData, index: number) => {
    setFormData(prev => ({
      ...prev,
      [field]: prev[field].filter((_, i) => i !== index),
    }));
  };

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-dark-800 rounded-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto border border-dark-700">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-dark-700">
          <h2 className="text-xl font-bold text-white">Nova Tarefa</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-dark-700 rounded-lg transition-colors"
          >
            <X className="w-5 h-5 text-gray-400" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* Title */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Título *
            </label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
              className="w-full bg-dark-900 border border-dark-600 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Ex: Criar API de usuários"
              required
            />
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Descrição
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
              className="w-full bg-dark-900 border border-dark-600 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
              rows={3}
              placeholder="Descreva o que precisa ser feito..."
            />
          </div>

          {/* Requirements */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Requisitos
            </label>
            <div className="space-y-2">
              {formData.requirements.map((req, index) => (
                <div key={index} className="flex gap-2">
                  <input
                    type="text"
                    value={req}
                    onChange={(e) => updateField('requirements', index, e.target.value)}
                    className="flex-1 bg-dark-900 border border-dark-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder={`Requisito ${index + 1}`}
                  />
                  {formData.requirements.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeField('requirements', index)}
                      className="p-2 hover:bg-red-500/20 rounded-lg transition-colors"
                    >
                      <X className="w-4 h-4 text-red-400" />
                    </button>
                  )}
                </div>
              ))}
            </div>
            <button
              type="button"
              onClick={() => addField('requirements')}
              className="mt-2 text-sm text-primary-400 hover:text-primary-300"
            >
              + Adicionar requisito
            </button>
          </div>

          {/* Acceptance Criteria */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Critérios de Aceitação
            </label>
            <div className="space-y-2">
              {formData.acceptanceCriteria.map((criteria, index) => (
                <div key={index} className="flex gap-2">
                  <input
                    type="text"
                    value={criteria}
                    onChange={(e) => updateField('acceptanceCriteria', index, e.target.value)}
                    className="flex-1 bg-dark-900 border border-dark-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder={`Critério ${index + 1}`}
                  />
                  {formData.acceptanceCriteria.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeField('acceptanceCriteria', index)}
                      className="p-2 hover:bg-red-500/20 rounded-lg transition-colors"
                    >
                      <X className="w-4 h-4 text-red-400" />
                    </button>
                  )}
                </div>
              ))}
            </div>
            <button
              type="button"
              onClick={() => addField('acceptanceCriteria')}
              className="mt-2 text-sm text-primary-400 hover:text-primary-300"
            >
              + Adicionar critério
            </button>
          </div>

          {/* Actions */}
          <div className="flex items-center justify-end gap-3 pt-4 border-t border-dark-700">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-gray-300 hover:bg-dark-700 rounded-lg transition-colors"
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="px-6 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors"
            >
              Criar Tarefa
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
