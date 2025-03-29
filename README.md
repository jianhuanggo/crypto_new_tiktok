# TikTok Influencer Analysis Application

This application automates the workflow of identifying top TikTok influencers, downloading their latest videos, extracting and summarizing content, and sending email summaries.

## Architecture Overview

The application follows a modular design with the following components:

### 1. TikTok Influencer Identification
- Retrieves data to determine the top 10 TikTok influencers based on metrics like engagement and follower count
- Supports multiple data sources: TikTok API, web scraping, or provided datasets
- Implemented in the `tiktok_analyzer.api` module

### 2. Video Downloading
- Downloads the most recent video from each top influencer
- Handles different video formats and access restrictions
- Stores videos locally for processing
- Implemented in the `tiktok_analyzer.video_processor` module

### 3. Content Extraction
- Extracts embedded text from videos when available
- Converts speech to text using speech recognition
- Processes and cleans extracted text for summarization
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
- Implemented in the main application module

## Project Structure

```
src/
├── tiktok_analyzer/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── influencer_analyzer.py  # TikTok influencer identification
│   │   └── tiktok_client.py        # TikTok API client
│   ├── video_processor/
│   │   ├── __init__.py
│   │   ├── downloader.py           # Video downloading
│   │   └── content_extractor.py    # Text and speech extraction
│   ├── summarizer/
│   │   ├── __init__.py
│   │   └── text_summarizer.py      # LLM-based summarization
│   ├── emailer/
│   │   ├── __init__.py
│   │   ├── email_composer.py       # Email composition
│   │   └── email_sender.py         # Email sending
│   └── utils/
│       ├── __init__.py
│       ├── config.py               # Configuration management
│       └── logger.py               # Logging utilities
├── main.py                         # Main application entry point
├── requirements.txt                # Dependencies
└── .env.example                    # Example environment variables
```

## Data Flow

1. The `main.py` script initializes the workflow
2. `InfluencerAnalyzer` identifies the top 10 TikTok influencers
3. `VideoDownloader` downloads the latest video from each influencer
4. `ContentExtractor` extracts text from the videos (embedded text and speech)
5. `TextSummarizer` creates concise summaries of the extracted content
6. `EmailComposer` creates an email with all the summaries
7. `EmailSender` sends the email to the designated recipient

## Dependencies

- TikTok-Api: For TikTok data access and video downloading
- SpeechRecognition: For speech-to-text conversion
- OpenAI: For text summarization
- Python's built-in email and smtplib: For email sending

## Setup and Usage

See the setup instructions in the documentation for details on how to install dependencies and configure the application.
