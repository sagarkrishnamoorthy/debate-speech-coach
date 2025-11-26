import React from 'react';
import { SpeechAnalysis } from '../services/api';

interface AnalysisDetailsProps {
  analysis: SpeechAnalysis;
}

const AnalysisDetails: React.FC<AnalysisDetailsProps> = ({ analysis }) => {
  return (
    <div className="space-y-6">
      {/* Transcription */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-xl font-semibold text-gray-800 mb-3">📝 Transcription</h3>
        <div className="bg-gray-50 p-4 rounded-lg">
          <p className="text-gray-700 whitespace-pre-wrap">{analysis.transcription}</p>
        </div>
        <div className="mt-3 text-sm text-gray-500">
          Duration: {Math.floor(analysis.duration_seconds / 60)}:{(analysis.duration_seconds % 60).toFixed(0).padStart(2, '0')}
        </div>
      </div>

      {/* Pace Analysis */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-xl font-semibold text-gray-800 mb-3">⏱️ Pace Analysis</h3>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-4">
          <div className="bg-blue-50 p-3 rounded">
            <div className="text-sm text-gray-600">Words per Minute</div>
            <div className="text-2xl font-bold text-blue-600">{analysis.pace_analysis.words_per_minute}</div>
          </div>
          <div className="bg-blue-50 p-3 rounded">
            <div className="text-sm text-gray-600">Total Words</div>
            <div className="text-2xl font-bold text-blue-600">{analysis.pace_analysis.total_words}</div>
          </div>
          <div className="bg-blue-50 p-3 rounded">
            <div className="text-sm text-gray-600">Rating</div>
            <div className="text-lg font-semibold text-blue-600 capitalize">{analysis.pace_analysis.pace_rating.replace('_', ' ')}</div>
          </div>
        </div>
        <p className="text-gray-700">{analysis.pace_analysis.feedback}</p>
      </div>

      {/* Filler Words Analysis */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-xl font-semibold text-gray-800 mb-3">🗣️ Filler Words Analysis</h3>
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div className="bg-purple-50 p-3 rounded">
            <div className="text-sm text-gray-600">Total Filler Words</div>
            <div className="text-2xl font-bold text-purple-600">{analysis.filler_word_analysis.total_filler_words}</div>
          </div>
          <div className="bg-purple-50 p-3 rounded">
            <div className="text-sm text-gray-600">Fillers per Minute</div>
            <div className="text-2xl font-bold text-purple-600">{analysis.filler_word_analysis.filler_word_rate}</div>
          </div>
        </div>
        <p className="text-gray-700 mb-3">{analysis.filler_word_analysis.feedback}</p>
        {analysis.filler_word_analysis.filler_words.length > 0 && (
          <div>
            <h4 className="font-semibold text-gray-700 mb-2">Most Common Fillers:</h4>
            <div className="flex flex-wrap gap-2">
              {analysis.filler_word_analysis.filler_words.map((filler, index) => (
                <span key={index} className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm">
                  "{filler.word}" ({filler.count}x)
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Argument Structure */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-xl font-semibold text-gray-800 mb-3">🏗️ Argument Structure</h3>
        <div className="grid grid-cols-3 gap-4 mb-4">
          <div className={`p-3 rounded ${analysis.argument_structure.has_clear_thesis ? 'bg-green-50' : 'bg-red-50'}`}>
            <div className="text-sm text-gray-600">Clear Thesis</div>
            <div className={`text-lg font-semibold ${analysis.argument_structure.has_clear_thesis ? 'text-green-600' : 'text-red-600'}`}>
              {analysis.argument_structure.has_clear_thesis ? '✓ Yes' : '✗ No'}
            </div>
          </div>
          <div className={`p-3 rounded ${analysis.argument_structure.has_supporting_points ? 'bg-green-50' : 'bg-red-50'}`}>
            <div className="text-sm text-gray-600">Supporting Points</div>
            <div className={`text-lg font-semibold ${analysis.argument_structure.has_supporting_points ? 'text-green-600' : 'text-red-600'}`}>
              {analysis.argument_structure.has_supporting_points ? '✓ Yes' : '✗ No'}
            </div>
          </div>
          <div className={`p-3 rounded ${analysis.argument_structure.has_conclusion ? 'bg-green-50' : 'bg-red-50'}`}>
            <div className="text-sm text-gray-600">Conclusion</div>
            <div className={`text-lg font-semibold ${analysis.argument_structure.has_conclusion ? 'text-green-600' : 'text-red-600'}`}>
              {analysis.argument_structure.has_conclusion ? '✓ Yes' : '✗ No'}
            </div>
          </div>
        </div>
        <div className="mb-3">
          <span className="text-sm text-gray-600">Logical Flow Score: </span>
          <span className="text-lg font-bold text-green-600">{analysis.argument_structure.logical_flow_score}/10</span>
        </div>
        <p className="text-gray-700 mb-3">{analysis.argument_structure.feedback}</p>
        {analysis.argument_structure.suggestions.length > 0 && (
          <div>
            <h4 className="font-semibold text-gray-700 mb-2">Suggestions:</h4>
            <ul className="space-y-1">
              {analysis.argument_structure.suggestions.map((suggestion, index) => (
                <li key={index} className="text-gray-600 flex items-start space-x-2">
                  <span className="text-blue-500">•</span>
                  <span>{suggestion}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Word Choice Analysis */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-xl font-semibold text-gray-800 mb-3">📚 Word Choice Analysis</h3>
        <div className="mb-3">
          <span className="text-sm text-gray-600">Vocabulary Richness Score: </span>
          <span className="text-lg font-bold text-yellow-600">{analysis.word_choice_analysis.vocabulary_richness_score}/10</span>
        </div>
        <p className="text-gray-700 mb-4">{analysis.word_choice_analysis.feedback}</p>
        
        {analysis.word_choice_analysis.weak_words.length > 0 && (
          <div className="mb-4">
            <h4 className="font-semibold text-gray-700 mb-2">💡 Word Improvements:</h4>
            <div className="space-y-2">
              {analysis.word_choice_analysis.weak_words.map((item, index) => (
                <div key={index} className="flex items-center space-x-2 text-sm">
                  <span className="px-2 py-1 bg-red-100 text-red-700 rounded">{item.word}</span>
                  <span className="text-gray-400">→</span>
                  <span className="px-2 py-1 bg-green-100 text-green-700 rounded">{item.suggestion}</span>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {analysis.word_choice_analysis.repetitive_words.length > 0 && (
          <div>
            <h4 className="font-semibold text-gray-700 mb-2">🔄 Repetitive Words:</h4>
            <div className="flex flex-wrap gap-2">
              {analysis.word_choice_analysis.repetitive_words.map((item, index) => (
                <span key={index} className="px-3 py-1 bg-yellow-100 text-yellow-700 rounded-full text-sm">
                  "{item.word}" ({item.count}x)
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AnalysisDetails;
