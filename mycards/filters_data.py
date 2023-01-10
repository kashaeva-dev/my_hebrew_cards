from .models import Topic, Category

topics = []
for topic in Topic.objects.all():
     if topic.pk != 2:
         topic_info = dict()
         if topic.name != None:
             topic_name = ": " + str(topic.name)
         else:
             topic_name = ""
         topic_info['pk'] = topic.pk
         topic_info['name'] = str(topic.category) + topic_name
         topic_info['icon'] = topic.name_icon
         topics.append(topic_info)
         topics = sorted(topics, key=lambda topic: topic['name'], reverse=False)



