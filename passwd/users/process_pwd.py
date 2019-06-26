def process_pwd_file(filepath):
    users = []
    with open(filepath, 'r') as f:
        for line in f:
            data = line.strip().split(':')
            if len(data) == 7:
                users.append({'name': data[0],
                              'uid': data[2],
                              'gid': data[3],
                              'comment': data[4],
                              'home': data[5],
                              'shell': data[6]})
    return users
