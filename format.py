from github3 import GitHub

f = open('file.html', 'w')
fp = open('template', 'rb')

f.write(fp.read())
f.write("")


def format_html(usr, contributions):
    f.write("<div class='col-md-12'>")
    f.write("<div class='col-md-2'>")
    f.write("<img src='{}' alt='Smiley face' height='150' width='150'>".format(usr.avatar_url))
    f.write("<h3><a href='{}'>&nbsp&nbspView Profile</h3></a> <br />".format(usr.html_url))
    f.write("</div>")
    f.write("<div class='col-md-3'>")
    f.write("<b>Name:</b> {}<br />".format(usr.name))
    f.write("<b>Login:</b> {}<br />".format(usr.login))
    f.write("<b>Email Id:</b> {} <br />".format(usr.email))
    f.write("<b>Company:</b> {}<br />".format(usr.company))
    f.write("<b>City:</b> {}<br />".format(usr.location))
    f.write("<b>GitHub user since:</b> {}<br />".format(usr.created_at.date()))
    f.write("<b>Contributions:</b> {}".format(contributions))
    f.write("</div></div></div>")
    # TODO Add LinkedIn profile URL if possible


def save_file():
    f.write("</body>")
    f.write("</html>")
    f.close()
