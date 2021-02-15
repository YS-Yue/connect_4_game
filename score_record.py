class Score_Record:

    def __init__(self, filename, player):
        self.filename = filename
        self.players_dic = {}
        self.player = player

    def read_and_update_data(self):
        """Read and update the player's times of win"""

        f = open(self.filename, 'r')

        for line in f:
            record = line.strip().split(' ')
            if record:
                win_times = int(record[-1])
                player_name = ' '.join(record[0: -1]).lower()
                self.players_dic[player_name] = win_times

        if self.player in self.players_dic.keys():
            self.players_dic[self.player] += 1
        else:
            self.players_dic[self.player] = 1

        sorted_records = sorted(self.players_dic.items(),
                                key=lambda x: x[1], reverse=True)

        f = open(self.filename, 'w')
        for new_record in sorted_records:
            f.write(str(new_record[0].title())+' '+str(new_record[1])+'\n')

        f.close()

        return sorted_records
