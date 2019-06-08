from nltk.corpus import wordnet as wn
from collections import deque
from threading import Semaphore
import random


# LOCK = Semaphore(1)

def is_hypernym(sem_class, term):
    hypernyms = deque()
    hypernyms.append(term)
    while len(hypernyms) > 0:
        synset = hypernyms.popleft()
        if synset in sem_class:
            return True
        for hyper in synset.hypernyms():
            hypernyms.append(hyper)
    return False


PERSON = set(wn.synsets('person'))
PERSON_COMBATANT = set(wn.synsets('combatant'))
PERSON_MERCENARY = set(wn.synsets('mercenary'))
PERSON_SNIPER = set(wn.synsets('sniper'))
PERSON_FAN = set(wn.synsets('fan'))
PERSON_POLICE = set(wn.synsets('police'))
PERSON_POLITICIAN = set(wn.synsets('politician'))
PERSON_AMBASSADOR = set(wn.synsets('ambassador'))
PERSON_FIREFIGHTER = set(wn.synsets('firefighter'))
PERSON_JOURNALIST = set(wn.synsets('journalist'))
PERSON_MINISTER = set(wn.synsets('minister'))
PERSON_PARAMEDIC = set(wn.synsets('paramedic'))
PERSON_SCIENTIST = set(wn.synsets('scientist'))
PERSON_SPOKEPERSON = set(wn.synsets('spokeperson'))
PERSON_SPY = set(wn.synsets('spy'))
PERSON_PROTESTER = set(wn.synsets('protester'))

ANIMAL = set(wn.synsets('animal'))

ORGANIZATION = set(wn.synsets('organization') + wn.synsets('military') + wn.synsets('group'))
ORGANIZATION_GOVERNMENT = set(wn.synsets('government'))
ORGANIZATION_POLITICAL = set(wn.synsets('party') + wn.synsets('court'))
ORGANIZATION_MILITARY = wn.synsets('military')

LOCATION = set(wn.synsets('location'))
GPE = set(wn.synsets('administrative_district'))
FACILITY = set(wn.synsets('facility') + wn.synsets('structure'))
TIME = set(wn.synsets('time') + wn.synsets('date') + wn.synsets('time_period'))
NUMBER = set(wn.synsets('number'))
QUANTITY = set(wn.synsets('definite_quantity'))
MONEY = set(wn.synsets('money'))
PERCENT = set(wn.synsets('percent'))

VEHICLE = set(wn.synsets('vehicle'))
VEHICLE_AIRCRAFT = set(wn.synsets('aircraft'))
VEHICLE_ROCKET = set(wn.synsets('rocket'))
VEHICLE_WATERCRAFT = set(wn.synsets('watercraft'))
VEHICLE_BUS = set(wn.synsets('bus'))
VEHICLE_CAR = set(wn.synsets('car'))
VEHICLE_TRAIN = set(wn.synsets('train'))
VEHICLE_TRUCK = set(wn.synsets('truck'))

WEAPON = set(wn.synsets('weapon') + wn.synsets('weaponry') + wn.synsets('arms') + wn.synsets('implements_of_war') + wn.synsets('weapons_system') + wn.synsets('munition'))

CRIME = set(wn.synsets('crime'))

def get_semantic_class(lemma):
    # rid = random.randint(0, 100)
    # print('wait!%d' % rid)
    # LOCK.acquire()
    # print('get!%d' % rid)

    result = 'UNKNOWN'
    try:
        term = wn.synsets(lemma)
    except:
        print('**' + lemma)
        term = None

    if not term:
        # LOCK.release()
        # print('release!%d' % rid)
        return result

    term = term[0]
    
    if is_hypernym(PERSON, term):
        result = 'PER'
    elif is_hypernym(ORGANIZATION, term):
        result = 'ORG'
    elif is_hypernym(GPE, term):
        result = 'GPE'
    elif is_hypernym(FACILITY, term):
        result = 'FAC'
    elif is_hypernym(LOCATION, term):
        result = 'LOC'
    elif is_hypernym(WEAPON, term):
        result = 'WEA'
    elif is_hypernym(VEHICLE, term):
        result = 'VEH'

    # LOCK.release()
    # print('release!%d' % rid)
    
    return result

