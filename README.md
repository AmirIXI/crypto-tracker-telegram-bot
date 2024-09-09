# Crypto Tracker

Crypto Tracker is a Telegram bot that provides real-time cryptocurrency prices and market information. Stay updated with the latest trends in the crypto world!

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)

## Features

- Real-time cryptocurrency price updates
- Support for multiple popular cryptocurrencies (BTC, ETH, BNB, DOGE, TRX, MATIC, SOL, FTM, OP, SHIB)
- User-friendly interface with button commands
- Group chat support
- User registration system

## Getting Started

### Prerequisites

- Python 3.7+
- A Telegram Bot Token (obtainable from [@BotFather](https://t.me/BotFather))
- A Telegram channel or group for user subscription

### Installation

1. Clone the repository: 
git clone https://github.com/AmirIXI/crypto-tracker-telegram-bot

2. Install the required packages:
pip install -r requirements.txt


3. Create a `.env` file in the root directory and add your Telegram Bot Token and Chat ID:
BOT_TOKEN=your_bot_token_here
CHAT_ID=@your_channel_or_group_username

4. Run the bot :)

## ----------------------------------------------------

## Usage

Start the bot by sending `/start` in a private chat with the bot. Use the keyboard buttons or type commands to get cryptocurrency prices.

## Commands

- `/start` - Initializes the bot and displays the main menu
- `/price` - Shows prices for popular cryptocurrencies
- `/BTC`, `/ETH`, `/BNB`, etc. - Get price for a specific cryptocurrency
- `/help` - Displays help information
- `/gpPrice` - Provides instructions for adding the bot to a group

## Roadmap

- [ ] Add support for more cryptocurrencies
- [ ] Implement price alerts
- [ ] Create a web dashboard for analytics
- [ ] Add multi-language support


## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Amir - Telegram : [@scream_hash](https://t.me/scream_hash) - amirixi666@gmail.com

Project Link: https://github.com/AmirIXI/crypto-tracker-telegram-bot

## Acknowledgments

- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- [Binance API](https://binance-docs.github.io/apidocs/)
- [Python-dotenv](https://github.com/theskumar/python-dotenv)
