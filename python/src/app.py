from Host import Host
import csv

VERSION_NUMBER="<VERSION_NUMBER>"

host1 = Host()
host2 = Host()

END_PHRASE = "'That's all we have for today folks'"
current_topic = 1
final_conversation_list = []
is_conversation_going = True

# The system message will specify how long responses should be
# The first messages from host1 is manually written
messages1 = [{"role": "system", "content": "You, Zoo, are a podcaster on a show called 'Am I the asshole?'"},
              {"role": "assistant", "content": "<INTRODUCTORY MESSAGE>"}]

messages2 = [{"role": "system", "content": "You, Zabba, are a podcaster on a show called 'Am I the asshole?'. You have a co-host, Zoo."},
             {"role": "user", "content": "<INTRODUCTORY MESSAGE>"}]

messages3 = [{"role": "system", "content": "You, Zoo, are a podcaster on a show called 'Am I the asshole?'"},
              {"role": "assistant", "content": "<INTRODUCTORY MESSAGE>"}]

messages4 = [{"role": "system", "content": "You, Zabba, are a podcaster on a show called 'Am I the asshole?'. You have a co-host, Zoo."},
             {"role": "user", "content": "<INTRODUCTORY MESSAGE>"}]

messages5 = [{"role": "system", "content": f"You, Zoo, are a podcaster on a show called 'Am I the asshole?'"},
              {"role": "assistant", "content": "<INTRODUCTORY MESSAGE>"}]

messages6 = [{"role": "system", "content": f"You, Zabba, are a podcaster on a show called 'Am I the asshole?'. You have a co-host, Zoo."},
             {"role": "user", "content": "<INTRODUCTORY MESSAGE>"}]

message_lists1 = [messages1, messages3, messages5]
message_lists2 = [messages2, messages4, messages6]

host1.conversation_history.extend(messages1)
host2.conversation_history.extend(messages2)
host1.set_message_lists(message_lists1)
host2.set_message_lists(message_lists2)

def switch_topics():
    global current_topic
    global final_conversation_list
    final_conversation_list.append(host2.conversation_history)
    current_topic += 1
    
    host1.set_conversation_history(host1.get_message_list(current_topic - 1))
    host2.set_conversation_history(host2.get_message_list(current_topic - 1))

def end_convo_if_over(message_content):
  global is_conversation_going
  if message_content.__contains__(END_PHRASE):
      print("Conversation over. Setting is_conversation_going to False")
      is_conversation_going = False

def write_messages_to_csv(message_lists):
    file_name = f'dialogue_{VERSION_NUMBER}.csv'
    with open(file_name, 'w', newline='') as csvfile:
        fieldnames = ['id', 'role', 'speech']
        writer = csv.writer(csvfile)

        writer.writerow(fieldnames)
        combined_messages_list = []

        # TODO: Exclude system messages
        for message_list in message_lists:
            combined_messages_list.extend(message_list)

        for index, message in enumerate(combined_messages_list):
            role = None
            if message["role"] == "system":
                role = "system"
            elif message["role"] == "assistant":
                role = "Zoo"
            else:
                role = "Zabba"

            writer.writerow([index, role, message["content"]])

num_turns_taken = 0
num_requests = 0
while num_turns_taken < 50 and is_conversation_going:

    if host1.get_is_max_tokens_exceeded():
        host2.append_message({"role": "user", "content": END_PHRASE})
        host1.append_message({"role": "assistant", "content": END_PHRASE})
        is_conversation_going = False
        break

    # Make requests to OpenAI API
    response_message = host2.make_request(num_requests)
    num_requests += 1

    print("Updating message lists.")
    
    host1.conversation_history.append({'role': 'user', 'content': response_message})

    response_message = host1.make_request(num_requests)
    num_requests += 1
    host2.conversation_history.append({'role': 'user', 'content': response_message})

    num_turns_taken += 1

    # Setup up for the next iteration
    do_switch_topics = host1.get_is_max_tokens_exceeded()
    if response_message.__contains__(END_PHRASE):
        print("Conversation over")
        is_conversation_going = False
    elif current_topic == 3 and do_switch_topics:
        print("Conversation over")
        is_conversation_going = False
    elif do_switch_topics:
        switch_topics()
        host1.set_max_tokens_exceeded_false()
        host2.set_max_tokens_exceeded_false()
        print(f"Max tokens exceeded should be false: {host1.get_is_max_tokens_exceeded()}")

if len(final_conversation_list) < len(message_lists1):
    final_conversation_list.append(host2.conversation_history)

write_messages_to_csv(final_conversation_list)
