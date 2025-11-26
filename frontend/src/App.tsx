import React, { useState, useEffect } from 'react';
import AudioRecorder from './components/AudioRecorder';
import ScoreDisplay from './components/ScoreDisplay';
import AnalysisDetails from './components/AnalysisDetails';
import { api, SpeechAnalysis } from './services/api';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [analysisId, setAnalysisId] = useState<string | null>(null);
  const [status, setStatus] = useState<string>('idle');
  const [analysis, setAnalysis] = useState<SpeechAnalysis | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [, setRecordedBlob] = useState<Blob | null>(null);

  useEffect(() => {
    let interval: NodeJS.Timeout;

    if (analysisId && status === 'processing') {
      interval = setInterval(async () => {
        try {
          const response = await api.getAnalysisStatus(analysisId);
          setStatus(response.status);

          if (response.status === 'completed' && response.analysis) {
            setAnalysis(response.analysis);
            clearInterval(interval);
          } else if (response.status === 'failed') {
            setError(response.error || 'Analysis failed');
            clearInterval(interval);
          }
        } catch (err) {
          console.error('Error checking status:', err);
        }
      }, 2000);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [analysisId, status]);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setRecordedBlob(null);
      setError(null);
      setAnalysis(null);
    }
  };

  const handleRecordingComplete = (blob: Blob) => {
    const file = new File([blob], `recording-${Date.now()}.webm`, { type: 'audio/webm' });
    setSelectedFile(file);
    setRecordedBlob(blob);
    setError(null);
    setAnalysis(null);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    try {
      setStatus('uploading');
      setError(null);

      const uploadResponse = await api.uploadSpeech(selectedFile);
      setAnalysisId(uploadResponse.analysis_id);

      setStatus('analyzing');
      await api.analyzeUpload(uploadResponse.analysis_id);
      setStatus('processing');
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Upload failed');
      setStatus('error');
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setRecordedBlob(null);
    setAnalysisId(null);
    setStatus('idle');
    setAnalysis(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-800 mb-3">
            🎤 Speech Analyzer & Coach
          </h1>
          <p className="text-xl text-gray-600">
            AI-powered speech analysis for debate and public speaking improvement
          </p>
        </header>

        {/* Main Content */}
        <div className="max-w-6xl mx-auto">
          {status === 'idle' && (
            <div className="bg-white rounded-lg shadow-lg p-8 space-y-8">
              {/* Recording Section */}
              <div className="border-t pt-6">
                <h2 className="text-2xl font-semibold text-gray-800 mb-4 text-center">
                  Record Your Speech
                </h2>
                <AudioRecorder onRecordingComplete={handleRecordingComplete} />
              </div>

              {/* OR Divider */}
              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-gray-300"></div>
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-4 bg-white text-gray-500 font-medium">OR</span>
                </div>
              </div>

              {/* File Upload Section */}
              <div>
                <h2 className="text-2xl font-semibold text-gray-800 mb-4 text-center">
                  Upload Audio File
                </h2>
                <div className="flex flex-col items-center space-y-4">
                  <label className="w-full max-w-md px-6 py-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-500 cursor-pointer transition-colors">
                    <div className="text-center">
                      <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 48 48">
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                        />
                      </svg>
                      <p className="mt-2 text-sm text-gray-600">
                        {selectedFile ? selectedFile.name : 'Click to upload audio file'}
                      </p>
                      <p className="text-xs text-gray-500 mt-1">MP3, WAV, OGG, M4A, FLAC (max 10 minutes)</p>
                    </div>
                    <input
                      type="file"
                      accept=".mp3,.wav,.ogg,.m4a,.flac"
                      onChange={handleFileSelect}
                      className="hidden"
                    />
                  </label>

                  {selectedFile && (
                    <button
                      onClick={handleUpload}
                      className="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold transition-colors"
                    >
                      Analyze Speech
                    </button>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Processing Status */}
          {(status === 'uploading' || status === 'analyzing' || status === 'processing') && (
            <div className="bg-white rounded-lg shadow-lg p-12 text-center">
              <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-6"></div>
              <h2 className="text-2xl font-semibold text-gray-800 mb-2">
                {status === 'uploading' && 'Uploading...'}
                {status === 'analyzing' && 'Starting Analysis...'}
                {status === 'processing' && 'Analyzing Speech...'}
              </h2>
              <p className="text-gray-600">
                This may take a minute. We're analyzing your speech for pace, clarity, structure, and vocabulary.
              </p>
            </div>
          )}

          {/* Error Display */}
          {status === 'error' && error && (
            <div className="bg-white rounded-lg shadow-lg p-8">
              <div className="text-center mb-6">
                <div className="text-red-500 text-6xl mb-4">⚠️</div>
                <h2 className="text-2xl font-semibold text-gray-800 mb-2">Analysis Failed</h2>
                <p className="text-red-600">{error}</p>
              </div>
              <button
                onClick={handleReset}
                className="w-full px-6 py-3 bg-gray-600 hover:bg-gray-700 text-white rounded-lg font-semibold transition-colors"
              >
                Try Again
              </button>
            </div>
          )}

          {/* Results Display */}
          {status === 'completed' && analysis && (
            <div className="space-y-6">
              <ScoreDisplay score={analysis.score} />
              <AnalysisDetails analysis={analysis} />
              <button
                onClick={handleReset}
                className="w-full px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold transition-colors"
              >
                Analyze Another Speech
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
