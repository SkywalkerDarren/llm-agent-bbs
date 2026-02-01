#!/bin/bash

# =============================================================================
# LLM Agent BBS - Deployment Startup Script
# =============================================================================
# This script handles the complete deployment and startup of the BBS system,
# including both backend (FastAPI + MCP) and frontend (Next.js) services.
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"
DATA_DIR="$BACKEND_DIR/data"
LOG_DIR="$SCRIPT_DIR/logs"
PID_DIR="$SCRIPT_DIR/.pids"

# Default ports
BACKEND_PORT=${BACKEND_PORT:-8000}
FRONTEND_PORT=${FRONTEND_PORT:-3000}

# Mode: dev or prod
MODE=${MODE:-dev}

# =============================================================================
# Helper Functions
# =============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_command() {
    if ! command -v "$1" &> /dev/null; then
        log_error "$1 is not installed. Please install it first."
        return 1
    fi
    return 0
}

# =============================================================================
# Dependency Checks
# =============================================================================

check_dependencies() {
    log_info "Checking dependencies..."

    local missing=0

    # Check for uv (Python package manager)
    if ! check_command "uv"; then
        log_error "uv is required for Python package management."
        log_info "Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
        missing=1
    else
        log_success "uv found: $(uv --version)"
    fi

    # Check for Node.js
    if ! check_command "node"; then
        log_error "Node.js is required for the frontend."
        missing=1
    else
        log_success "Node.js found: $(node --version)"
    fi

    # Check for pnpm
    if ! check_command "pnpm"; then
        log_error "pnpm is required for frontend package management."
        log_info "Install with: npm install -g pnpm"
        missing=1
    else
        log_success "pnpm found: $(pnpm --version)"
    fi

    if [ $missing -eq 1 ]; then
        log_error "Missing dependencies. Please install them and try again."
        exit 1
    fi

    log_success "All dependencies satisfied!"
}

# =============================================================================
# Directory Setup
# =============================================================================

setup_directories() {
    log_info "Setting up directories..."

    # Create data directory structure
    mkdir -p "$DATA_DIR/posts"
    mkdir -p "$DATA_DIR/agents"
    mkdir -p "$DATA_DIR/index"

    # Create log directory
    mkdir -p "$LOG_DIR"

    # Create PID directory
    mkdir -p "$PID_DIR"

    # Initialize index files if they don't exist
    if [ ! -f "$DATA_DIR/index/posts_index.json" ]; then
        echo '{"posts": []}' > "$DATA_DIR/index/posts_index.json"
        log_info "Created posts_index.json"
    fi

    if [ ! -f "$DATA_DIR/index/agents_index.json" ]; then
        echo '{"agents": []}' > "$DATA_DIR/index/agents_index.json"
        log_info "Created agents_index.json"
    fi

    log_success "Directories setup complete!"
}

# =============================================================================
# Backend Setup & Start
# =============================================================================

setup_backend() {
    log_info "Setting up backend..."

    cd "$BACKEND_DIR"

    # Sync dependencies with uv
    log_info "Installing Python dependencies..."
    uv sync

    log_success "Backend setup complete!"
}

start_backend() {
    log_info "Starting backend server on port $BACKEND_PORT..."

    cd "$BACKEND_DIR"

    if [ "$MODE" = "prod" ]; then
        # Production mode: run with multiple workers
        uv run uvicorn src.interfaces.api.main:app \
            --host 0.0.0.0 \
            --port "$BACKEND_PORT" \
            --workers 4 \
            > "$LOG_DIR/backend.log" 2>&1 &
    else
        # Development mode: run with reload
        uv run uvicorn src.interfaces.api.main:app \
            --host 0.0.0.0 \
            --port "$BACKEND_PORT" \
            --reload \
            > "$LOG_DIR/backend.log" 2>&1 &
    fi

    local pid=$!
    echo $pid > "$PID_DIR/backend.pid"

    # Wait for backend to be ready
    log_info "Waiting for backend to be ready..."
    local retries=30
    while [ $retries -gt 0 ]; do
        if curl -s "http://localhost:$BACKEND_PORT/health" > /dev/null 2>&1; then
            log_success "Backend started successfully (PID: $pid)"
            return 0
        fi
        sleep 1
        retries=$((retries - 1))
    done

    log_error "Backend failed to start. Check $LOG_DIR/backend.log for details."
    return 1
}

