def num_to_alphabet(num):
    if num > 675:
        return ''
    columns = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    if num < 27:
        return columns[num]
    rounds = num // 26
    tail = num % 26
    if tail == 0:
        rounds = rounds - 1
        tail = 26
    return columns[rounds] + columns[tail]