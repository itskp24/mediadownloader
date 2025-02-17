import { apiRequest } from "./queryClient";

export async function downloadInstagramContent(url: string) {
  try {
    const response = await apiRequest("POST", "/api/download", { url });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to download content');
    }

    const blob = await response.blob();
    const downloadUrl = window.URL.createObjectURL(blob);

    // Create temporary link and trigger download
    const link = document.createElement('a');
    link.href = downloadUrl;

    // Extract filename from content-disposition header or use default
    const contentDisposition = response.headers.get('content-disposition');
    const fileName = contentDisposition
      ? contentDisposition.split('filename=')[1].replace(/"/g, '')
      : 'instagram-content';

    link.download = fileName;
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