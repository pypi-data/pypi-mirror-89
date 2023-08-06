import json


class SkypeChatHistory:
    def __init__(self,file_path):
        self.chat_history = json.loads(self.__read_file(file_path))
        
    def __read_file(self, file_path):
        f = open(file_path)
        file_content = f.read()
        f.close()
        return file_content

    def __loop_convo(self):
        for convo in self.chat_history["conversations"]:
            for message in convo["MessageList"]:
                yield message

    def __is_call(self, message):
        return message["messagetype"] == "Event/Call"

    def __format_data(self, message):
        return (message["originalarrivaltime"], 
                message["from"].split(":")[-1], 
                message["conversationid"].split(":")[-1])

    def get_calls(self):
        return [self.__format_data(message) for message in self.__loop_convo() if self.__is_call(message)]
    
    def get_contacts(self):
        return [(conv["id"].split(":")[-1], conv["displayName"]) for conv in self.chat_history["conversations"] if "thread" not in conv["id"] and "cast" not in conv["id"]]

