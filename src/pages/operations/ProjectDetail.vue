<template>
  <v-container>
    <div v-if="project">
      <v-card>
        <v-card-title class="headline">{{ project.name }}</v-card-title>
        <v-card-subtitle>{{ project.status }}</v-card-subtitle>
        <v-card-text>
          <p>{{ project.description }}</p>

          <h3 class="mt-6 mb-2">Project Tasks</h3>
          <v-data-table
            :headers="taskHeaders"
            :items="tasks"
            item-key="id"
            class="elevation-1"
            no-data-text="No tasks found for this project."
          >
          </v-data-table>
        </v-card-text>
      </v-card>
    </div>
    <div v-else>
      <v-alert type="error">
        Project not found.
      </v-alert>
    </div>
  </v-container>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { useProjectsStore } from '@/stores/projectsStore';
import { VDataTable } from 'vuetify/labs/VDataTable';

const route = useRoute();
const projectsStore = useProjectsStore();

// Get the project ID from the route params and convert it to a number
const projectId = computed(() => parseInt(route.params.id, 10));

// Find the project from the store using the ID
const project = computed(() => {
  return projectsStore.projects.find(p => p.id === projectId.value);
});

// Filter tasks that belong to the current project
const tasks = computed(() => {
  if (!project.value) {
    return [];
  }
  return projectsStore.tasks.filter(t => t.projectId === projectId.value);
});

// Define headers for the tasks data table
const taskHeaders = [
  { title: 'Task Name', key: 'name' },
  { title: 'Description', key: 'description' },
  { title: 'Status', key: 'status' },
];
</script>

<style scoped>
.headline {
  font-weight: 500;
}
</style>
