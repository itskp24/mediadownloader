import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";
import { downloadInstagramContent } from "@/lib/api";
import { Download, Loader2 } from "lucide-react";

export function InstagramDownloader() {
  const [url, setUrl] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const handleDownload = async () => {
    if (!url) {
      toast({
        title: "Error",
        description: "Please enter an Instagram URL",
        variant: "destructive",
      });
      return;
    }

    try {
      setIsLoading(true);
      await downloadInstagramContent(url);
      toast({
        title: "Success",
        description: "Content downloaded successfully",
      });
      setUrl("");
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to download content",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle className="text-center text-3xl font-bold bg-gradient-to-r from-pink-500 to-orange-500 bg-clip-text text-transparent">
          Instagram Downloader
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="space-y-2">
          <p className="text-center text-muted-foreground">
            Download Instagram photos and reels in highest quality
          </p>
        </div>
        
        <div className="flex gap-2">
          <Input
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Paste Instagram URL here..."
            className="flex-1"
          />
          <Button 
            onClick={handleDownload}
            disabled={isLoading || !url}
            className="bg-gradient-to-r from-pink-500 to-orange-500 hover:from-pink-600 hover:to-orange-600"
          >
            {isLoading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <>
                <Download className="h-4 w-4 mr-2" />
                Download
              </>
            )}
          </Button>
        </div>

        <div className="text-sm text-muted-foreground">
          <p className="text-center">
            Supported formats:
          </p>
          <ul className="list-disc list-inside mt-2 space-y-1">
            <li>Instagram Photos (e.g., https://www.instagram.com/p/CueUzxluh5a/)</li>
            <li>Instagram Reels (e.g., https://www.instagram.com/reel/DGH4iFzpsby/)</li>
          </ul>
        </div>
      </CardContent>
    </Card>
  );
}
