import axios, { AxiosInstance } from 'axios';

export interface FillerWord {
  word: string;
  count: number;
  timestamps: number[];
}

export interface PaceAnalysis {
  words_per_minute: number;
  total_words: number;
  total_duration_seconds: number;
  pace_rating: string;
  feedback: string;
}

export interface FillerWordAnalysis {
  total_filler_words: number;
  filler_words: FillerWord[];
  filler_word_rate: number;
  feedback: string;
}

export interface ArgumentStructure {
  has_clear_thesis: boolean;
  has_supporting_points: boolean;
  has_conclusion: boolean;
  logical_flow_score: number;
  feedback: string;
  suggestions: string[];
}

export interface WordChoiceAnalysis {
  weak_words: Array<{ word: string; suggestion: string }>;
  repetitive_words: Array<{ word: string; count: number }>;
  vocabulary_richness_score: number;
  feedback: string;
}

export interface SpeechScore {
  total_score: number;
  pace_score: number;
  clarity_score: number;
  structure_score: number;
  vocabulary_score: number;
  explanation: string;
  strengths: string[];
  areas_for_improvement: string[];
}

export interface SpeechAnalysis {
  id: string;
  filename: string;
  analyzed_at: string;
  duration_seconds: number;
  transcription: string;
  pace_analysis: PaceAnalysis;
  filler_word_analysis: FillerWordAnalysis;
  argument_structure: ArgumentStructure;
  word_choice_analysis: WordChoiceAnalysis;
  score: SpeechScore;
  ai_provider: string;
  raw_ai_feedback: string;
}

export interface AnalysisResponse {
  analysis_id: string;
  status: string;
  analysis?: SpeechAnalysis;
  error?: string;
}

export interface HistoryItem {
  id: string;
  filename: string;
  status: string;
  created_at: string;
  score?: number;
}

class API {
  private client: AxiosInstance;

  constructor(baseURL: string = process.env.REACT_APP_API_URL || 'http://localhost:8000') {
    this.client = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  async uploadSpeech(file: File): Promise<{ analysis_id: string; status: string; message: string }> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await this.client.post('/api/speech/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  }

  async analyzeUpload(analysisId: string): Promise<{ analysis_id: string; status: string; ai_provider: string; message: string }> {
    const response = await this.client.post(`/api/speech/analyze/${analysisId}`);
    return response.data;
  }

  async getAnalysisStatus(analysisId: string): Promise<AnalysisResponse> {
    const response = await this.client.get(`/api/speech/status/${analysisId}`);
    return response.data;
  }

  async getHistory(): Promise<{ analyses: HistoryItem[]; total: number }> {
    const response = await this.client.get('/api/speech/history');
    return response.data;
  }

  async deleteAnalysis(analysisId: string): Promise<{ message: string }> {
    const response = await this.client.delete(`/api/speech/${analysisId}`);
    return response.data;
  }
}

export const api = new API();
