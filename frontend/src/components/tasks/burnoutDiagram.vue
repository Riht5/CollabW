<template>
  <div class="burndown-container">
    <!-- 数据统计卡片 -->
    <div class="stats-cards" v-if="actualProgresses.length > 0">
      <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-content">
          <div class="stat-label">当前进度</div>
          <div class="stat-value">{{ getCurrentProgress() }}%</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🎯</div>
        <div class="stat-content">
          <div class="stat-label">预期进度</div>
          <div class="stat-value">{{ getExpectedProgress() }}%</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" :class="getProgressStatusIcon()">{{ getProgressStatusEmoji() }}</div>
        <div class="stat-content">
          <div class="stat-label">进度状态</div>
          <div class="stat-value" :class="getProgressStatusClass()">{{ getProgressStatus() }}</div>
        </div>
      </div>
    </div>

    <!-- 图表容器 -->
    <div ref="chart" class="chart"></div>
  </div>
</template>

<script lang="ts">
import { ref, defineComponent, onMounted, onBeforeUnmount, watch } from 'vue';
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

    // 获取当前进度
    const getCurrentProgress = () => {
      if (props.actualProgresses.length === 0) return 0;
      const latest = props.actualProgresses[props.actualProgresses.length - 1];
      return Math.round(latest.progress * 100);
    };

    // 获取预期进度
    const getExpectedProgress = () => {
      if (props.idealProgresses.length === 0) return 0;
      const latest = props.idealProgresses[props.idealProgresses.length - 1];
      return Math.round(latest.progress * 100);
    };

    // 获取进度状态
    const getProgressStatus = () => {
      const current = getCurrentProgress();
      const expected = getExpectedProgress();
      const diff = current - expected;
      
      if (diff >= 10) return '超前';
      if (diff >= 0) return '正常';
      if (diff >= -10) return '略微延后';
      return '严重延后';
    };

    const getProgressStatusClass = () => {
      const status = getProgressStatus();
      return {
        '超前': 'status-ahead',
        '正常': 'status-normal',
        '略微延后': 'status-behind',
        '严重延后': 'status-critical'
      }[status] || 'status-normal';
    };

    const getProgressStatusEmoji = () => {
      const status = getProgressStatus();
      return {
        '超前': '🚀',
        '正常': '✅',
        '略微延后': '⚠️',
        '严重延后': '🚨'
      }[status] || '✅';
    };

    const getProgressStatusIcon = () => {
      return getProgressStatusClass();
    };

    // 渲染燃尽图函数
    const renderChart = (data: ProjectProgress[], idealData: ProjectProgress[]) => {
      if (!chart.value) return;
      
      if (!myChart) {
        myChart = echarts.init(chart.value);
        
        // 添加窗口resize监听
        window.addEventListener('resize', () => {
          myChart?.resize();
        });
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
        backgroundColor: '#ffffff',
        tooltip: {
          trigger: 'axis',
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          borderColor: '#e0e0e0',
          borderWidth: 1,
          textStyle: {
            color: '#333'
          },
          formatter: (params: any) => {
            interface TooltipParam {
              seriesName: string;
              value: [string, number];
            }
            
            const paramsArray = params as TooltipParam[];
            const actualParam = paramsArray.find(p => p.seriesName === '实际进度');
            const idealParam = paramsArray.find(p => p.seriesName === '理想进度');
            
            const date = new Date(params[0].value[0]).toLocaleDateString();
            const actual = actualParam?.value[1] ?? null;
            const ideal = idealParam?.value[1] ?? 0;
            
            return `
              <div style="padding: 8px;">
                <div style="font-weight: bold; margin-bottom: 4px;">📅 ${date}</div>
                <div style="color: #3498db;">📊 实际剩余: ${actual?.toFixed(1)}%</div>
                <div style="color: #FF4500;">🎯 理想剩余: ${ideal?.toFixed(1)}%</div>
                ${actual !== null ? `<div style="margin-top: 4px; color: ${actual > ideal ? '#e74c3c' : '#27ae60'};">
                  ${actual > ideal ? '⚠️ 进度延后' : '✅ 进度正常'}
                </div>` : ''}
              </div>
            `;
          }
        },
        legend: {
          data: ['实际进度', '理想进度'],
          bottom: 15,
          textStyle: {
            color: '#333333',
            fontSize: 13
          },
          itemStyle: {
            borderWidth: 0
          }
        },
        grid: {
          left: '8%',
          right: '5%',
          bottom: '15%',
          top: '15%',
          containLabel: true
        },
        xAxis: {
          type: 'time',
          boundaryGap: [0, '5%'],
          axisLabel: {
            formatter: (value: number) => {
              return echarts.time.format(value, '{MM}-{dd}', false);
            },
            color: '#333333',
            fontSize: 12,
            rotate: 45
          },
          axisLine: {
            show: true,
            lineStyle: {
              color: '#d0d0d0',
              width: 2
            }
          },
          axisTick: {
            show: true,
            lineStyle: {
              color: '#d0d0d0',
              width: 1
            }
          },
          splitLine: {
            show: true,
            lineStyle: {
              color: '#f5f5f5',
              width: 1,
              type: 'solid'
            }
          }
        },
        yAxis: {
          type: 'value',
          min: 0,
          max: 100,
          axisLabel: {
            formatter: '{value}%',
            color: '#333333',
            fontSize: 12
          },
          name: '剩余工作量',
          nameTextStyle: {
            color: '#333333',
            fontSize: 14,
            fontWeight: 'bold'
          },
          axisLine: {
            show: true,
            lineStyle: {
              color: '#d0d0d0',
              width: 2
            }
          },
          axisTick: {
            show: true,
            lineStyle: {
              color: '#d0d0d0',
              width: 1
            }
          },
          splitLine: {
            show: true,
            lineStyle: {
              color: '#f5f5f5',
              width: 1,
              type: 'solid'
            }
          }
        },
        series: [
          {
            name: '实际进度',
            type: 'line',
            data: actualData,
            lineStyle: { 
              width: 3, 
              color: '#3498db',
              shadowColor: 'rgba(52, 152, 219, 0.3)',
              shadowBlur: 10,
              shadowOffsetY: 3
            },
            itemStyle: { 
              color: '#3498db',
              borderWidth: 2,
              borderColor: '#fff'
            },
            symbol: 'circle',
            symbolSize: 8,
            smooth: false
          },
          {
            name: '理想进度',
            type: 'line',
            data: idealLineData,
            lineStyle: { 
              width: 3, 
              type: 'dashed', 
              color: '#FF4500',
              shadowColor: 'rgba(255, 69, 0, 0.3)',
              shadowBlur: 8,
              shadowOffsetY: 2
            },
            itemStyle: { 
              color: '#FF4500',
              borderWidth: 2,
              borderColor: '#fff'
            },
            symbol: 'diamond',
            symbolSize: 6,
            smooth: true,
            showSymbol: false
          }
        ],
        animation: true,
        animationDuration: 1000,
        animationEasing: 'cubicOut'
      };
      
      myChart.setOption(option, true);
    };

    // 监听数据变化
    watch(() => [props.actualProgresses, props.idealProgresses], () => {
      renderChart(props.actualProgresses, props.idealProgresses);
    }, { deep: true });

    onMounted(() => {
      renderChart(props.actualProgresses, props.idealProgresses);
    });

    onBeforeUnmount(() => {
      window.removeEventListener('resize', () => {});
      myChart?.dispose();
    });

    return {
      chart,
      getCurrentProgress,
      getExpectedProgress,
      getProgressStatus,
      getProgressStatusClass,
      getProgressStatusEmoji,
      getProgressStatusIcon
    };
  }
});
</script>

<style scoped>
.burndown-container {
  width: 100%;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 1rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 12px;
  border: 1px solid #dee2e6;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  font-size: 2rem;
  margin-right: 1rem;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: white;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: #6c757d;
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}

.status-ahead { color: #27ae60; }
.status-normal { color: #3498db; }
.status-behind { color: #f39c12; }
.status-critical { color: #e74c3c; }

.chart {
  width: 100%;
  height: 450px;
  border-radius: 8px;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .stats-cards {
    grid-template-columns: 1fr;
  }
  
  .chart {
    height: 350px;
  }
}
</style>
