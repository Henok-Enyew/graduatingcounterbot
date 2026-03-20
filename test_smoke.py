"""Smoke tests for core utility modules.

This script performs basic smoke tests to verify that all core utility
modules can be imported and their basic functionality works correctly.
"""

import sys
from datetime import date

# Test imports
print("Testing imports...")
try:
    from config import Config
    from countdown_calculator import CountdownCalculator
    from progress_bar_builder import ProgressBarBuilder
    from motivational_message_selector import MotivationalMessageSelector
    from message_formatter import MessageFormatter
    print("✓ All imports successful")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

# Test CountdownCalculator
print("\nTesting CountdownCalculator...")
try:
    days = CountdownCalculator.days_remaining()
    assert isinstance(days, int), "days_remaining should return int"
    assert days >= 0, "days_remaining should be non-negative"
    
    progress = CountdownCalculator.progress_percentage()
    assert isinstance(progress, float), "progress_percentage should return float"
    assert 0 <= progress <= 100, "progress_percentage should be between 0 and 100"
    
    is_grad = CountdownCalculator.is_graduation_day()
    assert isinstance(is_grad, bool), "is_graduation_day should return bool"
    
    is_past = CountdownCalculator.is_past_graduation()
    assert isinstance(is_past, bool), "is_past_graduation should return bool"
    
    print(f"✓ CountdownCalculator working (days: {days}, progress: {progress:.2f}%)")
except Exception as e:
    print(f"✗ CountdownCalculator failed: {e}")
    sys.exit(1)

# Test ProgressBarBuilder
print("\nTesting ProgressBarBuilder...")
try:
    bar_0 = ProgressBarBuilder.build(0)
    assert len(bar_0) == 10 * len(ProgressBarBuilder.EMPTY_BLOCK), "Progress bar should have 10 blocks"
    assert bar_0 == ProgressBarBuilder.EMPTY_BLOCK * 10, "0% should be all empty blocks"
    
    bar_50 = ProgressBarBuilder.build(50)
    assert len(bar_50) == 10 * len(ProgressBarBuilder.FILLED_BLOCK), "Progress bar should have 10 blocks"
    
    bar_100 = ProgressBarBuilder.build(100)
    assert bar_100 == ProgressBarBuilder.FILLED_BLOCK * 10, "100% should be all filled blocks"
    
    print(f"✓ ProgressBarBuilder working")
    print(f"  0%:   {bar_0}")
    print(f"  50%:  {bar_50}")
    print(f"  100%: {bar_100}")
except Exception as e:
    print(f"✗ ProgressBarBuilder failed: {e}")
    sys.exit(1)

# Test MotivationalMessageSelector
print("\nTesting MotivationalMessageSelector...")
try:
    message = MotivationalMessageSelector.get_message()
    assert isinstance(message, str), "get_message should return string"
    assert len(message) > 0, "Message should not be empty"
    assert message in MotivationalMessageSelector.MESSAGES, "Message should be from collection"
    
    print(f"✓ MotivationalMessageSelector working")
    print(f"  Today's message: {message[:60]}...")
except Exception as e:
    print(f"✗ MotivationalMessageSelector failed: {e}")
    sys.exit(1)

# Test MessageFormatter
print("\nTesting MessageFormatter...")
try:
    formatted = MessageFormatter.format_countdown_message(
        days_remaining=100,
        progress_bar="🟦🟦🟦⬜⬜⬜⬜⬜⬜⬜",
        motivational_message="Test message",
        is_graduation_day=False,
        is_past_graduation=False
    )
    assert isinstance(formatted, str), "format_countdown_message should return string"
    assert "100" in formatted, "Message should contain days remaining"
    assert "🟦" in formatted, "Message should contain progress bar"
    assert "Test message" in formatted, "Message should contain motivational message"
    assert "<b>" in formatted, "Message should contain HTML formatting"
    
    # Test graduation day message
    grad_msg = MessageFormatter.format_countdown_message(
        days_remaining=0,
        progress_bar="🟦" * 10,
        motivational_message="Congrats!",
        is_graduation_day=True,
        is_past_graduation=False
    )
    assert "Graduation Day" in grad_msg, "Should have graduation day message"
    
    print(f"✓ MessageFormatter working")
    print(f"  Sample output:\n{formatted[:100]}...")
except Exception as e:
    print(f"✗ MessageFormatter failed: {e}")
    sys.exit(1)

# Test Config (without actually setting env vars)
print("\nTesting Config...")
try:
    # Test that Config class exists and has required methods
    assert hasattr(Config, 'get_bot_token'), "Config should have get_bot_token method"
    assert hasattr(Config, 'get_group_ids'), "Config should have get_group_ids method"
    assert hasattr(Config, 'get_port'), "Config should have get_port method"
    
    # Test get_port with default (should work without env var)
    import os
    if 'PORT' not in os.environ:
        port = Config.get_port()
        assert port == 8080, "Default port should be 8080"
    
    print(f"✓ Config class structure verified")
except Exception as e:
    print(f"✗ Config failed: {e}")
    sys.exit(1)

# Integration test: Generate a complete message
print("\nIntegration test: Generating complete message...")
try:
    days = CountdownCalculator.days_remaining()
    progress_pct = CountdownCalculator.progress_percentage()
    progress_bar = ProgressBarBuilder.build(progress_pct)
    motivational = MotivationalMessageSelector.get_message()
    is_grad = CountdownCalculator.is_graduation_day()
    is_past = CountdownCalculator.is_past_graduation()
    
    complete_message = MessageFormatter.format_countdown_message(
        days_remaining=days,
        progress_bar=progress_bar,
        motivational_message=motivational,
        is_graduation_day=is_grad,
        is_past_graduation=is_past
    )
    
    print(f"✓ Integration test successful")
    print(f"\nComplete message preview:")
    print("=" * 60)
    print(complete_message)
    print("=" * 60)
except Exception as e:
    print(f"✗ Integration test failed: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ ALL SMOKE TESTS PASSED!")
print("=" * 60)
print("\nAll core utility modules are working correctly:")
print("  • Config - Configuration management")
print("  • CountdownCalculator - Date calculations")
print("  • ProgressBarBuilder - Visual progress bars")
print("  • MotivationalMessageSelector - Message selection")
print("  • MessageFormatter - Message formatting")
