# Local AI Support Bot Template

A template for creating a local AI-powered support bot that processes documents and provides intelligent responses using Ollama, with GPU acceleration support.

## Features

- 🐳 Docker-based setup with Ollama integration
- 📄 Document processing (PDF, TXT, DOC, DOCX)
- 🤖 Local AI processing using Ollama models
- 🔍 Document embeddings for semantic search
- 🌐 REST API interface with FastAPI
- 🚀 GPU acceleration support for faster responses
- 🔧 Configurable through environment variables

## Prerequisites

- Docker Desktop
- Docker Compose
- NVIDIA GPU with updated drivers (for GPU acceleration)
- NVIDIA Container Toolkit (for GPU support)

## Quick Start

1. Clone this template:

```bash
git clone <your-repo-url>
cd <your-project-directory>
```

2. Create a `.env` file in the project root:

```bash
OLLAMA_MODEL=llama2:7b
OLLAMA_HOST=http://ollama:11434
```

3. Start the services:

```bash
docker-compose up --build
```

The services will be available at:

- Ollama API: `http://localhost:11434`
- Support Bot API: `http://localhost:8000`

## Project Structure

```
.
├── app/                    # Application code
│   ├── main.py            # FastAPI application
│   ├── config.py          # Configuration settings
│   └── init_ollama.py     # Ollama initialization
├── documents/             # Document storage directory
├── Dockerfile            # Application container configuration
├── Dockerfile.ollama     # Ollama container configuration
├── docker-compose.yml    # Docker services configuration
├── requirements.txt      # Python dependencies
├── start-ollama.sh      # Ollama startup script
└── .env                 # Environment variables
```

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
OLLAMA_MODEL=llama2:7b    # The model to use
OLLAMA_HOST=http://ollama:11434  # Ollama service URL
```

### GPU Support

To enable GPU acceleration:

1. Ensure NVIDIA drivers are installed on your host machine
2. Install NVIDIA Container Toolkit
3. Configure Docker Desktop to use NVIDIA runtime
4. Set `runtime: nvidia` in docker-compose.yml (already configured)

## API Endpoints

- `POST /upload`: Upload new documents
- `GET /query`: Query the AI with your questions
- `GET /docs`: API documentation (Swagger UI)

## Development

### Testing

The API includes Swagger documentation at `http://localhost:8000/docs` for testing endpoints.

### CLI Interface

A command-line interface is available for easy interaction:

```bash
python app/cli.py
```

## Troubleshooting

1. If models fail to download:

   - Check your internet connection
   - Verify model names in `.env`
   - Check Docker logs: `docker-compose logs ollama`

2. If the API is not responding:

   - Ensure all containers are running: `docker-compose ps`
   - Check application logs: `docker-compose logs app`

3. If GPU is not being used:
   - Verify NVIDIA drivers are installed
   - Check GPU usage in Task Manager
   - Ensure NVIDIA Container Toolkit is installed
   - Check Docker Desktop settings for NVIDIA runtime

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
