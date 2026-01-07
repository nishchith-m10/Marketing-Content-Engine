#!/bin/bash

# Apply database migrations directly to Supabase
# Usage: ./apply-migrations.sh

SUPABASE_URL="https://vciscdagwhdpstaviakz.supabase.co"
SERVICE_KEY="[REDACTED]"

echo "🔐 Applying security and performance fixes migration..."
SQL_CONTENT=$(cat supabase/migrations/20260105154429_security_and_performance_fixes.sql)

curl -X POST \
  "${SUPABASE_URL}/rest/v1/rpc/exec_sql" \
  -H "apikey: ${SERVICE_KEY}" \
  -H "Authorization: Bearer ${SERVICE_KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"query\": $(echo "$SQL_CONTENT" | jq -Rs .)}"

echo ""
echo "🔐 Applying budget enforcement migration..."
SQL_CONTENT2=$(cat supabase/migrations/20260105160000_budget_enforcement.sql)

curl -X POST \
  "${SUPABASE_URL}/rest/v1/rpc/exec_sql" \
  -H "apikey: ${SERVICE_KEY}" \
  -H "Authorization: Bearer ${SERVICE_KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"query\": $(echo "$SQL_CONTENT2" | jq -Rs .)}"

echo ""
echo "✅ Migrations applied successfully!"
