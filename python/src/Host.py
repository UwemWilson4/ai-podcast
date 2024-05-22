from openai import OpenAI
import time

class HostException:
    def __init__(self, message) -> None:
        self.message = message
        self.message_lists = None

class Host():
    model = "gpt-3.5-turbo"
    is_max_tokens_exceeded = False

    def __init__(self) -> None:
        self.conversation_history = []
        self.client = OpenAI()

    def make_request(self, num_requests):
        self.sleep_or_continue(num_requests)
        print("Done waiting. Making API request.")

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.conversation_history
        )

        # Used to signal a change in topic, since only so many tokens can be used by the model
        if response.usage.total_tokens > 3048:
            self.is_max_tokens_exceeded = True

        try:
            message = response.choices[0].message.content
            print(f"Extracted message content: {message}")
        except Exception as e:
            print(f"Failed to get desired response from OpenAI API: {e}")
            raise Exception

        self.conversation_history.append({"role":"assistant", "content":message})

        print(f"Response received:\n{response}. Returning the message inside.")

        return message

    # Required so that free tier usage limits aren't exceeded
    def sleep_or_continue(self, num_requests):
        print("Waiting for 3 minites.")
        if num_requests % 3 == 0:
            time.sleep(300)

    def get_is_max_tokens_exceeded(self):
        return self.is_max_tokens_exceeded
    
    def set_max_tokens_exceeded_false(self):
        self.is_max_tokens_exceeded = False

    def set_message_lists(self, message_lists):
        self.message_lists = message_lists
        print(f"Set message_lists to: {self.message_lists}")

    def set_conversation_history(self, messages):
        self.conversation_history = messages
    
    def get_message_list(self, index):
        return self.message_lists[index]
    
    def append_message(self, message):
        self.conversation_history.append(message)