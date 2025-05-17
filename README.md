# PowerPoint Presentation Generator

A Flask-based web application that automatically generates beautiful PowerPoint presentations with modern styling and professional layouts. This application is particularly useful for creating technical presentations, comparisons, and detailed analyses.

For author information and additional project details, please see the [INCLUDE](INCLUDE) file.

## Features

- Automatic presentation generation from structured content
- Modern slide designs with consistent styling
- Support for different slide types:
  - Title slides
  - Content slides
  - Table slides
- Professional formatting with:
  - Consistent typography
  - Modern color scheme
  - Dynamic layouts
  - Decorative elements
- Clean and intuitive web interface

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ppt_generator.git
cd ppt_generator
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
python app.py
```
or
```bash
py app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Enter your presentation topic and content in the web interface

4. Click "Generate" to create your presentation

5. Download the generated PowerPoint file

## Project Structure

```
ppt_generator/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── presentations/         # Generated presentations storage
├── src/
│   ├── controllers/      # Request handlers
│   ├── models/           # Data models
│   ├── services/         # Business logic
│   └── templates/        # HTML templates
└── static/               # Static assets (CSS, JS, images)
```

## Configuration

The application can be configured through environment variables:
- `FLASK_ENV`: Set to `development` for debug mode
- `PORT`: Server port (default: 5000)
- `HOST`: Server host (default: 0.0.0.0)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the Apache License, Version 2.0 - see the [LICENSE](LICENSE) file for details.

## Author

For author information and contact details, please refer to the [INCLUDE](INCLUDE) file.

## Acknowledgments

- Built with Python-PPTX for PowerPoint generation
- Flask web framework
- Modern UI/UX design principles
- Special thanks to all contributors 