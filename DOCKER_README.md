# 🐳 Fives App Docker Setup

This document explains how to use Docker to run the Fives App in both development and production environments.

## 🚀 Quick Start

### Development Environment
```bash
# Build and start development containers
make -f Makefile.docker dev

# Or manually:
docker-compose -f docker-compose.yml --profile dev up -d
```

### Production Environment
```bash
# Build and start production containers
make -f Makefile.docker build
make -f Makefile.docker up

# Or manually:
docker-compose -f docker-compose.prod.yml up -d
```

## 📁 Docker Files

- **`Dockerfile.backend`** - FastAPI backend container
- **`Dockerfile.frontend`** - React frontend container (production)
- **`Dockerfile.frontend.dev`** - React frontend container (development with hot reload)
- **`docker-compose.yml`** - Development environment
- **`docker-compose.prod.yml`** - Production environment
- **`.dockerignore`** - Files excluded from Docker builds

## 🔧 Available Commands

### Using Makefile
```bash
make -f Makefile.docker help          # Show all available commands
make -f Makefile.docker build-dev     # Build development containers
make -f Makefile.docker up-dev        # Start development environment
make -f Makefile.docker build         # Build production containers
make -f Makefile.docker up            # Start production environment
make -f Makefile.docker down          # Stop all containers
make -f Makefile.docker logs          # Show container logs
make -f Makefile.docker clean         # Remove containers and images
make -f Makefile.docker health        # Check service health
```

### Using Docker Compose Directly
```bash
# Development
docker-compose -f docker-compose.yml --profile dev up -d

# Production
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.yml logs -f

# Stop services
docker-compose -f docker-compose.yml down
```

## 🌐 Service URLs

### Development
- **Frontend**: http://localhost:5173 (Vite dev server with hot reload)
- **Backend**: http://localhost:8000 (FastAPI)
- **API Docs**: http://localhost:8000/docs

### Production
- **Frontend**: http://localhost:3000 (Built React app)
- **Backend**: http://localhost:8000 (FastAPI)
- **API Docs**: http://localhost:8000/docs

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```bash
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Supabase      │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (Database)    │
│   Port 3000     │    │   Port 8000     │    │   (External)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📊 Health Checks

Both services include health check endpoints:
- **Backend**: `GET /health` - Checks Supabase connection
- **Frontend**: HTTP response check on root endpoint

## 🚨 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Check what's using the port
   lsof -i :8000
   lsof -i :3000
   lsof -i :5173
   
   # Kill the process
   kill -9 <PID>
   ```

2. **Container won't start**
   ```bash
   # Check logs
   docker-compose logs <service-name>
   
   # Rebuild containers
   make -f Makefile.docker rebuild
   ```

3. **Environment variables missing**
   ```bash
   # Check if .env file exists
   ls -la .env
   
   # Verify environment variables are loaded
   docker-compose config
   ```

### Reset Everything
```bash
# Stop and remove everything
make -f Makefile.docker clean

# Rebuild from scratch
make -f Makefile.docker rebuild
```

## 🔄 Development Workflow

1. **Start development environment**
   ```bash
   make -f Makefile.docker dev
   ```

2. **Make code changes** - Frontend will hot reload automatically

3. **Backend changes** - Restart backend container:
   ```bash
   docker-compose restart backend
   ```

4. **View logs**
   ```bash
   make -f Makefile.docker logs
   ```

5. **Stop when done**
   ```bash
   make -f Makefile.docker down
   ```

## 🚀 Production Deployment

1. **Build production images**
   ```bash
   make -f Makefile.docker build
   ```

2. **Start production services**
   ```bash
   make -f Makefile.docker up
   ```

3. **Optional: Add Nginx reverse proxy**
   ```bash
   make -f Makefile.docker up-nginx
   ```

## 📝 Notes

- Development containers use volume mounts for hot reload
- Production containers build optimized images
- Health checks ensure services are running properly
- All services restart automatically unless stopped manually
- Network isolation between services for security
