

class UsersIndices:
    def __init__(self):
        self.starting_index = 300000

    def get_user_index_dataset(self, index_db):
        return self.starting_index + index_db
