import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

export default function CustomScatterPlot({
  data = [],
  xKey = "x",
  yKey = "y",
  xLabel = "",
  yLabel = "",
  color = "#ff7300",
}) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <ScatterChart
        margin={{ top: 20, right: 30, bottom: 20, left: 20 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#333" />
        <XAxis
          type="number"
          dataKey={xKey}
          tick={{ fill: "#ccc" }}
          label={{
            value: xLabel,
            position: "insideBottom",
            dy: 15,
            fill: "#ccc",
          }}
        />
        <YAxis
          type="number"
          dataKey={yKey}
          tick={{ fill: "#ccc" }}
          label={{
            value: yLabel,
            angle: -90,
            position: "insideLeft",
            dx: -10,
            fill: "#ccc",
          }}
        />
        <Tooltip
          cursor={{ strokeDasharray: "3 3" }}
          contentStyle={{ backgroundColor: "#1e1e1e", border: "none", color: "#fff" }}
        />
        <Legend wrapperStyle={{ color: "#ccc" }} />
        <Scatter
          name="Data Points"
          data={data}
          fill={color}
          shape="circle"
        />
      </ScatterChart>
    </ResponsiveContainer>
  );
}
