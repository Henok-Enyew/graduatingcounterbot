# Implementation Plan: Telegram Graduation Countdown Bot

## Overview

This implementation plan breaks down the telegram-graduation-countdown-bot into discrete coding tasks. The bot is a Python application that sends daily countdown messages to multiple Telegram groups, featuring progress visualization and motivational content. The architecture includes a Flask keep-alive server for Render deployment, AsyncIOScheduler for daily execution, and comprehensive error handling with fault isolation.

Implementation follows a bottom-up approach: core utilities first, then message generation components, followed by distribution logic, and finally orchestration with scheduling and keep-alive server.

## Tasks

- [x] 1. Set up project structure and dependencies
  - Create project root directory structure
  - Create requirements.txt with python-telegram-bot, flask, apscheduler, hypothesis, pytest
  - Create Procfile with "web: python main.py"
  - Create .env.example file documenting required environment variables
  - _Requirements: 10.1, 10.2, 10.3_

- [ ] 2. Implement Configuration Module
  - [x] 2.1 Create config.py with Config class
    - Implement get_bot_token() to read TELEGRAM_BOT_TOKEN from environment
    - Implement get_group_ids() to parse comma-separated GROUP_IDS into list
    - Implement get_port() to read PORT with default 8080
    - Add validation to raise ValueError for missing required variables
    - Add whitespace trimming for group IDs
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 1.1_

  - [ ]* 2.2 Write property test for environment variable reading
    - **Property 14: Environment Variable Reading**
    - **Validates: Requirements 9.1, 9.2, 9.3**

  - [ ]* 2.3 Write property test for missing variable validation
    - **Property 15: Missing Variable Validation**
    - **Validates: Requirements 9.4**

  - [ ]* 2.4 Write property test for GROUP_IDS parsing
    - **Property 1: GROUP_IDS Parsing**
    - **Validates: Requirements 1.1**

  - [ ]* 2.5 Write unit tests for Config class
    - Test valid environment variable reading
    - Test missing TELEGRAM_BOT_TOKEN raises ValueError
    - Test missing GROUP_IDS raises ValueError
    - Test PORT defaults to 8080 when not set
    - Test GROUP_IDS parsing with single and multiple IDs
    - Test GROUP_IDS parsing with whitespace trimming
    - Test invalid PORT value handling
    - _Requirements: 9.1, 9.2, 9.3, 9.4_

- [ ] 3. Implement Countdown Calculator Module
  - [x] 3.1 Create countdown_calculator.py with CountdownCalculator class
    - Define START_DATE constant as date(2021, 10, 1)
    - Define GRADUATION_DATE constant as date(2026, 6, 27)
    - Implement days_remaining() returning max(0, days to graduation)
    - Implement progress_percentage() returning clamped 0-100 percentage
    - Implement is_graduation_day() checking if today equals graduation date
    - Implement is_past_graduation() checking if today is after graduation
    - _Requirements: 2.1, 2.3, 2.4, 3.1_

  - [ ]* 3.2 Write property test for days remaining calculation
    - **Property 4: Days Remaining Calculation**
    - **Validates: Requirements 2.1**

  - [ ]* 3.3 Write property test for progress percentage calculation
    - **Property 5: Progress Percentage Calculation**
    - **Validates: Requirements 3.1**

  - [ ]* 3.4 Write unit tests for CountdownCalculator
    - Test days_remaining on various dates
    - Test days_remaining on graduation day returns 0
    - Test days_remaining after graduation returns 0
    - Test progress_percentage at start date returns 0%
    - Test progress_percentage at graduation date returns 100%
    - Test progress_percentage at midpoint
    - Test is_graduation_day returns True on June 27, 2026
    - Test is_past_graduation returns True after June 27, 2026
    - _Requirements: 2.1, 2.3, 2.4, 3.1_