def get_semantic_class_with_subtype(lemma):
    type = 'UNKNOWN'
    subtype, subsubtype = 'n/a', 'n/a'

    term = wn.synsets(lemma)
    if not term:
        return type, subtype, subsubtype

    term = term[0]

    if is_hypernym(PERSON, term):
        type = 'PER'
        if is_hypernym(PERSON_COMBATANT, term):
            subtype = 'combatant'
            if is_hypernym(PERSON_MERCENARY, term):
                subsubtype = 'mercenary'
            elif is_hypernym(PERSON_SNIPER, term):
                subsubtype = 'sniper'
        elif is_hypernym(PERSON_FAN, term):
            subtype, subsubtype = 'fan', 'na'
        elif is_hypernym(PERSON_POLICE, term):
            subtype, subsubtype = 'police', 'na'
        elif is_hypernym(PERSON_POLITICIAN, term):
            subtype, subsubtype = 'politician', 'na'
        elif is_hypernym(PERSON_PROTESTER, term):
            subtype, subsubtype = 'protester', 'na'
        elif is_hypernym(PERSON_AMBASSADOR, term):
            subtype, subsubtype = 'professional_position', 'ambassador'
        elif is_hypernym(PERSON_FIREFIGHTER, term):
            subtype, subsubtype = 'professional_position', 'firefighter'
        elif is_hypernym(PERSON_JOURNALIST, term):
            subtype, subsubtype = 'professional_position', 'journalist'
        elif is_hypernym(PERSON_MINISTER, term):
            subtype, subsubtype = 'professional_position', 'minister'
        elif is_hypernym(PERSON_PARAMEDIC, term):
            subtype, subsubtype = 'professional_position', 'paramedic'
        elif is_hypernym(PERSON_SCIENTIST, term):
            subtype, subsubtype = 'professional_position', 'scientist'
        elif is_hypernym(PERSON_SPOKEPERSON, term):
            subtype, subsubtype = 'professional_position', 'spokeperson'
        elif is_hypernym(PERSON_SPY, term):
            subtype, subsubtype = 'professional_position', 'spy'

    elif is_hypernym(ORGANIZATION, term):
        type = 'ORG'
        if is_hypernym(ORGANIZATION_GOVERNMENT, term):
            subtype, subsubtype = 'government_organization', 'na'
        elif is_hypernym(ORGANIZATION_POLITICAL, term):
            subtype, subsubtype = 'political_organization', 'na'
        elif is_hypernym(ORGANIZATION_MILITARY, term):
            subtype, subsubtype = 'military_organization', 'na'

    elif is_hypernym(GPE, term):
        type = 'GPE'

    elif is_hypernym(FACILITY, term):
        type = 'FAC'

    elif is_hypernym(LOCATION, term):
        type = 'LOC'

    elif is_hypernym(WEAPON, term):
        type = 'WEA'

    elif is_hypernym(VEHICLE, term):
        type = 'VEH'
        if is_hypernym(VEHICLE_AIRCRAFT, term):
            subtype, subsubtype = 'aircraft', 'na'
        elif is_hypernym(VEHICLE_ROCKET, term):
            subtype, subsubtype = 'rocket', 'na'
        elif is_hypernym(VEHICLE_WATERCRAFT, term):
            subtype, subsubtype = 'watercraft', 'na'
        elif is_hypernym(VEHICLE_BUS, term):
            subtype, subsubtype = 'wheeled_vehicle', 'bus'
        elif is_hypernym(VEHICLE_CAR, term):
            subtype, subsubtype = 'wheeled_vehicle', 'car'
        elif is_hypernym(VEHICLE_TRAIN, term):
            subtype, subsubtype = 'wheeled_vehicle', 'train'
        elif is_hypernym(VEHICLE_TRUCK, term):
            subtype, subsubtype = 'wheeled_vehicle', 'truck'

    elif is_hypernym(CRIME, term):
        type = 'CRM'

    return type, subtype, subsubtype