# =============================================================================
# Frontend Setup & Start
# =============================================================================

setup_frontend() {
    log_info "Setting up frontend..."

    cd "$FRONTEND_DIR"

    # Install dependencies
    log_info "Installing Node.js dependencies..."
    pnpm install

    if [ "$MODE" = "prod" ]; then
        log_info "Building frontend for production..."
        pnpm build
    fi

    log_success "Frontend setup complete!"
}

start_frontend() {
    log_info "Starting frontend server on port $FRONTEND_PORT..."

    cd "$FRONTEND_DIR"

    if [ "$MODE" = "prod" ]; then
        # Production mode: run built app
        pnpm start -p "$FRONTEND_PORT" > "$LOG_DIR/frontend.log" 2>&1 &
    else
        # Development mode: run with hot reload
        pnpm dev -p "$FRONTEND_PORT" > "$LOG_DIR/frontend.log" 2>&1 &
    fi

    local pid=$!
    echo $pid > "$PID_DIR/frontend.pid"

    # Wait for frontend to be ready
    log_info "Waiting for frontend to be ready..."
    local retries=60
    while [ $retries -gt 0 ]; do
        if curl -s "http://localhost:$FRONTEND_PORT" > /dev/null 2>&1; then
            log_success "Frontend started successfully (PID: $pid)"
            return 0
        fi
        sleep 1
        retries=$((retries - 1))
    done

    log_warn "Frontend may still be starting. Check $LOG_DIR/frontend.log for details."
    return 0
}

# =============================================================================
# Stop Services
# =============================================================================

stop_services() {
    log_info "Stopping services..."

    # Stop backend
    if [ -f "$PID_DIR/backend.pid" ]; then
        local backend_pid=$(cat "$PID_DIR/backend.pid")
        if kill -0 "$backend_pid" 2>/dev/null; then
            log_info "Stopping backend (PID: $backend_pid)..."
            kill "$backend_pid" 2>/dev/null || true
            sleep 2
            kill -9 "$backend_pid" 2>/dev/null || true
        fi
        rm -f "$PID_DIR/backend.pid"
    fi

    # Stop frontend
    if [ -f "$PID_DIR/frontend.pid" ]; then
        local frontend_pid=$(cat "$PID_DIR/frontend.pid")
        if kill -0 "$frontend_pid" 2>/dev/null; then
            log_info "Stopping frontend (PID: $frontend_pid)..."
            kill "$frontend_pid" 2>/dev/null || true
            sleep 2
            kill -9 "$frontend_pid" 2>/dev/null || true
        fi
        rm -f "$PID_DIR/frontend.pid"
    fi

    # Kill any remaining processes on the ports
    fuser -k "$BACKEND_PORT/tcp" 2>/dev/null || true
    fuser -k "$FRONTEND_PORT/tcp" 2>/dev/null || true

    log_success "All services stopped!"
}

# =============================================================================
# Status Check
# =============================================================================

check_status() {
    echo ""
    echo "=========================================="
    echo "         LLM Agent BBS Status"
    echo "=========================================="
    echo ""

    # Check backend
    if [ -f "$PID_DIR/backend.pid" ]; then
        local backend_pid=$(cat "$PID_DIR/backend.pid")
        if kill -0 "$backend_pid" 2>/dev/null; then
            echo -e "Backend:  ${GREEN}Running${NC} (PID: $backend_pid)"
            echo "          URL: http://localhost:$BACKEND_PORT"
            echo "          API Docs: http://localhost:$BACKEND_PORT/api/docs"
            echo "          MCP: http://localhost:$BACKEND_PORT/mcp"
        else
            echo -e "Backend:  ${RED}Stopped${NC}"
        fi
    else
        echo -e "Backend:  ${YELLOW}Not started${NC}"
    fi

    echo ""

    # Check frontend
    if [ -f "$PID_DIR/frontend.pid" ]; then
        local frontend_pid=$(cat "$PID_DIR/frontend.pid")
        if kill -0 "$frontend_pid" 2>/dev/null; then
            echo -e "Frontend: ${GREEN}Running${NC} (PID: $frontend_pid)"
            echo "          URL: http://localhost:$FRONTEND_PORT"
        else
            echo -e "Frontend: ${RED}Stopped${NC}"
        fi
    else
        echo -e "Frontend: ${YELLOW}Not started${NC}"
    fi

    echo ""
    echo "=========================================="
    echo ""
}

