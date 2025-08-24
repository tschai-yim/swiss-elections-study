from data.attribute import SEX_ATTR, AGE_ATTR

AGE_WEIGHT = 'weight_age'
TOTAL_WEIGHT = 'weighttot'  # Existing column name
RESPONDENT_ID = 'userid'

SELECT_COLUMN_NAMES = {
    'year': "year",
    'userid': "interview/respondent number all",
    'useridpy': "interview number per year",
    'sex': "sex",
    'age': "age",
    'maritals': "marital status",
    'educ': "education",
    'income_sfr': "income in thousand SFR",
    'income': "income in quintiles",
    'income_hh': "income in quintiles (adjusted for household size)",
    'income2': "income compared to average household",
    'income3': "does R get along with income",
    'religion': "religious denomination",
    'churchg': "church attendance",
    'sg1': "linguistic region",
    'sg2': "canton of residence",
    'sg3': "canton in which R has the right to vote",
    'sg4': "canton in which R had the right to vote 4 years ago",
    'sg5': "postal zip code",
    'sg6': "community number BfS",
    'sg7a': "inhabitants (community) in thousand",
    'sg7b': "inhabitants (community resp. agglomeration) in cat",
    'sg9': "city-countryside",
    'sg10a': "resident in community/canton in years",
    'sg10b': "resident in community/canton in 5 cat",
    'sg11': "canton of residence in childhood",
    'sg12': "Swiss citizen since birth",
    'sg13': "primary level of geographic identity",
    'sh1': "household: number of persons",
    'sh2': "household: children",
    'sh2a': "household: no. of children up to 7 years",
    'sh2b': "household: no. of children from 7-12 years",
    'sh2c': "household: no. of children from 13y to majority",
    'sh3': "household: partner",
    'sh4': "household: main earner",
    'educp': "household: partner's education",
    'educh': "household: education main earner",
    'sc1': "social class: work situation",
    'sc1a': "social class: former work situation",
    'sc1b': "social class: if unemployed: worked before",
    'sc1c': "social class: if not gainfully employed: gainfully worked before",
    'sc2_75insee': "(ex-)occupation INSEE",
    'sc2g_71': "(ex-)occupation: social grade, INSEE",
    'sc2_75bit': "(ex-)occupation ISCO-68",
    'sc2_75src': "(ex-)occupation SRC",
    'sc2_79': "(ex-)occupation",
    'sc2_87': "(ex-)occupation",
    'sc2g_87': "(ex-)occupation, groups",
    'sc2_91': "(ex-)occupation",
    'sc2_bfs': "(ex-)profession BfS",
    'sc2_isco88': "(ex-)profession isco88",
    'sc2_isco08': "(ex-)profession isco08",
    'sc3': "social class: branch of activity",
    'sc4': "social class: employment status",
    'sc5': "social class: if employee: sector",
    'sc6a': "social class: if senior employee: no. of subordinates",
    'sc6b': "social class: if self-employer: no. of subordinates",
    'sc7a': "social class schema respondent (Kriesi_new)",
    'sc7b': "social class schema respondent (Kriesi_old)",
    'sc7c': "social class schema respondent (Oesch)",
    'scp1': "social class partner: occupation",
    'scp1a': "social class partner: last occupation",
    'scp2_bfs': "social class partner: (ex-)profession BfS",
    'scp2_isco88': "social class partner: (ex-)profession isco88",
    'scp2_isco08': "social class partner: (ex-)profession isco08",
    'scp4': "social class partner: employment status",
    'scp5': "social class partner: if employee: sector",
    'scp7a': "social class schema, partner (Kriesi_new)",
    'scp7c': "social class schema, partner (Oesch)",
    'sch1': "social class household: main earner's occupation",
    'sch1a': "social class household: main earner's last occupation",
    'sch1b': "social class household: if main earner without work: work before",
    'sch2_75insee': "social class household: main earner's (ex-)profession INSEE",
    'sch2g_71': "social class household: main earner's (ex-)profession: social grade, INSEE",
    'sch2_75bit': "social class household: main earner's (ex-)profession ISCO-68",
    'sch2_75src': "social class household: main earner's (ex-)profession SRC",
    'sch2_79': "social class household: main earner's (ex-)profession",
    'sch2_91': "social class household: main earner's (ex-)profession",
    'sch2_bfs': "social class household: main earner's (ex-)profession BfS",
    'sch2_isco88': "social class household: main earner's (ex-)profession isco88",
    'sch2_isco08': "social class household: main earner's (ex-)profession isco08",
    'sch3': "social class household: main earner's branch of activity",
    'sch4': "social class household: main earner's employment status",
    'sch5': "social class household: if main earner is employee: sector",
    'sch6a': "social class household: if main earner has supervision-function: no. of subordinates",
    'sch6b': "social class household: if main earner is self-employed: no. of subordinates",
    'sch7a': "social class schema household (Kriesi_new)",
    'sch7c': "social class schema household (Oesch)",
    'sch7r': "social class schema household (Kriesi_old)",
    'class8': "Class position (Oesch) based on R's, P's or M-E's class, 8 classes",
    'scc1': "social class childhood: financial situation parents",
    'scc3_75insee': "social class childhood: father's occupation INSEE",
    'scc3g_71': "social class childhood: father's occupation: social grade",
    'scc3_75bit': "social class childhood: father's occupation ISCO-68",
    'scc3_75src': "social class childhood: father's occupation SRC",
    'ses1': "economic situation: rent or property",
    'ses2': "economic situation: property car",
    'ses3': "economic situation: property telephone",
    'pi1': "political interest",
    'pi2': "political interest: election (campaign)",
    'pi3': "political interest: subjective importance of national elections",
    'pi4': "political interest: degree of information about the election",
    'pi5': "political interest: importance direct legislation vs national parliamentary elections",
    'pp1': "political participation: freq. political discussions",
    'pp2': "political participation: freq. political discussions about elections",
    'pp3': "political participation: freq. convincing others",
    'pp4': "political participation: freq. convincing others in election campaign",
    'pp5': "political participation: attending political meetings",
    'pp6': "political participation: attending electoral meetings/events",
    'pp7': "political participation: contact with politicians",
    'pp8': "political participation: donated money to organizations in last 5 years",
    'pp9': "political participation: active in political party",
    'pp10': "political participation: active for a party/candidate in campaign",
    'pp11a': "political participation: political actions of R at local level, 1st mention",
    'pp11b': "political participation: political actions of R at local level, 2nd mention",
    'pp12a': "political participation: freq. participation elections/votes at local level",
    'pp12b': "political participation: freq. participation elections/votes at cantonal level",
    'pp12c': "political participation: freq. participation elections/votes at national level",
    'pp13': "political participation: approve/disapprove boykotts",
    'pp14': "political participation: approve/disapprove (lawful) demonstration",
    'pp15': "political participation: approve/disapprove strikes",
    'pp16': "political participation: approve/disapprove painting slogans on the wall",
    'pp17': "political participation: signed a petition",
    'pp18': "political participation: helped with a referendum/initiative",
    'pp19': "political participation: joined a citizen's action/initiative",
    'pp20': "political participation: would join boykott",
    'pp21a': "political participation: participated in demonstration",
    'pp21b': "political participation: would participate in demonstration",
    'pp22': "political participation: would join strike",
    'pp23': "political participation: would paint slogans on wall",
    'sp1': "social participation: collective community work",
    'spm1': "social participation: membership trade union",
    'spm2': "social participation: membership employees' organization",
    'spm3': "social participation: membership employers' association",
    'spm4': "social participation: membership professionals' association",
    'spm5': "social participation: membership farmers' organization",
    'spm6': "social participation: membership in political party",
    'spm6a': "if member of political party: active or not?",
    'spm7': "social participation: membership women's organization",
    'spm8': "social participation: membership consumerism organization",
    'spm9': "social participation: membership environmental organization",
    'spm10': "social participation: membership automobile club",
    'spm11': "social participation: membership local association",
    'spm12': "social participation: membership religious group/organization",
    'spm13': "social participation: membership cultural association",
    'spm14': "social participation: membership sport club",
    'spm25': "social participation: membership human rights organization",
    'spm26': "social participation: membership animal rights organization",
    'spm27': "social participation: membership academic organization",
    'spm28': "social participation: membership other organizations",
    'spm29': "social participation: no membership",
    'lr1': "left right self-positioning",
    'lr2': "left right position: CVP/PDC",
    'lr3': "left right position: FDP/PRD",
    'lr4': "left right position: SPS/PSS",
    'lr5': "left right position: SVP/UDC (BGB/PAB)",
    'lr6': "left right position: Grüne/éco",
    'lr7': "left right position: LPS/PLS",
    'lr8': "left right position: LdU/AdI",
    'lr9': "left right position: Lega",
    'lr10': "left right position: EVP/PEP",
    'lr11': "left right position: FPS/PSL",
    'lr12': "left right position: PdA/PdT",
    'lr13': "left right position: MCG",
    'lr14': "left right position: GLP/PVL",
    'lr15': "left right position: BDP/PBD",
    'pm1a': "inglehart battery: 4q, 1st choice",
    'pm1b': "inglehart battery: 4q, 2nd choice",
    'pm2a': "inglehart battery: 6q, 1st choice",
    'pm2b': "inglehart battery: 6q, 2nd choice",
    'pm3': "index of postmaterialism",
    'pk1': "pol knowledge: number of parties in federal council?",
    'pk2': "pol knowledge: name of the president of the confederation?",
    'pk3': "pol knowledge: required number of signatures for federal initiative?",
    'pk4': "pol knowledge: how many nat. council members are from r's canton?",
    'pk5': "pol knowledge: party with most seats in National Council?",
    'pk6': "knowledge scale, out of 4 questions",
    'vp1': "voter's participation: federal elections",
    'vp2': "voter's participation: federal elections 4 years ago",
    'vp3': "voter's participation: last local/cantonal elections",
    'vp4': "voter's participation: reasons: interest v. duty",
    'vp5': "voter's participation: reasons",
    'vnp1': "voter's non-participation: reasons",
    'vnp2': "voter's non-participation: reasons",
    'vnp3a': "voter's non-participation: couldn't make up his mind",
    'vnp3b': "voter's non-participation: no interest in politics",
    'vnp3c': "voter's non-participation: too complicated",
    'vnp3d': "voter's non-participation: no eligible candidate/party",
    'vnp3e': "voter's non-participation: favorites had no chance",
    'vnp3f': "voter's non-participation: not worth to go voting",
    'vnp3g': "voter's non-participation: doesn't know the candidates",
    'vnp3h': "voter's non-participation: couldn't take part (absent, ill, etc.)",
    'vnp3i': "voter's non-participation: no influence on government composition",
    'vnp3j': "voter's non-participation: elections don't change anything",
    'vnp3k': "voter's non-participation: more influence through popular votes",
    'vdn1b': "voting decision nc: 1st vote, BfS parties",
    'vdn2b': "voting decision nc: 2nd vote, BfS parties",
    'vdn3b': "voting decision nc: 3rd vote, BfS parties",
    'vdn6': "voting decision nc: specific list",
    'hvdn1b': "hypothetic voting decision nc, BfS parties",
    'hvdn2b': "voting decision nc: real or hypothetical, BfS parties",
    'vdr1b': "voting decision nc: recall 4 years ago, BfS parties",
    'vds1b': "voting decision cs, first seat - BfS parties",
    'vds2b': "voting decision cs, second seat - BfS parties",
    'hvds1b': "hypothetic voting decision cs, first seat, BfS parties",
    'hvds2b': "hypothetic voting decision cs, second seat, BfS parties",
    'vdo1b': "voting decision: last cantonal/local elections, BfS parties",
    'ml1': "modification list",
    'ml2': "modification list: strike candidates",
    'ml3': "modification list: double candidates",
    'ml4': "modification list: candidates from other lists",
    'mvd1': "mode of voting decision: time of party decision",
    'mvd2': "mode of voting decision: time of decision not to vote",
    'mvd3': "mode of voting decision: way of participation",
    'mvd4': "mode of voting decision: time if participation by mail",
    'avd2a': "R's reason for voting candidate(s), 1st mention",
    'avd2b': "R's reason for voting candidate(s), 2nd mention",
    'avd2c': "R's reason for voting candidate(s), 3rd mention",
    'avd9': "voting decision: gender composition of list",
    'avd10': "voting decision: difficulty to form an opinion",
    'pid1': "party attachment (yes/no)",
    'pid2b': "party identification, BfS parties",
    'pid3': "party id.: closer to one party if no party id.",
    'pid4b': "party id.: closer to a party, BfS parties",
    'pid5': "party identification: strength",
    'pid6b': "party identification father, BfS parties",
    'pid7b': "party identification mother, BfS parties",
    'pid8': "party id: always voted for the same party",
    'sypa1': "sympathy parties: FDP/PRD",
    'sypa2': "sympathy parties: CVP/PDC",
    'sypa3': "sympathy parties: SPS/PSS",
    'sypa4': "sympathy parties: SVP/UDC",
    'sypa5': "sympathy parties: LPS/PLS",
    'sypa6': "sympathy parties: LdU/AdI",
    'sypa7': "sympathy parties: EVP/PEP",
    'sypa8': "sympathy parties: PdA/PdT",
    'sypa9': "sympathy parties: GPS/PES",
    'sypa10': "sympathy parties: NA/AN",
    'sypa11': "sympathy parties: FPS/PLS",
    'sypa12': "sympathy parties: Lega",
    'sypa14': "sympathy parties: GLP/PVL",
    'sypa15': "sympathy parties: BDP/PBD",
    'ptv1': "probability to vote: FDP/PRD",
    'ptv2': "probability to vote: CVP/PDC",
    'ptv3': "probability to vote: SPS/PSS",
    'ptv4': "probability to vote: SVP/UDC",
    'ptv5': "probability to vote: GPS/PES",
    'ptv6': "probability to vote: GLP/PVL",
    'ptv7': "probability to vote: BDP/PBD",
    'ptv8': "probability to vote: Lega",
    'ptv9': "probability to vote: EVP/PEP",
    'ptv10': "probability to vote: LPS/PLS",
    'ptv11': "probability to vote: MCG",
    'sypep1': "sympathy personalities according to parties: SP/PS",
    'sypep2': "sympathy personalities according to parties: FDP/PRD",
    'sypep3': "sympathy personalities according to parties: CVP/PDC",
    'sypep4': "sympathy personalities according to parties: SVP/UDC",
    'syg1': "sympathy groups: women's organizations",
    'syg2': "sympathy groups: environmental organizations",
    'trust1': "trust: federal council",
    'trust2': "trust: national parliament",
    'trust3': "trust: cantonal authorities",
    'trust4': "trust: local authorities",
    'trust5': "trust: national political parties",
    'trust6': "trust: justice/courts",
    'trust7': "trust: police",
    'peff1': "efficacy: government does what it wants",
    'peff2': "efficacy: vote as only possibility to influence politics",
    'peff3': "efficacy: politics is so complicated",
    'peff4': "efficacy: government/parties don't care about people like me",
    'peff5': "efficacy: politicians know what people think",
    'peff6': "efficacy: political parties only care about votes",
    'peff7': "efficacy: elections make a difference",
    'peff8': "efficacy: who people vote for makes a difference",
    'eps1': "evaluation: political system/democracy",
    'eps2': "evaluation: special interests of parliamentarians",
    'mip1': "most important problem, 1st mention",
    'mip2': "most important problem, 2nd mention",
    'ii3': "issue importance: law and order, safe from crimes",
    'ii5': "issue importance: equality men & women",
    'ii7': "issue importance: habitation/housing",
    'ip1': "issue position: lower taxes",
    'ip2': "issue position: taxes on high income",
    'ip3': "issue position: safeguarding of jobs",
    'ip4': "issue position: distribution of salary",
    'ip5': "issue position: state v. market",
    'ip6': "issue position: joining the EU/EC",
    'ip7': "issue position: joining the UN",
    'ip8': "issue position: anti-foreigner-initiatives",
    'ip9': "issue position: chances for foreigners",
    'ip10': "issue position: tradition",
    'ip11': "issue position: Swiss army",
    'ip12': "issue position: law&order",
    'ip13': "issue position: social expenditure",
    'ip14': "issue position: environmental protection v. economic growth",
    'ip15': "issue position: nuclear enery",
    'np1': "national pride: how proud is R of Switzerland?",
    'np2': "national pride: is recent critique on Swiss role during WWII justified?",
    'att1': "attachment: to Europe",
    'att2': "attachment: to the community",
    'att3': "attachment: to the canton",
    'att4': "attachment: to the linguistic region",
    'att5': "attachment: to the country (Switzerland)",
    'ee1': "how does R evaluate present state of economy in Switzerland?",
    'ee2': "how does R evaluate present state of economy as compared to 12 months ago?",
    'ep1': "most competent party: asylum/foreigner policies",
    'ep2': "most competent party: equality of men and women",
    'ep3': "most competent party: asylum policy",
    'ep4': "most competent party: environment",
    'ep5': "most competent party: Europe",
    'med1': "media use: daily newspaper",
    'med2': "media use (news): newspaper",
    'med3': "media use (news): TV",
    'med4': "media use (news): radio",
    'med5': "media use: ownership TV",
    'ci1': "campaign information: TV",
    'ci2': "campaign information: radio",
    'ci3': "campaign information: newspapers",
    'ci4': "campaign information: ads in newspapers",
    'ci5': "campaign information: ads in the streets",
    'ci6': "campaign information: parties' leaflets",
    'ci7': "campaign information: web pages",
    'ci8': "campaign information: parties' stands",
    'ci9': "campaign information: political events of the parties",
    'ci10': "campaign information: divers parties' information",
    'ci11': "campaign information: giveaways",
    'ci12': "campaign information: recommendations/slogans (parties)",
    'ci13': "campaign information: recommendations (not parties)",
    'ci14': "campaign information: conversation with candidate",
    'ici1': "importance of campaign information: newspaper",
    'ici2': "importance of campaign information: ads",
    'ici3': "importance of campaign information: leaflets",
    'ici4': "importance of campaign information: tv/radio",
    'slogan1': "assign slogan to party: FDP/PRD",
    'slogan2': "assign slogan to party: CVP/PDC",
    'slogan3': "assign slogan to party: SPS/PSS",
    'slogan4': "assign slogan to party: SVP/UDC",
    'slogan5': "assign slogan to party: GPS/PES",
    'slogan': "slogans correctly assigned to parties",
    'language': "language interview",
    'intinf1': "info interview: day of the interview",
    'intinf2': "info interview: month of the interview",
    'intinf3': "info interview: year of the interview",
    'intinf4': "info interview: duration of the interview",
    'intinf5': "info interview: presence of third person during the interview",
    'intinf6': "info interview: if 3rd person present: expression of opinion",
    'intinf7': "info interview: interest respondent on interview, judgement interviewer",
    'weightc': "weight: design weight to compensate for cantonal oversampling",
    'weightst': "weight: turnout bias (incl. design weight for 95-19)",
    'weightp': "weight: party choice (incl. design weight for 95-19)",
    'weighttot': "total weight: weight canton * turnout * party choice",
}

