from django import newforms as forms
from contest.apps.contests.models import Entry # The model that uses the zipfile (has a FileField called 'zip_file')
from django.newforms.util import ErrorList, ValidationError
from django.contrib.auth.models import User
from datetime import date
from models import Contest

def get_contests():
    choices=Contest.objects.filter(start_date__lte=date.today()).filter(end_date__gte=date.today())
    list = []
    for choice in choices:
        list.append((choice.id, choice.title))
    return list

class StrAndUnicode(object):
    """
    A class whose __str__ returns its __unicode__ as a UTF-8 bytestring.

    Useful as a mix-in.
    """
    def __str__(self):
        return self.__unicode__().encode('utf-8')


class FileField(forms.Field):
    widget = forms.FileInput
    def __init__(self, *args, **kwargs):
        super(FileField, self).__init__(*args, **kwargs)

    def clean(self, data):
        super(FileField, self).clean(data)
        if not self.required and data in EMPTY_VALUES:
            return None
        try:
            f = UploadedFile(data['filename'], data['content'])
        except TypeError:
            raise ValidationError("No file was submitted. Check the encoding type on the form.")
        except KeyError:
            raise ValidationError("No file was submitted.")
        if not f.content:
            raise ValidationError("The submitted file is empty.")
        return f

class ImageField(FileField):
    def clean(self, data):
        """
        Checks that the file-upload field data contains a valid image (GIF, JPG,
        PNG, possibly others -- whatever the Python Imaging Library supports).
        """
        f = super(ImageField, self).clean(data)
        if f is None:
            return None
        from PIL import Image
        from cStringIO import StringIO
        from contest.settings import SCREENSHOT_RESOLUTION
        res = SCREENSHOT_RESOLUTION.split("x")
        try:
            uploaded_image = Image.open(StringIO(f.content))
            size = uploaded_image.size
            if ((size[0] > int(res[0]) and size[1] > int(res[1])) or (size[0] > int(res[0]) or size[1] > int(res[1]))):
                uploaded_image.thumbnail([int(res[0]), int(res[1])]) # generate a 200x200 thumbnail
                smallerfile=StringIO()
                uploaded_image.save(smallerfile, uploaded_image.format)
                f.content = smallerfile.getvalue()
        except (IOError, OverflowError): # Python Imaging Library doesn't recognize it as an image
            # OverflowError is due to a bug in PIL with Python 2.4+ which can cause 
            # it to gag on OLE files. 
            raise ValidationError("Upload a valid image. The file you uploaded was either not an image or a corrupted image.")
        return f

class UploadedFile(StrAndUnicode):
    "A wrapper for files uploaded in a FileField"
    def __init__(self, filename, content):
        self.filename = filename
        self.content = content

    def __unicode__(self):
        """
        The unicode representation is the filename, so that the pre-database-insertion
        logic can use UploadedFile objects
        """
        return self.filename

class MapUploadForm(forms.Form):
    
    title = forms.CharField( max_length=200 )
    contest = forms.Field( widget=forms.Select(choices=get_contests()))
    map = FileField()
    screenshot = ImageField()
    user = forms.Field(widget = forms.HiddenInput)
                    
    def save(self):
        title = self.clean_data['title']
        user=self.clean_data['user']
        user=User.objects.get(pk=user)
        contest=Contest.objects.get(pk=self.clean_data['contest'])
        q = Entry(title=title, disqualified=False, user=user, contest=contest)
        Entry.save_map_file(q, self.clean_data['map'].filename, self.clean_data['map'].content)
        Entry.save_screenshot_file(q, self.clean_data['screenshot'].filename, self.clean_data['screenshot'].content)
        q.save()
        return q.id