from datetime import timedelta


def format_timedelta(td: timedelta):

    # Convert timedelta object to microseconds
    total_microseconds = td.seconds * 1000000 + td.microseconds
    hours, remainder = divmod(total_microseconds, 3600000000)
    minutes, remainder = divmod(remainder, 60000000)
    seconds, remainder = divmod(remainder, 1000000)
    tens, remainder = divmod(remainder, 100000)
    hundreds, remainder = divmod(remainder, 10000)

    formatted = ""
    # Show hours only if necessary
    if hours > 0:
        formatted += str(hours).zfill(2) + ":"
    # Always show minutes and seconds
    formatted += str(minutes).zfill(2) + ":" + str(seconds).zfill(2)
    # Show tens and hundreds only if under 10s
    if total_microseconds / 1000000 <= 10:
        formatted += "." + str(tens) + str(hundreds)
    
    return formatted
