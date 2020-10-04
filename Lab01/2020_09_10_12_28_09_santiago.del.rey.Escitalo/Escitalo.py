#%%
from collections import Counter
import time


def read_file(filePath):
    content = ''
    with open(filePath, 'r') as file:
        if file.mode == 'r':
            content = file.read()
        file.close()
        return content


def find_index(s, ch):
    """Return a list with all the intexes in the string s that match the character ch

    Args:
        s (str): A string
        ch (chr): The character to find

    Returns:
        list: A list with all the intexes in the string s that match the character ch
    """
    return [i for i, ltr in enumerate(s) if ltr == ch]


#%%
content = read_file('2020_09_10_12_28_09_santiago.del.rey.Escitalo')
print('File length {}'.format(len(content)))

# %%
start_timestamp = time.time()
t_indexes = find_index(content[:10000], 'T')
h_indexes = find_index(content[:10000], 'H')
e_indexes = find_index(content[:10000], 'E')

distance_list = []
tab = {}
tab_the = {}
for idx_t in t_indexes:
    for idx_h in reversed(h_indexes):
        distance = idx_h - idx_t

        # * Save distance if it is greater than or equal to the index of the first letter plus 1.
        if distance >= (idx_t + 1):
            distance_list.append(distance)
            if distance in tab:
                indexes = tab.get(distance)
            else:
                indexes = []
            indexes.append(idx_t)
            tab.update({distance: indexes})

        # * If the third letter is the same distance from the second as the second from the first, save the distance.
        if ((idx_h + distance) < len(content)) & (content[idx_h + distance] == 'E'):
            distance_list.append(distance)
            if distance in tab_the:
                indexes = tab_the.get(distance)
            else:
                indexes = []
            indexes.append(idx_t)
            tab_the.update({distance: indexes})

frequencies = Counter(distance_list)
common_freq = frequencies.most_common()


# %%
n = common_freq[0][0]
matrix = [content[index: index + n] for index in range(0, len(content),n)]
# * Add padding if necessary
matrix[-1] = matrix[-1] + '*'*(n - len(matrix[-1]))
trans = [''.join(row) for row in zip(*matrix)]
print("--- %s seconds" % (time.time() - start_timestamp))
#[print(row) for row in trans[0][:10]]

with open('SantiagoDelReyJuarez_HerbertGeorgeWells_TheSecretPlacesOfTheHeart.txt', 'w+') as file:
    [file.write(row) for row in trans]
    file.close()

print('Writing finished')
# %%
