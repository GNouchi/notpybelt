from django.db import models
from django.core.validators import validate_email
import datetime , bcrypt, re
NAME_REGEX = re.compile(r'^[a-zA-Z ]+$')

#  add models
class UserManager(models.Manager):
    def regValidator(self, postData):
        result = {'errors':[]}
        if len(postData['first_name']) <1:
            result['errors'].append("First Name too short")
        if len(postData['last_name']) <1:
            result['errors'].append("Last Name too short")
        if len(postData['email']) <1:
            result['errors'].append("Email too short")
        if len(postData['password']) <8:
            result['errors'].append("Password too short")
        if postData['password'] !=postData['confirm_password']:
            result['errors'].append("Passwords do not match")
        try:
            if not NAME_REGEX.match(postData['first_name']) or not NAME_REGEX.match(postData['last_name']):
                result['errors'].append("Name fields can only be english letters")
        except:
            pass
        try:
            validate_email(postData['email'])
        except:
            result['errors'].append("Invalid email")
        throwaway = User.objects.filter(email = postData['email'])
        if len(throwaway)> 0:
            result['errors'].append("Please use another email")
        if len(result['errors'])> 0:
            print("errors found, escaping now...")
            return result
# ******************************** VALIDATION PASS *************************************
        print("regValidator Pass")
        hash1 = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        hash1= hash1.decode()
        newUser = User.objects.create(
            first_name = postData['first_name'],
            last_name = postData['last_name'],
            email = postData['email'],
            password = hash1,
        )
        result['user_id'] = newUser.id
        return result

    def loginValidator(self, postData):
        result = {'errors':[]}
        throwaway = User.objects.filter(email = postData['email'])
        if len(throwaway) > 0:
            if bcrypt.checkpw(postData['password'].encode(),throwaway[0].password.encode() ):
                result['user_id'] = throwaway[0].id
                return result
        result['errors'].append("Password or Email did not match")
        return result
    
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    create_d = models.DateField(auto_now_add = True)
    update_d = models.DateField(auto_now = True)
    objects = UserManager()


class JobManager(models.Manager):
    def jobaddValidator(self, postData):
        result = {'errors':[]}
        if len(postData['title']) < 3:
            result['errors'].append("Title too short (3+ please)")
        if len(postData['description'])< 10:
            result['errors'].append("Description too short (10+ please)")
        if len(postData['location'] )< 1:
            result['errors'].append("Location needed")
        if len(result['errors'])> 0:
            print("errors found, escaping now...")
            return result
# ******************************** VALIDATION PASS *************************************
        print("AddJobs Validator Pass")
        current_user = User.objects.filter(id = postData['user_id'])
        if len(current_user)> 0:
            newjob = Job.objects.create(
                title= postData['title'],
                description= postData['description'],
                location= postData['location'],
                owner= current_user[0],
            )
            return result
    def editValidator(self, postData,id ):
        result = {'errors':[]}
        if len(postData['title']) < 3:
            result['errors'].append("Title too short (3+ please)")
        if len(postData['description'])< 10:
            result['errors'].append("Description too short (10+ please)")
        if len(postData['location'] )< 1:
            result['errors'].append("Location needed")
        current_user = User.objects.get(id = postData['user_id'])
        this_job = Job.objects.get(id = id)
        if this_job.owner.id != current_user.id:
            result['errors'].append("Location needed")
        if len(result['errors'])> 0:
            print("errors found, escaping now...")
            return result
# ******************************** VALIDATION PASS *************************************
        print("EditJobs Validator Pass")
        this_job.title = postData['title']
        this_job.description= postData['description']
        this_job.location= postData['location']
        this_job.save()
        return result


            


class Job(models.Model):
    title = models.CharField(max_length= 255)
    description = models.CharField(max_length= 255)
    location = models.CharField(max_length= 255)
    create_d = models.DateTimeField(auto_now_add = True)
    owner = models.ForeignKey(User, related_name="jobs" ,on_delete = models.CASCADE)
    worker = models.ForeignKey(User, related_name="joinedjobs", blank=True, null=True ,on_delete = models.CASCADE)
    objects = JobManager()