# Groups of columns for easier selection (with unnecessary columns left out)
SELECTS_DEMOGRAPHIC_BASICS_COLUMNS = [
    SEX_ATTR, AGE_ATTR,
    'maritals', 'educ', 'income', 'income_hh', 'income3', 'religion', 'churchg'
    # 'income_sfr', 'income2'
]
SELECTS_DEMOGRAPHIC_GEOGRAPHY_COLUMNS = [
    'sg1', 'sg2', 'sg3', 'sg7b', 'sg9', 'sg10b', 'sg11', 'sg12',
    # 'sg4', 'sg5', 'sg6','sg7a', 'sg10a', 'sg13'
]
SELECTS_DEMOGRAPHIC_HOUSEHOLD_COLUMNS = [
    'sh1', 'sh2', 'sh3', 'sh4', 'educp', 'educh'
    # 'sh2a', 'sh2b', 'sh2c'
]
SELECTS_SOCIAL_CLASS_RESPONDENT_COLUMNS = [
    'sc1', 'sc1a', 'sc1b', 'sc1c', 'sc4', 'sc5', 'sc7a', 'sc7c'
    # 'sc2_75insee', 'sc2g_71', 'sc2_75bit', 'sc2_75src', 'sc2_79', 'sc2_87', 'sc2g_87', 'sc2_91', 'sc2_bfs',
    # 'sc2_isco88', 'sc2_isco08', 'sc3', 'sc6a', 'sc6b', 'sc7b'
]
SELECTS_SOCIAL_CLASS_PARTNER_COLUMNS = [
    'scp1', 'scp1a', 'scp4', 'scp5', 'scp7a', 'scp7c'
    # 'scp2_bfs', 'scp2_isco88', 'scp2_isco08',
]
SELECTS_SOCIAL_CLASS_MAIN_EARNER_COLUMNS = [
    'sch1', 'sch1a', 'sch1b', 'sch3', 'sch4', 'sch5', 'sch7a', 'sch7c',
    # 'sch2_75insee', 'sch2g_71', 'sch2_75bit', 'sch2_75src', 'sch2_79', 'sch2_91', 'sch2_bfs', 'sch2_isco88',
    # 'sch2_isco08', 'sch6a', 'sch6b', 'sch7r'
]
# SELECTS_SOCIAL_CLASS_CHILDHOOD_COLUMNS = ['scc1', 'scc3_75insee', 'scc3g_71', 'scc3_75bit', 'scc3_75src']
SELECTS_SOCIAL_CLASS_COLUMNS = (['class8'] + SELECTS_SOCIAL_CLASS_RESPONDENT_COLUMNS +
                                SELECTS_SOCIAL_CLASS_PARTNER_COLUMNS + SELECTS_SOCIAL_CLASS_MAIN_EARNER_COLUMNS)
