import type { Express } from "express";
import { createServer, type Server } from "http";
import { createProxyMiddleware, type Options } from "http-proxy-middleware";
import type { IncomingMessage, ServerResponse } from "http";

export async function registerRoutes(app: Express): Promise<Server> {
  // Proxy /api requests to Python backend with increased timeout
  app.use(
    "/api",
    createProxyMiddleware({
      target: "http://localhost:8000",
      changeOrigin: true,
      proxyTimeout: 300000, // 5 minutes timeout
      timeout: 300000,
      onProxyReq: (proxyReq: any, req: IncomingMessage, res: ServerResponse) => {
        console.log(`Proxying request to: ${req.method} ${req.url}`);
      },
      onProxyRes: (proxyRes: any, req: IncomingMessage, res: ServerResponse) => {
        console.log(`Received proxy response for: ${req.method} ${req.url} with status: ${proxyRes.statusCode}`);
      },
      onError: (err: Error, req: IncomingMessage, res: ServerResponse) => {
        console.error('Proxy Error:', err);
        const statusCode = (err as any).code === 'ECONNRESET' ? 504 : 500;
        res.writeHead(statusCode, {
          'Content-Type': 'application/json',
        });
        res.end(JSON.stringify({ 
          error: 'Download failed',
          details: err.message || 'Proxy error occurred'
        }));
      }
    } as Options)
  );

  const httpServer = createServer(app);
  return httpServer;
}