import numpy as np

THRESHOLD = 0.54  # calculated with def calculate_threshold(data)
MEAN_CONSONANT_COST = 0.60  # calculated with code at the bottom
MEAN_VOWEL_COST = 0.49  # calculated with code at the bottom

def calculate_threshold(data):
    # This function calculates the threshold for clustering. The threshold was set to the value seperating the upper quartile of the similarity scores
    total_distance = 0
    count = 0
    distances = []
    data_without_duplicates = []

    for item in data:
        if item not in data_without_duplicates:
            data_without_duplicates.append(item)  # makes sure that no words are used more than once in the calculation

    for i in range(0, len(data_without_duplicates)):
        for j in range(i + 1, len(data_without_duplicates)):
            total_distance += pwld(data_without_duplicates[i], data_without_duplicates[j])
            count += 1
            distances.append(pwld(data_without_duplicates[i], data_without_duplicates[j]))

    # average = total_distance/count
    q1, q3 = np.percentile(distances, [25, 75])
    print('q3:', q3)  # upper quartile
    # print('average:', average)

def pwld(word1, word2):  # (Agarwal, 2022)
    m = len(word1)
    n = len(word2)
    distances = [[0] * (n + 1) for _ in range(m + 1)]  # creates matrix to store the PWLD scores

    for i in range(m + 1):  # initializes the first row
        distances[i][0] = i
    for j in range(n + 1):  # initializes the first column
        distances[0][j] = j

    # matrix is filled in with the PWLD scores
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # if phonemes are equal, the cost is 0, otherwise the cost depends on the similarity of the phonemes
            cost = 0 if word1[i - 1] == word2[j - 1] else costs(word1[i - 1], word2[j - 1])
            distances[i][j] = min(  # the matrix is filled with the operation with the lowest cost
                distances[i - 1][j] + 1,  # deletion
                distances[i][j - 1] + 1,  # insertion
                distances[i - 1][j - 1] + cost  # substitution
            )
    # final cell (cell to the bottom-right) of the matrix contains the minimal PWLD
    pwld = distances[m][n]

    # normalizes the score
    similarity_score = 1 - (pwld / max(m, n))  # so a small PWLD often results in a high similarity_score score
    return similarity_score


def costs(phoneme1, phoneme2):
    vowels = ['i', 'y', 'u', 'ɪ', 'ʏ', 'ɔ', 'e', 'ø', 'o', '3', 'œ', '^', 'ɛ', 'ɑ', 'a', 'ə']
    consonant = ['b', 'p', 'v', 'f', 'w', 'm', 'd', 't', 'z', 's', 'r', 'l', 'n', 'c', 'ʒ', 'ʃ', 'j', 'ɲ', 'g', 'k',
                 'x', 'h', 'ŋ']
    if (phoneme1 in vowels) and (phoneme2 in vowels):
        cost = vowel_cost(phoneme1, phoneme2)  # if phonemes are both vowels
    elif (phoneme1 in consonant) and (phoneme2 in consonant):
        cost = consonant_cost(phoneme1, phoneme2)  # if phonemes are both consonants
    else:
        cost = 1  # cost is 1 if the phonemes are not of the same type
    return cost


def vowel_cost(vow1, vow2):
    cost_vertical_position = abs(
        pos_vertical(vow1) - pos_vertical(vow2))  # calculates the difference in vertical position
    cost_horizontal_position = abs(
        pos_horizontal(vow1) - pos_horizontal(vow2))  # calculates the difference in horizontal position
    if rounding(vow1) == rounding(vow2):  # if both rounded or both unrounded
        cost_rounding = 0
    else:
        cost_rounding = 1  # if one is rounded and the other unrounded
    if stress(vow1) == stress(vow2):  # if they are of the same type
        cost_stress = 0
    else:
        cost_stress = 1  # if the types do not match
    cost = (cost_vertical_position * 0.4) + (cost_horizontal_position * 0.3) + (cost_rounding * 0.1) + (cost_stress * 0.2)
    return cost  # return the cost of substituting vow1 and vow2. Low cost means that the vowels share many similarities. High cost means very different vowels.


def pos_vertical(vow):
    high = ['i', 'y', 'u']
    mid = ['ɪ', 'ʏ', 'ɔ', 'e', 'ø', 'o']
    low = ['3', 'œ', '^', 'ɛ', 'ɑ', 'a', 'ə']
    if vow in high:
        pos_vertical = 0
    elif vow in mid:
        pos_vertical = 0.5
    elif vow in low:
        pos_vertical = 1
    else:
        pos_vertical = -100  # this was to make sure there was no missing letter (a letter in the word list that did not exist in my code). This was never the case
    return pos_vertical


def pos_horizontal(vow):
    front = ['i', 'ɪ', 'e', '3', 'ɛ']
    central = ['y', 'ʏ', 'ø', 'œ', 'ə']
    back = ['u', 'ɔ', 'o', '^', 'ɑ', 'a']
    if vow in front:
        pos_horizontal = 0
    elif vow in central:
        pos_horizontal = 0.5
    elif vow in back:
        pos_horizontal = 1
    else:
        pos_horizontal = -100  # this was to make sure there was no missing letter (a letter in the word list that did not exist in my code). This was never the case
    return pos_horizontal


def rounding(vow):
    if vow in ['i', 'ɪ', 'e', '3', 'ɛ']:
        return "unrounded"
    else:
        return "rounded"


