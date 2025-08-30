#!/usr/bin/env bash
set -euo pipefail

# ========= CONFIG =========
API_KEY_FILE="/Users/odysseus/git/HRPC-YouTube-Scheduler/Shell_Scripts/.openai_api_key"
MODEL="gpt-4o-mini"
ENDPOINT="https://api.openai.com/v1/chat/completions"

INPUT_DIR="/Users/odysseus/Documents/Church_Docs/HRPC_Sermon/Transcript"
OUTPUT_DIR="/Users/odysseus/Documents/Church_Docs/HRPC_Sermon/Summary"

SYSTEM_PROMPT="You write concise podcast blurbs for weekly church sermons."
USER_PROMPT=$"Return 2–3 sentences (≈350 characters max), plain English, warm but not “church-insider,” and include zero emojis or hashtags. Emphasise the big idea + everyday relevance. Avoid repeating the title but it's ok to talk about the passage that is being preached on. Use only the transcript below."
#==========================

if [[ ! -f "$API_KEY_FILE" ]]; then
  $HOME/hrpc_po.sh "❌ API key file not found at $API_KEY_FILE"
  exit 1
fi

OPENAI_API_KEY="$(cat "$API_KEY_FILE" | tr -d '[:space:]')"

if [[ $# -lt 1 ]]; then
  $HOME/hrpc_po.sh "❌ Usage error: missing transcript filename"
  exit 1
fi

INPUT_FILE="$INPUT_DIR/$1"
BASENAME="$(basename "$INPUT_FILE" .txt)"
OUTPUT_FILE="$OUTPUT_DIR/${BASENAME}-blurb.txt"

echo "→ Processing: $INPUT_FILE"

if [[ ! -f "$INPUT_FILE" ]]; then
  $HOME/hrpc_po.sh "❌ Transcript not found: $INPUT_FILE"
  exit 1
fi

TRANSCRIPT="$(cat "$INPUT_FILE")"

payload=$(jq -n \
  --arg model "$MODEL" \
  --arg sys "$SYSTEM_PROMPT" \
  --arg user "$USER_PROMPT" \
  --arg t "$TRANSCRIPT" \
  '{
     model: $model,
     temperature: 0.7,
     max_tokens: 300,
     messages: [
       {role:"system", content:$sys},
       {role:"user",   content: ($user + "\n\nTranscript:\n" + $t)}
     ]
   }')

response="$(curl -sS "$ENDPOINT" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$payload")"

blurb="$(echo "$response" | jq -r '.choices[0].message.content // empty')"

if [[ -z "$blurb" ]]; then
  echo "ERROR: No content returned. Raw response follows:" >&2
  echo "$response" >&2
  $HOME/hrpc_po.sh "❌ Summary failed for: $BASENAME"
  exit 1
fi

printf "%s\n" "$blurb" > "$OUTPUT_FILE"
echo "✓ Wrote: $OUTPUT_FILE"

# Success notification with filename
$HOME/hrpc_po.sh "✅ Summary finished: $BASENAME"
exit 0