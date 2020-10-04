#%%
from collections import Counter

def readFile(filePath):
    content = ''
    with open(filePath, 'r') as file:
        if file.mode == 'r':
            content = file.read()
        file.close()
        return content


def get_frequencies(txt):
    freq = Counter(txt)
    ordered_freq = freq.most_common()
    for idx, element in enumerate(ordered_freq):
        print("{}: '{}'".format(idx, element[0]))
    return ordered_freq


#%%
content = readFile('2020_09_10_12_28_09_santiago.del.rey.Cifrado')
ordered_freq = get_frequencies(content)

pen#%%
def decode(txt, ordered_freq):
    txt = txt.replace('⏥', 'a')
    txt = txt.replace('⏦', 'b')
    txt = txt.replace('⏧', 'c')
    txt = txt.replace('⏨', 'd')
    txt = txt.replace('⏩', 'e')
    txt = txt.replace('⏪', 'f')
    txt = txt.replace('⏫', 'g')
    txt = txt.replace('⏬', 'h')
    txt = txt.replace('⏭', 'i')
    txt = txt.replace('⏮', 'j')
    txt = txt.replace('⏯', 'k')
    txt = txt.replace('⏰', 'l')
    txt = txt.replace('⏱', 'm')
    txt = txt.replace('⏲', 'n')
    txt = txt.replace('⏳', 'o')
    txt = txt.replace('⏴', 'p')
    txt = txt.replace('⏵', 'q')
    txt = txt.replace('⏶', 'r')
    txt = txt.replace('⏷', 's')
    txt = txt.replace('⏸', 't')
    txt = txt.replace('⏹', 'u')
    txt = txt.replace('⏠', 'v')
    txt = txt.replace('⏡', 'w')
    txt = txt.replace('⏢', 'x')
    txt = txt.replace('⏣', 'y')
    txt = txt.replace('⏤', 'z')
    return txt


decoded_content = decode(content, ordered_freq)
print(decoded_content[:5000])

# %%
with open('SantiagoDelReyJuarez_HerbertGeorgeWells_TheWorldSetFree.txt', 'w+') as file:
    file.write(decoded_content)
    file.close()
print('Writing finished')
# %%
