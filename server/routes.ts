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
      proxyTimeout: 60000, // 60 seconds timeout
      timeout: 60000,
    })
  );

  const httpServer = createServer(app);
  return httpServer;
}