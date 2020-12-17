class GMailProfile(object):
    def __init__(self, name, email, primary, sent=0, drafts=0, spam=0, starred=0, snoozed=0, labels=None, categories=None):
        self.name=name
        self.email=email
        self.primary=primary
        self.sent=sent
        self.drafts=drafts
        self.spam=spam
        self.starred=starred
        self.snoozed=snoozed
        self.labels=labels # dict type
        self.categories=categories # dict type

    def to_dict(self):
        profile={}

        profile['name']=self.name 
        profile['email']=self.email
        profile['inbox']=self.primary
        profile['sent']=self.sent
        profile['drafts']=self.drafts
        profile['spam']=self.spam
        profile['starred']=self.starred
        profile['snoozed']=self.snoozed
        profile['labels']=self.labels
        profile['categories']=self.categories

        return profile

    def __str__(self):
        op = f"name: {self.name}, "
        op += f"email: {self.email}\n"
        op += f"✉  {self.primary}\n"
        op += f"☆  {self.starred}\n"
        op += f"🕑  {self.snoozed}\n"
        return op