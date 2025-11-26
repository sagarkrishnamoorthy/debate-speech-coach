import React from 'react';
import { SpeechScore } from '../services/api';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer } from 'recharts';

interface ScoreDisplayProps {
  score: SpeechScore;
}

const ScoreDisplay: React.FC<ScoreDisplayProps> = ({ score }) => {
  const chartData = [
    { category: 'Pace', value: (score.pace_score / 25) * 100, fullMark: 100 },
    { category: 'Clarity', value: (score.clarity_score / 25) * 100, fullMark: 100 },
    { category: 'Structure', value: (score.structure_score / 25) * 100, fullMark: 100 },
    { category: 'Vocabulary', value: (score.vocabulary_score / 25) * 100, fullMark: 100 },
  ];

  const getScoreColor = (score: number): string => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 space-y-6">
      {/* Overall Score */}
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">Overall Score</h2>
        <div className={`text-6xl font-bold ${getScoreColor(score.total_score)}`}>
          {score.total_score}
          <span className="text-2xl text-gray-400">/100</span>
        </div>
        <p className="mt-4 text-gray-600">{score.explanation}</p>
      </div>

      {/* Score Breakdown */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="text-center p-4 bg-blue-50 rounded-lg">
          <div className="text-sm text-gray-600 mb-1">Pace</div>
          <div className="text-2xl font-bold text-blue-600">
            {score.pace_score}<span className="text-sm">/25</span>
          </div>
        </div>
        <div className="text-center p-4 bg-purple-50 rounded-lg">
          <div className="text-sm text-gray-600 mb-1">Clarity</div>
          <div className="text-2xl font-bold text-purple-600">
            {score.clarity_score}<span className="text-sm">/25</span>
          </div>
        </div>
        <div className="text-center p-4 bg-green-50 rounded-lg">
          <div className="text-sm text-gray-600 mb-1">Structure</div>
          <div className="text-2xl font-bold text-green-600">
            {score.structure_score}<span className="text-sm">/25</span>
          </div>
        </div>
        <div className="text-center p-4 bg-yellow-50 rounded-lg">
          <div className="text-sm text-gray-600 mb-1">Vocabulary</div>
          <div className="text-2xl font-bold text-yellow-600">
            {score.vocabulary_score}<span className="text-sm">/25</span>
          </div>
        </div>
      </div>

      {/* Radar Chart */}
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart data={chartData}>
            <PolarGrid />
            <PolarAngleAxis dataKey="category" />
            <PolarRadiusAxis angle={90} domain={[0, 100]} />
            <Radar name="Score" dataKey="value" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.6} />
          </RadarChart>
        </ResponsiveContainer>
      </div>

      {/* Strengths */}
      <div>
        <h3 className="text-lg font-semibold text-gray-800 mb-3">💪 Strengths</h3>
        <ul className="space-y-2">
          {score.strengths.map((strength, index) => (
            <li key={index} className="flex items-start space-x-2">
              <span className="text-green-500 mt-1">✓</span>
              <span className="text-gray-700">{strength}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Areas for Improvement */}
      <div>
        <h3 className="text-lg font-semibold text-gray-800 mb-3">📈 Areas for Improvement</h3>
        <ul className="space-y-2">
          {score.areas_for_improvement.map((area, index) => (
            <li key={index} className="flex items-start space-x-2">
              <span className="text-yellow-500 mt-1">→</span>
              <span className="text-gray-700">{area}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ScoreDisplay;
