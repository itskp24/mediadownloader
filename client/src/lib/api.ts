import { apiRequest } from "./queryClient";

export async function downloadInstagramContent(url: string) {
  try {
    const response = await fetch('/api/download', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url }),
    });

    if (!response.ok) {
      let errorMessage = 'Failed to download content';
      try {
        const errorData = await response.json();
        errorMessage = errorData.error || errorMessage;
      } catch {
        // If response isn't JSON, use status text
        errorMessage = response.statusText;
      }
      throw new Error(errorMessage);
    }

    // Get the filename from the content-disposition header
    const contentDisposition = response.headers.get('content-disposition');
    const filenameMatch = contentDisposition && contentDisposition.match(/filename="?([^"]+)"?/);
    const filename = filenameMatch ? filenameMatch[1] : 'instagram-content';

    // Create a blob from the response
    const blob = await response.blob();
    const downloadUrl = window.URL.createObjectURL(blob);

    // Create and trigger download
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(downloadUrl);

  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Download failed: ${error.message}`);
    }
    throw new Error('An unexpected error occurred');
  }
}