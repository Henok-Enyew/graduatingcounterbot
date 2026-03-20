# Telegram Graduation Countdown Bot 🎓

A Python-based Telegram bot that sends daily countdown messages with photos to multiple class group chats, tracking progress toward graduation (June 27, 2026) from a start date (October 1, 2021).

## ✨ Key Features

### 📸 Photo + Caption Messages
- **Every message** (daily automated posts AND /start command) is sent as a photo with caption
- Random image selection from the `/images` folder
- Automatic fallback to text-only if images fail to load
- Supports HTML formatting for bold text and styling

### 🥷 /start Command (Direct Message)
When a user starts the bot, they receive:
- Personalized greeting: "Hey Graduating Ninja! 🥷"
- Days remaining until graduation
- Visual progress bar (🟦⬜)
- Motivational message
- All sent as a photo with caption

### 📅 Daily Automated Group Messages
- Scheduled to send at 00:01 AM daily
- Countdown of days remaining
- Visual progress bar (10 blocks)
- Daily motivational message for Software Engineering students
- Sent to multiple groups simultaneously
- Photo with caption format

### 🔧 Technical Features
- **Multi-Group Support**: Send to multiple Telegram groups
- **Error Isolation**: Failure in one group doesn't affect others
- **Keep-Alive Server**: Flask server for Render platform deployment
- **Robust Scheduling**: AsyncIOScheduler for reliable daily execution
- **Comprehensive Logging**: Detailed logs for debugging
- **Fallback Support**: Gracefully handles missing images

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)
- Telegram Group Chat IDs

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export TELEGRAM_BOT_TOKEN="your_bot_token"
export GROUP_IDS="-1001234567890,-1009876543210"

# Run the bot
python main.py
```

## 📋 Configuration

### Environment Variables

Create a `.env` file or set these variables:

```bash
# Required: Bot token from @BotFather
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# Required: Comma-separated group IDs
GROUP_IDS=-1001234567890,-1009876543210

# Optional: Port for keep-alive server (default: 8080)
PORT=8080
```

### Getting Group IDs

1. Add your bot to target groups
2. Send a message in the group
3. Visit: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
4. Find `"chat":{"id":-1001234567890}` in response

### Adding Images

Place images in the `/images` folder:
- Supported: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
- Images are randomly selected for each message
- Bot falls back to text if no images available

## 🌐 Deployment on Render

### Step 1: Create Web Service
- Connect your GitHub repository
- Select "Python" environment

### Step 2: Configuration
Render uses the `Procfile` automatically:
```
web: python main.py
```

### Step 3: Environment Variables
Add in Render dashboard:
- `TELEGRAM_BOT_TOKEN`
- `GROUP_IDS`
- `PORT` (auto-set by Render)

### Step 4: Deploy
- Dependencies install from `requirements.txt`
- Keep-alive server prevents sleeping
- Daily messages at 00:01 AM server time

## 📁 Project Structure

```
.
├── main.py                          # Main entry point with /start handler
├── config.py                        # Environment variable management
├── countdown_calculator.py          # Date calculations
├── progress_bar_builder.py          # Progress bar generation
├── motivational_message_selector.py # Motivational quotes
├── message_formatter.py             # Message formatting (HTML)
├── message_distributor.py           # Multi-group sending with photos
├── image_selector.py                # Random image selection
├── scheduler.py                     # Daily scheduling (APScheduler)
├── keep_alive_server.py             # Flask keep-alive server
├── logging_config.py                # Logging configuration
├── requirements.txt                 # Dependencies
├── Procfile                         # Render config
├── .env.example                     # Environment template
└── images/                          # Image folder
```

## 🏗️ Architecture

### Component Flow

```
┌─────────────────────────────────────────────────────────────┐
│                         main.py                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Keep-Alive   │  │  Scheduler   │  │ /start       │     │
│  │ Server       │  │  (00:01 AM)  │  │ Handler      │     │
│  │ (Flask)      │  │              │  │              │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                  │                  │              │
│    Background         Daily Job          User Command       │
│    Thread             Trigger            Response           │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
          │                  ▼                  ▼
          │         ┌────────────────────────────────┐
          │         │   Message Generation           │
          │         │  • CountdownCalculator         │
          │         │  • ProgressBarBuilder          │
          │         │  • MotivationalMessageSelector │
          │         │  • MessageFormatter            │
          │         │  • ImageSelector               │
          │         └────────────┬───────────────────┘
          │                      │
          │                      ▼
          │         ┌────────────────────────────────┐
          │         │   MessageDistributor           │
          │         │  • send_photo with caption     │
          │         │  • Fallback to text            │
          │         │  • Error isolation per group   │
          │         └────────────────────────────────┘
          │
          ▼
    ┌─────────────┐
    │   Render    │
    │  Platform   │
    │ Health Check│
    └─────────────┘
