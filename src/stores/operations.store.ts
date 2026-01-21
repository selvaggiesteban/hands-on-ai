import { defineStore } from 'pinia';

interface Task {
  id: number;
  title: string;
  description: string;
  status: 'pending' | 'in-progress' | 'completed';
  dueDate: string;
}

interface Project {
  id: number;
  name: string;
  description: string;
  startDate: string;
  endDate: string;
  status: 'active' | 'inactive' | 'completed';
  tasks: Task[];
}

interface OperationsState {
  projects: Project[];
  tasks: Task[];
}

export const useOperationsStore = defineStore('operations', {
  state: (): OperationsState => ({
    projects: [
      {
        id: 1,
        name: 'Project Alpha',
        description: 'This is the first project.',
        startDate: '2024-01-01',
        endDate: '2024-12-31',
        status: 'active',
        tasks: [
          { id: 101, title: 'Task 1 for Alpha', description: 'Description for task 1', status: 'completed', dueDate: '2024-02-01' },
          { id: 102, title: 'Task 2 for Alpha', description: 'Description for task 2', status: 'in-progress', dueDate: '2024-03-01' },
        ],
      },
      {
        id: 2,
        name: 'Project Beta',
        description: 'This is the second project.',
        startDate: '2024-02-01',
        endDate: '2025-01-31',
        status: 'active',
        tasks: [
            { id: 201, title: 'Task 1 for Beta', description: 'Description for task 1', status: 'pending', dueDate: '2024-04-01' },
        ],
      },
      {
        id: 3,
        name: 'Project Gamma',
        description: 'This is a completed project.',
        startDate: '2023-01-01',
        endDate: '2023-12-31',
        status: 'completed',
        tasks: [],
      },
    ],
    tasks: [], // Can be used for tasks not directly associated with a project or a flat list
  }),
  getters: {
    getProjects: (state) => state.projects,
    getProjectById: (state) => (id: number) => {
      return state.projects.find(p => p.id === id);
    },
  },
  actions: {
    // Actions to fetch or modify data can be added here later
  },
});
