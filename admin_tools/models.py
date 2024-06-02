from django.db import models

class Document(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    doc_id = models.TextField()
    text = models.TextField()
    dataset_name = models.TextField(null=False)

    def __str__(self):
        return f"Document {self.doc_id}"
