# REQUIRED - IF YOU DELETE THESE EVERYTHING BREAKS
try:
    from data.crosswalkmaps import crosswalks
except ImportError:
    crosswalks = {}
sources = []
destinations = []


# GENERAL CONFIGURATION


#SOURCE CONFIGURATIONS
# CARNEGIE/DARLET SOURCE CONFIGURATION
sources.append( { 'name': 'Carnegie',
                  'type': 'carnegie',
                  'user': '',
                  'auth': ''
                } )

# COMMONAPP SOURCE CONFIGURATION
sources.append( { 'name': 'CommonApp',
                  'type': 'sftp',
                  'user': '',
                  'auth': '',
                  'host': 'ftp.commonapp.org',
                  'dateformat': '%m_%d_%Y'
                } )

# SAT SOURCE CONFIGURATION
sources.append( { 'name': 'SAT',
                  'type': 'sat',
                  'user': '',
                  'auth': '',
                  'dateformat': '%Y-%m-%dT00:00:00-1000'
                } )

# ACT SOURCE CONFIGURATION
# Still working on the ACT process.  I mean seriously, who still emails notifications and then tells you to download PGP files???
# Right now ACT is probably going to be a smb source for us where Admissions puts the decrypted text file
# Later this tool might do the decryption too, but I'll probably never add the pieces needed to read the notification email


# DESTINATION CONFIGURATIONS
# FIREWORKS DESTINATION CONFIGURATION
destinations.append( { 'name': 'FileServer',
                       'type': 'smb',
                       'user': '',
                       'auth': '',
                       'host': 'fileserver',
                       'hostip': '10.10.220.5',
                       'clientname': 'automation',
                       'share': 'MyShare',
                       'path': 'My/Path'
                       'filters': 'CommonApp:.zip, SAT:.zip',
                     } )

destinations.append( { 'name': 'Local',
                       'type': 'localfile',
                       'path': '/My/Path',
                     } )

