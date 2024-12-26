# Hotel Customer Feedback Analysis

## Project Overview
The Hotel Customer Feedback Analysis project focuses on analyzing customer reviews to extract meaningful insights. The application identifies the sentiment (positive or negative) and provides summarized feedback to help hotel management improve their services. The tool also integrates user ratings (on a scale of 1-5) for comprehensive feedback analysis.

## Features
- Sentiment Analysis: Classifies reviews as positive or negative.
- Summarization: Generates concise summaries of user reviews.
- Integration of ratings (1-5) for enhanced review insights.
- Interactive and user-friendly web interface for submitting reviews.

## Technologies Used
- **Frontend:** HTML
- **Backend:** Python (Flask)
- **Machine Learning:** Sentiment analysis and summarization models
- **Data Handling:** Pandas for data preprocessing
- **Deployment:** Flask-based server for handling requests

## File Structure
```
.
|-- templates/                # HTML templates for the web interface
|-- static/                   # Static files (CSS, JavaScript)
|-- app.py                    # Flask application
|--Hotel_reviews.csv
|-- README.md                 # Project documentation
```

## Setup Instructions
### Prerequisites
- Python 3.8 or above
- Virtual environment (recommended)

### Steps
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd hotel_customer_feedback_analysis
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the Flask server:
   ```bash
   python app.py
   ```

5. Open the application in a browser:
   ```

   http://localhost:5000
   ```

## Usage
1. Enter a review and provide a rating on the web interface.
2. Submit the review to view the sentiment and summarized feedback.
3. Review the insights for further analysis.

## Future Enhancements
- Multi-language support for reviews.
- Enhanced visualizations for data insights.
- Advanced filtering options based on date, rating, or sentiment.

## Contributors
- **Tanu Sree** - [GitHub Profile](https://github.com/kolliparatanusree)

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- OpenAI for NLP tools.
- Flask and Python communities for robust support and documentation.

