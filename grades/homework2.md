homework2 Feedback
==================

Commit graded: c538c2dcf22bd10d024ae6ca4752d52711a03bba

### Routing and configuration (20/20)

Good job!

### Calculator functionality (5/20)

-0, Pressing a repeated operation should not result in the evaluation of the expression.
- For example, the following input "10 + + 5 =" should result in 15, rather than 25

-10, Your calculator crashes on "+ =" and "+ 5 =" input, the application should not crash as a result of any client provided information.

-5, Your calculator crashes when the hidden input fields are removed. The application should not crash as a result of any client provided information. You shouldn’t assume that clients will always send input in the format that you specify. HTTP requests can be very easily forged.

- See https://github.com/CMU-Web-Application-Development/haodongl/blob/7aa7d9a3e3faebb87a4650c7657d8cb12ac366c5/homework/2/webapps/calculator/views.py#L28
- You should always check that something exists in the request before using it.

Your calculator crashes on a string entered as a button value.

- See https://github.com/CMU-Web-Application-Development/haodongl/blob/7aa7d9a3e3faebb87a4650c7657d8cb12ac366c5/homework/2/webapps/calculator/views.py#L52
- For example, replace "1" with "wood" as the value of button 1 will result in a crash when the expression is evaluated.

Your calculator crashes on a non-numeric input in the hidden field.

- Same explanation as previous one.

### Calculator implementation (20/20)

Good job!

### Version control - Git (5/5)

Good job!

### Additional feedback

I was looking at your README, and in your steps you mention "2. python manage.py migrate". This command is usually only needed after you have made changes to your model. This is obviously something that you will be doing when  you write your application. This should not be a requirement for running the application.

---

#### Total score (50/65)

---

Graded by: Eliot Wong (eliotw@cmu.edu)

To view this file with formatting, visit the following page: https://github.com/CMU-Web-Application-Development/haodongl/blob/master/grades/homework2.md