destinations.append( { 'name': 'Fireworks',
                       'type': 'ftps',
                       'user': '',
                       'auth': '',
                       'host': '',
                       'port': 997,
                       'passive': True,
                       'authtls': False,
                       'ssl': True,
                       'filters': 'SAT:.csv, CommonApp:.txt',
                       'mergefiles': True,
                       'hasheaders': {'ACT': False}
                       'transforms': 'Carnegie:changefields, SAT:changefields, CommonApp:filerename; changefields,  ACT:fixedtocsv',
                       'Carnegie_changefields_config': {'transforms': [
                                                          {'column':30, 'name':'dropcolumn'}
                                                                       ]},
                       'SAT_changefields_config': {'transforms':[
                                                     {'column':33, 'name':'replace', 'search':r'(.*)-(.*)', 'replace':r'Fall \1', 'default':'Unknown'},
                                                     {'column':666, 'name':'dropcolumn'}
                                                                 ]},
                       'CommonApp_filerename_config': {'search':r'(^[^FT]*)(.*)_.*txt', 'replace':r'CommonApp_\2_\1.csv'},
                       'CommonApp_changefields_config': {'transforms':[
                                                            {'column':34, 'name':'trimchoicelist', 'priority': ['Native Hawaiian or Other Pacific Islander',
                                                                                                                'Asian', 'American Indian or Alaska Native',
                                                                                                                'Black or African American','White']}
                                                                  ]},
                       'ACT_fixedtocsv_config':{'encoding':'utf-8-sig', 'colspec':[(1, 2), (3, 27), (28, 43), (44, 44), (45, 84), (85, 86), (87, 87), (88, 88), (89, 90),(91, 99), (100, 100), (101, 106), (107, 116), (117, 141), (142, 143), (144, 145),(146, 154), (155, 162), (163, 164), (165, 166), (167, 170), (171, 172), (173, 174), (175, 176),(177, 178), (179, 180), (181, 182), (183, 184), (185, 186), (187, 188), (189, 190), (191, 191), (192, 204), (205, 210), (211, 212), (213, 214), (215, 216), (217, 218), (219, 219), (220, 222), (223, 226), (227, 232), (233, 236), (237, 248), (249, 249), (250, 251), (252, 252), (253, 259), (260, 260), (261, 262), (263, 264), (265, 266), (267, 268), (269, 270), (271, 271), (272, 274), (275, 278), (279, 280), (281, 282), (283, 284), (285, 286), (287, 288), (289, 290), (291, 292), (293, 294), (295, 296), (297, 298), (299, 300), (301, 302), (303, 304), (305, 306), (307, 308), (309, 310), (311, 311), (312, 315), (316, 319), (320, 321), (322, 323), (324, 325), (326, 327), (328, 329), (330, 331), (332, 333), (334, 341), (342, 344), (345, 347), (348, 350), (351, 353), (354, 356), (357, 359), (360, 362), (363, 365), (366, 368), (369, 370), (371, 372), (373, 374), (375, 376), (377, 378), (379, 380), (381, 388), (389, 390), (391, 392), (393, 394), (395, 396), (397, 398), (399, 400), (401, 401), (402, 403), (404, 404), (405, 405), (406, 406), (407, 407), (408, 408), (409, 410), (411, 413), (414, 416), (417, 419), (420, 420), (421, 421), (422, 422), (423, 423), (424, 424), (425, 425), (426, 426), (427, 427), (428, 428), (429, 429), (430, 430), (431, 431), (432, 432), (433, 433), (434, 445), (446, 446), (447, 447), (448, 448), (449, 449), (450, 450), (451, 451), (452, 452), (453, 453), (454, 454), (455, 455), (456, 456), (457, 457), (458, 458), (459, 459), (460, 460), (461, 461), (462, 462), (463, 463), (464, 464), (465, 465), (466, 466), (467, 467), (468, 468), (469, 469), (470, 470), (471, 471), (472, 472), (473, 473), (474, 475), (476, 477), (478, 483), (484, 484), (485, 485), (486, 486), (487, 487), (488, 488), (489, 489), (490, 490), (491, 491), (492, 492), (493, 493), (494, 494), (495, 495), (496, 496), (497, 497), (498, 498), (499, 499), (500, 500), (501, 501), (502, 502), (503, 503), (504, 504), (505, 505), (506, 506), (507, 508), (509, 509), (510, 510), (511, 511), (512, 512), (513, 513), (514, 514), (515, 515), (516, 516), (517, 517), (518, 518), (519, 519), (520, 520), (521, 521), (522, 522), (523, 523), (524, 524), (525, 525), (526, 526), (527, 527), (528, 528), (529, 529), (530, 530), (531, 531), (532, 532), (533, 533), (534, 534), (535, 535), (536, 536), (537, 537), (538, 538), (539, 539), (540, 540), (541, 541), (542, 542), (543, 543), (544, 544), (545, 545), (546, 546), (547, 547), (548, 548), (549, 549), (550, 550), (551, 600), (601, 604), (605, 605), (606, 607), (608, 608), (609, 609), (610, 610), (611, 611), (612, 612), (613, 613), (614, 614), (615, 615), (616, 630), (631, 631), (632, 632), (633, 633), (634, 634), (635, 635), (636, 636), (637, 637), (638, 638), (639, 639), (640, 640), (641, 641), (642, 642), (643, 643), (644, 644), (645, 645), (646, 646), (647, 647), (648, 648), (649, 649), (650, 650), (651, 651), (652, 652), (653, 653), (654, 654), (655, 655), (656, 656), (657, 657), (658, 658), (659, 659), (660, 660), (661, 661), (662, 662), (663, 663), (664, 664), (665, 665), (666, 666), (667, 667), (668, 668), (669, 669), (670, 670), (671, 671), (672, 672), (673, 673), (674, 674), (675, 675), (676, 676), (677, 677), (678, 678), (679, 679), (680, 680), (681, 681), (682, 682), (683, 683), (684, 684), (685, 685), (686, 686), (687, 687), (688, 688), (689, 689), (690, 690), (691, 700), (701, 703), (704, 706), (707, 709), (710, 712), (713, 715), (716, 718), (719, 721), (722, 724), (725, 727), (728, 730), (731, 732), (733, 734), (735, 736), (737, 738), (739, 740), (741, 742), (743, 744), (745, 746), (747, 748), (749, 750), (751, 752), (753, 754), (755, 756), (757, 758), (759, 760), (761, 762), (763, 764), (765, 766), (767, 768), (769, 770), (771, 773), (774, 776), (777, 779), (780, 782), (783, 783), (784, 786), (787, 789), (790, 790), (791, 792), (793, 795), (796, 797), (798, 799), (800, 801), (802, 803), (804, 805), (806, 807), (808, 809), (810, 811), (812, 813), (814, 816), (817, 819), (820, 820), (821, 821), (822, 823), (824, 825), (826, 828), (829, 831), (832, 833), (834, 835), (836, 838), (839, 841), (842, 843), (844, 845), (846, 848), (849, 851), (852, 853), (854, 855), (856, 858), (859, 861), (862, 863), (864, 865), (866, 868), (869, 871), (872, 873), (874, 875), (876, 878), (879, 881), (882, 883), (884, 885), (886, 888), (889, 891), (892, 893), (894, 895), (896, 898), (899, 901), (902, 903), (904, 905), (906, 908), (909, 911), (912, 913), (914, 915), (916, 918), (919, 921), (922, 923), (924, 925), (926, 928), (929, 931), (932, 941), (942, 943), (944, 945), (946, 948), (949, 951), (952, 953), (954, 955), (956, 958), (959, 961), (962, 963), (964, 965), (966, 968), (969, 971), (972, 973), (974, 975), (976, 978), (979, 981), (982, 983), (984, 985), (986, 988), (989, 991), (992, 993), (994, 995), (996, 998), (999, 1001), (1002, 1007), (1008, 1010), (1011, 1013), (1014, 1016), (1017, 1019), (1020, 1022), (1023, 1025), (1026, 1028), (1029, 1031), (1032, 1034), (1035, 1037), (1038, 1040), (1041, 1043), (1044, 1050)], 'header':["Reporting Year", "Student Last Name", "Student First Name", "Student Middle Initial", "Street Address", "Country Code", "Gender Numeric", "Gender Alpha", "Grade Level", "ACT ID or SSN", "Type of Telephone", "Date of Birth", "Telephone Number", "City", "Mailing State Numeric", "Mailing State Abbreviation", "Zip Plus 4", "Expanded Date of Birth", "Combined English-Writing Score", "Writing Score", "Blank1", "Writing Comment 1", "Writing Comment 2", "Writing Comment 3", "Writing Comment 4", "Blank2", "English before 10-89", "Math before 10-89", "Social Studies before 10-89", "Natural Sciences before 10-89", "Composite Score before 10-89", "Blank3", "State-Assigned Student ID Number", "High School Code", "High School Grade English", "High School Grade Math", "High School Grade Social Studies", "High School Grade Natural Sciences", "Blank4", "High School Average", "Year High School Graduation", "Expanded Test Date", "Test Date", "Blank5", "Test Location", "Canadian Province", "Blank6", "Canadian Postal Code", "Corrected Report", "English Score", "Math Score", "Reading Score", "Science Score", "Composite Score", "Blank7", "Sum of Scale Scores", "Blank8", "II Science", "II Science Standard Score", "II Arts", "II Art Standard Score", "II Social Service", "II Social Service Standard Score", "II Business Contact", "II Business Contact Standard Score", "II Business Operations", "II Business Operations Standard Score", "II Technical", "II Technical Standard Score", "II Map Region 1", "II Map Region 2", "II Map Region 3", "Blank9", "College Choice Number", "Blank10", "College Code Number", "Usage Mechanics Subscore", "Rhetorical Skills Subscore", "Elem Algebra Subscore", "Alg Coord Geometry Subscore", "Plane Geom Trig Subscore", "Social Studies Science Subscore", "Arts Literature Subscore", "Blank11", "Institutional Rank - STEM beginning 9-2016", "Institutional Rank - ELA beginning 9-2016", "Institutional Norm Usage-Mech Subscore", "Institutional Norm Rhetorical Skills Subscore", "Institutional Norm Elem Algebra Subscore", "Institutional Norm Alg-Coord Geom Subscore", "Institutional Norm Plane Geom-Trig Subscore", "Institutional Norm Soc Stud-Sci Subscore", "Institutional Norm Arts-Lit Subscore", "II Pct Rank Science", "II Pct Rank Arts", "II Pct Rank Social Service", "II Pct Rank Business Contact", "II Pct Rank Business Operations", "II Pct Rank Technical", "Local ID", "Blank12", "Mobility Index", "Institution Type Index", "Selectivity Index", "Institution Size Index", "Interest-Major Fit Score", "Attend Full or Part Time", "Blank13", "Plan To Live Where", "Blank14", "Citizenship Status", "Legal Resident Of State", "Have Disability", "Blank15", "Planned Educational Major", "Vocational Choice 1", "Blank16", "Certainty of Planned Educational Major", "Certainty of Vocational Choice 1", "Highest Level Education Expected to Complete", "Blank17", "Interested in ROTC, NROTC, AFROTC, etc.", "Want Help with Education-Occupational Plans", "Want Help Writing", "Want Help Reading", "Want Help with Study Skills", "Want Help with Math Skills", "Blank18", "Want Independent Study", "Want Honors Courses", "Want Study Abroad", "Blank19", "Instrumental Music College", "Vocal Music College", "Student Government College", "Publications College", "Debate College", "Blank20", "Theater College", "Religious Organizations College", "Racial Ethnic Organizations College", "Blank21", "Varsity Athletics College", "Political Organizations College", "Radio TV College", "Fraternity Sorority College", "Blank22", "Service Organizations College", "Expect to Apply for Financial Aid", "Expect to Work in College", "Hours to Work per Week in College", "Level Parents Income", "Level Mother-Guardian Education", "Level Father-Guardian Education", "Blank23", "Preferred Distance From Home to College", "Is English Most Frequent Language Spoken at Home", "Racial Ethnic Background", "Institution Type Preference", "Male Female Preference", "State Prefer to Attend 1", "State Prefer to Attend 2", "Blank24", "Maximum Tuition Preference", "College Size Preference", "Rank Institution Type Preference", "Rank Male Female Preference", "Rank Location Preference", "Rank Cost Preference", "Rank Size of Enrollment Preference", "Rank Field of Study Preference", "Rank Other Factor", "High School Type", "High School Size", "Blank25", "High School Class Rank", "High School GPA", "High School Curriculum", "Years Studied English", "Years Studied Math", "Years Studied Social Studies", "Years Studied Natural Sciences", "Years Studied Spanish", "Years Studied German", "Years Studied French", "Years Studied Other Lang", "Blank26", "Enrolled AP-Honors English", "Enrolled AP-Honors Math", "Enrolled AP-Honors Social Studies", "Enrolled AP-Honors Natural Sciences", "Enrolled AP-Honors For Lang", "Instrumental Music High School", "Vocal Music High School", "Student Government High School", "Publications High School", "Debate High School", "Blank27", "Theater High School", "Religious Organizations High School", "Racial Ethnic Organizations High School", "Blank28", "Varsity Athletics High School", "Political Organizations High School", "Radio TV High School", "Fraternity, Sorority, Social Club High School", "Blank29", "Service Organizations High School", "Organized Political Group", "Elected Student Office", "Received Award or Special Recognition for Leadership", "Performed with Professional Music Group", "Superior State Music Rating", "Placed in State or Regional Debate Contest", "Had Substantial Roles in Plays", "Appeared on Radio or TV as a Performer", "Exhibited a Work of Art", "Won a Prize in Art Competition at HS", "Won a Prize in a Regional Art Competition", "Published in Non-School Newspaper or Magazine", "Won Literary Award for Creative Writing", "Published in Magazine or Book", "Participated in NSF Summer Program", "Placed in  Science Contest", "Placed in School Science Contest", "Earned a Varsity Letter in One or More Sports", "Received Athletic Award", "Received a Community Service Award", "Started My Own Business or Service", "Student Email Address", "Blank30", "Educational Opportunity Service Release", "Religious Affiliation", "Raw Race-Ethnicity Hispanic-Latino", "Raw Race-Ethnicity American Ind-AK Nat", "Raw Race-Ethnicity Asian", "Raw Race-Ethnicity Black-African Amer", "Raw Race-Ethnicity Hawaiian-Pacific Isl", "Raw Race-Ethnicity White", "Raw Race-Ethnicity Prefer not to respond", "Raw Race-Ethnicity Multiracial", "Blank31", "High School Course Eng 9", "High School Course Eng 10", "High School Course Eng 11", "High School Course Eng 12", "High School Course Other English", "High School Course Algebra 1", "High School Course Algebra 2", "High School Course Geometry", "High School Course Trig", "High School Course Beg Calc", "High School Course Other Adv Math", "High School Course Computer", "High School Course Gen Sci", "High School Course Biology", "High School Course Chemistry", "High School Course Physics", "High School Course US Hist", "High School Course World Hist", "High School Course Other Hist", "High School Course Amer Govt", "High School Course Econ", "High School Course Geog", "High School Course Psych", "High School Course Spanish", "High School Course French", "High School Course German", "High School Course Other Lang", "High School Course Art", "High School Course Music", "High School Course Drama", "High School Grade Eng 9", "High School Grade Eng 10", "High School Grade Eng 11", "High School Grade Eng 12", "High School Grade Other English", "High School Grade Algebra 1", "High School Grade Algebra 2", "High School Grade Geometry", "High School Grade Trig", "High School Grade Beg Calc", "High School Grade Other Adv Math", "High School Grade Computer", "High School Grade Gen Sci", "High School Grade Biology", "High School Grade Chemistry", "High School Grade Physics", "High School Grade US Hist", "High School Grade World Hist", "High School Grade Other Hist", "High School Grade Amer Govt", "High School Grade Econ", "High School Grade Geog", "High School Grade Psych", "High School Grade Spanish", "High School Grade French", "High School Grade German", "High School Grade Other Lang", "High School Grade Art", "High School Grade Music", "High School Grade Drama", "State-Assigned Student ID Number2", "Composite Score Group 1", "Composite Score Group 2", "Composite Score Group 3", "Composite Score Group 4", "Composite Score Group 5", "Subject Area Score Course 1", "Subject Area Score Course 2", "Subject Area Score Course 3", "Subject Area Score Course 4", "Subject Area Score Course 5", "Prob C or Higher Group 1", "Prob C or Higher Group 2", "Prob C or Higher Group 3", "Prob C or Higher Group 4", "Prob C or Higher Group 5", "Prob C or Higher Course 1", "Prob C or Higher Course 2", "Prob C or Higher Course 3", "Prob C or Higher Course 4", "Prob C or Higher Course 5", "Prob B or Higher Group 1", "Prob B or Higher Group 2", "Prob B or Higher Group 3", "Prob B or Higher Group 4", "Prob B or Higher Group 5", "Prob B or Higher Course 1", "Prob B or Higher Course 2", "Prob B or Higher Course 3", "Prob B or Higher Course 4", "Prob B or Higher Course 5", "Institutional Rank English", "Institutional Rank Math", "Institutional Rank Read", "Institutional Rank Science", "Ranks Type", "Institutional Rank - Writing Subject Score", "Institutional Rank - Enrollment Populations", "Blank32", "Writing Subject Score", "US Rank - Writing Subject Score", "Writing Domain Score:  Ideas and Analysis", "Writing Domain Score:  Development and Support", "Writing Domain Score:  Organization", "Writing Domain Score:  Language Use and Conventions", "Writing Subject Score", "English Language Arts Score", "US Rank - ELA", "Blank33", "STEM Score", "US Rank - STEM", "Blank34", "Understanding Complext Text Indicator", "Progress Toward Career Readiness", "Points Earned - English - Production of Writing", "Points Possible - English - Prod of Writing", "Correct - English - Prod of Writing", "Readiness Range - English - Production of Writing", "Points Earned - English - Knowledge of Lang", "Points Possible - English - Knowledge of Lang", "Correct - English - Knowledge of Lang", "Readiness Range - English - Knowledge of Lang", "Points Earned - English - Convention of English", "Points Possible - English - Convention of English", "Correct - English - Convention of English", "Readiness Range - English - Convention of English", "Points Earned - Math - Prep for Higher Math", "Points Possible - Math - Prep for Higher Math", "Correct - Math - Prep for Higher Math", "Readiness Range - Math - Prep for Higher Math", "Points Earned - Math - Number - Quantity", "Points Possible - Math - Number - Quantity", "Correct - Math - Number - Quantity", "Readiness Range - Math - Number - Quantity", "Points Earned - Math - Algebra", "Points Possible - Math - Algebra", "Correct - Math - Algebra", "Readiness Range - Math - Algebra", "Points Earned - Math - Functions", "Points Possible - Math - Functions", "Correct - Math - Functions", "Readiness Range - Math - Functions", "Points Earned - Math - Geometry", "Points Possible - Math - Geometry", "Correct - Math - Geometry", "Readiness Range - Math - Geometry", "Points Earned - Math - Statis - Probablility ", "Points Possible - Math - Statis - Probablility ", "Correct - Math - Statistics - Probablility ", "Readiness Range - Math - Stats - Probablility ", "Points Earned - Math - Integrating Skills", "Points Possible - Math - Integrating Skills", "Correct - Math - Integrating Skills", "Readiness Range - Math - Integrating Skills", "Points Earned - Math - Modeling", "Points Possible - Math - Imodeling", "Correct - Math - Modeling", "Readiness Range - Math - Modeling", "Blank35", "Points Earned - Reading - Key Ideas - Details", "Points Possible - Reading - Key Ideas - Details", "Correct - Reading - Key Ideas - Details", "Readiness Range - Reading - Key Ideas - Details", "Points Earned - Reading - Craft - Structure", "Points Possible - Reading - Craft - Structure", "Correct - Reading - Craft - Structure", "Readiness Range - Reading - Craft - Structure", "Points Earned - Reading - Knowledge - Ideas", "Points Possible - Reading - Knowledge - Ideas", "Correct - Reading - Reading - Knowledge - Ideas", "Readiness Range - Reading - Knowledge - Ideas", "Points Earned - Science - Integration of Data", "Points Possible - Science - Integration of Data", "Correct - Science - Integration of Data", "Readiness Range - Science - Integration of Data", "Points Earned - Science - Investigation", "Points Possible - Science - Investigation", "Correct - Science - Investigation", "Readiness Range - Science - Investigation", "Points Earned - Science - Evaluation", "Points Possible - Science - Evaluation", "Correct - Science - Evaluation", "Readiness Range - Science - Evaluation", "US Ranks Writing", "US Rank Usage - Mech Subscore", "US Rank Rhetorical Skills Subscore", "US Rank Elem Algebra Subscore", "US Rank Alg-Coord Geom Subscore", "US Rank Plane Geom-Trig Subscore", "US Rank Soc Stud-Sci Subscore", "US Rank Arts-Lit Subscore", "US Rank Scale Score English", "US Rank Scale Score Mathematics", "US Rank Scale Score Reading", "US Rank Scale Score Science", "US Rank Scale Score Composite", "Blank36"]}
                     } )
