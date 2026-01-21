import { defineStore } from 'pinia';

export interface User {
  id: number;
  fullName: string;
  email: string;
  role: 'Admin' | 'Editor' | 'Viewer';
  status: 'Active' | 'Inactive' | 'Pending';
  avatar: string;
  about: string;
}

export const useTeamStore = defineStore('team', {
  state: () => ({
    users: [] as User[],
    loading: false,
    error: null as string | null,
  }),
  getters: {
    getUserById: (state) => (userId: number): User | undefined => {
      return state.users.find(user => user.id === userId);
    }
  },
  actions: {
    async fetchUsers() {
      if (this.users.length > 0) return; // Evita fetches innecesarios

      this.loading = true;
      this.error = null;
      try {
        // Simulación de una llamada a API
        await new Promise(resolve => setTimeout(resolve, 1000));

        const mockUsers: User[] = [
          {
            id: 1,
            fullName: 'Esteban Selvaggi',
            email: 'esteban.selvaggi@example.com',
            role: 'Admin',
            status: 'Active',
            avatar: 'https://randomuser.me/api/portraits/men/1.jpg',
            about: 'Lead developer with 10 years of experience in Vue and Node.js.'
          },
          {
            id: 2,
            fullName: 'Jane Smith',
            email: 'jane.smith@example.com',
            role: 'Editor',
            status: 'Active',
            avatar: 'https://randomuser.me/api/portraits/women/2.jpg',
            about: 'Content specialist and technical writer.'
          },
          {
            id: 3,
            fullName: 'John Doe',
            email: 'john.doe@example.com',
            role: 'Viewer',
            status: 'Inactive',
            avatar: 'https://randomuser.me/api/portraits/men/3.jpg',
            about: 'Junior developer, passionate about frontend technologies.'
          },
          {
            id: 4,
            fullName: 'Peter Jones',
            email: 'peter.jones@example.com',
            role: 'Editor',
            status: 'Pending',
            avatar: 'https://randomuser.me/api/portraits/men/4.jpg',
            about: 'UX/UI designer with a keen eye for detail.'
          }
        ];
        this.users = mockUsers;
      } catch (err) {
        this.error = 'Failed to fetch users. Please try again later.';
        console.error(err);
      } finally {
        this.loading = false;
      }
    }
  }
});
