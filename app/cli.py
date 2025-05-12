import requests
import json
import sys
import os
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown
from config import OLLAMA_HOST, MODEL_NAME
from document_processor import DocumentProcessor
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

console = Console()

class SupportBotCLI:
    def __init__(self):
        self.api_url = f"{OLLAMA_HOST}/api"
        self.console = Console()
        self.document_processor = DocumentProcessor()
        logger.info("Document processor initialized")

    def get_ollama_response(self, prompt: str, context: list = None) -> str:
        """Get response from Ollama API with optional context."""
        try:
            # Construct the full prompt with context if available
            full_prompt = prompt
            if context:
                context_text = "\n\n".join([doc["content"] for doc in context])
                full_prompt = f"""Context information:
{context_text}

Based on the above context, please answer the following question:
{prompt}"""

            logger.info("Sending request to Ollama API...")
            response = requests.post(
                f"{self.api_url}/generate",
                json={
                    "model": MODEL_NAME,
                    "prompt": full_prompt,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                logger.error(f"Error from Ollama API: {response.status_code} - {response.text}")
                return "Error: Could not get response from Ollama API"
        except Exception as e:
            logger.error(f"Error communicating with Ollama API: {str(e)}")
            return f"Error: {str(e)}"

    def process_question(self, question: str):
        """Process a question with document context."""
        try:
            # Get relevant context from documents
            logger.info("Retrieving relevant context from documents...")
            context = self.document_processor.get_relevant_context(question)
            
            if context:
                logger.info(f"Found {len(context)} relevant document chunks")
                self.console.print("[green]Found relevant context in documents[/green]")
            else:
                logger.info("No relevant context found in documents")
                self.console.print("[yellow]No relevant context found in documents[/yellow]")

            # Get response from Ollama with context
            response = self.get_ollama_response(question, context)
            self.console.print(Panel(response, title="Bot's Response", border_style="yellow"))

        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")

    def run(self):
        """Run the CLI interface."""
        self.console.print(Panel(
            "Local AI Support Bot\nType 'exit' to quit",
            title="Welcome",
            border_style="blue"
        ))

        while True:
            try:
                question = self.console.input("\n[bold blue]You:[/bold blue] ")
                
                if question.lower() == 'exit':
                    self.console.print("[yellow]Goodbye![/yellow]")
                    break
                
                if not question.strip():
                    continue

                self.process_question(question)

            except KeyboardInterrupt:
                self.console.print("\n[yellow]Goodbye![/yellow]")
                break
            except Exception as e:
                self.console.print(f"[red]Error: {str(e)}[/red]")

if __name__ == "__main__":
    cli = SupportBotCLI()
    cli.run() 