SELECTS_ECONOMIC_SITUATION_COLUMNS = ['ses1', 'ses2', 'ses3']
SELECTS_DEMOGRAPHIC_COLUMNS = (
        SELECTS_DEMOGRAPHIC_BASICS_COLUMNS + SELECTS_DEMOGRAPHIC_GEOGRAPHY_COLUMNS +
        SELECTS_DEMOGRAPHIC_HOUSEHOLD_COLUMNS + SELECTS_SOCIAL_CLASS_RESPONDENT_COLUMNS +
        SELECTS_SOCIAL_CLASS_PARTNER_COLUMNS + SELECTS_SOCIAL_CLASS_MAIN_EARNER_COLUMNS +
        SELECTS_SOCIAL_CLASS_COLUMNS + SELECTS_ECONOMIC_SITUATION_COLUMNS
)

SELECTS_POLITICAL_INTEREST_COLUMNS = ['pi1']  # 'pi2', 'pi3', 'pi4', 'pi5'
SELECTS_POLITICAL_PARTICIPATION_COLUMNS = [
    'pp1', 'pp2', 'pp3', 'pp4', 'pp5', 'pp6', 'pp7', 'pp8', 'pp9', 'pp10', 'pp11a', 'pp11b', 'pp12a', 'pp12b', 'pp12c'
]
# SELECTS_POLITICAL_PARTICIPATION_PROTEST_APPROVAL_COLUMNS = ['pp13', 'pp14', 'pp15', 'pp16']
# SELECTS_POLITICAL_PARTICIPATION_PROTEST_ACTIVITY_COLUMNS = ['pp17', 'pp18', 'pp19', 'pp20', 'pp21a', 'pp21b', 'pp22',
#                                                             'pp23']
SELECTS_SOCIAL_PARTICIPATION_COLUMNS = [
    'sp1', 'spm1', 'spm2', 'spm3', 'spm4', 'spm5', 'spm6', 'spm6a', 'spm7', 'spm8', 'spm9', 'spm10', 'spm11', 'spm12',
    'spm13', 'spm14', 'spm25', 'spm26', 'spm27', 'spm28', 'spm29'
]
SELECTS_LEFT_RIGHT_POSITIONING_COLUMNS = [
    'lr1', 'lr2', 'lr3', 'lr4', 'lr5', 'lr6', 'lr7', 'lr8', 'lr9', 'lr10', 'lr11', 'lr12', 'lr13', 'lr14', 'lr15'
]
# SELECTS_MATERIALISM_POSTMATERIALISM_COLUMNS = ['pm1a', 'pm1b', 'pm2a', 'pm2b', 'pm3']
SELECTS_POLITICAL_KNOWLEDGE_COLUMNS = ['pk6']  # 'pk1', 'pk2', 'pk3', 'pk4', 'pk5',
SELECTS_VOTE_PARTICIPATION_COLUMNS = [
    'vp1', 'vp3', 'vp5',
    'vnp3a', 'vnp3b', 'vnp3c', 'vnp3d', 'vnp3e', 'vnp3f', 'vnp3g', 'vnp3h', 'vnp3i', 'vnp3j', 'vnp3k'
    # 'vp2', 'vp4', 'vnp1', 'vnp2',
]
SELECTS_VOTING_DECISION_COLUMNS = [
    'vdn1b', 'hvdn2b', 'vds1b', 'vds2b', 'ml1', 'ml2', 'ml3', 'ml4', 'mvd1', 'mvd2', 'mvd3', 'mvd4',
    # 'vdn2b', 'vdn3b', 'vdn6', 'hvdn1b', 'vdr1b', 'hvds1b', 'hvds2b', 'vdo1b',
    # 'avd2a', 'avd2b', 'avd2c', 'avd9', 'avd10'
]
SELECTS_PARTY_IDENTIFICATION_COLUMNS = ['pid1', 'pid2b', 'pid4b', 'pid6b', 'pid7b']  # 'pid3', 'pid5', 'pid8'
# SELECTS_SYMPATHY_PARTIES_COLUMNS = ['sypa1', 'sypa2', 'sypa3', 'sypa4', 'sypa5', 'sypa6', 'sypa7', 'sypa8', 'sypa9',
#                                     'sypa10', 'sypa11', 'sypa12', 'sypa14', 'sypa15']
SELECTS_PROBABILITY_TO_VOTE_COLUMNS = ['ptv1', 'ptv2', 'ptv3', 'ptv4', 'ptv5', 'ptv6', 'ptv7', 'ptv8', 'ptv9', 'ptv10',
                                       'ptv11']
