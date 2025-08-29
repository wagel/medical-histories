# Medical Histories API

## Setup

1. Install required packages:
```bash
pip install fastapi uvicorn python-dotenv openai
```

2. Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_key_here
```

## Start the backend server locally

```bash
uvicorn src.app:app --reload --port 8000
```

The server will start at `http://localhost:8000`
- Auto-reload is enabled for development
- API documentation available at: `http://localhost:8000/docs`

## Test Endpoints

### 1. Health Check
```bash
curl http://localhost:8000/healthz
```

### 2. Create a new conversation
```bash
curl -X POST http://localhost:8000/conversations/ \
  -H "Content-Type: application/json" \
  -d '{"initial_message": "Hello, I need help with a claim"}'
```

### 3. Add message to conversation
```bash
curl -X POST http://localhost:8000/conversations/{conversation_id}/messages \
  -H "Content-Type: application/json" \
  -d '{"message": "What information do you need from me?"}'
```

### 4. Get conversation history
```bash
curl http://localhost:8000/conversations/{conversation_id}
```

## Development Notes
- Server will reset conversations on restart (in-memory storage)
- Future updates will include database persistence
- Remember to never commit your `.env` file to version control