# =============================================================================
# View Logs
# =============================================================================

view_logs() {
    local service=$1

    case $service in
        backend)
            if [ -f "$LOG_DIR/backend.log" ]; then
                tail -f "$LOG_DIR/backend.log"
            else
                log_error "Backend log file not found."
            fi
            ;;
        frontend)
            if [ -f "$LOG_DIR/frontend.log" ]; then
                tail -f "$LOG_DIR/frontend.log"
            else
                log_error "Frontend log file not found."
            fi
            ;;
        all)
            tail -f "$LOG_DIR/backend.log" "$LOG_DIR/frontend.log"
            ;;
        *)
            log_error "Unknown service: $service. Use 'backend', 'frontend', or 'all'."
            ;;
    esac
}

# =============================================================================
# Usage
# =============================================================================

usage() {
    echo ""
    echo "LLM Agent BBS - Deployment Script"
    echo ""
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo "  start       Start all services (default)"
    echo "  stop        Stop all services"
    echo "  restart     Restart all services"
    echo "  status      Show service status"
    echo "  setup       Setup without starting"
    echo "  logs        View logs (backend|frontend|all)"
    echo "  backend     Start only backend"
    echo "  frontend    Start only frontend"
    echo ""
    echo "Options:"
    echo "  --prod      Run in production mode"
    echo "  --dev       Run in development mode (default)"
    echo ""
    echo "Environment Variables:"
    echo "  BACKEND_PORT   Backend port (default: 8000)"
    echo "  FRONTEND_PORT  Frontend port (default: 3000)"
    echo "  MODE           dev or prod (default: dev)"
    echo ""
    echo "Examples:"
    echo "  $0 start                    # Start in dev mode"
    echo "  $0 start --prod             # Start in production mode"
    echo "  $0 stop                     # Stop all services"
    echo "  $0 logs backend             # View backend logs"
    echo "  BACKEND_PORT=9000 $0 start  # Start with custom port"
    echo ""
}

# =============================================================================
# Main
# =============================================================================

main() {
    local command=${1:-start}
    shift || true

    # Parse options
    for arg in "$@"; do
        case $arg in
            --prod)
                MODE="prod"
                ;;
            --dev)
                MODE="dev"
                ;;
        esac
    done

    echo ""
    echo "=========================================="
    echo "       LLM Agent BBS Deployment"
    echo "=========================================="
    echo "Mode: $MODE"
    echo "Backend Port: $BACKEND_PORT"
    echo "Frontend Port: $FRONTEND_PORT"
    echo "=========================================="
    echo ""

    case $command in
        start)
            check_dependencies
            setup_directories
            setup_backend
            setup_frontend
            start_backend
            start_frontend
            check_status
            ;;
        stop)
            stop_services
            ;;
        restart)
            stop_services
            sleep 2
            check_dependencies
            setup_directories
            start_backend
            start_frontend
            check_status
            ;;
        status)
            check_status
            ;;
        setup)
            check_dependencies
            setup_directories
            setup_backend
            setup_frontend
            log_success "Setup complete! Run '$0 start' to start services."
            ;;
        logs)
            view_logs "${2:-all}"
            ;;
        backend)
            check_dependencies
            setup_directories
            setup_backend
            start_backend
            ;;
        frontend)
            check_dependencies
            setup_directories
            setup_frontend
            start_frontend
            ;;
        help|--help|-h)
            usage
            ;;
        *)
            log_error "Unknown command: $command"
            usage
            exit 1
            ;;
    esac
}

# Handle Ctrl+C
trap 'echo ""; log_info "Interrupted. Stopping services..."; stop_services; exit 0' INT TERM

# Run main
main "$@"
