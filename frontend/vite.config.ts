import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',  // Allow access from any network interface
    port: 5173,        // Ensure the port is 5173
    hmr: {
      host: 'localhost', // This ensures Hot Module Replacement works locally
    },
  },
})