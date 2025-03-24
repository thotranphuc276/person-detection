import config from './config';

const API_BASE_URL = config.apiUrl;

export async function uploadImage(file, confidenceThreshold = 0.5) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('confidence_threshold', confidenceThreshold);

  const response = await fetch(`${API_BASE_URL}/detection/`, {
    method: 'POST',
    body: formData,
  });
  
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to upload image');
  }
  
  return await response.json();
}

export async function getDetectionHistory(params = {}) {
  const defaultParams = {
    page: 1,
    limit: 10,
    ...params
  };

  const queryParams = new URLSearchParams(defaultParams);
  const response = await fetch(`${API_BASE_URL}/history/?${queryParams.toString()}`);
  
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to fetch detection history');
  }
  
  return await response.json();
}

export async function getDetectionById(id) {
  const response = await fetch(`${API_BASE_URL}/history/${id}`);
  
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to fetch detection');
  }
  
  return await response.json();
}