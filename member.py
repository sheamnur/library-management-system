class Member:
    def __init__(self,name,email,phone,address,member_id=None,created_at=None):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.member_id = member_id
        self.created_at = created_at