- [ ] 4. Implement Progress Bar Builder Module
  - [x] 4.1 Create progress_bar_builder.py with ProgressBarBuilder class
    - Define FILLED_BLOCK constant as "🟦"
    - Define EMPTY_BLOCK constant as "⬜"
    - Define TOTAL_BLOCKS constant as 10
    - Implement build(percentage) returning 10-block progress bar string
    - Calculate filled_blocks as round(percentage / 10)
    - Ensure filled_blocks + empty_blocks always equals 10
    - _Requirements: 3.2, 3.3, 3.4, 3.5, 3.6_

  - [ ]* 4.2 Write property test for progress bar structure
    - **Property 6: Progress Bar Structure**
    - **Validates: Requirements 3.2, 3.3**

  - [ ]* 4.3 Write property test for progress bar rounding
    - **Property 7: Progress Bar Rounding**
    - **Validates: Requirements 3.6**

  - [ ]* 4.4 Write unit tests for ProgressBarBuilder
    - Test 0% progress returns 10 empty blocks
    - Test 100% progress returns 10 filled blocks
    - Test 50% progress returns 5 filled, 5 empty blocks
    - Test rounding behavior (14% -> 1 block, 15% -> 2 blocks)
    - Test progress bar always has exactly 10 blocks
    - Test progress bar only contains valid emoji (🟦 and ⬜)
    - _Requirements: 3.2, 3.3, 3.4, 3.5, 3.6_

- [ ] 5. Implement Motivational Message Selector Module
  - [x] 5.1 Create motivational_message_selector.py with MotivationalMessageSelector class
    - Define collection of software engineering-themed motivational quotes
    - Implement get_message() returning a motivational message
    - Use date-based or rotation-based selection for variation
    - _Requirements: 4.1, 4.2, 4.3_

  - [ ]* 5.2 Write property test for message variation
    - **Property 8: Message Variation**
    - **Validates: Requirements 4.3**

  - [ ]* 5.3 Write unit tests for MotivationalMessageSelector
    - Test get_message() returns non-empty string
    - Test messages are appropriate for software engineering context
    - Test variation across multiple calls
    - _Requirements: 4.1, 4.2, 4.3_

- [ ] 6. Implement Message Formatter Module
  - [x] 6.1 Create message_formatter.py with MessageFormatter class
    - Implement format_countdown_message() accepting days, progress bar, motivational message
    - Add parameters for is_graduation_day and is_past_graduation flags
    - Structure message with emoji headers, days remaining, progress bar, motivational message
    - Apply MarkdownV2 or HTML formatting
    - Handle special character escaping for chosen format
    - Handle graduation day and post-graduation special messages
    - _Requirements: 5.1, 5.2, 5.3, 2.2, 4.1_

  - [ ]* 6.2 Write property test for valid format mode
    - **Property 9: Valid Format Mode**
    - **Validates: Requirements 5.1**

  - [ ]* 6.3 Write property test for message completeness
    - **Property 10: Message Completeness**
    - **Validates: Requirements 5.2, 2.2, 4.1**

  - [ ]* 6.4 Write unit tests for MessageFormatter
    - Test message includes all required components
    - Test message format is valid (MarkdownV2 or HTML)
    - Test special character escaping
    - Test graduation day message format
    - Test post-graduation message format
    - _Requirements: 5.1, 5.2, 5.3_

- [x] 7. Checkpoint - Ensure all core utility tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 8. Implement Message Distributor Module
  - [ ] 8.1 Create message_distributor.py with MessageDistributor class
    - Implement __init__(bot_token, group_ids) to initialize Telegram bot instance
    - Implement async distribute_message(message) to send to all groups
    - Iterate through all group IDs independently
    - Log success with group ID and timestamp for each delivery
    - Log failure with group ID, error details, and timestamp
    - Ensure failure in one group doesn't prevent delivery to others
    - Return dict mapping group_id to success status
    - Add timeout handling to complete within 60 seconds
    - _Requirements: 1.2, 1.3, 1.4, 8.1, 8.3_

  - [ ]* 8.2 Write property test for multi-group distribution
    - **Property 2: Multi-Group Distribution**
    - **Validates: Requirements 1.2**

  - [ ]* 8.3 Write property test for fault tolerance
    - **Property 3: Fault Tolerance**
    - **Validates: Requirements 1.3, 8.2, 8.4**

  - [ ]* 8.4 Write property test for delivery logging
    - **Property 13: Delivery Logging**
    - **Validates: Requirements 8.1, 8.3**

  - [ ]* 8.5 Write unit tests for MessageDistributor
    - Test message sent to all groups in list
    - Test error in one group doesn't affect others (use mock)
    - Test logging on success includes group ID and timestamp
    - Test logging on failure includes group ID, error, and timestamp
    - Test empty group list handling
    - Test timeout behavior
    - _Requirements: 1.2, 1.3, 1.4, 8.1, 8.3_

