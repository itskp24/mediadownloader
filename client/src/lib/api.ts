import { apiRequest } from "./queryClient";

export async function downloadInstagramContent(url: string) {
  try {
    // Show detailed errors from the response
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
        if (errorData.details) {
          console.error('Detailed error:', errorData.details);
        }
      } catch {
        errorMessage = response.statusText;
      }
      throw new Error(errorMessage);
    }

    // Handle streaming response
    const reader = response.body?.getReader();
    const contentLength = response.headers.get('Content-Length');
    const contentDisposition = response.headers.get('content-disposition');
    const filenameMatch = contentDisposition && contentDisposition.match(/filename="?([^"]+)"?/);
    const filename = filenameMatch ? filenameMatch[1] : 'instagram-content';

    if (!reader) {
      throw new Error('Failed to initialize download stream');
    }

    // Read the stream
    const chunks: Uint8Array[] = [];
    let receivedLength = 0;

    while (true) {
      const { done, value } = await reader.read();

      if (done) {
        break;
      }

      chunks.push(value);
      receivedLength += value.length;

      // Log progress for large files
      if (contentLength) {
        const progress = (receivedLength / parseInt(contentLength)) * 100;
        console.log(`Download progress: ${progress.toFixed(2)}%`);
      }
    }

    // Combine chunks into a single Uint8Array
    const chunksAll = new Uint8Array(receivedLength);
    let position = 0;
    for (const chunk of chunks) {
      chunksAll.set(chunk, position);
      position += chunk.length;
    }

    // Create blob and trigger download
    const blob = new Blob([chunksAll]);
    const downloadUrl = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(downloadUrl);

  } catch (error) {
    console.error('Download error:', error);
    if (error instanceof Error) {
      throw new Error(`Download failed: ${error.message}`);
    }
    throw new Error('An unexpected error occurred');
  }
}