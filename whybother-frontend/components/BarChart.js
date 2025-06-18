import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

export default function CustomLineChart({
  data = [],
  xKey = "year",
  yKeys = ["value"],
  labels = {},
  colors = ["#61dafb", "#ff6384", "#82ca9d"],
}) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart
        data={data}
        margin={{ top: 20, right: 30, bottom: 20, left: 20 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#333" />
        <XAxis
          dataKey={xKey}
          tick={{ fill: "#ccc" }}
          label={{
            value: xKey.toUpperCase(),
            position: "insideBottom",
            dy: 15,
            fill: "#ccc",
          }}
        />
        <YAxis
          tick={{ fill: "#ccc" }}
          label={{
            value: "Value",
            angle: -90,
            position: "insideLeft",
            dx: -10,
            fill: "#ccc",
          }}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: "#1e1e1e",
            border: "none",
            color: "#fff",
          }}
        />
        <Legend wrapperStyle={{ color: "#ccc" }} />
        {yKeys.map((key, i) => (
          <Line
            key={key}
            type="monotone"
            dataKey={key}
            stroke={colors[i % colors.length]}
            strokeWidth={2}
            name={labels[key] || key}
            dot={{ r: 3 }}
            activeDot={{ r: 6 }}
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
}
