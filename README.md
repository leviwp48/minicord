# twilio video test

## Description
Flask app that has user registration and login and the data is stored in SQLite. 

It uses the Twilio API on the frontend with JavaScript to create and join a video room. As of now, you can register an account, login, and create and join a video room where the video is your devices camera. 

Another user can join by creating another tab or by using something like `ngrok` to create a forwarding address for the localhost, where you can pass it to another device 

todo: add video 

## Setup

1. Clone the repo onto your device
2. Create a Twilio account and an api key
3. Add the account SID, api key, and secret key to the docker compose file under `environment` to use them as environment variables
4. Install SQLite if necessary 
5. Go to the twilio-video-test directory and run `docker compose up` (be sure the Docker Daemon is running)



