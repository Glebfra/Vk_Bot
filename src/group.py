import json


class Group(object):
    def __init__(self, vk):
        self.vk = vk
        self.group_id = 213831540
        self.users = self.vk.method('groups.getMembers', {'group_id': self.group_id})

        with open('users.json', 'w') as file_users:
            json.dump(self.users, file_users)

    def get_last_wall_post(self):
        pass
