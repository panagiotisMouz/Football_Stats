import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

export default function CustomLineChart({ data, xKey, yKeys, labels }) {
  // Define a color palette to cycle through for multiple lines
  const colors = ["#8884d8", "#82ca9d", "#ffc658", "#ff7300", "#d0ed57"];

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data} margin={{ top: 20, right: 20, bottom: 5, left: 0 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey={xKey} label={{ value: xKey, position: 'insideBottom', dy: 10 }} />
        <YAxis />
        <Tooltip />
        <Legend />
        {yKeys.map((key, index) => (
          <Line
            key={key}
            type="monotone"
            dataKey={key}
            name={labels && labels[key] ? labels[key] : key}
            stroke={colors[index % colors.length]}
            dot={false}  // Remove dots for a smoother line (adjust as needed)
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
}
