def convert(milliseconds):
    seconds = milliseconds // 1000  # Convert milliseconds to seconds
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)