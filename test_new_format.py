"""Test script for the new 100-day sprint countdown format"""

from countdown_calculator import CountdownCalculator
from progress_bar_builder import ProgressBarBuilder
from message_formatter import MessageFormatter


def test_new_format():
    """Test the new BiT graduation countdown format"""
    
    print("=" * 60)
    print("BiT GRADUATION COUNTDOWN - NEW FORMAT TEST")
    print("=" * 60)
    
    # Get countdown data
    calculator = CountdownCalculator()
    days = calculator.days_remaining()
    progress_pct = calculator.progress_percentage()
    
    print(f"\n📊 Countdown Data:")
    print(f"   Days Remaining: {days}")
    print(f"   Progress: {progress_pct:.1f}%")
    print(f"   Sprint Days: {CountdownCalculator.SPRINT_DAYS}")
    print(f"   Graduation Date: {CountdownCalculator.GRADUATION_DATE}")
    print(f"   Sprint Start: {CountdownCalculator.START_DATE}")
    print(f"   Timezone: {CountdownCalculator.TIMEZONE}")
    
    # Generate progress bar
    progress_bar = ProgressBarBuilder.build(progress_pct)
    
    print(f"\n📈 Progress Bar (25 chars):")
    print(f"   {progress_bar}")
    print(f"   Length: {len(progress_bar)} characters")
    
    # Format message
    message = MessageFormatter.format_start_command_message(
        days_remaining=days,
        progress_bar=progress_bar,
        progress_percent=progress_pct
    )
    
    print(f"\n💬 Formatted Message:")
    print("=" * 60)
    print(message)
    print("=" * 60)
    
    # Test edge cases
    print(f"\n🧪 Edge Case Tests:")
    
    # Test 100 days (0% progress)
    print(f"\n   100 days remaining (0%):")
    bar_100 = ProgressBarBuilder.build(0)
    print(f"   {bar_100}")
    
    # Test 50 days (50% progress)
    print(f"\n   50 days remaining (50%):")
    bar_50 = ProgressBarBuilder.build(50)
    print(f"   {bar_50}")
    
    # Test 0 days (100% progress)
    print(f"\n   0 days remaining (100%):")
    bar_0 = ProgressBarBuilder.build(100)
    print(f"   {bar_0}")
    msg_grad = MessageFormatter.format_start_command_message(0, bar_0, 100)
    print(f"   Message:\n{msg_grad}")
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    test_new_format()
