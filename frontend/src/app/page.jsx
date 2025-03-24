'use client';

import { useState } from 'react';
import Link from 'next/link';
import ImageUpload from '@/components/ImageUpload';
import ResultDisplay from '@/components/ResultDisplay';

export default function Home() {
  const [detectionResult, setDetectionResult] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleUploadStart = () => {
    setIsProcessing(true);
    setDetectionResult(null);
  };

  const handleUploadSuccess = (data) => {
    setDetectionResult(data);
    setIsProcessing(false);
  };

  return (
    <main className="max-w-6xl mx-auto p-4">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-3xl font-bold">Person Detection System</h1>
        <Link 
          href="/history" 
          className="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300"
        >
          View History
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <ImageUpload 
          onUploadSuccess={handleUploadSuccess}
          onUploadStart={handleUploadStart}
        />
        
        {isProcessing ? (
          <div className="p-6 bg-white rounded-lg shadow-md flex flex-col items-center justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent"></div>
            <p className="mt-4 text-gray-600">Processing your image...</p>
          </div>
        ) : (
          <ResultDisplay result={detectionResult} />
        )}
      </div>
    </main>
  );
}