from github3 import GitHub

f = open('file.html', 'w')
fp = open('template', 'rb')
not_specified = "Not Specified"

def initialize(count):
    f.write(fp.read())
    f.write("")
    f.write("<h2>&nbspTop {} Matching GitHub Profiles</h2><br />".format(count))


def generate_linkedin_query(name, location):
    first_name = name.split(' ')[0]
    last_name = name.split(' ')[1] if len(name.split(' ')) >= 2 else None

    city = location.split(',')[0].strip()
    city = city.split('Metro')[1].strip() if 'Metro' in city else city

    query = None
    if first_name and last_name and city:
        query = "https://www.linkedin.com/vsearch/f?type=all&keywords={}+{}+{}&orig=GLHD&rsid=&pageKey=oz-winner&trkInfo=tarId%3A1472482173239&trk=global_header&search=Search".format(first_name, last_name, city)
    return query


def format_html(usr, contributions, stackoverflow_url):

    if usr.company == None or 'Hooklogic' not in usr.company and 'HookLogic' not in usr.company:
        f.write("<div class='col-md-12'>")
        f.write("<div class='col-md-2'>")
        f.write("<img src='{}' alt='defaultIcon.png' height='150' width='150'>".format(usr.avatar_url))
        f.write("<h5>&nbsp&nbsp&nbsp<a href='{}'>GitHub Profile</h5></a>".format(usr.html_url))
        query = generate_linkedin_query(usr.name, usr.location)

        if query:
            f.write("<h5>&nbsp&nbsp&nbsp<a href='{}'>LinkedIn Profile</h5></a>".format(query))
        
        if stackoverflow_url != '':
            f.write("<h5>&nbsp&nbsp&nbsp<a href='{}'>Stackoverflow Profile</h5></a>".format(stackoverflow_url))
        f.write("<br /><br /></div>")
        f.write("<div class='col-md-3'>")
        f.write("<b>Name:</b> {}<br />".format(usr.name))
        f.write("<b>Login:</b> {}<br />".format(usr.login))
        f.write("<b>Email Id:</b> {} <br />".format(usr.email if usr.email != None else not_specified))
        f.write("<b>Company:</b> {}<br />".format(usr.company if usr.company != None else not_specified))
        f.write("<b>City:</b> {}<br />".format(usr.location))
        f.write("<b>GitHub user since:</b> {}<br />".format(usr.created_at.date()))
        f.write("<b>GitHub contributions:</b> {}".format(contributions))
        f.write("</div></div></div>")


def save_file():
    f.write("</body>")
    f.write("</html>")
    f.close()
