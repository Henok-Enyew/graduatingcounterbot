"""Motivational Message Selector Module

This module provides software engineering-themed motivational quotes for daily
countdown messages. Messages are selected with variation to keep content fresh.
"""

from datetime import date


class MotivationalMessageSelector:
    """Selects motivational messages for software engineering students.
    
    Provides a collection of inspirational quotes relevant to software engineering
    and computer science education. Uses date-based selection to ensure variation
    across different days.
    """
    
    # Collection of software engineering-themed motivational quotes
    MESSAGES = [
        "Code is like humor. When you have to explain it, it's bad. – Cory House",
        "First, solve the problem. Then, write the code. – John Johnson",
        "The best error message is the one that never shows up. – Thomas Fuchs",
        "Experience is the name everyone gives to their mistakes. – Oscar Wilde",
        "In order to be irreplaceable, one must always be different. – Coco Chanel",
        "Java is to JavaScript what car is to Carpet. – Chris Heilmann",
        "Knowledge is power. – Francis Bacon",
        "Sometimes it pays to stay in bed on Monday, rather than spending the rest of the week debugging Monday's code. – Dan Salomon",
        "Perfection is achieved not when there is nothing more to add, but rather when there is nothing more to take away. – Antoine de Saint-Exupery",
        "Code never lies, comments sometimes do. – Ron Jeffries",
        "Simplicity is the soul of efficiency. – Austin Freeman",
        "Before software can be reusable it first has to be usable. – Ralph Johnson",
        "Make it work, make it right, make it fast. – Kent Beck",
        "Clean code always looks like it was written by someone who cares. – Robert C. Martin",
        "Any fool can write code that a computer can understand. Good programmers write code that humans can understand. – Martin Fowler",
        "The only way to learn a new programming language is by writing programs in it. – Dennis Ritchie",
        "Programs must be written for people to read, and only incidentally for machines to execute. – Harold Abelson",
        "Walking on water and developing software from a specification are easy if both are frozen. – Edward V. Berard",
        "The most disastrous thing that you can ever learn is your first programming language. – Alan Kay",
        "Testing leads to failure, and failure leads to understanding. – Burt Rutan",
        "It's not a bug – it's an undocumented feature. – Anonymous",
        "Talk is cheap. Show me the code. – Linus Torvalds",
        "Don't worry if it doesn't work right. If everything did, you'd be out of a job. – Mosher's Law",
        "The best thing about a boolean is even if you are wrong, you are only off by a bit. – Anonymous",
        "Without requirements or design, programming is the art of adding bugs to an empty text file. – Louis Srygley",
        "The function of good software is to make the complex appear to be simple. – Grady Booch",
        "Debugging is twice as hard as writing the code in the first place. – Brian Kernighan",
        "Good code is its own best documentation. – Steve McConnell",
        "Measuring programming progress by lines of code is like measuring aircraft building progress by weight. – Bill Gates",
        "Controlling complexity is the essence of computer programming. – Brian Kernighan",
    ]
    
    @staticmethod
    def get_message() -> str:
        """Returns a motivational message appropriate for software engineering students.
        
        Uses date-based selection to ensure variation across different days.
        The selection is deterministic for a given date, meaning the same
        message will be returned for the same date.
        
        Returns:
            str: A motivational message from the collection.
        """
        # Use day of year for date-based selection to ensure variation
        today = date.today()
        day_of_year = today.timetuple().tm_yday
        
        # Select message based on day of year modulo collection size
        index = day_of_year % len(MotivationalMessageSelector.MESSAGES)
        
        return MotivationalMessageSelector.MESSAGES[index]
