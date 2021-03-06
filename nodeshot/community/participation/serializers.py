from rest_framework import serializers,pagination

from django.contrib.auth import get_user_model
User = get_user_model()

from nodeshot.core.nodes.models import Node

from .models import NodeRatingCount, NodeParticipationSettings,LayerParticipationSettings,Comment, Vote, Rating


__all__ = [
    'CommentAddSerializer',
    'CommentListSerializer',
    'CommentSerializer',
    'NodeCommentSerializer',
    'ParticipationSerializer',
    'NodeParticipationSerializer',
    'RatingListSerializer',
    'RatingAddSerializer' ,
    'VoteListSerializer',
    'VoteAddSerializer',
    'PaginationSerializer',
    'LinksSerializer',
    'NodeParticipationSettingsSerializer',
    'NodeSettingsSerializer',
    'LayerParticipationSettingsSerializer',
    'LayerSettingsSerializer'
]


#Pagination serializers

class LinksSerializer(serializers.Serializer):
    
    next = pagination.NextPageField(source='*')
    prev = pagination.PreviousPageField(source='*')


class PaginationSerializer(pagination.BasePaginationSerializer):

    links = LinksSerializer(source='*')  # Takes the page object as the source
    total_results = serializers.Field(source='paginator.count')
    results_field = 'nodes'

#Comments serializers

class CommentAddSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment       
        fields= ('node', 'user', 'text', )
    
    
class CommentListSerializer(serializers.ModelSerializer):
    """ Comment serializer """
    node = serializers.Field(source='node.name')
    username = serializers.Field(source='user.username')
    
    class Meta:
        model = Comment
        fields = ('node','username', 'text','added')
        read_only_fields = ('added',)


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.Field(source='user.username')
    class Meta:
        model = Comment
        fields = ('username', 'text', 'added',)
      
  
class NodeCommentSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(source='comment_set')
    
    class Meta:
        model = Node
        fields = ('name', 'description', 'comments')
        
#Rating serializers
        
class RatingAddSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Rating       
        fields= ('node', 'user', 'value', )
    
    
class RatingListSerializer(serializers.ModelSerializer):
    """ Rating serializer """
    node = serializers.Field(source='node.name')
    username = serializers.Field(source='user.username')
    
    class Meta:
        model = Rating
        fields = ('node', 'username', 'value',)
        read_only_fields = ('added',)

#Vote serializers
        
class VoteAddSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Vote       
        fields= ('node', 'user', 'vote', )
    
    
class VoteListSerializer(serializers.ModelSerializer):
    """ Votes serializer """
    node = serializers.Field(source='node.name')
    username = serializers.Field(source='user.username')
    
    class Meta:
        model = Vote
        fields = ('node', 'username', 'vote',)
        read_only_fields = ('added',)   

#Participation serializers
 
class ParticipationSerializer(serializers.ModelSerializer):
    
        
    class Meta:
        model = NodeRatingCount
        fields = ('likes', 'dislikes', 'rating_count',
                  'rating_avg', 'comment_count')

    
class NodeParticipationSerializer(serializers.ModelSerializer):
    """ Node participation details"""

    participation = ParticipationSerializer(source='noderatingcount')
    
    class Meta:
        model=Node
        fields= ('name', 'slug', 'address', 'participation')
        
#Participation settings
 
class NodeSettingsSerializer(serializers.ModelSerializer):
    
        
    class Meta:
        model = NodeParticipationSettings
        fields = ('voting_allowed', 'rating_allowed', 'comments_allowed',)

    
class NodeParticipationSettingsSerializer(serializers.ModelSerializer):
    """ Node participation settings"""

    participation_settings = NodeSettingsSerializer(source='node_participation_settings')
    
    class Meta:
        model = Node
        fields = ('name', 'slug', 'address', 'participation_settings')


class LayerSettingsSerializer(serializers.ModelSerializer):
    
        
    class Meta:
        model = LayerParticipationSettings
        fields = ('voting_allowed', 'rating_allowed', 'comments_allowed',)

    
class LayerParticipationSettingsSerializer(serializers.ModelSerializer):
    """ Layer participation settings"""

    participation_settings = LayerSettingsSerializer(source='layer_participation_settings')
    
    class Meta:
        model=Node
        fields= ('name','slug', 'participation_settings')  


