'use client';

import { useState, useEffect } from 'react';

interface UploadProgress {
  percentage: number;
  message: string;
  successful_count: number;
  failed_count: number;
  timestamp: string;
}

interface ProgressMonitorProps {
  uploadId: number;
  onComplete?: () => void;
  onError?: (error: string) => void;
}

export default function UploadProgressMonitor({ uploadId, onComplete, onError }: ProgressMonitorProps) {
  const [progress, setProgress] = useState<UploadProgress>({
    percentage: 0,
    message: 'Starting...',
    successful_count: 0,
    failed_count: 0,
    timestamp: '',
  });
  const [isActive, setIsActive] = useState(true);

  useEffect(() => {
    if (!isActive) return;

    const fetchProgress = async () => {
      try {
        const response = await fetch(`/api/admin/csv-uploads/${uploadId}/progress`);
        if (!response.ok) {
          throw new Error('Failed to fetch progress');
        }

        const data = await response.json();
        setProgress(data);

        // Check if completed
        if (data.percentage >= 100 || data.message?.includes('Completed')) {
          setIsActive(false);
          onComplete?.();
        }

      } catch (error) {
        console.error('Error fetching progress:', error);
        setIsActive(false);
        onError?.(error instanceof Error ? error.message : 'Unknown error');
      }
    };

    // Initial fetch
    fetchProgress();

    // Set up polling
    const interval = setInterval(fetchProgress, 2000); // Poll every 2 seconds

    return () => clearInterval(interval);
  }, [uploadId, isActive, onComplete, onError]);

  const formatTime = (timestamp: string) => {
    if (!timestamp) return '';
    return new Date(timestamp).toLocaleTimeString();
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-medium text-gray-900">Upload Progress</h3>
        <span className="text-sm text-gray-500">{formatTime(progress.timestamp)}</span>
      </div>

      {/* Progress Bar */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-gray-700">
            Processing: {progress.percentage.toFixed(1)}%
          </span>
          <span className="text-sm text-gray-500">
            {progress.successful_count + progress.failed_count > 0 && (
              <>
                {progress.successful_count} success, {progress.failed_count} failed
              </>
            )}
          </span>
        </div>
        
        <div className="w-full bg-gray-200 rounded-full h-2.5">
          <div
            className={`h-2.5 rounded-full transition-all duration-300 $${
              progress.percentage >= 100 
                ? 'bg-green-600' 
                : progress.percentage > 0 
                  ? 'bg-blue-600' 
                  : 'bg-gray-400'
            }`}
            style={{ width: `${Math.min(progress.percentage, 100)}%` }}
          ></div>
        </div>
      </div>

      {/* Status Message */}
      <div className="mb-4">
        <p className="text-sm text-gray-600">
          <span className="font-medium">Status:</span> {progress.message}
        </p>
      </div>

      {/* Processing Animation */}
      {isActive && progress.percentage < 100 && (
        <div className="flex items-center text-sm text-blue-600">
          <svg className="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Processing in background...
        </div>
      )}

      {/* Completion Status */}
      {!isActive && progress.percentage >= 100 && (
        <div className="flex items-center text-sm text-green-600">
          <svg className="mr-2 h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
          Processing completed!
        </div>
      )}

      {/* Performance Stats */}
      {progress.successful_count > 0 && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-500">Imported:</span>
              <span className="ml-2 font-medium text-green-600">{progress.successful_count}</span>
            </div>
            {progress.failed_count > 0 && (
              <div>
                <span className="text-gray-500">Failed:</span>
                <span className="ml-2 font-medium text-red-600">{progress.failed_count}</span>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}