SELECTS_SYMPATHY_PERSONALITIES_COLUMNS = ['sypep1', 'sypep2', 'sypep3', 'sypep4']
# SELECTS_SYMPATHY_GROUPS_COLUMNS = ['syg1', 'syg2']
SELECTS_TRUST_IN_POLITICAL_INSTITUTIONS_COLUMNS = ['trust1', 'trust2', 'trust3', 'trust4', 'trust5', 'trust6', 'trust7']
SELECTS_POLITICAL_EFFICACY_COLUMNS = ['peff1', 'peff2', 'peff3', 'peff4', 'peff5', 'peff6', 'peff7', 'peff8']
SELECTS_EVALUATION_OF_THE_POLITICAL_SYSTEM_COLUMNS = ['eps1', 'eps2']
SELECTS_MOST_IMPORTANT_PROBLEM_COLUMNS = ['mip1', 'mip2']
SELECTS_ISSUE_IMPORTANCE_COLUMNS = ['ii3', 'ii5', 'ii7']
SELECTS_ISSUE_POSITION_COLUMNS = ['ip1', 'ip2', 'ip3', 'ip4', 'ip5', 'ip6', 'ip7', 'ip8', 'ip9', 'ip10', 'ip11', 'ip12',
                                  'ip13', 'ip14', 'ip15']
