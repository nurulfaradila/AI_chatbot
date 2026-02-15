#!/bin/bash

echo "=========================================="
echo "RAG Chatbot API Test Script"
echo "=========================================="
echo ""

BASE_URL="http://localhost:8000"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' 

echo -e "${BLUE}1. Health Check${NC}"
echo "GET $BASE_URL/health"
echo ""
curl -s $BASE_URL/health | python3 -m json.tool
echo ""
echo ""

echo -e "${BLUE}2. Creating FAISS Index${NC}"
echo "POST $BASE_URL/index"
echo ""
curl -s -X POST $BASE_URL/index \
  -H "Content-Type: application/json" \
  -d '{"documents_path": "data/documents"}' | python3 -m json.tool
echo ""
echo ""

echo -e "${BLUE}3. Query: What is RAG?${NC}"
echo "POST $BASE_URL/query"
echo ""
curl -s -X POST $BASE_URL/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is RAG and how does it work?",
    "k": 4
  }' | python3 -m json.tool
echo ""
echo ""

echo -e "${BLUE}4. Query: What are the benefits of RAG?${NC}"
echo "POST $BASE_URL/query"
echo ""
curl -s -X POST $BASE_URL/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the benefits of using RAG?",
    "k": 3
  }' | python3 -m json.tool
echo ""
echo ""

echo -e "${BLUE}5. Query: Local vs Cloud RAG${NC}"
echo "POST $BASE_URL/query"
echo ""
curl -s -X POST $BASE_URL/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the advantages of local RAG over cloud-based solutions?",
    "k": 4
  }' | python3 -m json.tool
echo ""
echo ""

echo -e "${BLUE}6. Query: Question NOT in documents${NC}"
echo "POST $BASE_URL/query"
echo ""
curl -s -X POST $BASE_URL/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the capital of France?",
    "k": 4
  }' | python3 -m json.tool
echo ""
echo ""

echo -e "${GREEN}=========================================="
echo "Test script completed!"
echo "==========================================${NC}"
