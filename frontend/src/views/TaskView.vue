<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { Task } from '@/types/index';
import { useTaskStore } from '@/stores/task';

export default defineComponent({
  name: 'TaskView',
  setup() {
    const route = useRoute();
    const taskId = route.params.id as string;
    const task = ref<Task | null>(null);
    const taskStore = useTaskStore();

    onMounted(async () => {
      task.value = await taskStore.getTaskById(taskId);
    });

    const editTask = () => {
      // TODO
    };

    const deleteTask = async () => {
      // TODO
    };

    return {
      task,
      editTask,
      deleteTask,
    };
  },
});
</script>