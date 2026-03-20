#!/usr/bin/env python3
"""Quick verification script for core modules."""

import sys

results = []

# Test 1: Import all modules
try:
    from config import Config
    from countdown_calculator import CountdownCalculator
    from progress_bar_builder import ProgressBarBuilder
    from motivational_message_selector import MotivationalMessageSelector
    from message_formatter import MessageFormatter
    results.append("PASS: All modules imported successfully")
except Exception as e:
    results.append(f"FAIL: Import error - {e}")
    sys.exit(1)

# Test 2: CountdownCalculator basic functionality
try:
    days = CountdownCalculator.days_remaining()
    progress = CountdownCalculator.progress_percentage()
    assert isinstance(days, int) and days >= 0
    assert isinstance(progress, float) and 0 <= progress <= 100
    results.append(f"PASS: CountdownCalculator (days={days}, progress={progress:.1f}%)")
except Exception as e:
    results.append(f"FAIL: CountdownCalculator - {e}")

# Test 3: ProgressBarBuilder
try:
    bar = ProgressBarBuilder.build(50)
    assert isinstance(bar, str) and len(bar) > 0
    results.append(f"PASS: ProgressBarBuilder")
except Exception as e:
    results.append(f"FAIL: ProgressBarBuilder - {e}")

# Test 4: MotivationalMessageSelector
try:
    msg = MotivationalMessageSelector.get_message()
    assert isinstance(msg, str) and len(msg) > 0
    results.append(f"PASS: MotivationalMessageSelector")
except Exception as e:
    results.append(f"FAIL: MotivationalMessageSelector - {e}")

# Test 5: MessageFormatter
try:
    formatted = MessageFormatter.format_countdown_message(
        days_remaining=100,
        progress_bar="🟦🟦🟦⬜⬜⬜⬜⬜⬜⬜",
        motivational_message="Test",
        is_graduation_day=False,
        is_past_graduation=False
    )
    assert isinstance(formatted, str) and "100" in formatted
    results.append(f"PASS: MessageFormatter")
except Exception as e:
    results.append(f"FAIL: MessageFormatter - {e}")

# Test 6: Config structure
try:
    assert hasattr(Config, 'get_bot_token')
    assert hasattr(Config, 'get_group_ids')
    assert hasattr(Config, 'get_port')
    results.append(f"PASS: Config structure")
except Exception as e:
    results.append(f"FAIL: Config - {e}")

# Write results
with open('test_results.txt', 'w') as f:
    for result in results:
        f.write(result + '\n')
        print(result)

# Check if all passed
if all('PASS' in r for r in results):
    print("\nALL TESTS PASSED!")
    sys.exit(0)
else:
    print("\nSOME TESTS FAILED!")
    sys.exit(1)
