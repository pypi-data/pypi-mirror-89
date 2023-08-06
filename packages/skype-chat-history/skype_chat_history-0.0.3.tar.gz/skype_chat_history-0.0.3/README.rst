# Skype Chat History

Easily extract calls and contacts from messages.json file.

history = SkypeChatHistory("/home/Documents/messages.json")
print(history.extract_calls()) # extract calls
print(history.extract_contacts()) # get list of contacts