#!/usr/bin/env python3

from zube import client

CLIENT_ID = '16049ef4-e76b-11e9-9790-93aeddece9a7'
PRIVATE_KEY = './zube_api_key.pem'


def main():
    config = {
        'client_id': CLIENT_ID,
        'key_file': PRIVATE_KEY,
    }

    api = client.ZubeAPI(**config)
    api.authenticate()

    projects_incidents = 21525
    # args = {
    #     'project_id':   projects_incidents,
    #     'title':        'event',
    #     'category_id':  'category_pending',
    #     'labels':       'service_name',
    #     'priority':     'alert_rating', # p1 - p5
    #     'body':         'date/time: some comment text. Probably the SMS content',
    #     'assignees':    [],
    #     'comment':      'any further messages. [escalation, event_repeat]'
    # }
    # api.cards_create(project_id=projects_incidents, title='event')

    # args = {
    # }
    # print('Projects List:\n %s' % api.projects_list(**args))

    projects_operations = 17406
    args = {
        'order[direction]':     'asc',
        'order[by]':            'points',
        'select[]':             'title',
        'where[project_id]':    projects_incidents,
        'page':                 1,
    }
    print('Cards List:\n %s' % api.cards_list(**args))


if __name__ == "__main__":
    main()

# print('Cards List: %s' % api.cards_list(state='pending', category_name='operations'))

# TODO: document that you need to build a dictionary and unpack it with `**` like below,
#       if you use parameter names with braces in, eg. `order[by]` or `order[direction`

# TODO: BUG: doesn't accept multiple `select[]` statements
#       when we use a dictionary, as keys are unique
