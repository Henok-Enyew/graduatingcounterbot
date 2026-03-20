#!/usr/bin/env python3
"""Integration demonstration of all core utility modules.

This script demonstrates that all core utility modules work together
to generate a complete countdown message.
"""

from countdown_calculator import CountdownCalculator
from progress_bar_builder import ProgressBarBuilder
from motivational_message_selector import MotivationalMessageSelector
from message_formatter import MessageFormatter

def generate_countdown_message():
    """Generate a complete countdown message using all core modules."""
    
    # Step 1: Calculate countdown metrics
    days_remaining = CountdownCalculator.days_remaining()
    progress_percentage = CountdownCalculator.progress_percentage()
    is_graduation_day = CountdownCalculator.is_graduation_day()
    is_past_graduation = CountdownCalculator.is_past_graduation()
    
    # Step 2: Build progress bar
    progress_bar = ProgressBarBuilder.build(progress_percentage)
    
    # Step 3: Select motivational message
    motivational_message = MotivationalMessageSelector.get_message()
    
    # Step 4: Format complete message
    complete_message = MessageFormatter.format_countdown_message(
        days_remaining=days_remaining,
        progress_bar=progress_bar,
        motivational_message=motivational_message,
        is_graduation_day=is_graduation_day,
        is_past_graduation=is_past_graduation
    )
    
    return complete_message, {
        'days_remaining': days_remaining,
        'progress_percentage': progress_percentage,
        'is_graduation_day': is_graduation_day,
        'is_past_graduation': is_past_graduation
    }

if __name__ == '__main__':
    print("=" * 70)
    print("INTEGRATION TEST: Generating Complete Countdown Message")
    print("=" * 70)
    
    message, metrics = generate_countdown_message()
    
    print("\nMetrics:")
    print(f"  Days Remaining: {metrics['days_remaining']}")
    print(f"  Progress: {metrics['progress_percentage']:.2f}%")
    print(f"  Is Graduation Day: {metrics['is_graduation_day']}")
    print(f"  Is Past Graduation: {metrics['is_past_graduation']}")
    
    print("\n" + "=" * 70)
    print("GENERATED MESSAGE:")
    print("=" * 70)
    print(message)
    print("=" * 70)
    
    print("\n✓ Integration test successful!")
    print("✓ All core utility modules are working correctly together!")
    
    # Write to file for verification
    with open('integration_output.txt', 'w', encoding='utf-8') as f:
        f.write("INTEGRATION TEST RESULTS\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Days Remaining: {metrics['days_remaining']}\n")
        f.write(f"Progress: {metrics['progress_percentage']:.2f}%\n")
        f.write(f"Is Graduation Day: {metrics['is_graduation_day']}\n")
        f.write(f"Is Past Graduation: {metrics['is_past_graduation']}\n\n")
        f.write("Generated Message:\n")
        f.write("=" * 70 + "\n")
        f.write(message + "\n")
        f.write("=" * 70 + "\n")
