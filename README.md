# Scam Ad Mock API & Data Generator

This project provides a mock API for generating realistic scam advertisement data and a script to populate a Supabase database with this data.

## Files

- `mock_api.py` - FastAPI-based mock API that generates scam ad data
- `insert_mock_ads.py` - Script to fetch data from the mock API and insert it into Supabase
- `insert_batches.py` - Alternative batch insertion script
- `requirements.txt` - Python dependencies
- `Procfile` - For Railway/Heroku deployment
- `railway.json` - Railway deployment configuration

## Features

- **50 Scam-related Keywords**: Investment, crypto, lottery, tech support, authority impersonation, etc.
- **Keyword-based Categories**: Categories generated based on search keywords
- **Thai Localization**: Default location set to Thailand with Thai locations
- **Image Upload**: Downloads and uploads images to Supabase storage
- **Flexible Filtering**: Filter by location, language, advertiser, platform, media type, status, date range

## API Usage

### Local Development
```bash
# Start the API
python mock_api.py

# The API will be available at http://localhost:8000
```

### Request Format
```json
{
  "keyword": ["investment", "crypto", "winner"],
  "location": "thailand",
  "language": "thai",
  "limit": 100
}
```

## Deployment

### Railway (Recommended - Free)
1. Push to GitHub
2. Connect to Railway.app
3. Deploy automatically

### Environment Variables
- `MOCK_API_URL` - URL of the deployed mock API (for insert_mock_ads.py)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Update the Supabase credentials in `insert_mock_ads.py`:
- `SUPABASE_URL`
- `SUPABASE_KEY`

## Usage

1. Deploy the mock API or run locally
2. Set the `MOCK_API_URL` environment variable if using deployed version
3. Run the data insertion script:
   ```bash
   python insert_mock_ads.py
   ``` 