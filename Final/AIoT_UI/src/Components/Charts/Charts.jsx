import { useEffect, useRef } from "react";
import * as echarts from "echarts";



export function PieBarChart(props) {
  const chartRef = useRef(null);
  useEffect(() => {
    let chartInstance = echarts.init(chartRef.current);
    const option = {
        tooltip: {
          show: true,
        },
        legend: {
          bottom: '1%',
          left: 'center',
          textStyle: {
            color: '#fff',
            }
        },
        series: [
          {
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            label: {
              show: true,
              position: 'center'
            },
            data: [
                {   
                    value: props.value,
                    name: props.label[0],
                    itemStyle:{
                        color:props.colormap[0],
                    },
                },
                {   
                    value: 255 - props.value, 
                    name: null, 
                    tooltip:{
                        show:false,
                    },
                    itemStyle:{
                        color:"#222222",
                    },
                    emphasis: {
                        disabled:true,
                }},
            ],
            showBackground: true,
            emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
          }
        ]
      };
    chartInstance.setOption(option);
  }, [props.value]);

  return (
    <div style={{ textAlign: "center" }}>
      {/* <h2>React Echarts 折线+柱状图</h2> */}
      <div ref={chartRef} style={{ height: "15rem", width: "15rem" }}></div>
    </div>
  );
}



export function LineBarChart(props) {
    const chartRef = useRef(null);
  
    useEffect(() => {
      let chartInstance = echarts.init(chartRef.current);
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985'
            }
          }
        },
        legend: {
          data: ['Red', 'Green', 'Blue'],
          bottom: '1%',
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: [
          {
            type: 'category',
            boundaryGap: false,
            data: ['0', '.125', '.25', '.375', '.5', '.625', '.75',]
          }
        ],
        yAxis: [
          {
            type: 'value'
          }
        ],
        series: [
          {
            name: 'Red',
            type: 'line',
            stack: 'Total',
            areaStyle: {
                color: props.colormap[0],
            },
            emphasis: {
              focus: 'series'
            },
            data: [120, 132, 101, 134, 90, 230, 210]
          },
          {
            name: 'Green',
            type: 'line',
            stack: 'Total',
            areaStyle: {
                color: props.colormap[1],
            },
            emphasis: {
              focus: 'series'
            },
            data: [220, 182, 191, 234, 290, 330, 310]
          },
          {
            name: 'Blue',
            type: 'line',
            stack: 'Total',
            areaStyle: {
                color: props.colormap[2],
            },
            emphasis: {
              focus: 'series'
            },
            data: [150, 232, 201, 154, 190, 330, 410]
          },
        ]
      };
      chartInstance.setOption(option);
    }, []);
  
    return (
      <div style={{ textAlign: "center" }}>
        <div ref={chartRef} style={{ height: "25rem", width: "60rem" }}></div>
      </div>
    );
  }