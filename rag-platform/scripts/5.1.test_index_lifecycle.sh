#!/bin/bash

set -e

CHUNKS="data/processed/chunks/ZCompanyLLC"
BACKUP="/tmp/m53_backup"
LOG="logs/indexing.log"

rm -rf "$BACKUP"
mkdir -p "$BACKUP"

echo
echo "========================================"
echo "M5.3 LIFECYCLE VALIDATION"
echo "========================================"

# --------------------------------------------------
# Select two document chunk files
# --------------------------------------------------

FILES=($(find "$CHUNKS" -type f -name "*.jsonl" | sort))

FILE1="${FILES[0]}"
FILE2="${FILES[1]}"

echo
echo "Test document : $FILE1"
echo "Delete document: $FILE2"

# Back up both
cp "$FILE1" "$BACKUP/file1.jsonl"
cp "$FILE2" "$BACKUP/file2.jsonl"

# --------------------------------------------------
# 1. CHANGED DOCUMENT
# --------------------------------------------------

echo
echo "========================================"
echo "1. CHANGED DOCUMENT"
echo "========================================"

python - "$FILE1" <<'PY'
import json
import sys

path = sys.argv[1]

with open(path, encoding="utf-8") as f:
    records = [json.loads(line) for line in f if line.strip()]

records[0]["text"] += "\n\nM53_TEST_CHANGE: temporary lifecycle validation."

with open(path, "w", encoding="utf-8") as f:
    for record in records:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
PY

uv run python scripts/5.index_documents.py

echo
echo "Expected: 1 changed, remaining documents unchanged."

# --------------------------------------------------
# Restore changed document
# --------------------------------------------------

echo
echo "Restoring changed document..."

cp "$BACKUP/file1.jsonl" "$FILE1"

uv run python scripts/5.index_documents.py

echo
echo "Restoration complete."

# --------------------------------------------------
# 2. DELETED DOCUMENT
# --------------------------------------------------

echo
echo "========================================"
echo "2. DELETED DOCUMENT"
echo "========================================"

mkdir -p "$BACKUP/deleted"

mv "$FILE2" "$BACKUP/deleted/"

uv run python scripts/5.index_documents.py

echo
echo "Expected: 1 deleted, remaining documents unchanged."

# --------------------------------------------------
# Restore deleted document
# --------------------------------------------------

echo
echo "Restoring deleted document..."

mv "$BACKUP/deleted/$(basename "$FILE2")" "$FILE2"

uv run python scripts/5.index_documents.py

echo
echo "Deletion restoration complete."

# --------------------------------------------------
# 3. FULL REBUILD
# --------------------------------------------------

echo
echo "========================================"
echo "3. FULL REBUILD"
echo "========================================"

uv run python scripts/5.index_documents.py --rebuild

echo
echo "Expected: full corpus indexed."

# --------------------------------------------------
# 4. TEST SUITE
# --------------------------------------------------

echo
echo "========================================"
echo "4. TEST SUITE"
echo "========================================"

uv run pytest

# --------------------------------------------------
# 5. LOG SUMMARY
# --------------------------------------------------

echo
echo "========================================"
echo "5. INDEXING LOG — LIFECYCLE EVENTS"
echo "========================================"

grep -E \
"document_new_indexing|document_changed_reindexing|document_unchanged_skipped|document_deleted_from_index|full_index_rebuild_started|indexing_manifest_saved|indexing_completed" \
"$LOG" | tail -40

echo
echo "========================================"
echo "M5.3 LIFECYCLE VALIDATION COMPLETE"
echo "========================================"

rm -rf "$BACKUP"
