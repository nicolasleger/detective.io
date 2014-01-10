from .utils                     import get_topics
from app.detective.permissions  import create_permissions
from django.contrib.auth.models import User
from django.core.exceptions     import ValidationError
from django.db                  import models
from tinymce.models             import HTMLField
import os
import random
import string

class QuoteRequest(models.Model):
    RECORDS_SIZE = (
        (0, "Less than 200"),
        (200, "Between 200 and 1000"),
        (1000, "Between 1000 & 10k"),
        (10000, "More than 10k"),
        (-1, "I don't know yet"),
    )
    USERS_SIZE = (
        (1, "1"),
        (5, "1-5"),
        (0, "More than 5"),
        (-1, "I don't know yet"),
    )
    PUBLIC = (
        (True, "Yes, public"),
        (False, "No, just for a small group of users"),
    )
    name     = models.CharField(max_length=100)
    employer = models.CharField(max_length=100)
    email    = models.EmailField(max_length=100)
    phone    = models.CharField(max_length=100, blank=True, null=True)
    domain   = models.TextField(help_text="Which domain do you want to investigate on?")
    records  = models.IntegerField(choices=RECORDS_SIZE, blank=True, null=True, help_text="How many entities do you plan to store?")
    users    = models.IntegerField(choices=USERS_SIZE, blank=True, null=True, help_text="How many people will work on the investigation?")
    public   = models.NullBooleanField(choices=PUBLIC, null=True, help_text="Will the data be public?")
    comment  = models.TextField(blank=True, null=True, help_text="Anything else you want to tell us?")

    def __unicode__(self):
        return "%s - %s" % (self.name, self.email,)

class Topic(models.Model):
    MODULES     = tuple( (topic, topic,) for topic in get_topics() )
    title       = models.CharField(max_length=250, help_text="Title of your topic.")
    # Value will be set for this field if it's blank
    module      = models.SlugField(choices=MODULES, blank=True, max_length=250, help_text="Module to use to create your topic. Leave blank to create a virtual one.")
    slug        = models.SlugField(max_length=250, unique=True, help_text="Token to use into the url.")
    description = HTMLField(null=True, blank=True, help_text="A short description of what is your topic.")
    about       = HTMLField(null=True, blank=True, help_text="A longer description of what is your topic.")
    public      = models.BooleanField(help_text="Is your topic public?", default=True)
    ontology    = models.FileField(null=True, blank=True, upload_to="ontologies", help_text="Ontology file that descibes your field of study.")
    background  = models.ImageField(null=True, blank=True, upload_to="topics", help_text="Background image displayed on the topic's landing page.")
    author      = models.ForeignKey(User, null=True, blank=True, help_text="The author of this topic.")

    def __unicode__(self):
        return self.title

    def app_label(self):
        if self.slug in ["common", "energy"]:
            return self.slug
        elif not self.module:
            # Already saved topic
            if self.id:
                # Restore the previous module value
                self.module = Topic.objects.get(id=self.id).module
                # Call this function again.
                # Continue if module is still empty
                if self.module: return self.app_label()
            while True:
                token = Topic.get_module_token()
                # Break the loop only if the token doesn't exist
                if not Topic.objects.filter(module=token).exists(): break
            # Save the new token
            self.module = token
            # Save a first time if no idea given
            models.Model.save(self)
        return self.module

    @staticmethod
    def get_module_token(size=10, chars=string.ascii_uppercase + string.digits):
        return "topic%s" % ''.join(random.choice(chars) for x in range(size))

    def get_module(self):
        from app.detective import topics
        return getattr(topics, self.module)

    def get_models(self):
        return getattr(self.get_module(), "models")

    def clean(self):
        if self.ontology == "" and not self.has_default_ontology():
            raise ValidationError( 'An ontology file is required with this module.',  code='invalid')
        models.Model.clean(self)


    def save(self):
        # Ensure that the module field is populated with app_label()
        self.module = self.app_label()
        models.Model.save(self)
        # Then create the permissions related to the label module
        # @TODO check that the slug changed or not to avoid permissions hijacking
        create_permissions( self.get_models(), app_label=self.slug )

    def has_default_ontology(self):
        module = self.get_module()
        # File if it's a virtual module
        if not hasattr(module, "__file__"): return False
        directory     = os.path.dirname(os.path.realpath( module.__file__ ))
        # Path to the ontology file
        ontology = "%s/ontology.owl" % directory
        if os.path.exists(ontology): return True
        # At last, checks that a model file exists
        models = "%s/models.py" % directory
        return os.path.exists(models)


    def get_absolute_path(self):
        return "/%s/" % self.slug

    def link(self):
        path = self.get_absolute_path()
        return '<a href="%s">%s</a>' % (path, path, )
    link.allow_tags = True


class Article(models.Model):
    topic      = models.ForeignKey(Topic, help_text="The topic this article is related to.")
    title      = models.CharField(max_length=250, help_text="Title of your article.")
    slug       = models.SlugField(max_length=250, unique=True, help_text="Token to use into the url.")
    content    = HTMLField(null=True, blank=True)
    public     = models.BooleanField(default=False, help_text="Is your article public?")
    created_at = models.DateTimeField(auto_now_add=True, default=None, null=True)

    def get_absolute_path(self):
        return self.topic.get_absolute_path() + ( "p/%s/" % self.slug )

    def __unicode__(self):
        return self.title

    def link(self):
        path = self.get_absolute_path()
        return '<a href="%s">%s</a>' % (path, path, )
    link.allow_tags = True


# @TODO finish this feature!
# This model aims to describe a research alongside a relationship.
class RelationshipSearch(models.Model):
    # This field is deduced from the relationship name
    subject = models.CharField(editable=False, max_length=250, help_text="Kind of entity to look for (Person, Organization, ...).")
    # Every field are required
    label   = models.CharField(max_length=250, help_text="Label of the relationship (typically, an expression such as 'was educated in', 'was financed by', ...).")
    name    = models.CharField(max_length=250, help_text="Name of the relationship inside the subject.")
    topic   = models.ForeignKey(Topic, help_text="The topic this relationship is related to.")