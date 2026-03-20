"""Test script to show the difference between group and direct messages"""

from countdown_calculator import CountdownCalculator
from progress_bar_builder import ProgressBarBuilder
from message_formatter import MessageFormatter


def test_messages():
    """Test both group and direct message formats"""
    
    print("=" * 70)
    print("GROUP vs DIRECT MESSAGE COMPARISON")
    print("=" * 70)
    
    # Get countdown data
    calculator = CountdownCalculator()
    days = calculator.days_remaining()
    progress_pct = calculator.progress_percentage()
    progress_bar = ProgressBarBuilder.build(progress_pct)
    
    print(f"\n📊 Current Status:")
    print(f"   Days Remaining: {days}")
    print(f"   Progress: {progress_pct:.1f}%")
    print(f"   Progress Bar: {progress_bar}")
    
    # Direct Message (/start command)
    print("\n" + "=" * 70)
    print("📱 DIRECT MESSAGE (when user sends /start)")
    print("=" * 70)
    direct_msg = MessageFormatter.format_start_command_message(
        days_remaining=days,
        progress_bar=progress_bar,
        progress_percent=progress_pct
    )
    print(direct_msg)
    
    # Group Message (daily automated)
    print("\n" + "=" * 70)
    print("👥 GROUP MESSAGE (daily automated to groups)")
    print("=" * 70)
    group_msg = MessageFormatter.format_group_message(
        days_remaining=days,
        progress_bar=progress_bar,
        progress_percent=progress_pct
    )
    print(group_msg)
    
    print("\n" + "=" * 70)
    print("✅ Both message formats ready!")
    print("=" * 70)


if __name__ == "__main__":
    test_messages()
