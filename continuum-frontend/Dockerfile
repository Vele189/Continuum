# Use Node 20 slim image as base
FROM node:20-slim

# Set working directory
WORKDIR /app

# Copy package files first to leverage cache
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the application code
COPY . .

# Expose the port Vite runs on
EXPOSE 5173

# Start the development server
# --host is needed to expose the server to the network
CMD ["npm", "run", "dev", "--", "--host"]
