import { defineStore } from 'pinia';
import { ref } from 'vue';
import axios from 'axios';
import type { Project } from '@/types/index';

export const useProjectStore = defineStore('project', () => {
    const projects = ref<Project[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const fetchProjects = async () => {
        loading.value = true;
        error.value = null;
        try {
            const response = await axios.get('/api/projects');
            projects.value = response.data;
        } catch (err: any) {
            error.value = err instanceof Error ? err.message : String(err) || 'Failed to fetch projects';
        } finally {
            loading.value = false;
        }
    };

    const fetchProjectById = async (id: number | string) => {
        loading.value = true;
        error.value = null;
        try {
            const response = await axios.get(`/api/projects/${id}`);
            return response.data as Project;
        } catch (err: any) {
            error.value = err instanceof Error ? err.message : String(err) || 'Failed to fetch project';
            return null;
        } finally {
            loading.value = false;
        }
    };

    const addProject = async (project: Omit<Project, 'id'>) => {
        loading.value = true;
        error.value = null;
        try {
            await axios.post('/api/projects', project);
            await fetchProjects();
        } catch (err: any) {
            error.value = err instanceof Error ? err.message : String(err) || 'Failed to add project';
        } finally {
            loading.value = false;
        }
    };

    const removeProject = async (projectId: number) => {
        loading.value = true;
        error.value = null;
        try {
            await axios.delete(`/api/projects/${projectId}`);
            await fetchProjects();
        } catch (err: any) {
            error.value = err instanceof Error ? err.message : String(err) || 'Failed to remove project';
        } finally {
            loading.value = false;
        }
    };

    return { projects, loading, error, fetchProjects, fetchProjectById, addProject, removeProject };
});