def stress(vow):
    stressed = ['i', 'y', 'e', 'ø', 'o', 'u', 'a']
    unstressed = ['ɪ', 'ʏ', 'ɔ', 'ɛ', 'ɑ', 'ə']
    diphthong = ['3', 'œ', '^']
    if vow in stressed:
        return "stressed"
    elif vow in unstressed:
        return "unstressed"
    elif vow in diphthong:
        return "diphthong"
    else:
        return "error"  # this was to make sure there was no missing letter (a letter in the word list that did not exist in my code). This was never the case


def consonant_cost(con1, con2):  # calculates the costs of substituting two consonants
    # calculates the cost_place_of_articulation

    # if con1 == "r" and con2 == "r":
    #     cost_place_of_articulation = 0 # if

    # Pronounciation of r depends on the accent
    if con1 == "r" and (place_of_articulation(con2) == "alveolair" or place_of_articulation(con2) == "velaar"):
        cost_place_of_articulation = 0
    elif con2 == "r" and (place_of_articulation(con1) == "alveolair" or place_of_articulation(con1) == "velaar"):
        cost_place_of_articulation = 0
    else:
        # in the cases that letters different than r are compared
        cost_place_of_articulation = abs(place_of_articulation(con1) - place_of_articulation(con2))

    # calculates the cost_method_of_articulation
    if method_of_articulation(con1) == method_of_articulation(con2):
        cost_method_of_articulation = 0  # if the methods are the same
    else:
        cost_method_of_articulation = 1  # if the methods are not the same

    # if both con1 and con2 are either plosive or fricative (they don't have to be the same type), it is compared if
    # they are voiced
    if (method_of_articulation(con1) == "plosive" or method_of_articulation(con1) == "fricative") and (
            method_of_articulation(con2) == "plosive" or method_of_articulation(con2) == "fricative"):
        voiced1 = voiced(con1)
        voiced2 = voiced(con2)
        if voiced1 == voiced2:
            cost = (cost_place_of_articulation * 0.4) + (cost_method_of_articulation * 0.4) + 0 #if both voiced or both unvoiced
        else:
            cost = (cost_place_of_articulation * 0.4) + (cost_method_of_articulation * 0.4) + 0.2 #if not same type
    # if not both con1 and con2 plosive or fricative (when either con1 or con2 was liquida, semivowel or nasal)
    else:
        cost = (cost_place_of_articulation * 0.5) + (cost_method_of_articulation * 0.5)

    # this ensures that the mean cost of vowels and the mean cost of consonants are equal.
    # otherwise, there could be a bias towards words with more vowels in it or with more consonants
    scaling_factor = MEAN_VOWEL_COST / MEAN_CONSONANT_COST
    adjusted_cost = cost * scaling_factor
    return adjusted_cost

def place_of_articulation(con):
    labiaal = ['b', 'p', 'v', 'f', 'w', 'm']
    alveolair = ['d', 't', 'z', 's', 'l', 'n', 'r']  # r in alveolair, because when r is compared with a letter from labiaal or postalveolair, the cost is always 0.33
    postalveolair = ['c', 'ʒ', 'ʃ', 'j', 'ɲ']
    velaar = ['g', 'k', 'x', 'h', 'ŋ']
    if con in labiaal:
        place_of_articulation = 0
    elif con in alveolair:
        place_of_articulation = 0.3333333333
    elif con in postalveolair:
        place_of_articulation = 0.666666666
    elif con in velaar:
        place_of_articulation = 1
    else:
        place_of_articulation = -100 # this was to make sure there was no missing letter. This was never the case
    return place_of_articulation

def method_of_articulation(con):
    plosive = ['b', 'p', 'd', 't', 'c', 'g', 'k']
    fricative = ['v', 'f', 'z', 's', 'ʒ', 'ʃ', 'x']
    liquida = ['r', 'l']
    semivowels = ['w', 'j', 'h']
    nasal = ['m', 'n', 'ɲ', 'ŋ']
    if con in plosive:
        return "plosive"
    elif con in fricative:
        return "fricative"
    elif con in liquida:
        return "liquida"
    elif con in semivowels:
        return "semivowels"
    elif con in nasal:
        return "nasal"
    else:
        return "error" # this was to make sure there was no missing letter. This was never the case

def voiced(con):
    if con in ['b', 'd', 'g', 'v', 'z', 'ʒ']:
        return "voiced"
    else:
        return "unvoiced"

def make_clusters(PVF_responses):
    #this function made the clusters given an list of words
    clusters = [] #keep track of all the clusters
    for index, word in enumerate(PVF_responses): #keeps track of the index and word
        next_word_index = index + 1
        cluster = [word]  # start current cluster

        cluster_complete = False
        while not cluster_complete:
            if next_word_index < len(PVF_responses): #as long as there are still words to check
                next_word = PVF_responses[next_word_index]
                #checks if next word is similar to every other word in cluster
                add_to_cluster = all([pwld(next_word, clustered_words) >= THRESHOLD for clustered_words in cluster])
                if add_to_cluster:
                    cluster.append(next_word) # if it is similar to all, the next word is added
                    # and the next index is taken, such that the word that follows the word that was just added is
                    # compared to all words in the cluster
                    next_word_index += 1
                else:
                    # if the word was not similar to all other words in the cluster, the cluster is completed
                    cluster_complete = True
            else:
                # if the last word of the given list of words has been reached
                cluster_complete = True

        if not sub_cluster(cluster, clusters):
            # checks if the current cluster is not a subcluster of an already existing cluster
            clusters.append(cluster)

    return clusters #list of clusters is returned

