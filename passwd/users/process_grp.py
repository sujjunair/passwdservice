def process_grp_file(filepath):
    groups = []
    with open(filepath, 'r') as f:
        for line in f:
            data = line.split(':')
            if len(data) == 4:
                if data[3].strip():
                    members = data[3].strip().split(',')
                else:
                    members = []
                groups.append({'name': data[0],
                               'gid': data[2],
                               'members': members})
    return groups
