import type { Express } from "express";
import { createServer, type Server } from "http";
import { createProxyMiddleware } from "http-proxy-middleware";

export async function registerRoutes(app: Express): Promise<Server> {
  // Proxy /api requests to Python backend with increased timeout
  app.use(
    "/api",
    createProxyMiddleware({
      target: "http://localhost:8000",
      changeOrigin: true,
      proxyTimeout: 300000, // 5 minutes timeout
      timeout: 300000,
      onProxyReq: (proxyReq, req, res) => {
        console.log(`Proxying request to: ${req.method} ${req.url}`);
      },
      onProxyRes: (proxyRes, req, res) => {
        console.log(`Received proxy response for: ${req.method} ${req.url} with status: ${proxyRes.statusCode}`);
      },
      onError: (err, req, res, target) => {
        console.error('Proxy Error:', err);
        const statusCode = err.code === 'ECONNRESET' ? 504 : 500;
        res.writeHead(statusCode, {
          'Content-Type': 'application/json',
        });
        res.end(JSON.stringify({ 
          error: 'Download failed',
          details: err.message || 'Proxy error occurred'
        }));
      }
    })
  );

  const httpServer = createServer(app);
  return httpServer;
}