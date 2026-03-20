"""Test script to verify photo + caption functionality"""

import sys
from image_selector import ImageSelector
from message_formatter import MessageFormatter
from countdown_calculator import CountdownCalculator
from progress_bar_builder import ProgressBarBuilder
from motivational_message_selector import MotivationalMessageSelector


def test_image_selector():
    """Test image selection functionality"""
    print("Testing ImageSelector...")
    selector = ImageSelector()
    image_path = selector.get_random_image_path()
    
    if image_path:
        print(f"✓ Image selected: {image_path}")
        return True
    else:
        print("✗ No image selected (this is OK if images folder is empty)")
        return False


def test_start_command_format():
    """Test /start command message format"""
    print("\nTesting /start command message format...")
    
    calculator = CountdownCalculator()
    days = calculator.days_remaining()
    progress_pct = calculator.progress_percentage()
    
    progress_bar = ProgressBarBuilder.build(progress_pct)
    motivational_msg = MotivationalMessageSelector.get_message()
    
    message = MessageFormatter.format_start_command_message(
        days_remaining=days,
        progress_bar=progress_bar,
        motivational_message=motivational_msg
    )
    
    print("Generated /start message:")
    print("=" * 60)
    print(message)
    print("=" * 60)
    
    # Verify message contains expected elements
    checks = [
        ("Hey Graduating Ninja! 🥷" in message, "Greeting"),
        (f"{days} days" in message, "Days remaining"),
        (progress_bar in message, "Progress bar"),
        ("<b>" in message, "HTML formatting"),
        ("<i>" in message, "Italic formatting"),
    ]
    
    all_passed = True
    for passed, check_name in checks:
        status = "✓" if passed else "✗"
        print(f"{status} {check_name}")
        if not passed:
            all_passed = False
    
    return all_passed


def test_daily_message_format():
    """Test daily countdown message format"""
    print("\nTesting daily countdown message format...")
    
    calculator = CountdownCalculator()
    days = calculator.days_remaining()
    progress_pct = calculator.progress_percentage()
    is_grad_day = calculator.is_graduation_day()
    is_past_grad = calculator.is_past_graduation()
    
    progress_bar = ProgressBarBuilder.build(progress_pct)
    motivational_msg = MotivationalMessageSelector.get_message()
    
    message = MessageFormatter.format_countdown_message(
        days_remaining=days,
        progress_bar=progress_bar,
        motivational_message=motivational_msg,
        is_graduation_day=is_grad_day,
        is_past_graduation=is_past_grad
    )
    
    print("Generated daily message:")
    print("=" * 60)
    print(message)
    print("=" * 60)
    
    # Verify message contains expected elements
    checks = [
        ("🎓" in message, "Graduation emoji"),
        (f"{days} days" in message, "Days remaining"),
        (progress_bar in message, "Progress bar"),
        ("<b>" in message, "HTML formatting"),
        ("💡" in message, "Motivational emoji"),
    ]
    
    all_passed = True
    for passed, check_name in checks:
        status = "✓" if passed else "✗"
        print(f"{status} {check_name}")
        if not passed:
            all_passed = False
    
    return all_passed


def main():
    """Run all tests"""
    print("=" * 60)
    print("PHOTO + CAPTION FUNCTIONALITY TEST")
    print("=" * 60)
    
    results = []
    
    # Test 1: Image Selector
    results.append(("Image Selector", test_image_selector()))
    
    # Test 2: /start Command Format
    results.append(("/start Command Format", test_start_command_format()))
    
    # Test 3: Daily Message Format
    results.append(("Daily Message Format", test_daily_message_format()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ All tests passed! Photo + caption functionality is ready.")
        return 0
    else:
        print("\n✗ Some tests failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
