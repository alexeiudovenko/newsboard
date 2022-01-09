from rest_framework import serializers

from newsboard.models import Post, Comment, Voted

from django.db.models import F


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    post_comment = CommentSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = "__all__"


class VotedSerializer(serializers.ModelSerializer):
    voted = serializers.HiddenField(default=True)

    def validate(self, attrs):
        if not Voted.objects.filter(
            user_voted=attrs["user_voted"], post_voted=attrs["post_voted"], voted=True
        ):
            attrs["post_voted"].votes = F("votes") + 1
            attrs["post_voted"].save()
            return super().validate(attrs)
        raise serializers.ValidationError()

    class Meta:
        model = Voted
        fields = "__all__"
