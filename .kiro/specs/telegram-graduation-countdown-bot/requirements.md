# Requirements Document

## Introduction

A Python-based Telegram bot that sends daily countdown messages to multiple class group chats, tracking progress toward a graduation date (June 27, 2026) from a start date (October 1, 2021). The bot displays days remaining, a visual progress bar, and motivational messages. It includes a Flask server for deployment on Render's platform to maintain uptime.

## Glossary

- **Bot**: The Telegram bot application that sends scheduled messages
- **Countdown_Message**: A formatted message containing days remaining, progress bar, and motivational text
- **Progress_Bar**: A visual representation using emoji blocks showing elapsed time percentage
- **Group_ID**: A unique Telegram chat identifier for a group conversation
- **Scheduler**: The APScheduler component that triggers daily message sending
- **Keep_Alive_Server**: A Flask HTTP server running in a background thread for Render platform compatibility
- **Graduation_Date**: June 27, 2026 - the target date for countdown
- **Start_Date**: October 1, 2021 - the beginning date for progress calculation

## Requirements

### Requirement 1: Multi-Group Message Distribution

**User Story:** As a class administrator, I want the bot to send messages to multiple Telegram groups simultaneously, so that all class sections receive the same daily update.

#### Acceptance Criteria

1. THE Bot SHALL read group identifiers from the GROUP_IDS environment variable as a comma-separated list
2. WHEN the scheduled time arrives, THE Bot SHALL iterate through all group identifiers and send the Countdown_Message to each
3. IF sending to one Group_ID fails, THEN THE Bot SHALL log the error and continue sending to remaining groups
4. THE Bot SHALL complete message distribution to all groups within 60 seconds

### Requirement 2: Countdown Calculation

**User Story:** As a student, I want to see how many days remain until graduation, so that I can track my progress through the program.

#### Acceptance Criteria

1. THE Bot SHALL calculate days remaining from the current date to Graduation_Date (June 27, 2026)
2. THE Bot SHALL include the days remaining count in the Countdown_Message
3. WHEN the current date equals Graduation_Date, THE Bot SHALL display zero days remaining
4. WHEN the current date is after Graduation_Date, THE Bot SHALL display a completion message instead of negative days

### Requirement 3: Progress Bar Visualization

**User Story:** As a student, I want to see a visual progress bar showing how far we've come, so that I can visualize our journey through the program.

#### Acceptance Criteria

1. THE Bot SHALL calculate the percentage of time elapsed from Start_Date (October 1, 2021) to Graduation_Date (June 27, 2026)
2. THE Progress_Bar SHALL consist of exactly 10 blocks
3. THE Bot SHALL represent completed progress using 🟦 emoji and remaining progress using ⬜ emoji
4. WHEN 0% time has elapsed, THE Progress_Bar SHALL display 10 ⬜ blocks
5. WHEN 100% time has elapsed, THE Progress_Bar SHALL display 10 🟦 blocks
6. THE Bot SHALL round the percentage to the nearest 10% for block calculation

### Requirement 4: Motivational Message Generation

**User Story:** As a student, I want to receive daily motivational messages relevant to software engineering, so that I stay inspired throughout my studies.

#### Acceptance Criteria

1. THE Bot SHALL include a motivational message in each Countdown_Message
2. THE Bot SHALL select motivational messages appropriate for a Software Engineering class context
3. THE Bot SHALL vary the motivational messages across different days

### Requirement 5: Message Formatting

**User Story:** As a student, I want the countdown message to be cleanly formatted and easy to read, so that I can quickly understand the information.

#### Acceptance Criteria

1. THE Bot SHALL format the Countdown_Message using either MarkdownV2 or HTML formatting
2. THE Countdown_Message SHALL include days remaining, the Progress_Bar, and a motivational message
3. THE Bot SHALL structure the message with clear visual separation between components

### Requirement 6: Daily Scheduling

**User Story:** As a class administrator, I want the bot to automatically send messages at a consistent time each day, so that students receive updates without manual intervention.

#### Acceptance Criteria

1. THE Scheduler SHALL use AsyncIOScheduler for task scheduling
2. THE Bot SHALL trigger message sending at 00:01 AM daily
3. THE Scheduler SHALL use the system timezone for scheduling
4. WHEN the Bot starts, THE Scheduler SHALL initialize and begin monitoring for the scheduled time

### Requirement 7: Keep-Alive Server for Render Platform

**User Story:** As a system administrator, I want the bot to remain active on Render's free tier, so that the service continues running without manual restarts.

#### Acceptance Criteria

1. THE Keep_Alive_Server SHALL run a Flask HTTP server in a background thread
2. THE Keep_Alive_Server SHALL listen on the port specified by the PORT environment variable
3. WHERE the PORT environment variable is not set, THE Keep_Alive_Server SHALL default to port 8080
4. WHEN a GET request is made to the root path (/), THE Keep_Alive_Server SHALL return the text "Bot is active" with HTTP status 200
5. THE Keep_Alive_Server SHALL start before the Bot begins its main operation

### Requirement 8: Error Handling and Logging

**User Story:** As a system administrator, I want detailed error logs when message delivery fails, so that I can diagnose and fix issues.

#### Acceptance Criteria

1. WHEN sending to a Group_ID fails, THE Bot SHALL log the Group_ID and error details
2. WHEN an exception occurs during message formatting, THE Bot SHALL log the exception and continue operation
3. THE Bot SHALL log successful message deliveries with timestamps and Group_IDs
4. WHEN the Scheduler encounters an error, THE Bot SHALL log the error and attempt to continue scheduling

### Requirement 9: Configuration Management

**User Story:** As a system administrator, I want to configure the bot through environment variables, so that I can deploy it without modifying code.

#### Acceptance Criteria

1. THE Bot SHALL read the Telegram bot token from a TELEGRAM_BOT_TOKEN environment variable
2. THE Bot SHALL read group identifiers from the GROUP_IDS environment variable
3. THE Bot SHALL read the server port from the PORT environment variable
4. WHEN a required environment variable is missing, THE Bot SHALL log an error and fail to start

### Requirement 10: Deployment Configuration

**User Story:** As a system administrator, I want deployment files for Render platform, so that I can easily deploy and run the bot.

#### Acceptance Criteria

1. THE Bot SHALL provide a requirements.txt file listing python-telegram-bot, flask, and apscheduler dependencies
2. THE Bot SHALL provide a Procfile with the command "web: python main.py"
3. THE requirements.txt SHALL specify compatible versions of all dependencies
