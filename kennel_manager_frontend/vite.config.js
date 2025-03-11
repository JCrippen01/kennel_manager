import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: "0.0.0.0",  // Allow access from Docker
    strictPort: true,
  },
  define: {
    "process.env.VITE_API_BASE_URL": JSON.stringify("http://backend:8000/api"),
  },
});
