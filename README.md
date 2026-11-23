# SenseHAT Battleship

A Flask web app for the Raspberry Pi Sense HAT. It includes a Battleship-style game played on the Sense HAT’s 8×8 LED matrix, plus a page for viewing sensor readings.

This project was developed as the final project for the *Internet of Things (IoT) in Action: with Raspberry Pi and Python* course offered by Mathesis.

## Features

- Battleship and bonus game modes
- LED-grid interaction through a web browser
- Sense HAT temperature, humidity, and pressure readings

## Run

Install Flask and the Sense HAT emulator, then start the app:

```bash
pip install Flask sense-emu
python3 myapp.py
```

Open `http://localhost:5000` in your browser.
