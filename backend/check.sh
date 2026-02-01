#!/usr/bin/env bash
# Static code quality checks script

set -e

echo "🔍 Running static code checks..."
echo ""

echo "1️⃣  Running ruff linter..."
uv run ruff check src/ tests/
echo "✅ Ruff checks passed!"
echo ""

echo "2️⃣  Running ruff formatter check..."
uv run ruff format --check src/ tests/
echo "✅ Format checks passed!"
echo ""

echo "3️⃣  Running pyright type checker..."
uv run pyright src/ tests/
echo "✅ Type checks passed!"
echo ""

echo "4️⃣  Running tests..."
uv run pytest tests/unit/domain/ -v --tb=short
echo "✅ Tests passed!"
echo ""

echo "🎉 All checks passed successfully!"
