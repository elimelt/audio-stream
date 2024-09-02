# Audio Streaming Server

A real-time audio streaming server with support for multiple channels, and a built-in client

## Setup

1. Clone the repository:
   ```
   git clone git@github.com:elimelt/audio-streaming-server.git
   cd audio-streaming-server
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create SSL certs for HTTPS support (required if not running behind reverse proxy/on localhost):
   ```
   openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
   ```

## Running the Server

To start the server, run:
```
python run.py
```

The server will start on `http://0.0.0.0:8080`.

## Usage

1. Open a web browser and navigate to `http://0.0.0.0:8080/channel/{channel_id}/index.html`, replacing `{channel_id}` with any string to create a channel.

2. Use the buttons on the page to start/stop producing (sending) audio or consuming (receiving) audio.

3. Multiple clients can connect to the same channel to produce or consume audio.

## License

[MIT License](https://opensource.org/licenses/MIT)