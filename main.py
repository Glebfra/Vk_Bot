from VkBot import VkBot

vkBot = VkBot.create_bot()
vkBot.load_answers_from_file('messages.json')
print(vkBot.answers)
