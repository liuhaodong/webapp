homework3 Feedback
==================

Commit graded: `948e2a3c367c5ed7ea1db19bc0237f0e61872936`

### Version control - Git (9/10)
  * -1, You should avoid submitting files (such as .pyc, ~, or .swp files) that are not part of your intentionally-submitted work.  Either manually stage each file (using git add) you want to commit, or use a .gitignore file to exclude files you never want to commit (such as compiled binary .pyc files).

### Iterative design (10/10)

### Implementation and functionality (83/85)

##### Routing and configuration (urls.py/settings.py)

##### Models (models.py)
  * -0 We suggest using a OneToOneField to a user because there should only be one instance of this object per user. Selecting the correct relation is important for database performance.

##### Views (views.py)

##### Authentication

##### Templates
  * -2, A GET request would be better suited for search. GET requests are not expected to change server state, and are allowed to be cacheable by browsers. POST requests are expected to modify the server state.
  * -0, You should remove the empty style tag from your header.

### Additional feedback

---

#### Total score (102/105)

---

Graded by: Salem Hilal (salem@cmu.edu)

To view this file with formatting, visit the following page: https://github.com/CMU-Web-Application-Development/haodongl/blob/master/grades/homework3.md
