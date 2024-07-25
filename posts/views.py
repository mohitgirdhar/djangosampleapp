from rest_framework import authentication, permissions
from .models import Post, Comment, PostLikes
from rest_framework import generics
from .serializers import PostLikeSerializer, PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

from rest_framework import viewsets, status
from rest_framework.response import Response


class PostView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating posts.

    **Permissions:**
        - Requires authentication using a token (TokenAuthentication).
        - Only authenticated users can access this endpoint (IsAuthenticated).

    **List (GET):**
        - Retrieves a list of all posts.
        - Response includes serialized data for each post.

    **Create (POST):**
        - Creates a new post.
        - Requires valid user authentication and authorization.
        - Request body should contain data in the format specified by `PostSerializer`.
        - Response includes the serialized data of the newly created post.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a specific post.

    **Permissions:**
        - Requires authentication using a token (TokenAuthentication).
        - Only the authenticated user who owns the post can update or delete it (IsAuthenticated, IsOwnerOrReadOnly).

    **Retrieve (GET):**
        - Retrieves a specific post based on its ID.
        - Response includes the serialized data of the retrieved post.

    **Update (PUT):**
        - Updates an existing post.
        - Requires valid user authentication and ownership of the post.
        - Request body should contain data in the format specified by `PostSerializer`.
        - Response includes the serialized data of the updated post.

    **Delete (DELETE):**
        - Deletes an existing post.
        - Requires valid user authentication and ownership of the post.
        - Response includes a success message upon successful deletion.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating comments on a specific post.

    **Permissions:**
        - Requires authentication using a token (TokenAuthentication).
        - Only authenticated users can access this endpoint (IsAuthenticated).

    **List (GET):**
        - Retrieves a list of comments for a specific post based on its Post ID.
        - Request URL should include the post ID using the `lookup_field` (`post_id` by default).
        - Response includes serialized data for each comment associated with the post.

    **Create (POST):**
        - Creates a new comment under the specified post.
        - Requires valid user authentication.
        - Request body should contain data in the format specified by `CommentSerializer`.
        - Response includes the serialized data of the newly created comment.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "post_id"


class PostLikeViewSet(viewsets.ViewSet):
    """
    API endpoint for liking and unliking posts.
    """

    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, pk=None):
        """
        Likes a post.

        **Permissions:**
            - Requires authentication (IsAuthenticated).

        **Request:**
            - The URL should include the post ID (`pk`).
            - Request body is empty (no data required).

        **Response:**
            - Status code 201 Created upon successful like.
            - Status code 400 Bad Request if the post doesn't exist or the user already liked it.
        """

        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_400_BAD_REQUEST)

        if PostLikes.objects.filter(user=request.user, post=post).exists():
            return Response({"error": "You already liked this post"}, status=status.HTTP_400_BAD_REQUEST)

        like = PostLikes.objects.create(user=request.user, post=post)
        serializer = PostLikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        """
        Unlikes a post.

        **Permissions:**
            - Requires authentication (IsAuthenticated).

        **Request:**
            - The URL should include the post ID (`pk`).
            - Request body is empty (no data required).

        **Response:**
            - Status code 204 No Content upon successful unlike.
            - Status code 400 Bad Request if the post doesn't exist or the user didn't like it.
        """

        try:
            like = PostLikes.objects.get(user=request.user, post=pk)
        except PostLikes.DoesNotExist:
            return Response({"error": "You haven't liked this post"}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
