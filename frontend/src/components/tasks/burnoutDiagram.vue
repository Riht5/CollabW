<template>
  <div class="d-flex flex-column gap-md">
      <!-- 图表容器 -->
      <div ref="chart" class="chart"></div>
  </div>
</template>

<script lang="ts">
import { ref, defineComponent, onMounted, onBeforeUnmount } from 'vue';
import { ProjectProgress } from '@/types/index';
import * as echarts from 'echarts'

export default defineComponent({
  name: 'BurnDownChart',
  props: {
    actualProgresses: {
      type: Array as () => ProjectProgress[],
      required: true
    },
    idealProgresses: {
      type: Array as () => ProjectProgress[],
      default: []
    },
  },
  setup(props) {
    const chart = ref<HTMLDivElement | null>(null)
    let myChart: echarts.ECharts | null = null

    // 渲染燃尽图函数
    const renderChart = (data: ProjectProgress[], idealData: ProjectProgress[]) => {
      if (!chart.value) return;
      
      if (!myChart) {
        myChart = echarts.init(chart.value);
      }
      
      // 处理实际进度数据
      const actualData = data.map(item => ({
        name: item.date,
        value: [item.date, (1 - item.progress) * 100]
      })).sort((a, b) => 
        new Date(a.name).getTime() - new Date(b.name).getTime()
      );
      
      // 处理理想进度数据
      const idealLineData = idealData.map(item => ({
        name: item.date,
        value: [item.date, (1 - item.progress) * 100]
      })).sort((a, b) => 
        new Date(a.name).getTime() - new Date(b.name).getTime()
      );

      // 配置图表选项
      const option: echarts.EChartsOption = {
        tooltip: {
          trigger: 'axis',
          formatter: (params: any) => {
            interface TooltipParam {
              seriesName: string;
              value: [string, number];
            }
            
            const paramsArray = params as TooltipParam[];
            
            const actualParam = paramsArray.find(p => p.seriesName === '实际进度');
            const idealParam = paramsArray.find(p => p.seriesName === '理想进度');
            
            const date = params[0].name;
            const actual = actualParam?.value[1] ?? null;
            const ideal = idealParam?.value[1] ?? 0;
            return `
              <div>日期: ${date}</div>
              <div>实际剩余: ${actual?.toFixed(1)}%</div>
              <div>理想剩余: ${ideal?.toFixed(1)}%</div>
            `;
          }
        },
        legend: {
          data: ['实际进度', '理想进度'],
          bottom: 10
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '15%',
          top: '10%',
          containLabel: true
        },
        xAxis: {
          type: 'time',
          boundaryGap: [0, '10%'], // [起点, 终点] 百分比格式
          axisLabel: {
            formatter: (value: number) => {
              return echarts.time.format(value, '{yyyy}-{MM}-{dd}', false);
            },
          }
        },
        yAxis: {
          type: 'value',
          min: 0,
          max: 100,
          axisLabel: {
            formatter: '{value}%'
          },
          name: '剩余工作量'
        },
        series: [
        {
          name: '实际进度',
          type: 'line',
          data: actualData,
          lineStyle: { width: 2, color: '#3498db' },
          itemStyle: { color: '#3498db' },
        },
        {
          name: '理想进度',
          showSymbol: false,
          type: 'line',
          data: idealLineData,
          lineStyle: { width: 2, type: 'dashed', color: '#FF4500' },
          smooth: true
        }
      ],
        dataZoom: [
          {
            type: 'inside',
            start: 0,
            end: 100
          },
          {
            type: 'slider',
            start: 0,
            end: 100,
            handleSize: '80%',
            handleStyle: {
              color: '#fff',
              shadowBlur: 3,
              shadowColor: 'rgba(0, 0, 0, 0.6)',
              shadowOffsetX: 2,
              shadowOffsetY: 2
            }
          }
        ]
      };
      
      // 应用配置并渲染图表
      myChart.setOption(option);
    };

    onMounted(async () => {
      renderChart(props.actualProgresses, props.idealProgresses)
    });

    // 在组件卸载时销毁图表实例
    onBeforeUnmount(() => {
      myChart?.dispose()
    })

    return {
      chart,
    }
  }
})
</script>

<style scoped>
.chart {
  width: 100%;
  height: 400px;
}
</style>
