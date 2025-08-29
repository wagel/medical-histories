# Medical Histories POC :)

## Quick Start 🚀

### Prerequisites
- Docker and Docker Compose installed
- OpenAI API key

### Setup
1. Clone the repository
2. Create a `.env` file in the root directory with:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

### Launch
1. Build and start the services:
   ```bash
   docker-compose up --build
   ```
2. Access the application:
   - Frontend: http://localhost
   - Backend API: http://localhost:8000

### Development
- Frontend: Static HTML/JS served via Nginx
- Backend: FastAPI application with OpenAI integration
- Both services are containerized and orchestrated via Docker Compose

### API Endpoints
- `POST /conversations/` - Initialize a new conversation
- `POST /conversations/{conversation_id}/messages` - Continue an existing conversation
- `GET /conversations/{conversation_id}` - Get conversation history

## Resources 📚

- [Notion Page](https://www.notion.so/waggel/Medical-History-Automation-Discovery-250f6406262c80d697cbc00be15fee34?source=copy_link)
- [Vet Lexicon](https://docs.google.com/spreadsheets/d/12CggC5YvgsNhHpTsuYx7n1i5DeiMdYQDdFnRuX7CWLM/edit?gid=0#gid=0)

## Goals 🎯

- Extract data in a reliable structured way
    - Use lexicon if required
    - Use policy wording if required

## Flag System ‼️⚠️
The system flags the following issues:
- Mismatch on internal pet info
- Mismatch on internal vet info
- Mismatch on internal vet info
- Unaccounted for dates
- Illness occurring BEFORE policy
