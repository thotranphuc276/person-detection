import logging
import json
import time
from pythonjsonlogger import jsonlogger
from elasticsearch import Elasticsearch
from datetime import datetime
from app.config import settings
from queue import Queue, Empty
import threading

# Configure JSON logger
logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    '%(asctime)s %(levelname)s %(name)s %(message)s'
)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# Configure Elasticsearch client with retries
def get_elasticsearch_client(max_retries=5, retry_delay=5):
    for attempt in range(max_retries):
        try:
            client = Elasticsearch(
                settings.ELASTICSEARCH_URL,
                request_timeout=10,  # Reduced timeout
                max_retries=3,  # Increased retries
                retry_on_timeout=True,
                sniff_on_start=True,
                sniff_on_connection_fail=True,
                sniffer_timeout=30,  # Reduced sniffer timeout
                http_compress=True,  # Enable compression
                verify_certs=False,  # Disable SSL verification for local development
                ssl_show_warn=False  # Disable SSL warnings
            )
            if client.ping():
                logger.info("Successfully connected to Elasticsearch")
                return client
            else:
                logger.warning(f"Elasticsearch ping failed (attempt {attempt + 1}/{max_retries})")
        except Exception as e:
            logger.warning(f"Failed to connect to Elasticsearch (attempt {attempt + 1}/{max_retries}): {str(e)}")
        
        if attempt < max_retries - 1:
            time.sleep(retry_delay)
    
    logger.warning("Failed to connect to Elasticsearch after all retries. Logging will be console-only.")
    return None

# Initialize Elasticsearch client
es_client = get_elasticsearch_client()

# Create a queue for async logging
log_queue = Queue()
is_worker_running = True

def log_worker():
    """Background worker to process log queue"""
    while is_worker_running:
        try:
            # Get log entry from queue with timeout
            try:
                log_data = log_queue.get(timeout=1)
            except Empty:
                continue  # No data available, continue waiting
                
            if log_data is None:  # Poison pill to stop the worker
                log_queue.task_done()
                break
                
            try:
                current_time = datetime.now()
                index_name = f"person-detection-logs-{current_time.strftime('%Y.%m.%d')}"
                es_client.index(
                    index=index_name,
                    document={
                        "@timestamp": current_time.isoformat(),
                        **log_data
                    },
                    refresh=False  # Disable refresh for better performance
                )
            except Exception as e:
                logger.error(f"Failed to send log to Elasticsearch: {str(e)}")
            finally:
                log_queue.task_done()
                
        except Exception as e:
            logger.error(f"Error in log worker: {str(e)}")
            if 'log_data' in locals() and log_data is not None:
                log_queue.task_done()

# Start the background worker
log_worker_thread = threading.Thread(target=log_worker, daemon=True)
log_worker_thread.start()

def log_to_elasticsearch(log_data):
    """Send log data to Elasticsearch asynchronously"""
    if es_client is None:
        return  # Silently skip if Elasticsearch is not available

    try:
        # Add to queue instead of sending directly
        log_queue.put(log_data, timeout=0.1)  # Short timeout to prevent blocking
    except Exception:
        pass  # Silently fail if queue is full

def setup_logging():
    """Setup logging configuration"""
    if es_client is None:
        return

    # Create index template for Elasticsearch with optimized settings
    template_name = "person-detection-logs-template"
    template_body = {
        "index_patterns": ["person-detection-logs-*"],
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "refresh_interval": "30s",  # Increase refresh interval further
            "index.translog.durability": "async",  # Use async translog
            "index.translog.sync_interval": "30s",  # Sync translog less frequently
            "index.translog.flush_threshold_size": "1gb",  # Increase flush threshold
            "index.merge.scheduler.max_thread_count": 1,  # Limit merge threads
            "index.routing.allocation.total_shards_per_node": 1,
            "index.unassigned.node_left.delayed_timeout": "5m"
        },
        "mappings": {
            "properties": {
                "@timestamp": {"type": "date"},
                "level": {"type": "keyword"},
                "message": {"type": "text"},
                "service": {"type": "keyword"},
                "detection_id": {"type": "keyword"},
                "num_people": {"type": "integer"},
                "confidence_threshold": {"type": "float"},
                "processing_time": {"type": "float"}
            }
        }
    }
    
    try:
        es_client.indices.put_template(
            name=template_name,
            body=template_body
        )
        logger.info("Successfully created Elasticsearch index template")
    except Exception as e:
        logger.error(f"Failed to create index template: {str(e)}")

# Cleanup function to stop the worker
def cleanup():
    global is_worker_running
    is_worker_running = False
    log_queue.put(None)  # Send poison pill
    log_worker_thread.join(timeout=5)  # Wait for worker to finish 