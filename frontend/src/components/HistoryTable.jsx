'use client';

import { useState, useEffect } from 'react';
import { format } from 'date-fns';
import { getDetectionHistory } from '@/utils/api';
import config from '@/utils/config';

export default function HistoryTable() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalItems, setTotalItems] = useState(0);
  const itemsPerPage = 10;
  
  useEffect(() => {
    const fetchHistory = async () => {
      try {
        setLoading(true);
        const data = await getDetectionHistory({ page: currentPage, limit: itemsPerPage });
        setHistory(Array.isArray(data) ? data : (data.items || []));
        setTotalPages(Math.ceil((data.total || 0) / itemsPerPage));
        setTotalItems(data.total || 0);
      } catch (err) {
        console.error('Failed to fetch history:', err);
        setError('Failed to load detection history. Please try again later.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchHistory();
  }, [currentPage]);
  
  const handlePageChange = (newPage) => {
    if (newPage >= 1 && newPage <= totalPages) {
      setCurrentPage(newPage);
    }
  };
  
  if (loading) return <div className="text-center py-10">Loading history...</div>;
  if (error) return <div className="text-center py-10 text-red-500">{error}</div>;
  if (!history || history.length === 0) return <div className="text-center py-10">No detection history found.</div>;
  
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full bg-white shadow-md rounded-lg overflow-hidden">
        <thead className="bg-gray-100">
          <tr>
            <th className="py-3 px-4 text-left font-medium text-gray-600">ID</th>
            <th className="py-3 px-4 text-left font-medium text-gray-600">Timestamp</th>
            <th className="py-3 px-4 text-left font-medium text-gray-600">People Detected</th>
            <th className="py-3 px-4 text-left font-medium text-gray-600">Confidence</th>
            <th className="py-3 px-4 text-left font-medium text-gray-600">Result</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {history.map((item) => {
            const resultImageUrl = `${config.apiUrl}/${item.result_image_path}`;
            
            return (
              <tr key={item.id} className="hover:bg-gray-50">
                <td className="py-3 px-4">{item.id}</td>
                <td className="py-3 px-4">
                  {format(new Date(item.timestamp), 'MMM d, yyyy HH:mm')}
                </td>
                <td className="py-3 px-4 font-medium">
                  {item.num_people} {item.num_people === 1 ? 'person' : 'people'}
                </td>
                <td className="py-3 px-4">{item.confidence_threshold}</td>
                <td className="py-3 px-4">
                  <a 
                    href={resultImageUrl} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-blue-500 hover:underline"
                  >
                    View Result
                  </a>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
      
      {/* Pagination Controls */}
      <div className="mt-4 flex items-center justify-between">
        <div className="text-sm text-gray-700">
          Showing {((currentPage - 1) * itemsPerPage) + 1} to {Math.min(currentPage * itemsPerPage, totalItems)} of {totalItems} entries
        </div>
        <div className="flex space-x-2">
          <button
            onClick={() => handlePageChange(currentPage - 1)}
            disabled={currentPage === 1}
            className={`px-3 py-1 rounded ${
              currentPage === 1
                ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
                : 'bg-blue-500 text-white hover:bg-blue-600'
            }`}
          >
            Previous
          </button>
          <span className="px-3 py-1">
            Page {currentPage} of {totalPages}
          </span>
          <button
            onClick={() => handlePageChange(currentPage + 1)}
            disabled={currentPage === totalPages}
            className={`px-3 py-1 rounded ${
              currentPage === totalPages
                ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
                : 'bg-blue-500 text-white hover:bg-blue-600'
            }`}
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
}