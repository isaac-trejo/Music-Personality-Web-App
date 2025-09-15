import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Legend } from 'recharts';

interface RadarChartProps {
  data?: Array<{
    trait: string;
    value: number;
    fullMark: number;
  }>;
}

const defaultData = [
  { trait: 'Conscientiousness', value: 75, fullMark: 100 },
  { trait: 'Agreeableness', value: 80, fullMark: 100 },
  { trait: 'Neuroticism', value: 35, fullMark: 100 },
  { trait: 'Openness', value: 90, fullMark: 100 },
  { trait: 'Extraversion', value: 65, fullMark: 100 },
];

const traitDescriptions = [
  {
    trait: 'Conscientiousness',
    description: 'Impulsive, disorganized vs. disciplined, careful'
  },
  {
    trait: 'Agreeableness',
    description: 'Suspicious, uncooperative vs. trusting, helpful'
  },
  {
    trait: 'Neuroticism',
    description: 'Calm, confident vs. anxious, pessimistic'
  },
  {
    trait: 'Openness',
    description: 'Prefers routine, practical vs. imaginative, spontaneous'
  },
  {
    trait: 'Extraversion',
    description: 'Reserved, thoughtful vs. sociable, fun-loving'
  }
];

export default function PersonalityRadarChart({ data = defaultData }: RadarChartProps) {
  return (
    <div className="radar-chart-container">
      <h3>Music Personality Profile</h3>
      <ResponsiveContainer width="100%" height={400}>
        <RadarChart data={data} margin={{ top: 20, right: 80, bottom: 20, left: 80 }}>
          <PolarGrid stroke="#404040" />
          <PolarAngleAxis dataKey="trait" tick={{ fill: 'white', fontSize: 12 }} />
          <PolarRadiusAxis 
            angle={90} 
            domain={[0, 100]} 
            tickCount={6}
            tick={{ fill: '#b3b3b3', fontSize: 10 }}
          />
          <Radar
            name="Personality Traits"
            dataKey="value"
            stroke="#1db954"
            fill="#1db954"
            fillOpacity={0.3}
            strokeWidth={2}
          />
          <Legend wrapperStyle={{ color: 'white' }} />
        </RadarChart>
      </ResponsiveContainer>
      
      <div className="trait-descriptions">
        <h4>Trait Descriptions</h4>
        {traitDescriptions.map((item, index) => (
          <div key={index} className="trait-description">
            <strong>{item.trait}:</strong> {item.description}
          </div>
        ))}
      </div>
    </div>
  );
}
