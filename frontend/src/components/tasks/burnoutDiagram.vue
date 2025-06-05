<template>
  <div class="d-flex flex-column gap-md">
    <!-- <div v-for="task in tasks" :key="task.id" class="card">
      <div class="card-body">
      <div class="d-flex justify-between align-start mb-md">
        <h4 class="mb-0">{{ task.name }}</h4>
        <div class="d-flex gap-sm">
          <span class="workload-badge" :class="task.workload">
          {{ getWorkloadText(task.workload) }}
          </span>
          <span class="status-badge" :class="{ completed: task.finished, pending: !task.finished }">
          {{ task.finished ? '已完成' : '进行中' }}
          </span>
        </div>
      </div> -->
      
    <div class="burn-down-container">
        <!-- 图表容器 -->
        <div ref="chart" class="chart"></div>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, defineComponent, onMounted, onBeforeUnmount, nextTick } from 'vue';
import { ProjectProgress } from '@/types/index';
import axios from 'axios'
import * as echarts from 'echarts'

// // 定义燃尽图数据接口
// interface BurnDownData {
//   dates: string[]
//   idealRemain: number[]
//   actualRemain: number[]
// }

// // 示例数据
// const exampleData: BurnDownData = {
//   dates: [
//     '2025-06-01',
//     '2025-06-02',
//     '2025-06-03',
//     '2025-06-04',
//     '2025-06-05',
//     '2025-06-06',
//     '2025-06-07',
//     '2025-06-08',
//     '2025-06-09',
//     '2025-06-10'
//   ],
//   idealRemain: [100, 90, 80, 70, 60, 50, 40, 30, 20, 10],
//   actualRemain: [100, 85, 75, 65, 55, 45, 42, 28, 15, 8]
// }

// 定义组件
export default defineComponent({
  name: 'BurnDownChart',
  props: {
    projectProgresses: {
      type: Array as () => ProjectProgress[],
      required: true
    }
  },
  setup(props) {
    const chart = ref<HTMLDivElement | null>(null)
    let myChart: echarts.ECharts | null = null

    // 渲染燃尽图函数
    const renderChart = (data: ProjectProgress[]) => {
      if (!chart.value) return

      myChart?.dispose()
      myChart = echarts.init(chart.value)

      myChart.setOption({
        title: {
          text: '燃尽图（Burndown Chart）',
          left: 'center',
          top: 20,
          textStyle: { fontSize: 16, fontWeight: 'bold' }
        },
        tooltip: { trigger: 'axis' },
        legend: { data: ['理想剩余', '实际剩余'], top: 50 },
        grid: { left: '10%', right: '10%', bottom: '15%' },
        xAxis: {
          type: 'category',
          data: data.map((item) => item.date),  // 这里应该是一个日期数组
          boundaryGap: false,
          axisLabel: {
            rotate: 45,
            formatter: (val: string) => val.slice(5)
          }
        },
        yAxis: { type: 'value', name: '剩余工作量占比（%）' },
        series: [
          {
            name: '理想剩余',
            type: 'line',
            data: data.map((item) => item.progress),  // 使用 progress 数据
            smooth: true,
            lineStyle: { type: 'dashed', color: '#FF0000' },
            itemStyle: { color: '#FF0000' }
          },
          {
            name: '实际剩余',
            type: 'line',
            data: data.map((item) => 1 - item.progress),  // 使用 progress 数据
            smooth: true,
            lineStyle: { color: '#00A0E9' },
            itemStyle: { color: '#00A0E9' }
          }
        ]
      })
    }

    // 在组件挂载后渲染图表
    onMounted(() => {
      nextTick(() => {
        renderChart(props.projectProgresses)  // 访问 props.projectProgresses
      })
      window.addEventListener('resize', () => {
        myChart?.resize()
      })
    })

    // 在组件卸载时销毁图表实例
    onBeforeUnmount(() => {
      myChart?.dispose()
    })

    return {
      chart
    }
  }
})
</script>

<style scoped>
.burn-down-container {
  width: 100%;
  min-height: 400px; /* 确保至少有 400px 高度 */
}

.chart {
  width: 100%;
  height: 400px;     /* 图表主体也要给一个非 0 的高度 */
}
</style>