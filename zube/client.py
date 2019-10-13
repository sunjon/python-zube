from . import zube
from .bind import bind_method

# TODO: look into etag caching


class ZubeAPI(zube.AccessToken):
    host = 'https://zube.io'
    base_path = '/api'

    def __init__(self, **kwargs):
        # format = kwargs.get('format', 'json')
        # if format in SUPPORTED_FORMATS:
        #     self.format = format
        # else:
        #     raise Exception("Unsupported format")
        super(ZubeAPI, self).__init__(**kwargs)

    projects_list = bind_method(
        path='/projects',
        method='get',
        filter_parameters=[
            'account_id',
            'created_at',
            'id',
            'name',
            'private',
            'slug',
            'updated_at'
        ],
        response_type='list')

    cards_list = bind_method(
        path='/cards',
        method='get',
        filter_parameters=[
            'category_name',
            'closed_at',
            'closer_id',
            'comments_count',
            'created_at',
            'creator_id',
            'epic_id',
            'id',
            'last_comment_at',
            'number',
            'points',
            'priority',
            'project_id',
            'search_key',
            'sprint_id',
            'state',
            'status',
            'updated_at',
            'upvotes_count',
            'workspace_id',
        ],
        response_type='list')

    cards_create = bind_method(
        path='/cards',
        method='post',
        accepts_parameters=[
            'assignee_ids',
            'body',
            'category_name',
            'epic_id',
            'github_issue[milestone_id]',
            'github_issue[source_id]',
            'label_ids',
            'points',
            'priority',
            'project_id',
            'sprint_id',
            'title',
            'workspace_id',
        ],
        response_type='list')

    # cards_create = bind_method(
    #     path='/cards',
    #     method='POST',
    #     required_parameters=['project_id', 'title'],
    #     accepts_parameters=[
    #         'assignee_ids',
    #         'body',
    #         'category_name',
    #         'epic_id',
    #         'github_issue[milestone_id]',
    #         'github_issue[source_id]',
    #         'label_ids',
    #         'points',
    #         'priority',
    #         'sprint_id',
    #         'workspace_id',
    #     ],
    #     response_type="empty")

    # cards_get = bind_method(
    #     path='cards/L:card_id',
    #     method='get',
    #     required_parameters=[],
    # )

    # cards_update = bind_method(
    #     path='cards/L:card_id',
    #     method='PUT',
    #     required_parameters=[
    #         'assignee_ids',
    #         'body',
    #         'epic_id',
    #         'github_issue[milestone_id]',
    #         'label_ids',
    #         'points',
    #         'priority',
    #         'project_id',
    #         'sprint_id',
    #         'state',
    #         'title',
    #         'workspace_id',
    #     ],
    # )