- [ ] 9. Implement Keep-Alive Server Module
  - [ ] 9.1 Create keep_alive_server.py with KeepAliveServer class
    - Implement __init__(port) to initialize Flask app
    - Define health_check() route handler for GET / returning ("Bot is active", 200)
    - Implement start() to run Flask server in daemon background thread
    - Configure server to listen on specified port
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

  - [ ]* 9.2 Write property test for server port configuration
    - **Property 11: Server Port Configuration**
    - **Validates: Requirements 7.2**

  - [ ]* 9.3 Write property test for health check response
    - **Property 12: Health Check Response**
    - **Validates: Requirements 7.4**

  - [ ]* 9.4 Write unit tests for KeepAliveServer
    - Test server starts on configured port
    - Test GET / returns "Bot is active" with status 200
    - Test server runs in background thread (doesn't block)
    - Test server responds to multiple requests
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [ ] 10. Implement Scheduler Module
  - [ ] 10.1 Create scheduler.py with DailyScheduler class
    - Implement __init__(job_function) to initialize AsyncIOScheduler
    - Implement start() to configure daily job at 00:01 AM and start scheduler
    - Implement async execute_daily_job() orchestrating message generation and distribution
    - Use system timezone for scheduling
    - Add error handling and logging for job execution failures
    - Ensure scheduler continues after job errors
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 8.4_

  - [ ]* 10.2 Write unit tests for DailyScheduler
    - Test scheduler initializes with correct time (00:01 AM)
    - Test scheduler uses system timezone
    - Test job function is called on schedule trigger (use mock time)
    - Test scheduler continues after job execution error
    - _Requirements: 6.1, 6.2, 6.3, 6.4_

- [ ] 11. Checkpoint - Ensure all component tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 12. Implement main entry point and orchestration
  - [ ] 12.1 Create main.py with bot initialization and startup
    - Import all modules (config, scheduler, keep_alive_server, message_distributor, etc.)
    - Load configuration using Config class with error handling
    - Initialize KeepAliveServer and start in background thread
    - Initialize MessageDistributor with bot token and group IDs
    - Create job function that orchestrates countdown calculation, progress bar, message formatting, and distribution
    - Initialize DailyScheduler with job function
    - Start scheduler
    - Add main loop to keep process alive
    - Add comprehensive error logging for startup failures
    - _Requirements: 6.4, 7.5, 9.4_

  - [ ]* 12.2 Write integration tests for main entry point
    - Test bot startup with valid configuration
    - Test bot startup fails with missing TELEGRAM_BOT_TOKEN
    - Test bot startup fails with missing GROUP_IDS
    - Test keep-alive server starts before main bot logic
    - Test scheduler initializes correctly
    - _Requirements: 6.4, 7.5, 9.4_

- [ ] 13. Implement end-to-end message flow integration
  - [ ] 13.1 Create integration test for complete message flow
    - Mock Telegram API to capture sent messages
    - Trigger scheduler job execution
    - Verify countdown calculation produces correct values
    - Verify progress bar generation produces correct format
    - Verify message formatting includes all components
    - Verify message distribution attempts delivery to all groups
    - Verify error isolation (one group failure doesn't affect others)
    - _Requirements: 1.2, 1.3, 2.1, 3.1, 4.1, 5.2_

  - [ ]* 13.2 Write integration test for error scenarios
    - Test message distribution continues after single group failure
    - Test scheduler continues after job execution error
    - Test logging captures all error details
    - _Requirements: 1.3, 8.1, 8.2, 8.4_

- [ ] 14. Add logging configuration
  - [ ] 14.1 Create logging_config.py with logging setup
    - Configure logging format with timestamp, level, component, message
    - Set up console and file handlers
    - Configure log levels (INFO for normal operation, ERROR for failures)
    - Use ISO 8601 timestamp format
    - _Requirements: 8.1, 8.2, 8.3, 8.4_

  - [ ] 14.2 Integrate logging into all modules
    - Add logging to Config for validation errors
    - Add logging to MessageDistributor for delivery success/failure
    - Add logging to DailyScheduler for job execution
    - Add logging to main.py for startup and shutdown
    - _Requirements: 8.1, 8.2, 8.3, 8.4_

- [ ] 15. Final checkpoint - Run full test suite and verify deployment files
  - Run pytest with coverage report
  - Verify requirements.txt exists and contains all dependencies
  - Verify Procfile exists with correct command
  - Verify .env.example documents all required variables
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Property tests use Hypothesis library with minimum 100 iterations
- Unit tests cover specific examples and edge cases
- Integration tests verify end-to-end flows
- Checkpoints ensure incremental validation
- All modules include comprehensive error handling and logging
- The bot is designed for Render platform deployment with keep-alive server
