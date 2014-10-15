homework4 Feedback
==================

Commit graded: 42791bd3ec4b42443506101cee4325658c11524f

### Version control - Git (9/10)

  * -1, You should avoid submitting files (such as .pyc, ~, or .swp files) that are not part of your intentionally-submitted work. Either manually stage each file (using git add) you want to commit, or use a .gitignore file to exclude files you never want to commit (such as compiled binary .pyc files).

### Iterative development (27/30)

  * -3, The email confirmation pages do not seem to be based on your Grumblr design. All pages of a web app should have a unified look and feel.

### ORM usage (30/30)

  * -0, For following/blocking/disliking, it's not necessary to make a separate model for that relation unless you want to attach additional information to that relation. Instead, a better relation to use would be the [Many-to-many relationships](https://docs.djangoproject.com/en/dev/topics/db/examples/many_to_many/).

### Coverage of technologies (30/40)

##### Template inheritance

##### Django forms

  * -10, No Django forms apart from examples used. Using this feature improves your web app by encapsulating (and performing) input validation.

##### Image upload and dynamic display

##### Sending email

  * Hmm... *"Welcome to Simple Address Book."*

### Validation (20/20)

  * All input should be validated. For example, the email address entered in during registration is not validated.

### Design (0/0)

  * You should have a 'confirm password' field along with your 'password' field in the registration form to prevent user error.

### Additional feedback

---

#### Total score (116/130)

---

Graded by: Shannon Lee (sjl1@andrew.cmu.edu)

To view this file with formatting, visit the following page: https://github.com/CMU-Web-Application-Development/haodongl/blob/master/grades/homework4.md