```

### Key Components

1. **Keep-Alive Server** (Flask)
   - Runs in daemon thread
   - Responds to GET / with "Bot is active"
   - Prevents Render hibernation

2. **Telegram Bot** (python-telegram-bot)
   - Handles /start command
   - Sends photos with captions
   - HTML formatting support

3. **Scheduler** (APScheduler)
   - Daily trigger at 00:01 AM
   - Async execution
   - Error recovery

4. **Message Distributor**
   - Photo + caption sending
   - Text fallback
   - Per-group error isolation

5. **Image Selector**
   - Random selection from `/images`
   - File validation
   - Graceful None return

## 💬 Message Examples

### Daily Group Message
```
🎓 Graduation Countdown 🎓

📅 Days Remaining: 99 days

Progress:
🟦🟦🟦🟦🟦🟦🟦🟦🟦⬜

💡 Code is like humor. When you have to explain it, it's bad. – Cory House
```
*Sent as photo with caption*

### /start Command Response
```
Hey Graduating Ninja! 🥷

How are you doing? You have 99 days left until graduation!

Progress:
🟦🟦🟦🟦🟦🟦🟦🟦🟦⬜

💡 First, solve the problem. Then, write the code. – John Johnson
```
*Sent as photo with caption*

## 📊 Logging

### Log Destinations
- **Console**: INFO level and above
- **bot.log**: DEBUG level and above

### Log Format
```
2024-03-20T00:01:23 [INFO] main: Starting daily countdown message generation
2024-03-20T00:01:24 [INFO] image_selector: Selected image: 11.jpeg
2024-03-20T00:01:25 [INFO] message_distributor: Successfully sent photo message to group -1001234567890
```

## 🛠️ Error Handling

### Image Loading Failures
- **Cause**: File not found or unreadable
- **Action**: Falls back to text-only message
- **Log**: Warning logged, operation continues

### Group Delivery Failures
- **Cause**: Bot kicked or network error
- **Action**: Logs error, continues to next group
- **Log**: Error with group ID and details

### Scheduler Errors
- **Cause**: Job execution failure
- **Action**: Logs error, continues for next day
- **Log**: Full stack trace

## 🔍 Troubleshooting

### Bot Not Sending Messages
1. ✅ Check `TELEGRAM_BOT_TOKEN` is correct
2. ✅ Verify bot added to groups
3. ✅ Check `GROUP_IDS` format (comma-separated)
4. ✅ Review `bot.log` for errors

### Images Not Appearing
1. ✅ Verify images in `/images` folder
2. ✅ Check file extensions
3. ✅ Ensure files readable
4. ✅ Bot falls back to text automatically

### Keep-Alive Not Responding
1. ✅ Check `PORT` environment variable
2. ✅ Verify port not in use
3. ✅ Check Render logs

## 🧪 Testing

### Manual Testing
```bash
# Test modules
python verify_modules.py

# Test integration
python integration_demo.py

# Test /start command
# Send /start to your bot in Telegram
```

## 📝 License

Educational purposes.

## 🤝 Support

Check logs in `bot.log` for detailed error information.
