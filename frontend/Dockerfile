# Base image
FROM node:16

# Set working directory
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the app
COPY . .

# Build the Vue app
RUN npm run build

# Serve the app with a simple web server
RUN npm install -g serve
CMD ["serve", "-s", "dist"]

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl --fail http://localhost:5000 || exit 1