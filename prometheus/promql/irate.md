| action | time | 
| :--- | :--- |
| describe promql irate function | 2020.04.29 |

----

### irate()

```yaml
irate(v range-vector) calculates the per-second instant rate of increase of the time series in the range vector. This is based on the last two data points. Breaks in monotonicity (such as counter resets due to target restarts) are automatically adjusted for.

计算范围矢量<range-vector>中时间序列的每秒瞬时增加率。这基于最后两个数据点。单调性中断（例如由于目标重新启动而导致的计数器重置）会自动进行调整。

irate should only be used when graphing volatile, fast-moving counters. Use rate for alerts and slow-moving counters, as brief changes in the rate can reset the FOR clause and graphs consisting entirely of rare spikes are hard to read.

使用场景推荐:
    - irate
    类型为 counters 数据波动峰值波谷明显 [绘制易变，快速移动]
    - rate
     - 预警
     - 数据波动缓存

注意事项:
    - 当 irate() 与聚合类的函数组合时，先获取irate 的值再去聚合
```


### 源代码

```golang
// Point represents a single data point for a given timestamp.
// Point T: 精确到毫秒的时间戳 V: 值
type Point struct {
	T int64
	V float64
}

// Sample is a single sample belonging to a metric.
// 样本: 包含标签的一个数据点(metric)
// example: node_load1{project="demo",service="demo"}@1101010101 2 
// (metrics name): __name__ = node_load1
// labels: project="demo",service="demo"
// (Point) T:1101010101  V:2

type Sample struct {
	Point
	Metric labels.Labels
}
// 矢量: 在一定意义上等同于矩阵(Matrix)
// 赋值: 既可以是相同labels 不同时间范围内的值，也可以是不同labels 不同时间范围内的值
type Vector []Sample

// === irate(node parser.ValueTypeMatrix) Vector ===
// example: 100*(sum by (cpu) (irate(node_cpu_guest_seconds_total[1m])))
func funcIrate(vals []parser.Value, args parser.Expressions, enh *EvalNodeHelper) Vector {
	return instantValue(vals, enh.out, true)
}

func instantValue(vals []parser.Value, out Vector, isRate bool) Vector {
	samples := vals[0].(Matrix)[0]
	// No sense in trying to compute a rate without at least two points. Drop
	// this Vector element.
	if len(samples.Points) < 2 {
		return out
	}

	lastSample := samples.Points[len(samples.Points)-1]
	previousSample := samples.Points[len(samples.Points)-2]

	var resultValue float64
	if isRate && lastSample.V < previousSample.V {
		// Counter reset.
		resultValue = lastSample.V
	} else {
		resultValue = lastSample.V - previousSample.V
	}

	sampledInterval := lastSample.T - previousSample.T
	if sampledInterval == 0 {
		// Avoid dividing by 0.
		return out
	}

	if isRate {
		// Convert to per-second.
		resultValue /= float64(sampledInterval) / 1000
	}

	return append(out, Sample{
		Point: Point{V: resultValue},
	})
}
```


-----

**跳转门**

[prometheus.function.irate.docs](https://prometheus.io/docs/prometheus/latest/querying/functions/#irate)