def sub_cluster(cluster, clusters):
    for c in clusters: # every cluster (c) that already exist in clusters is compared with the new cluster
        if set(cluster).issubset(c):
            # if the new cluster is a subcluster of one of the already existing clusters, the new cluster will not be added
            return True
    return False # it is not a subcluster, and the cluster will be added to clusters

def analyze_clusters(clusters): #this function was made for me to make analyzing the clusters easier.
    total_clusters = 0
    total_words = 0
    cluster_sizes = []
    percentages = {}
    unclustered_words = 0
    for cluster in clusters:
        total_clusters += 1
        cluster_sizes.append(len(cluster))
        total_words += len(cluster)
        if len(cluster) == 1:
            unclustered_words += 1
    print(cluster_sizes)

    for size in set(cluster_sizes):
        count = cluster_sizes.count(size)
        print("Cluster size", size, ": ", count)
        percentage = ((size * count) / total_words) * 100
        percentages[size] = percentage
    print("Total clusters: ", total_clusters)
    print("Total words given: ", total_words)
    print(percentages)
    print("Total unclustered words:", unclustered_words)


if __name__ == '__main__':
    all_responses = ['makəlar', 'mʏskɛtir', 'mɔrtir', 'mɑn', 'mes', 'mew', 'mes', 'merəl', 'mɑkɛlək', 'mujlək', 'moj',
                     'matəx', 'mesopotamiə', 'mɪdəl', 'medijʏm', 'mɑxtəx', 'mɑxt', 'mɑxtsvərh^dɪŋ', 'minimal',
                     'mɑksimal', 'mermals', 'mɛldə', 'medun', 'man', 'moral', 'morel', 'mɪndər', 'mer', 'maxis',
                     'maxistral', 'metodə', 'metodik', 'm3mərə', 'mezɪŋə', 'mandɑx', 'mɔnt', 'mɑrkt', 'mɑrkcə',
                     'mɑrktə', 'mɑrktɔndərzuk',
                     'moxə', 'mɑx', 'maxə', 'max', 'mal', 'malə', 'malt', 'maldə', 'mœlkɔrf', 'myslirep', 'mɑstyrbatsi',
                     'mɔŋxol', 'mɔŋxolcə', 'mudər', 'mudərcə', 'mudərs', 'mɛnsap', 'mɛnsapə', 'mɛnsapjə', 'mʏrf',
                     'mɑxma', 'møtə', 'mudər', 'mɪdəl', 'mɑrko', 'median', 'metro', 'mɑpjə', 'myzikɪnstrymɛnt',
                     'mɑskər', 'mɑl', 'mɑn', 'mɑm', 'matəx', 'metlɪnt', 'mɑksi-kosi', 'mɔpjə', 'mɪni', 'myrsxɪldərɪŋ',
                     'mʏrf', 'mʏsk',
                     'məner', 'mɑt', 'man', 'merkut', 'mœs', 'mɛs', 'makəlar', 'mɑʃɛtə', 'mɑnʃɛtknop', 'moj', 'mɑkɛlək',
                     'mat', 'macəsprojɛkt', 'mɑma', 'mudər', 'mujlək', 'mɑti', 'merkut''mɑma', 'modəratɔr', 'mudərtal',
                     'mɑlot', 'modəm', 'morel', 'mɑrkt', 'mɪnar', 'mer', 'mɑrkerə', 'mɑrkerstɪft', 'mɑksimal', 'metər',
                     'mandɑx', 'myr', 'mɪndərh3t', 'matstɑf', 'mɑksimal', 'mɔrxə', 'mutə', 'mest', 'mɑxtəlos', 'mɑxt',
                     'mɑn', 'mɑtrɑs', 'mɑnt', 'man', 'mort', 'mi^', 'm^', 'mɑl', 'mɑt', 'mɑnk', 'mɛlvɪn', 'mew', 'mes',
                     'myr', 'mœlkɔrf', 'mortzak', 'məvr^', 'məner', 'moj', 'mir', 'mincə', 'maxi', 'maxis', 'mɑtrɑs',
                     'mɑtros', 'mɑtr3s', 'mɛns', 'matsxɑp3', 'moj', 'mar', 'məner', 'mɑtʃo', 'mɑnəcə', 'makəlar',
                     'mɑdɑxɑskɑr', 'melopər', 'macə', 'mɪkpʏnt', 'mɪsbɑksəl', 'mɑxnet', 'mɪnɑxtənt', 'mɑn', 'mɑma',
                     'mɑtros',
                     'mɑlot', 'mɪnpʏnt', 'mar', 'mɑma', 'moj', 'medis3nə', 'makəlars', 'mœzə', 'mirə', 'mɔt',
                     'mɑrmɑladə', 'mestər', 'mɑxtəx', 'mɑkɛlək', 'mujlək', 'm3nwɛrkər', 'mipə', 'marɔkan',
                     'mɑsədonijər', 'mɑterial', 'mɛns', 'mɪdəl', 'mɑrsəp3n', 'manijɑk', 'mɔnʃu', 'man', 'mɪdəl', 'mar',
                     'ram', 'moj', 'matix', 'mediʏm', 'mɑnir', 'moj', 'mɑma', 'mestər', 'metər', 'madən', 'manir',
                     'makər', 'melər', 'mɑstər',
                     'mel', 'meldrat', 'mɛnədʒər', 'maxijər', 'meladrɛs', 'mɑnt', 'mɑndə', 'makər', 'maxər', 'mɑma',
                     'mudər', 'makəlar', 'mɑfkes', 'mesopotamiə', 'mɔŋxol', 'mɔŋxoliʏ', 'mojstə', 'moj', 'man',
                     'manəsx3n', 'manlɪxt', 'mesopotamiə', 'misofoni', 'm^', 'mɔk', 'mɑpjə', 'mɑkɛlək', 'mujlək',
                     'mɪdəlmatəx', 'manəsx3nə', 'moj', 'mujlək', 'mɪndərwardəx', 'mɪndər', 'moxələk', 'mɪsxin', 'mar',
                     'moxə', 'mɑx', 'mɔx',
                     'mɔxt', 'mɔxtə', 'moxələk', 'mustə', 'makə', 'maktə', 'mak', 'makt', 'mɪsxin', 'mɑrko', 'mora',
                     'moj', 'mɑn', 'mɑnələk', 'mujzam', 'mu', 'muh3t', 'mat', 'matstaf', 'man', 'myr', 'myrə', 'm3n',
                     'm3', 'mir', 'mujzam', 'memoriɑm', 'mɛnsə', 'mɛns', 'mɛnsh3t', 'mɑrko', 'mɑrkʏs', 'mes',
                     'metejorit', 'matwɛrk', 'mudər', 'mɪsplatst', 'mexant', 'metejolox', 'medikʏs', 'mɪdɑx',
                     'mɪdɑxdel', 'mustœn',
                     'musplɑnt', 'mɑzda', 'mɛrcedəs', 'mas', 'mok', 'mɔl', 'mɔt', 'mar', 'mudər', 'mɑma', 'max',
                     'mirəetər', 'mizoxinɪst', 'mizoxini', 'mur', 'mɑn', 'mɑxtəx', 'mip', 'mɑkɛlək', 'mujlək', 'mer',
                     'mɪndər', 'maksimʏm', 'minimʏm', 'molə', 'molənar', 'mel', 'mel', 'mɛs', 'mɔs', 'mɛkərə', 'mestər',
                     'myrvʏlər', 'm3tər', 'mat', 'mɑʃinɪst', 'metlɪnt', 'metlɑt', 'max', 'mɔnthɑrmonika', 'mudər', 'ma',
                     'mœs',
                     'maxɪnh^t', 'mɔndəlɪŋ', 'mɑstər', 'moj', 'mɛlk', 'mɑn', 'mandɑx', 'mel', 'm3ʃə', 'mɑnt',
                     'mortwapə', 'mort', 'mɛs', 'mɑndolinə', 'mɪst', 'minimal', 'mɑksimal', 'mudər', 'mɑma', 'mʏs',
                     'mɔt', 'mɑx', 'me', 'medijʏm', 'mir', 'mɪkə', 'mɪsə', 'mɛt', 'mʏts', 'melevə', 'mar', 'mɪnstəns',
                     'matrɪks', 'matərijal', 'mɑma', 'mesopotamiə', 'mɑn', 'makrel', 'maxistral', 'maxi', 'mʏskylɛr',
                     'mɑnəcəspʏtər', 'mɔk',
                     'mɔka', 'mytɑnt', 'mytɛla', 'mɑstʏrberə', 'mɑf', 'mɑfɛrt', 'mɑfkes', 'mɑzəltɔf', 'mɔl', 'mɔlə',
                     'mɔsəlmɑn', 'mɔsəls', 'mɑx', 'mɑskər', 'mɔf', 'mɑst', 'mɑjs', 'mani', 'molə', 'mel', 'mel',
                     'maxis', 'maxijər', 'mɑŋgo', 'mɔnt', 'mɑskər', 'mɑt', 'mokər', 'mɑn', 'merəl', 'mɑl', 'mɑf',
                     'mɑnt', 'motər', 'motorik', 'mɛmori', 'mɔnt', 'mandɑx', 'myrə', 'modɛl', 'man', 'mɔrxə', 'mɔdər',
                     'm3n', 'moj', 'mɑkɛlək',
                     'mujlək', 'mexant', 'medɛŋkənt', 'mestɑl', 'mest', 'moxələk', 'mezɪŋə', 'mɪdəlbar', 'moj', 'mɑt',
                     'mɛlk', 'medijʏm', 'mɔnstər', 'møbəls', 'møbəlmakər', 'møbəlxəbrœkər', 'mɛst', 'mɪn', 'mɪnzam',
                     'maxər', 'mɑl', 'mɑk', 'man', 'me', 'mɔrxə', 'mɪdɑx', 'mexrujə', 'mexan', 'mudər', 'mexan', 'moj',
                     'mɑndrel', 'makə', 'mœs', 'mas', 'mexafon', 'mudər', 'mɑma', 'mɑriakakjə', 'mɔnt', 'mɔnthuk',
                     'mɔnthixijənɪstə',
                     'myr', 'mɔp', 'mɔpshɔnt', 'mokər', 'm3t', 'm3dəkamər', 'm3ʃəskledɪŋ', 'm3ʃə', 'mɪnt', 'mir',
                     'mini', 'minirɔk', 'mɪn', 'minʏskyl', 'minimʏm', 'maksimʏm', 'mestər', 'mudər', 'merəl', 'mew',
                     'mɑrxrit', 'mɪdəllɑntsə ze', 'mɪdə-ostə', 'mɑʃinə', 'maxaz3n', 'mestər', 'məvr^', 'mat', 'mu',
                     'mɪsələk', 'maxər', 'moj', 'man', 'mɪdəl', 'metər', 'maxər', 'moj', 'mɪdəvutsbencəs', 'mɑrtər',
                     'mɑrxarinə', 'mɑntəl',
                     'mɪndər', 'mer', 'mɑndar3n', 'mɛrxp3pjə', 'mɛrxəlɑnt', 'man', 'mɔnt', 'mɔstərt', 'medədoxə',
                     'medəl3də', 'mujzam', 'mujlək', 'mɛns', 'metər', 'maxər', 'majo', 'metronom', 'mɛlk', 'mɑrs',
                     'mel', 'mexa', 'mɑn', 'mudər', 'm3ʃə', 'moj', 'mur', 'm^', 'mʏts', 'mew', 'mij^wə', 'mer', 'mɑk',
                     'mɑkɛlək', 'mest', 'mɪndər', 'mɔnt', 'mew', 'mɑntəl', 'mɑnt', 'məner', 'mudər', 'man', 'metər',
                     'm3lpal', 'mɔnt', 'mʏts',
                     'maxt', 'max', 'metərkɑst', 'mir', 'myr', 'mini', 'mɑrs', 'motɔr', 'matpɑk', 'mobil', 'mɑrsmɑnəcə',
                     'morkɔp', 'mɑn', 'mur', 'mokər', 'mir', 'mɪs', 'mɪsdinar', 'molə', 'mɪnar', 'mɔnstər', 'mœtər3',
                     'makəlar', 'mɔnstər', 'mɑkɛlək', 'm3n', 'm3nb^', 'moj', 'mɔs', 'mɔstərt', 'mɑn', 'mɑnə', 'mɑkɛlək',
                     'mes', 'mɑnɛlək', 'makbar', 'molənar', 'molə', 'makə', 'molə', 'mutə', 'mɑnt', 'mirə', 'mʏstɑŋ',
                     'mɑʃinə',
                     'mahoni', 'marətɑk', 'merə', 'mewə', 'mɑrjol3nə', 'mɛŋə', 'motɔr', 'm3nwɛrkər', 'mɑtros',
                     'mexaloman', 'man', 'mewɛrkənt ɛxtxənot', 'mɑʃinɪst', 'mœs', 'mɑksi-kosi', 'motɔr', 'motɔrr3bəw3s',
                     'man', 'manrakɛt', 'mobi dɪk', 'minʏskyl', 'mɑksimal', 'mozɑrt', 'm3nəvɛlt', 'marinə', 'matəx',
                     'modɛrn', 'matəxə', 'mœs', 'mɑndrel', 'mɑmut', 'mestər', 'manir', 'matəxə', 'momɛnt', 'mɪdəlmatəx',
                     'midi',
                     'man', 'm^', 'makə', 'max', 'mɔl', 'mɔnstər', 'mɔs', 'm3n', 'm3l', 'm3tər', 'mʏnt', 'mynitsi',
                     'mɪnt', 'mɪlt', 'modɛrn', 'modə', 'modɛst', 'matərijal', 'matjə', 'mɔstərt', 'makaroni', 'mɪɲo',
                     'mɪndər', 'mer', 'morel', 'mɑrsəp3n', 'mɪnt', 'mʏnt', 'mɔpərə', 'makə', 'mɪndərə', 'mɔlɛsterə',
                     'mɑrkerə', 'mimosa', 'matərijalə', 'mɑrkerɪŋ', 'mɑndar3n', 'morel', 'mɪsdinar', 'mɔpərə', 'mɛnsə',
                     'mɑndar3n',
                     'mɑnt', 'motɔr', 'motɔrfits', 'malt3t', 'medun', 'moxə', 'mynitsi', 'mɪndər', 'mɛnsə', 'medədelɪŋ',
                     'melodi', 'modijøs', 'modə', 'memorɑndʏm', 'matrexələ', 'mʏntə', 'milimetər', 'mexa', 'mɔnstryøs',
                     'mɔnstərlək', 'mɑxnet', 'molotɔv kɔktel', 'mɑrs', 'mini', 'mœs', 'mɑrmɔt', 'moxə', 'merəl',
                     'moxənth3t', 'mɑxma', 'mɛgnʏm', 'melopə', 'mevurə', 'mexan', 'medun', 'me', 'met', 'menə', 'mutə',
                     'morɛl', 'mɑn',
                     'mɑma', 'makə', 'menemə', 'manifɑktyr', 'manipylerə', 'mestər', 'mikro', 'mini', 'mɑksi',
                     'mikrofon', 'mikrobə', 'mɑstərm3nt', 'mexafon', 'mexa', 'mɑrs', 'melanom', 'mɛkərə', 'mestər',
                     'mer', 'mɑkɛlək', 'mujlək', 'møbəl', 'møbəltonzal', 'migrɛnə', 'mer', 'mizərə', 'mɪst', 'mœs',
                     'mʏs', 'mut', 'mutə', 'must', 'mɛns', 'mɛnsə', 'mɛnʃə', 'mœʃə', 'mʏsʃə', ]

    # These were the words by each participant translated to their phonetic representation.
    p1 = ['makəlar', 'mʏskɛtir', 'mɔrtir', 'mɑn', 'mew', 'mes', 'merəl', 'mew', 'mɑkɛlək', 'mujlək', 'moj', 'matəx',
          'mesopotamiə', 'mɪdəl', 'medijʏm', 'mɑxtəx', 'mɑxt', 'mɑxtsvərh^dɪŋ']
    p2 = ['minimal', 'mɑksimal', 'mermals', 'mɛldə', 'medun', 'man', 'moral', 'morel', 'mɪndər', 'mer', 'maxis',
          'maxistral', 'metodə', 'metodik', 'm3mərə', 'mezɪŋə', 'mandɑx', 'mɔnt']
    p3 = ['mœs', 'mʏs', 'mut', 'mutə', 'must', 'mɛns', 'mɛnsə', 'mɛnʃə', 'mœʃə', 'mʏsʃə', 'mɑrkt', 'mɑrkcə', 'mɑrktə',
          'mɑrktɔndərzuk', 'moxə', 'mɑx', 'maxə', 'max', 'mal', 'malə', 'malt', 'maldə', 'mœlkɔrf', 'myslirep',
          'mɑstyrbatsi', 'mɔŋxol', 'mɔŋxolcə', 'mudər', 'mudərcə', 'mudərs', 'mɛnsap', 'mɛnsapə', 'mɛnsapjə', 'mʏrf',
          'mɑxma', 'møtə']
    p4 = ['mudər', 'mɪdəl', 'mɑrko', 'median', 'metro', 'mɑpjə', 'myzikɪnstrymɛnt', 'mɑskər', 'mɑl', 'mɑn', 'mɑm',
          'matəx', 'metlɪnt', 'mɑksi-kosi', 'mɔpjə', 'mɪni', 'myrsxɪldərɪŋ', 'mʏrf', 'mʏsk', 'məner', 'mɑt']
    p5 = ['man', 'merkut', 'mœs', 'mɛs', 'makəlar', 'mɑʃɛtə', 'mɑnʃɛtknop', 'moj', 'mɑkɛlək', 'mat', 'macəsprojɛkt',
          'mɑma', 'mudər', 'mujlək', 'mɑti', 'merkut']
    p6 = ['mɑma', 'modəratɔr', 'mudərtal', 'mɑlot', 'modəm', 'morel', 'mɑrkt', 'mɪnar', 'mer', 'mɑrkerə', 'mɑrkerstɪft',
          'mɑksimal', 'metər', 'mandɑx', 'myr', 'mɪndərh3t', 'matstɑf', 'mɑksimal', 'mɔrxə', 'mutə', 'mest', 'mɑxtəlos',
          'mɑxt']
    p7 = ['mɑn', 'mɑtrɑs', 'mɑnt', 'man', 'mort', 'mi^', 'm^', 'mɑl', 'mɑt', 'mɑnk', 'mɛlvɪn', 'mew', 'mes', 'myr',
          'mœlkɔrf', 'mortzak', 'məvr^', 'məner', 'moj', 'mir', 'mincə', 'maxi', 'maxis', 'mɑtrɑs', 'mɑtros', 'mɑtr3s']
    p8 = ['mɛns', 'matsxɑp3', 'moj', 'mar', 'məner', 'mɑtʃo', 'mɑnəcə', 'makəlar', 'mɑdɑxɑskɑr', 'melopər', 'macə',
          'mɪkpʏnt', 'mɪsbɑksəl', 'mɑxnet', 'mɪnɑxtənt', 'mɑn', 'mɑma', 'mɑtros', 'mɑlot', 'mɪnpʏnt', 'mar']
    p9 = ['mɑma', 'moj', 'medis3nə', 'makəlars', 'mœzə', 'mirə', 'mɔt', 'mɑrmɑladə', 'mestər', 'mɑxtəx', 'mɑkɛlək',
          'mujlək', 'm3nwɛrkər', 'mipə', 'marɔkan', 'mɑsədonijər']
    p10 = ['mɑterial', 'mɛns', 'mɪdəl', 'mɑrsəp3n', 'manijɑk', 'mɔnʃu', 'man', 'mɪdəl', 'mar', 'ram', 'moj', 'matix',
           'mediʏm', 'mɑnir']
    p11 = ['moj', 'mɑma', 'mestər', 'metər', 'madən', 'manir', 'makər', 'melər', 'mɑstər', 'mel', 'meldrat', 'mɛnədʒər',
           'maxijər', 'meladrɛs', 'mɑnt', 'mɑndə', 'makər', 'maxər']
    p12 = ['mɑma', 'mudər', 'makəlar', 'mɑfkes', 'mesopotamiə', 'mɔŋxol', 'mɔŋxoliʏ', 'mojstə', 'moj', 'man',
           'manəsx3n', 'manlɪxt', 'mesopotamiə', 'misofoni', 'm^', 'mɔk', 'mɑpjə', 'mɑkɛlək', 'mujlək', 'mɪdəlmatəx',
           'manəsx3nə']
    p13 = ['moj', 'mujlək', 'mɪndərwardəx', 'mɪndər', 'moxələk', 'mɪsxin', 'mar', 'moxə', 'mɑx', 'mɔx', 'mɔxt', 'mɔxtə',
           'moxələk', 'mustə', 'makə', 'maktə', 'mak', 'makt', 'mɪsxin']
    p14 = ['mɑrko', 'mora', 'moj', 'mɑn', 'mɑnələk', 'mujzam', 'mu', 'muh3t', 'mat', 'matstaf', 'man', 'myr', 'myrə',
           'm3n', 'm3', 'mir', 'mujzam', 'memoriɑm', 'mɛnsə', 'mɛns', 'mɛnsh3t']
    p15 = ['mɑrko', 'mɑrkʏs', 'mes', 'metejorit', 'matwɛrk', 'mudər', 'mɪsplatst', 'mexant', 'metejolox', 'medikʏs',
           'mɪdɑx', 'mɪdɑxdel', 'mustœn', 'musplɑnt', 'mɑzda', 'mɛrcedəs', 'mas', 'mok']
    p16 = ['mɔl', 'mɔt', 'mar', 'mudər', 'mɑma', 'max', 'mirəetər', 'mizoxinɪst', 'mizoxini', 'myr', 'mɑn', 'mɑxtəx',
           'mip', 'mɑkɛlək', 'mujlək', 'mer', 'mɪndər', 'maksimʏm', 'minimʏm', 'molə', 'molənar', 'mel', 'mel', 'mɛs',
           'mɔs', 'mɛkərə', 'mestər', 'myrvʏlər']
    p17 = ['m3tər', 'mat', 'mɑʃinɪst', 'metlɪnt', 'metlɑt', 'max', 'mɔnthɑrmonika', 'mudər', 'ma', 'mœs', 'maxɪnh^t',
           'mɔndəlɪŋ', 'mɑstər', 'moj', 'mɛlk', 'mɑn', 'mandɑx', 'mel', 'm3ʃə', 'mɑnt', 'mortwapə', 'mort', 'mɛs',
           'mɑndolinə']
    p18 = ['mɪst', 'minimal', 'mɑksimal', 'mudər', 'mɑma', 'mʏs', 'mɔt', 'mɑx', 'me', 'medijʏm', 'mir', 'mɪkə', 'mɪsə',
           'mɛt', 'mʏts', 'melevə', 'mar', 'mɪnstəns']
    p19 = ['matrɪks', 'matərijal', 'mɑma', 'mesopotamiə', 'mɑn', 'makrel', 'maxistral', 'maxi', 'mʏskylɛr',
           'mɑnəcəspʏtər', 'mɔk', 'mɔka', 'mytɑnt', 'mytɛla', 'mɑstʏrberə', 'mɑf', 'mɑfɛrt', 'mɑfkes', 'mɑzəltɔf',
           'mɔl', 'mɔlə', 'mɔsəlmɑn', 'mɔsəls', 'mɑx', 'mɑskər', 'mɔf']
    p20 = ['mɑst', 'mɑjs', 'mani', 'molə', 'mel', 'mel', 'maxis', 'maxijər', 'mɑŋgo', 'mɔnt', 'mɑskər', 'mɑt', 'mokər',
           'mɑn', 'merəl', 'mɑl', 'mɑf']
    p21 = ['mɑnt', 'motər', 'motorik', 'mɛmori', 'mɔnt', 'mandɑx', 'myrə', 'modɛl', 'man', 'mɔrxə']
    p22 = ['mɔdər', 'm3n', 'moj', 'mɑkɛlək', 'mujlək', 'mexant', 'medɛŋkənt', 'mestɑl', 'mest', 'moxələk', 'mezɪŋə']
    p23 = ['mɪdəlbar', 'moj', 'mɑt', 'mɛlk', 'medijʏm', 'mɔnstər', 'møbəls', 'møbəlmakər', 'møbəlxəbrœkər', 'mɛst',
           'mɪn', 'mɪnzam', 'maxər', 'mɑl', 'mɑk', 'man', 'me', 'mɔrxə', 'mɪdɑx', 'mexrujə', 'mexan']
    p24 = ['mudər', 'mexan', 'moj', 'mɑndrel', 'makə']
    p25 = ['mœs', 'mas', 'mexafon', 'mudər', 'mɑma', 'mɑriakakjə', 'mɔnt', 'mɔnthuk', 'mɔnthixijənɪstə', 'myr', 'mɔp',
           'mɔpshɔnt', 'mokər', 'm3t', 'm3dəkamər', 'm3ʃəskledɪŋ', 'm3ʃə', 'mɪnt', 'mir', 'mini', 'minirɔk', 'mɪn',
           'minʏskyl', 'minimʏm', 'maksimʏm']
    p26 = ['mestər', 'mudər', 'merəl', 'mew', 'mɑrxrit', 'mɪdəllɑntsə ze', 'mɪdə-ostə', 'mɑʃinə', 'maxaz3n', 'mestər',
           'məvr^', 'mat', 'mu', 'mɪsələk', 'maxər', 'moj']
    p27 = ['man', 'mɪdəl', 'metər', 'maxər', 'moj', 'mɪdəvutsbencəs', 'mɑrtər', 'mɑrxarinə', 'mɑntəl', 'mɪndər', 'mer',
           'mɑndar3n', 'mɛrxp3pjə', 'mɛrxəlɑnt']
    p28 = ['man', 'mɔnt', 'mɔstərt', 'medədoxə', 'medəl3də', 'mujzam', 'mujlək', 'mɛns', 'metər', 'maxər', 'majo',
           'metronom', 'mɛlk', 'mɑrs', 'mel', 'mexa', 'mɑn', 'mudər', 'm3ʃə', 'moj']
    p29 = ['myr', 'm^', 'mʏts', 'mew', 'mij^wə', 'mer', 'mɑk', 'mɑkɛlək', 'mest', 'mɪndər', 'mɔnt', 'mew', 'mɑntəl',
           'mɑnt', 'məner']
    p30 = ['mudər', 'man', 'metər', 'm3lpal', 'mɔnt', 'mʏts', 'maxt', 'max', 'metərkɑst', 'mir', 'myr', 'mini']
    p31 = ['mɑrs', 'motɔr', 'matpɑk', 'mobil', 'mɑrsmɑnəcə', 'morkɔp', 'mɑn', 'mur', 'mokər', 'mir', 'mɪs', 'mɪsdinar']
    p32 = ['molə', 'mɪnar', 'mɔnstər', 'mœtər3', 'makəlar', 'mɔnstər', 'mɑkɛlək', 'm3n', 'm3nb^', 'moj', 'mɔs',
           'mɔstərt', 'mɑn', 'mɑnə', 'mɑkɛlək', 'mes', 'mɑnɛlək', 'makbar', 'molənar', 'molə']
    p33 = ['makə', 'molə', 'mutə', 'mɑnt', 'mirə', 'mʏstɑŋ', 'mɑʃinə', 'mahoni', 'marətɑk', 'merə', 'mewə', 'mɑrjol3nə',
           'mɛŋə', 'motɔr']
    p34 = ['m3nwɛrkər', 'mɑtros', 'mexaloman', 'man', 'mewɛrkənt ɛxtxənot', 'mɑʃinɪst', 'mœs', 'mɑksi-kosi', 'motɔr',
           'motɔrr3bəw3s', 'man', 'manrakɛt', 'mobi dɪk', 'minʏskyl', 'mɑksimal', 'mozɑrt', 'm3nəvɛlt']
    p35 = ['marinə', 'matəx', 'modɛrn', 'matəxə', 'mœs', 'mɑndrel', 'mɑmut', 'mestər', 'manir', 'matəxə', 'momɛnt']
    p36 = ['mɪdəlmatəx', 'midi', 'man', 'm^', 'makə', 'max', 'mɔl', 'mɔnstər', 'mɔs', 'm3n', 'm3l', 'm3tər', 'mʏnt',
           'mynitsi', 'mɪnt', 'mɪlt', 'modɛrn', 'modə', 'modɛst', 'matərijal', 'matjə']
    p37 = ['mɔstərt', 'makaroni', 'mɪɲo', 'mɪndər', 'mer', 'morel', 'mɑrsəp3n', 'mɪnt', 'mʏnt', 'mɔpərə', 'makə',
           'mɪndərə', 'mɔlɛsterə', 'mɑrkerə', 'mimosa', 'matərijalə', 'mɑrkerɪŋ', 'mɑndar3n', 'morel', 'mɪsdinar',
           'mɔpərə', 'mɛnsə']
    p38 = ['mɑndar3n', 'mɑnt', 'motɔr', 'motɔrfits', 'malt3t', 'medun', 'moxə', 'mynitsi', 'mɪndər', 'mɛnsə',
           'medədelɪŋ', 'melodi', 'modijøs', 'modə', 'memorɑndʏm', 'matrexələ', 'mʏntə', 'milimetər', 'mexa',
           'mɔnstryøs', 'mɔnstərlək']
    p39 = ['mɑxnet', 'molotɔv kɔktel', 'mɑrs', 'mini', 'mœs', 'mɑrmɔt', 'moxə', 'merəl', 'moxənth3t', 'mɑxma', 'mɛgnʏm',
           'melopə', 'mevurə', 'mexan', 'medun', 'me', 'met', 'menə', 'mutə', 'morɛl', 'mɑn', 'mɑma']
    p40 = ['makə', 'menemə', 'manifɑktyr', 'manipylerə', 'mestər', 'mikro', 'mini', 'mɑksi']
    p41 = ['mikrofon', 'mikrobə', 'mɑstərm3nt', 'mexafon', 'mexa', 'mɑrs', 'melanom', 'mɛkərə', 'mestər', 'mer',
           'mɑkɛlək', 'mujlək', 'møbəl', 'møbəltonzal', 'migrɛnə', 'mer', 'mizərə', 'mɪst']

    # calculate_threshold(all_responses)

    input = p1 # words generated by participant
    clusters = make_clusters(input)
    print(clusters) #clusters made by PWLD clustering system

    # calculation of MEAN_VOWEL_COST and MEAN_CONSONANT_COST was done by the following. Running the code now will result
    # in a cost of 0.49 for both the vowels and the consonants, since the scaling factor is applied

    # vowels = ['i', 'y', 'e', 'ø', 'o', 'u', 'a', 'ɪ', 'ʏ', 'ɔ', 'ɛ', 'ɑ', 'ə', '3', 'œ', '^']
    # total_vow = 0
    # count_vow = 0
    # for i in range (0, len(vowels)):
    #     next_letter = i + 1
    #     for j in range(next_letter, len(vowels)-1):
    #         total_vow += vowel_cost(vowels[i], vowels[j])
    #         count_vow += 1
    #         #print(vowels[i], "&", vowels[j], ": ", vowel_cost(vowels[i], vowels[j]))
    #         #print(vowel_cost(vowels[i], vowels[j]))
    # print(total_vow/count_vow)
    #
    # consonants = ['b', 'p', 'd', 't', 'c', 'g', 'k', 'v', 'f', 'z', 's', 'ʒ', 'ʃ', 'x', 'r', 'l', 'w', 'j', 'h', 'm', 'n', 'ɲ', 'ŋ']
    # total_con = 0
    # count_con = 0
    # for i in range (0, len(consonants)):
    #     next_letter = i + 1
    #     for j in range(next_letter, len(consonants)-1):
    #         #print(consonants[i], "&", consonants[j], ": ",consonant_cost(consonants[i], consonants[j]))
    #         total_con += consonant_cost(consonants[i], consonants[j])
    #         count_con += 1
    #         #print(consonant_cost(consonants[i], consonants[j]))
    # print(total_con/count_con)
