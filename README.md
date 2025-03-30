# TikTok Influencer Analysis Application

This application automates the workflow of identifying top TikTok influencers, downloading their latest videos, extracting and summarizing content, and sending email summaries.

## Architecture Overview

The application follows a modular design with the following components:

### 1. TikTok Influencer Identification
- Retrieves data to determine the top 10 TikTok influencers based on metrics like engagement and follower count
- Supports multiple data sources: TikTok API, CSV files, or mock data
- Implemented in the `tiktok_analyzer.api` module

### 2. Video Downloading
- Downloads the most recent video from each top influencer in parallel
- Handles different video formats and access restrictions
- Stores videos locally for processing
- Implemented in the `tiktok_analyzer.video_processor` module

### 3. Content Extraction and Analysis
- Extracts embedded text from videos when available
- Converts speech to text using speech recognition
- Processes and cleans extracted text for summarization
- Analyzes content sentiment and extracts key points
- Implemented in the `tiktok_analyzer.video_processor` module

### 4. Content Summarization
- Uses an LLM (OpenAI) to create concise summaries of extracted text
- Handles rate limits and errors gracefully
- Implemented in the `tiktok_analyzer.summarizer` module

### 5. Email Sending
- Composes emails with summaries for each influencer's video
- Sends emails to designated recipients
- Configurable SMTP or email service integration
- Implemented in the `tiktok_analyzer.emailer` module

### 6. Workflow Orchestration
- Coordinates the entire process from influencer identification to email sending
- Handles errors and logging
- Supports command-line arguments for configuration
- Implemented in the main application module

## Project Structure

```
crypto_new_tiktok/
├── data/                           # Sample data for testing
│   ├── tiktok_users.csv            # Sample influencer data
│   └── tiktok_videos.csv           # Sample video data
├── src/
│   ├── tiktok_analyzer/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── influencer_analyzer.py      # TikTok influencer identification
│   │   │   ├── tiktok_client.py            # TikTok API client
│   │   │   └── data_sources/               # Data source implementations
│   │   │       ├── __init__.py
│   │   │       ├── base_data_source.py     # Base data source interface
│   │   │       ├── tiktok_api_source.py    # TikTok API data source
│   │   │       ├── csv_data_source.py      # CSV file data source
│   │   │       ├── mock_data_source.py     # Mock data source for testing
│   │   │       └── data_source_factory.py  # Factory for creating data sources
│   │   ├── video_processor/
│   │   │   ├── __init__.py
│   │   │   ├── downloader.py               # Video downloading
│   │   │   ├── content_extractor.py        # Text and speech extraction
│   │   │   └── content_analyzer.py         # Content analysis and summarization
│   │   ├── summarizer/
│   │   │   ├── __init__.py
│   │   │   └── text_summarizer.py          # LLM-based summarization
│   │   ├── emailer/
│   │   │   ├── __init__.py
│   │   │   ├── email_composer.py           # Email composition
│   │   │   ├── email_sender.py             # Email sending
│   │   │   └── email_manager.py            # Email management
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── config.py                   # Configuration management
│   │       └── logger.py                   # Logging utilities
│   └── main.py                             # Main application entry point
├── requirements.txt                        # Dependencies
├── .env.example                            # Example environment variables
└── README.md                               # This file
```

## Data Flow

1. The `main.py` script initializes the workflow with configuration options
2. `InfluencerAnalyzer` identifies the top 10 TikTok influencers using the configured data source
3. `VideoDownloader` downloads the latest video from each influencer in parallel
4. `ContentAnalyzer` extracts text from the videos and generates summaries
5. `EmailManager` composes and sends an email with all the summaries to the designated recipient

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- ffmpeg (for video processing)
- tesseract-ocr (for OCR text extraction)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/jianhuanggo/crypto_new_tiktok.git
   cd crypto_new_tiktok
   ```

2. Install ffmpeg and tesseract-ocr:
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install -y ffmpeg tesseract-ocr
   
   # macOS
   brew install ffmpeg tesseract
   
   # Windows
   # Download and install from respective websites
   ```

3. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   
   # Activate on Windows
   venv\Scripts\activate
   
   # Activate on macOS/Linux
   source venv/bin/activate
   ```

4. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file with your API keys and configuration:
   ```
   # TikTok API Configuration
   TIKTOK_API_KEY=your_tiktok_api_key
   
   # OpenAI API Configuration
   OPENAI_API_KEY=your_openai_api_key
   
   # Email Configuration
   EMAIL_SENDER=your_email@example.com
   EMAIL_PASSWORD=your_email_password
   EMAIL_RECIPIENT=recipient@example.com
   SMTP_SERVER=smtp.example.com
   SMTP_PORT=587
   
   # Data Source Configuration
   # Options: api, csv, mock
   DATA_SOURCE_TYPE=csv
   
   # Storage Configuration
   VIDEO_STORAGE_PATH=./downloads/videos
   ```

### Configuration Options

#### Data Sources

The application supports multiple data sources for TikTok influencer data:

1. **TikTok API** (`api`): Uses the TikTok API to fetch real-time data. Requires a valid API key.
2. **CSV Files** (`csv`): Uses local CSV files for testing. Sample files are provided in the `data/` directory.
3. **Mock Data** (`mock`): Generates mock data for testing without external dependencies.

Configure the data source in the `.env` file or using the `--data-source` command-line argument.

#### Email Configuration

The application uses SMTP to send emails. Configure your email settings in the `.env` file:

- `EMAIL_SENDER`: Your email address
- `EMAIL_PASSWORD`: Your email password or app password
- `EMAIL_RECIPIENT`: Default recipient email address
- `SMTP_SERVER`: SMTP server address (e.g., smtp.gmail.com)
- `SMTP_PORT`: SMTP server port (e.g., 587 for TLS)

For Gmail, you may need to use an app password instead of your regular password. See [Google's documentation](https://support.google.com/accounts/answer/185833) for details.

## Usage

### Basic Usage

Run the application with default settings:

```bash
python src/main.py
```

This will:
1. Identify the top 10 TikTok influencers
2. Download their latest videos
3. Extract and summarize the content
4. Send an email with the summaries to the configured recipient

### Command-Line Options

The application supports several command-line options:

```bash
python src/main.py --help
```

Available options:

- `--data-source {api,csv,mock}`: Data source type (default: from .env file)
- `--limit INT`: Number of top influencers to analyze (default: 10)
- `--recipient EMAIL`: Email recipient (default: from .env file)
- `--max-workers INT`: Maximum number of concurrent downloads (default: 5)
- `--test-email`: Send a test email to verify email configuration

Examples:

```bash
# Use mock data and analyze only 5 influencers
python src/main.py --data-source mock --limit 5

# Use CSV data and send to a specific recipient
python src/main.py --data-source csv --recipient user@example.com

# Use TikTok API with 8 parallel downloads
python src/main.py --data-source api --max-workers 8

# Send a test email to verify configuration
python src/main.py --test-email
```

## Module Details

### 1. Influencer Identification Module

The `InfluencerAnalyzer` class in `tiktok_analyzer.api.influencer_analyzer` identifies top TikTok influencers based on metrics like engagement rate, follower count, and video views.

Key features:
- Supports multiple data sources through the Strategy pattern
- Calculates engagement rates and other metrics
- Sorts and filters influencers based on configurable criteria
- Handles pagination and rate limits for API requests

### 2. Video Downloader Module

The `VideoDownloader` class in `tiktok_analyzer.video_processor.downloader` downloads videos from TikTok influencers.

Key features:
- Parallel downloading using ThreadPoolExecutor
- Robust error handling for network issues
- Automatic retries for failed downloads
- Metadata preservation for downloaded videos
- Support for different video formats

### 3. Content Extraction and Summarization Module

The `ContentAnalyzer` class in `tiktok_analyzer.video_processor.content_analyzer` extracts and summarizes video content.

Key features:
- Extracts embedded text using OCR (Optical Character Recognition)
- Converts speech to text using the SpeechRecognition library
- Summarizes content using OpenAI's GPT models
- Analyzes sentiment and extracts key points
- Handles videos with no extractable content

### 4. Email Sending Module

The `EmailManager` class in `tiktok_analyzer.emailer.email_manager` composes and sends emails with video summaries.

Key features:
- Composes HTML emails with influencer information and video summaries
- Sends emails using SMTP with TLS encryption
- Supports batch sending to multiple recipients
- Includes error handling and notification
- Test email functionality for configuration verification

## Troubleshooting

### Common Issues

1. **TikTok API Access**: TikTok's API has usage restrictions. If you encounter rate limits, try using the CSV or mock data source for testing.

2. **Video Download Failures**: Some TikTok videos may be restricted or unavailable. The application will log these issues and continue with available videos.

3. **Speech Recognition Accuracy**: Speech-to-text conversion may not be perfect, especially for videos with background music or poor audio quality.

4. **Email Sending Issues**: If emails fail to send, check your SMTP configuration and credentials. For Gmail, ensure you're using an app password if 2FA is enabled.

### Logging

The application logs detailed information to help diagnose issues:

- Log files are stored in the `logs/` directory
- Log level can be configured in the `.env` file
- Each module logs its operations with appropriate severity levels

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [TikTokApi](https://github.com/davidteather/TikTok-Api) for TikTok data access
- [SpeechRecognition](https://github.com/Uberi/speech_recognition) for speech-to-text conversion
- [OpenAI](https://github.com/openai/openai-python) for text summarization
- [MoviePy](https://github.com/Zulko/moviepy) for video processing
