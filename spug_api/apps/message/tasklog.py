from apps.message.models import  LoggerTaskRecord
import json

def tasksave(action,content,status):
    R = LoggerTaskRecord.objects.create(
        action_task=action,
        content=json.dumps(content),
        status=status
    )
    R.save()