# SELECTS_NATIONAL_PRIDE_COLUMNS = ['np1', 'np2']
SELECTS_ATTACHMENT_COLUMNS = ['att1', 'att2', 'att3', 'att4', 'att5']
SELECTS_ECONOMIC_EVALUATIONS_COLUMNS = ['ee1', 'ee2']
SELECTS_EVALUATION_OF_POLITICAL_PARTIES_COLUMNS = ['ep1', 'ep2', 'ep3', 'ep4', 'ep5']
SELECTS_MEDIA_USE_COLUMNS = ['med1', 'med2', 'med3', 'med4', 'med5']
SELECTS_CAMPAIGN_INFORMATION_COLUMNS = ['ci1', 'ci2', 'ci3', 'ci4', 'ci5', 'ci6', 'ci7', 'ci8', 'ci9', 'ci10', 'ci11',
                                        'ci12', 'ci13', 'ci14']
# SELECTS_IMPORTANCE_OF_CAMPAIGN_INFORMATION_COLUMNS = ['ici1', 'ici2', 'ici3', 'ici4']
SELECTS_SLOGANS_OF_POLITICAL_PARTIES_COLUMNS = ['slogan']  # 'slogan1', 'slogan2', 'slogan3', 'slogan4', 'slogan5'
SELECTS_INFORMATION_INTERVIEW_COLUMNS = [
    'language',
    # 'intinf1', 'intinf2', 'intinf3', 'intinf4', 'intinf5', 'intinf6', 'intinf7'
]
SELECTS_POLITICAL_COLUMNS = (
        SELECTS_POLITICAL_INTEREST_COLUMNS +
        SELECTS_POLITICAL_PARTICIPATION_COLUMNS +
        SELECTS_SOCIAL_PARTICIPATION_COLUMNS +
        SELECTS_LEFT_RIGHT_POSITIONING_COLUMNS +
        SELECTS_POLITICAL_KNOWLEDGE_COLUMNS +
        SELECTS_VOTING_DECISION_COLUMNS +
        SELECTS_PARTY_IDENTIFICATION_COLUMNS +
        SELECTS_PROBABILITY_TO_VOTE_COLUMNS +
        SELECTS_SYMPATHY_PERSONALITIES_COLUMNS +
        SELECTS_TRUST_IN_POLITICAL_INSTITUTIONS_COLUMNS +
        SELECTS_POLITICAL_EFFICACY_COLUMNS +
        SELECTS_EVALUATION_OF_THE_POLITICAL_SYSTEM_COLUMNS +
        SELECTS_MOST_IMPORTANT_PROBLEM_COLUMNS +
        SELECTS_ISSUE_IMPORTANCE_COLUMNS +
        SELECTS_ISSUE_POSITION_COLUMNS +
        SELECTS_ATTACHMENT_COLUMNS +
        SELECTS_ECONOMIC_EVALUATIONS_COLUMNS +
        SELECTS_EVALUATION_OF_POLITICAL_PARTIES_COLUMNS +
        SELECTS_MEDIA_USE_COLUMNS +
        SELECTS_CAMPAIGN_INFORMATION_COLUMNS +
        SELECTS_SLOGANS_OF_POLITICAL_PARTIES_COLUMNS
)
