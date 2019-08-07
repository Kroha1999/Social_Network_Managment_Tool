import json

#Twitter tokens
global tweet_credentials 

#general functional instances
global myImg
global Task_data
global choosePhotoImg

#accounts instanses
global accountsInstancesInsta




def globals_init():
    global myImg
    myImg = {}

    global accountsInstancesInsta
    accountsInstancesInsta={}

    global tweet_credentials
    #tweet_credentials['CONSUMER_KEY'] = ''
    #tweet_credentials['CONSUMER_SECRET'] = ''
    #tweet_credentials['ACCESS_TOKEN'] = ''
    #tweet_credentials['ACCESS_SECRET'] = ''
    with open('data//twitter_api.json', "r") as f:
        tweet_credentials = json.load(f)
    

    resetTask()


def resetTask():
    global Task_data
    Task_data = {
        'DateTimeCreated': None,
        'DateTimeFinished': None,
        'DateTimeSchedule': None,
        
        'SocialNetwork': None, #  'Instagram','Facebook','Twitter','Custom'
        'TaskType': None, # 'Post','Download','Analyze'
        'AllAccounts': {}, #All accounts in the system for that moment - must not be stored

        #Task[key] => key = globalVal.Task_data['SocialNetwork']+globalVal.Task_data['TaskType']
        'Task':{
            'InstagramPost':{          
                'chosen_acc':{            #chosen accounts to make post on
                    'Instagram':[],
                    'Facebook':[],
                    'Twitter':[]
                },          
                
                'choose_trans':{},        #chosen accounts to keep the description in original language
                
                'chosen_trans':{          #chosen accounts to translate post with account language
                    'Instagram':[],
                    'Facebook':[],
                    'Twitter':[]
                },        

                'photo_path':None,        #path
                
                'not_change_text1': None, #upper not changeble description
                'description':None,       #translateble text
                'not_change_text2': None, #lower not changeble description
            },
            'InstagramDownload':None,
            'InstagramAnalyze':None,
        
            'FacebookPost':None,
            'FacebookDownload':None,
            'FacebookAnalyze':None,

            'TwitterPost':None,
            'TwitterDownload':None,
            'TwitterAnalyze':None
        }  
    }
    #saving all accounts
    with open('data\\data.json') as json_file:  
        Task_data['AllAccounts'] = json.load(json_file)
        #for acc in globalVal.Task_data['AllAccounts']['Instagram']:

