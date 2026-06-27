# Dockerfile untuk Next.js Dashboard di Hugging Face Spaces
FROM node:20-slim

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy semua file proyek
COPY . .

# Build Next.js untuk production
RUN npm run build

# Expose port (Hugging Face biasanya pakai 7860, tapi bisa disesuaikan)
EXPOSE 7860

# Jalankan server Next.js
CMD ["npm", "start", "--", "--port", "7860"]
