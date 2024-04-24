from django.db import models

class Login(models.Model):
    """
    A Django model representing a Login.

    This model has three fields: 'username', 'password', and 'created_at'. The 'username' field is a CharField 
    with a maximum length of 30 characters and must be unique. The 'password' field is a CharField with a maximum 
    length of 30 characters. The 'created_at' field is a DateField that is automatically set to the current date 
    when a Login object is created.

    Attributes:
        username (CharField): The username field.
        password (CharField): The password field.
        created_at (DateField): The date the Login object was created.

    Methods:
        __str__: Returns a string representation of the Login object, which is the username.
    """
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username

class group(models.Model):
    """
    A Django model representing a group.

    This model has five fields: 'name', 'msg', 'timestamp', 'retracted', and 'groupcode'. The 'name' and 'msg' 
    fields are CharFields with maximum lengths of 30 and 255 characters respectively. The 'timestamp' field is a 
    DateTimeField that is automatically set to the current date and time when a group object is created. The 
    'retracted' field is a BooleanField that is set to False by default. The 'groupcode' field is a CharField with 
    a maximum length of 40 characters.

    Attributes:
        name (CharField): The name of the group.
        msg (CharField): The message of the group.
        timestamp (DateTimeField): The date and time the group object was created.
        retracted (BooleanField): Whether the group is retracted.
        groupcode (CharField): The group code.

    Methods:
        __str__: Returns a string representation of the group object, which is the name of the group.
    """
    name = models.CharField(max_length=30)
    msg = models.CharField(max_length=255)  # or any other field type
    timestamp = models.DateTimeField(auto_now_add=True)
    retracted = models.BooleanField(default=False)
    groupcode = models.CharField(max_length=40)

    def __str__(self):
        return self.name