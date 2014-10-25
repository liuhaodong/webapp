This homework finishes Grumblr's implementation. New features are listed below

New Added Features:<br>
1. Include a photo when posting.<br>
2. Adding/Deleting comment using ajax without reloading whole page.<br>
3. Dynamically update (every 10s) following stream without reloading page.<br>
4. Change password when logged in.<br>
5. Reset password without logging in.<br>
6. Change database from SQLite to Postgres.<br>

How to Use:<br>
1. Import grumblr.json to your postgres database.<br>
2. python manage.py runserver<br>
3. visit localhost:8000<br>
4. Included test users are: haodongl, testuser1, testuser2, password: testpassword<br>

Note: After registration, the confirmation email will be printed on console. Copy and visit the printed confirmation link to activate your account.<br>
Note: When you follow a user, his/her posts will be displayed by clicking 'Following' tab in the navi-bar. To view your following post, click the "Following" tab<br>
Note: You can't follow yourself, because you can see your post in your homepage<br>
Note: Click 'Like' button to remove your Dislike on a post<br>
Note: Clike 'Comment' button to fold/unfold comment section<br>
Note: Click the cross-icon beside your comment to delete.<br>
Note: You need to be logged-in to search.<br>
Note: Click a user's icon to visit that user's home. Click Follow/Unfollow, Block/Unblock on the right-top side to perform certain actions. Click the small user icon beside Block/Unblock button to view user's profile.<br>
Note: Currently the recommended users are the users you are not following.<br>
