# AI Presentation Generator

A modern web application that generates beautiful presentations using AI, with a focus on interactivity and professional design using reveal.js.

## Features

- **AI-Powered Content Generation**: 
  - Automatically generates comprehensive presentation content based on your topic
  - Smart content structuring and organization
  - Professional tone and formatting

- **Interactive HTML Presentations**: 
  - Built with reveal.js for smooth, modern presentations
  - Real-time preview in the browser
  - Beautiful transitions and animations
  - Responsive design for all screen sizes
  - Four presentation styles:
    - Corporate (Professional and clean)
    - Modern (Bold and contemporary)
    - Minimal (Simple and elegant)
    - Creative (Dynamic and engaging)

- **Export Options**:
  1. **PDF Export**
     - Professional print quality
     - Perfect page breaks
     - Maintains all styling and formatting
     - Optimized for both screen and print
  
  2. **PowerPoint Export**
     - Converted from PDF for consistency
     - Maintains professional formatting
     - Compatible with Microsoft PowerPoint
     - Editable for further customization

## Technical Architecture

1. **Frontend Stack**:
   - HTML5 + CSS3
   - reveal.js for presentations
   - Modern responsive design
   - Font Awesome icons
   - Inter font family

2. **Backend Stack**:
   - Flask web framework
   - OpenAI for content generation
   - WeasyPrint for PDF export
   - pdf2pptx for PowerPoint conversion

3. **Content Flow**:
   ```
   User Input → AI Generation → HTML Preview (reveal.js) → Export (PDF/PPT)
   ```

## Dependencies

### Python Dependencies
```
Flask==2.0.1
openai==1.0.0
WeasyPrint==54.3
pdf2pptx==1.0.5
python-dotenv==0.19.0
```

### System Requirements

#### Windows
1. **Python 3.8+**
2. **GTK3 Runtime**
   - Required for WeasyPrint PDF generation
   - Download from: [GTK3 Runtime Environment Installer](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)
   - Install the latest version (gtk3-runtime-x.x.x-x-x.exe)
   - Restart your terminal after installation

#### Linux
```bash
# Ubuntu/Debian
sudo apt-get install python3-pip python3-cffi python3-brotli libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0

# Fedora
sudo dnf install python3-pip python3-cffi python3-brotli pango harfbuzz
```

#### macOS
```bash
brew install python3 cairo pango gdk-pixbuf libffi
```

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/presentation-generator.git
   cd presentation-generator
   ```

2. Install system dependencies:
   - Windows: Install GTK3 Runtime (see System Requirements)
   - Linux/macOS: Run the appropriate commands above

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create and configure .env file:
   ```bash
   # Create .env file with the following content:
   OPENAI_API_KEY=your_openai_api_key_here
   FLASK_ENV=development
   DEBUG=True
   SECRET_KEY=your_secret_key_here
   OUTPUT_DIR=presentations
   CLEANUP_INTERVAL=3600
   ```

5. Run the application:
   ```bash
   python app.py
   ```

## Usage

1. Open your browser and navigate to `http://localhost:5000`
2. Enter your presentation topic
3. Choose a presentation style (Corporate, Modern, Minimal, or Creative)
4. Preview your interactive presentation in the browser
5. Export to PDF or PowerPoint as needed

## Project Structure

```
presentation-generator/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── static/
│   └── css/
│       ├── style.css     # Main application styles
│       └── presentation.css  # Presentation-specific styles
├── templates/
│   ├── index.html        # Main application template
│   └── presentation.html # Presentation template
└── src/
    ├── controllers/      # Application controllers
    ├── services/         # Business logic services
    └── models/           # Data models
```

## Troubleshooting

### Common Issues

1. **WeasyPrint Installation**
   - Error: "Could not import external libraries"
   - Solution: Install GTK3 Runtime and restart your terminal

2. **PDF Export Issues**
   - Error: "libgobject-2.0-0 not found"
   - Solution: Ensure GTK3 is properly installed and system PATH is updated

3. **PowerPoint Export**
   - Error: "Failed to convert PDF"
   - Solution: Check if both WeasyPrint and pdf2pptx are properly installed

### Getting Help
If you encounter any issues:
1. Check the logs in the `logs` directory
2. Ensure all system dependencies are installed
3. Verify your Python environment and dependencies
4. Create an issue in the GitHub repository

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 