from django.db import models
from apps.users.models import User
from datetime import datetime

class OrganizationManager(models.Manager):
    def validate_organization_creation(self,postData):
        errors = {}
        if len(postData['organization']) < 3:
            errors['organization_error'] = "At least 3 characters"
        if len(postData['description']) < 3:
            errors['description_error'] = "At least 3 characters"
        return errors

    def process_organization_creation(self, postData, userid):
        user = User.objects.get(id=userid)
        org_id = self.create(
            organization = postData['organization'],
            description = postData['description'],
            creator = user
        ).id
        return org_id

    def update_org(self, postData, org_id):
        org = self.get(id=org_id)
        org.organization = postData['organization']
        org.description = postData['description']
        org.save()
        return


class org(models.Model):
    organization = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255 )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, related_name='joining_organization')
    creator = models.ForeignKey(User, related_name = 'created_organization')
    objects = OrganizationManager()
