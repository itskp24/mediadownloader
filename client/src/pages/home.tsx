import { InstagramDownloader } from "@/components/instagram-downloader";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-muted p-6">
      <div className="container mx-auto py-12 space-y-12">
        <InstagramDownloader />
      </div>
    </div>
  );
}
