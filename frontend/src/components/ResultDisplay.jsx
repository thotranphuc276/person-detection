import config from '@/utils/config';

export default function ResultDisplay({ result }) {
    if (!result) return null;
  
    const formattedTimestamp = new Date(result.timestamp).toLocaleString();
    
    const resultImageUrl = `${config.apiUrl}/${result.result_image_path}`;
  
    return (
      <div className="p-6 bg-white rounded-lg shadow-md">
        <h2 className="text-xl font-semibold mb-4">Detection Results</h2>
        
        <div className="space-y-4">
          <div>
            <h3 className="font-medium text-gray-700">Detection Summary</h3>
            <p className="text-2xl font-bold text-blue-600">
              {result.num_people} {result.num_people === 1 ? 'person' : 'people'} detected
            </p>
            <p className="text-sm text-gray-500">
              Confidence threshold: {result.confidence_threshold}
            </p>
            <p className="text-sm text-gray-500">
              Processed on: {formattedTimestamp}
            </p>
          </div>
          
          <div>
            <h3 className="font-medium text-gray-700 mb-2">Detection Result</h3>
            <div className="relative border border-gray-200 rounded-lg overflow-hidden">
              <img 
                src={resultImageUrl} 
                alt="Detection Result"
                className="w-full max-h-96 object-contain"
              />
            </div>
          </div>
        </div>
      </div>
    );
  }