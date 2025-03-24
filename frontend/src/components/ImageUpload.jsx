import { useState } from 'react';
import { uploadImage } from '@/utils/api';

export default function ImageUpload({ onUploadSuccess, onUploadStart }) {
  const [file, setFile] = useState(null);
  const [confidenceThreshold, setConfidenceThreshold] = useState(0.5);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleConfidenceChange = (e) => {
    setConfidenceThreshold(parseFloat(e.target.value));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      setError('Please select an image file');
      return;
    }

    try {
      setIsUploading(true);
      onUploadStart();

      const formData = new FormData();
      formData.append('file', file);
      formData.append('confidence_threshold', confidenceThreshold.toString());

      const result = await uploadImage(formData);
      onUploadSuccess(result);
    } catch (err) {
      console.error('Upload error:', err);
      setError('Error uploading image. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4">Upload Image for Person Detection</h2>

      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Select Image
          </label>
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-500
                      file:mr-4 file:py-2 file:px-4
                      file:rounded-md file:border-0
                      file:text-sm file:font-semibold
                      file:bg-blue-50 file:text-blue-700
                      hover:file:bg-blue-100"
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Confidence Threshold: {confidenceThreshold}
          </label>
          <input
            type="range"
            min="0.1"
            max="0.9"
            step="0.1"
            value={confidenceThreshold}
            onChange={handleConfidenceChange}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
          />
        </div>

        {error && (
          <div className="mb-4 text-sm text-red-600">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={isUploading || !file}
          className={`w-full py-2 px-4 rounded-md text-white font-medium
                    ${isUploading || !file
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700'}`}
        >
          {isUploading ? 'Processing...' : 'Detect People'}
        </button>
      </form>
    </div>
  );
}