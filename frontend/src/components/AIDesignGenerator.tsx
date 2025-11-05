"use client";

import { useState } from 'react';

interface AIDesignGeneratorProps {
  lang: string;
}

export default function AIDesignGenerator({ lang }: AIDesignGeneratorProps) {
  const [prompt, setPrompt] = useState('');
  const [generatedHTML, setGeneratedHTML] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const generateDesign = async () => {
    if (!prompt.trim()) return;
    
    setIsLoading(true);
    setError('');
    
    try {
      // This would call your backend API that uses the OpenAI key
      const response = await fetch('/api/ai/generate-design', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: `Create a modern, responsive HTML component for a European business directory with Tailwind CSS classes. The component should: ${prompt}. Use the brand color #1f4fff and follow European design patterns. Return only the HTML with Tailwind classes, no explanations.`,
          lang,
        }),
      });

      const data = await response.json();
      
      if (response.ok) {
        setGeneratedHTML(data.html);
      } else {
        setError(data.error || 'Failed to generate design');
      }
    } catch (err) {
      setError('Network error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="card shadow-2xl border-0 bg-gradient-to-br from-white to-gray-50 animate-fade-in-up">
        <div className="card-body p-8">
          <div className="text-center mb-8">
            <div className="text-4xl mb-4">🎨</div>
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Create Your Design</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Describe what kind of component you want to create for your European business directory
            </p>
          </div>
          
          <div className="space-y-6">
            <div>
              <label className="block text-lg font-semibold mb-4 text-gray-900">Design Prompt</label>
              <textarea
                className="w-full min-h-[120px] p-4 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand focus:border-transparent resize-none text-lg"
                placeholder="e.g., Create a hero section with search box for finding restaurants in European cities, include country flags and modern gradient background..."
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
              />
            </div>
            
            <div className="flex justify-center">
              <button
                onClick={generateDesign}
                disabled={isLoading || !prompt.trim()}
                className="bg-gradient-to-r from-brand to-purple-600 text-white font-bold text-lg px-12 py-4 rounded-2xl shadow-xl hover:shadow-2xl transform hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center gap-3"
              >
                {isLoading ? (
                  <>
                    <div className="w-6 h-6 border-3 border-white border-t-transparent rounded-full animate-spin"></div>
                    Generating Design...
                  </>
                ) : (
                  <>
                    <span className="text-xl">✨</span>
                    Generate Design
                  </>
                )}
              </button>
            </div>
          </div>
          
          {error && (
            <div className="mt-6 p-6 bg-red-50 border-2 border-red-200 rounded-2xl text-red-700 text-center animate-fade-in-up">
              <div className="text-2xl mb-2">⚠️</div>
              <div className="font-semibold">{error}</div>
            </div>
          )}
        </div>
      </div>

      {generatedHTML && (
        <div className="grid lg:grid-cols-2 gap-8 animate-fade-in-up">
          {/* Code Preview */}
          <div className="card shadow-xl border-0 bg-gray-900 text-white">
            <div className="card-header bg-gray-800 border-b border-gray-700">
              <div className="flex items-center gap-3">
                <span className="text-xl">💻</span>
                <span className="font-bold">Generated HTML Code</span>
              </div>
            </div>
            <div className="card-body p-0">
              <pre className="text-sm overflow-x-auto bg-gray-900 p-6 rounded-b-xl h-96 overflow-y-auto">
                <code className="text-green-400">{generatedHTML}</code>
              </pre>
            </div>
          </div>

          {/* Live Preview */}
          <div className="card shadow-xl border-0">
            <div className="card-header bg-gradient-to-r from-brand to-purple-600 text-white">
              <div className="flex items-center gap-3">
                <span className="text-xl">👀</span>
                <span className="font-bold">Live Preview</span>
              </div>
            </div>
            <div className="card-body p-6">
              <div 
                className="border-2 border-dashed border-gray-200 rounded-xl p-6 bg-white min-h-96 overflow-auto"
                dangerouslySetInnerHTML={{ __html: generatedHTML }}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}