# 🤖 AI Impact Proof

Measure, explain and prove the impact of AI on software delivery.

## Overview

AI Impact Proof is a Streamlit application that analyzes GitHub repositories to measure and demonstrate the impact of AI on software development. It collects evidence, calculates impact metrics, and generates comprehensive reports.

## Features

- **GitHub Integration**: Connect any GitHub repository (public or private)
- **AI Evidence Detection**: Identify AI references in commits and pull requests
- **Impact Analysis**: Calculate time saved, quality improvements, and ROI
- **Confidence Scoring**: Assess the reliability of measurements
- **Safety Checking**: Detect potentially sensitive information
- **PDF Reports**: Generate professional impact reports

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/alinidbouhou87-alt/ai-impact-proof.git
cd ai-impact-proof

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Run the Streamlit App

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

### Step-by-Step Guide

1. **Connect a GitHub Project**
   - Enter a GitHub repository URL (e.g., `https://github.com/owner/repository`)
   - Optionally provide a GitHub personal access token for private repositories
   - Click "Analyze Project"

2. **Review Project Evidence**
   - View the number of commits and pull requests analyzed
   - See AI evidence detected in the repository

3. **Input AI Impact Metrics**
   - Estimate hours saved by AI
   - Set quality score (0-100)
   - Enter rework hours
   - Specify AI tool cost
   - Define developer hourly rate

4. **View Results**
   - AI Impact score
   - Time saved calculations
   - Estimated monetary value and ROI
   - Confidence level assessment
   - Safety analysis results

5. **Download Report**
   - Generate a professional PDF report
   - Download and share with stakeholders

## GitHub Token Setup

For private repositories or higher API rate limits, create a GitHub personal access token:

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Click "Generate new token (classic)"
3. Select `repo` scope
4. Copy the token and paste it in the application

## API Rate Limits

- **Without token**: 60 requests/hour
- **With token**: 5,000 requests/hour

## Modules

### `github_data.py`
Fetches repository data including commits, pull requests, and metadata.

### `evidence_engine.py`
Detects AI-related keywords and evidence in repository metadata.

### `confidence_engine.py`
Calculates confidence scores based on available data and evidence quality.

### `safety_checker.py`
Scans for potentially sensitive information like API keys and credentials.

### `impact_engine.py`
Calculates AI impact metrics including time saved, cost, and ROI.

### `report_generator.py`
Generates professional PDF reports of the analysis.

## Configuration

Edit `requirements.txt` to adjust library versions or add additional dependencies.

## Troubleshooting

### "Repository not found" error
- Verify the repository URL is correct
- For private repositories, ensure your GitHub token has `repo` scope
- Check your network connection

### Rate limit errors
- Use a personal access token
- Wait for the rate limit window to reset (typically 1 hour)

### PDF generation issues
- Ensure `reportlab` is installed: `pip install reportlab`
- Check file permissions in the output directory

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

MIT License - see LICENSE file for details

## Support

For issues and questions, please open an issue on the GitHub repository.
