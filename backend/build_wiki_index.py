import re
import argparse
import wikipedia
import logging
from typing import List, Dict, Any
from retrieval.faiss_index import DocumentRetriever

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Core topics to build a robust initial database
DEFAULT_TOPICS = [
    "Earth",
    "Solar System",
    "Moon",
    "Moon landing",
    "Climate change",
    "Vaccine",
    "mRNA vaccine",
    "DNA",
    "Artificial intelligence",
    "World War II"
]

def segment_text(text: str) -> List[str]:
    """Segments raw text into individual sentences."""
    # Split on punctuation followed by space and capital letter
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
    return [s.strip() for s in sentences if len(s.strip()) > 10]

def build_wikipedia_index(topics: List[str] = DEFAULT_TOPICS, max_articles: int = 5):
    """Fetches Wikipedia articles and adds them to the FAISS index."""
    retriever = DocumentRetriever(storage_dir="storage")
    
    logger.info(f"Starting Wikipedia knowledge base build for {len(topics)} topics...")
    
    all_chunks = []
    all_metadata = []
    
    for topic in topics:
        logger.info(f"Searching Wikipedia for: {topic}")
        try:
            # Search for relevant page titles
            search_results = wikipedia.search(topic, results=max_articles)
            
            for title in search_results:
                logger.info(f"  -> Fetching page: {title}")
                try:
                    page = wikipedia.page(title, auto_suggest=False)
                    text = page.content
                    
                    # Clean up wiki headers (e.g., "== History ==")
                    text = re.sub(r'==+[^=]+==+', '', text)
                    
                    # Segment into sentences to use as chunks
                    sentences = segment_text(text)
                    
                    for i, sentence in enumerate(sentences):
                        all_chunks.append(sentence)
                        all_metadata.append({
                            "source": "Wikipedia",
                            "title": title,
                            "url": page.url,
                            "chunk_index": i
                        })
                except wikipedia.exceptions.DisambiguationError as e:
                    logger.warning(f"  -> Disambiguation page for {title}, skipping. Options: {e.options[:3]}")
                except wikipedia.exceptions.PageError:
                    logger.warning(f"  -> Page not found: {title}")
                except Exception as e:
                    logger.error(f"  -> Error processing {title}: {e}")
                    
        except Exception as e:
            logger.error(f"Error searching for {topic}: {e}")
            
    # Add to FAISS index in batches to avoid memory blowouts
    BATCH_SIZE = 1000
    total_added = 0
    
    logger.info(f"Total chunks extracted: {len(all_chunks)}. Beginning embedding and indexing...")
    
    for i in range(0, len(all_chunks), BATCH_SIZE):
        batch_chunks = all_chunks[i:i+BATCH_SIZE]
        batch_meta = all_metadata[i:i+BATCH_SIZE]
        
        logger.info(f"Processing batch {i//BATCH_SIZE + 1} ({len(batch_chunks)} chunks)...")
        retriever.add_documents(batch_chunks, batch_meta)
        total_added += len(batch_chunks)
        
    logger.info(f"✅ Successfully built Wikipedia FAISS index! Extracted {total_added} facts from {len(topics)} topics.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build FAISS Knowledge Base from Wikipedia")
    parser.add_argument("--topics", nargs="+", help="Specific Wikipedia topics to index")
    parser.add_argument("--max-articles", type=int, default=5, help="Number of articles per topic")
    
    args = parser.parse_args()
    
    topics_to_index = args.topics if args.topics else DEFAULT_TOPICS
    build_wikipedia_index(topics_to_index, args.max_articles)
