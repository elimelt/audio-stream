# Audio Streaming Project

This project implements a real-time audio streaming server with support for multiple channels.

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/audio_streaming_project.git
   cd audio_streaming_project
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Server

To start the server, run:
```
python run.py
```

The server will start on `http://localhost:8080`.

## Usage

1. Open a web browser and navigate to `http://localhost:8080/channel/{channel_id}/index.html`, replacing `{channel_id}` with any string to create or join a channel.

2. Use the buttons on the page to start/stop producing (sending) audio or consuming (receiving) audio.

3. Multiple clients can connect to the same channel to produce or consume audio.

## Project Structure

- `run.py`: Entry point for running the server
- `audio_streaming/`: Main package containing the application code
  - `main.py`: Application factory and configuration
  - `routes.py`: URL routes definition
  - `handlers.py`: Request handlers
  - `config.py`: Configuration settings
  - `static/`: Static files (CSS, JavaScript)
- `templates/`: HTML templates
- `requirements.txt`: Required Python packages

## License

[MIT License](https://opensource.org/licenses/MIT)