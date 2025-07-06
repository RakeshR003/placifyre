from flask import *
import os
import sqlite3
import random
import string
import smtplib
from email.message import EmailMessage
from werkzeug.utils import secure_filename
from datetime import datetime
from pyresparser import ResumeParser
from werkzeug.security import generate_password_hash, check_password_hash
import nltk
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def send_email(from_email_addr, from_email_pass, to_email_addr, subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['From'] = from_email_addr
    msg['To'] = to_email_addr
    msg['Subject'] = subject

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email_addr, from_email_pass)
    server.send_message(msg)
    server.quit()

# Database initialization
connection = sqlite3.connect('databse.db')
cursor = connection.cursor()

cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            dob DATE NOT NULL,
            parent_phone TEXT NOT NULL,
            gender TEXT NOT NULL,
            address TEXT NOT NULL,
            student_id TEXT NOT NULL,
            degree TEXT NOT NULL,
            branch TEXT NOT NULL,
            cgpa1 REAL NOT NULL,
            cgpa2 REAL NOT NULL,
            cgpa3 REAL NOT NULL,
            cgpa4 REAL NOT NULL,
            cgpa5 REAL NOT NULL,
            cgpa6 REAL NOT NULL,
            cgpa_total REAL NOT NULL,
            backlogs INTEGER DEFAULT 0,
            join_date DATE NOT NULL,
            passout_date DATE NOT NULL,
            resume_path TEXT,
            password TEXT NOT NULL,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

cursor.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            website TEXT,
            industry TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT NOT NULL,
            city TEXT NOT NULL,
            country TEXT NOT NULL,
            hr_name TEXT NOT NULL,
            hr_phone TEXT NOT NULL,
            hr_email TEXT NOT NULL,
            description TEXT,
            established_date TEXT,
            employees INTEGER,
            logo_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            password TEXT NOT NULL
        )
    ''')

cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            job_title TEXT NOT NULL,
            job_type TEXT NOT NULL,
            location TEXT NOT NULL,
            job_description TEXT NOT NULL,
            degree_required TEXT NOT NULL,
            branch_required TEXT NOT NULL,
            min_cgpa REAL,
            max_backlogs INTEGER,
            skills_required TEXT,
            min_salary REAL,
            max_salary REAL,
            posting_date TEXT NOT NULL,
            deadline TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

cursor.execute('''
        CREATE TABLE IF NOT EXISTS appliedjobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT,
            company_name TEXT NOT NULL,
            job_title TEXT NOT NULL,
            job_type TEXT NOT NULL,
            location TEXT NOT NULL,
            job_description TEXT NOT NULL,
            degree_required TEXT NOT NULL,
            branch_required TEXT NOT NULL,
            min_cgpa REAL,
            max_backlogs INTEGER,
            skills_required TEXT,
            min_salary REAL,
            max_salary REAL,
            posting_date TEXT NOT NULL,
            deadline TEXT NOT NULL,
            email TEXT,
            name TEXT,
            phone TEXT,
            CGPA TEXT,
            branch TEXT,
            cource TEXT,
            status TEXT
        )
    ''')

cursor.close()
connection.close()

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route("/studentlogin", methods = ['POST', 'GET'])
def studentlogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        data = [email]
        connection = sqlite3.connect('databse.db')
        cursor = connection.cursor()

        cursor.execute("select * from students where email = ?", data)
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        if result:
            if check_password_hash(result[-3], password):
                if result[-2] == 'pending':
                    return render_template('student.html', msg = 'approval status is pending')
                else:
                    otp = str(random.randint(1111, 9999))
                    session['otp'] = otp
                    session['user'] = result
                    send_email('placifya@gmail.com', 'eboc pggz yoca bfuy', email, 'Student Registration', f'Hi, {otp} is your one time password for login into student portal')
                    return render_template('verify.html')
            else:
                return render_template('student.html', msg = 'Entered wrong credantials')
        else:
            return render_template('student.html', msg = 'Entered wrong credantials')
    return render_template('student.html')

@app.route("/companylogin", methods = ['POST', 'GET'])
def companylogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        data = [email]
        connection = sqlite3.connect('databse.db')
        cursor = connection.cursor()

        cursor.execute("select * from companies where hr_email = ?", data)
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()

        if result:
            if check_password_hash(result[-1], password):
                session['company_name'] = result[1]
                session['cid'] = result[0]
                return redirect(url_for('companyhome'))
            else:
                return render_template('company.html', msg = 'Entered wrong credantials')
        else:
            return render_template('company.html', msg = 'Entered wrong credantials')
    return render_template('company.html')

@app.route('/companyhome')
def companyhome():
    conn = sqlite3.connect('databse.db')
    cursor = conn.cursor()

    cursor.execute("select * from appliedjobs where company_name = ? and status = 'accepted'", [session['company_name']])
    placed = cursor.fetchall()

    cursor.execute("select * from appliedjobs where company_name = ? and status = 'rejected'", [session['company_name']])
    unplaced = cursor.fetchall()

    cursor.execute("select * from appliedjobs where company_name = ? and status = 'pending'", [session['company_name']])
    pending = cursor.fetchall()

    cursor.execute("select * from companies where id = ?", [session['cid']])
    user = cursor.fetchone()
    return render_template('companypage.html', user=user, placed_count = len(placed), unplaced_count = len(unplaced), pending_count = len(pending))

@app.route("/adminlogin", methods = ['POST', 'GET'])
def adminlogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == 'admin@gmail.com' and password == 'admin123':
            return redirect(url_for('admindashboard'))
        else:
            return render_template('admin.html')
    return render_template('admin.html')

@app.route("/verify", methods = ['POST', 'GET'])
def verify():
    if request.method == 'POST':
        otp = str(request.form['otp'])

        if session['otp'] == otp:
            return redirect(url_for('studenthome'))
        else:
            return render_template('student.html', msg="Entered wrong OTP")
    return render_template('student.html')

@app.route('/studenthome')
def studenthome():
    conn = sqlite3.connect('databse.db')
    cursor = conn.cursor()
    cursor.execute("select * from students")
    students = cursor.fetchall()

    cursor.execute("select * from appliedjobs where email = ?", [session['user'][3]])
    applied = cursor.fetchall()

    cursor.execute("select * from appliedjobs where email = ? and status = 'accepted'", [session['user'][3]])
    placed = cursor.fetchall()

    cursor.execute("select * from appliedjobs where email = ? and status = 'rejected'", [session['user'][3]])
    unplaced = cursor.fetchall()

    cursor.execute("select * from appliedjobs where email = ? and status = 'pending'", [session['user'][3]])
    pending = cursor.fetchall()

    return render_template('studentpage.html', placed_count = len(placed), unplaced_count = len(unplaced), pending_count = len(pending), applied_jobs = len(applied), user = session['user'], name = session['user'][0], email = session['user'][1])

@app.route('/addstudent', methods=['GET', 'POST'])
def addstudent():
    if request.method == 'POST':
        personal_data = {
            'first_name': request.form['fname'],
            'last_name': request.form['lname'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'dob': request.form['dob'],
            'parent_phone': request.form['parent_phone'],
            'gender': request.form['gender'],
            'address': request.form['address']
        }
        
        academic_data = {
            'student_id': request.form['studentid'],
            'degree': request.form['degree'],
            'branch': request.form['branch'],
            'cgpa1': float(request.form['cgpa1']),
            'cgpa2': float(request.form['cgpa2']),
            'cgpa3': float(request.form['cgpa3']),
            'cgpa4': float(request.form['cgpa4']),
            'cgpa5': float(request.form['cgpa5']),
            'cgpa6': float(request.form['cgpa6']),
            'cgpa_total': float(request.form['cgpatotal']),
            'backlogs': int(request.form['backlogs'] or 0),
            'join_date': request.form['join'],
            'passout_date': request.form['passout']
        }
        
        # Handle file upload
        resume_path = None
        if 'resume' in request.files:
            file = request.files['resume']
            if file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to filename to avoid collisions
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}_{filename}"
                resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(resume_path)
            elif file.filename != '':
                flash('Only PDF files are allowed for resume upload', 'error')
                return redirect(url_for('home'))
        
        # Combine all data
        student_data = {
            **personal_data,
            **academic_data,
            'resume_path': resume_path
        }

        upper = random.choice(string.ascii_uppercase)
        lower = random.choice(string.ascii_lowercase)
        digit = random.choice(string.digits)
        special = random.choice(string.punctuation)
        remaining = random.choices(string.ascii_letters + string.digits + string.punctuation, k=4)
        password_list = [upper, lower, digit, special] + remaining
        random.shuffle(password_list)
        password = ''.join(password_list)
        hash_password = generate_password_hash(password)

        conn = sqlite3.connect('databse.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO students (
                first_name, last_name, email, phone, dob, parent_phone, gender, address,
                student_id, degree, branch,
                cgpa1, cgpa2, cgpa3, cgpa4, cgpa5, cgpa6, cgpa_total,
                backlogs, join_date, passout_date,
                resume_path, password, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            student_data['first_name'], student_data['last_name'], student_data['email'],
            student_data['phone'], student_data['dob'], student_data['parent_phone'],
            student_data['gender'], student_data['address'], student_data['student_id'],
            student_data['degree'], student_data['branch'],
            student_data['cgpa1'], student_data['cgpa2'], student_data['cgpa3'],
            student_data['cgpa4'], student_data['cgpa5'], student_data['cgpa6'],
            student_data['cgpa_total'], student_data['backlogs'],
            student_data['join_date'], student_data['passout_date'],
            student_data['resume_path'], hash_password, 'pending'
        ))
        
        conn.commit()
        conn.close()

        name = student_data['first_name']+' '+student_data['last_name']
        email = student_data['email']
        send_email('placifya@gmail.com', 'eboc pggz yoca bfuy', email, 'Student Registration', f'Hi {name}, Username: {email} and password: {password}. These are your login credantials for student portal')
        return redirect(url_for('home'))
    return render_template('addstudent.html')

@app.route('/studentlist')
def studentlist():
    search_query = request.args.get('search', '').strip()
    conn = sqlite3.connect('databse.db')
    cursor = conn.cursor()
    
    if search_query:
        # Search across all relevant text fields
        query = """
            SELECT * FROM students 
            WHERE 
                first_name LIKE ? OR 
                last_name LIKE ? OR 
                email LIKE ? OR 
                phone LIKE ? OR 
                student_id LIKE ? OR 
                degree LIKE ? OR 
                branch LIKE ? OR 
                address LIKE ? OR
                CAST(cgpa_total AS TEXT) LIKE ? OR
                CAST(backlogs AS TEXT) LIKE ?
            ORDER BY first_name, last_name
        """
        search_pattern = f'%{search_query}%'
        cursor.execute(query, (
            search_pattern, search_pattern, search_pattern,
            search_pattern, search_pattern, search_pattern,
            search_pattern, search_pattern, search_pattern,
            search_pattern
        ))
    else:
        cursor.execute("SELECT * FROM students ORDER BY first_name, last_name")
        
    students = cursor.fetchall()
    conn.close()
    return render_template('studentlist.html', 
                         students=students, 
                         search_query=search_query)

@app.route('/deletestudent/<Id>')
def deletestudent(Id):
    conn = sqlite3.connect('databse.db')
    cursor = conn.cursor()

    cursor.execute("select * from students where id = '"+str(Id)+"'")
    row = cursor.fetchone()
    email = row[3]
    name = row[1] +' '+ row[2] 
    send_email('placifya@gmail.com', 'eboc pggz yoca bfuy', email, 'Student Registration', f'Hi {name}, Your student registration profile rejected by admin. recreate your account')

    cursor.execute("delete from students where id = ?", [Id])
    conn.commit()
    cursor.execute("select * from students")
    students = cursor.fetchall()
    return render_template('studentlist.html', students=students)

@app.route('/acceptstudent/<Id>')
def acceptstudent(Id):
    conn = sqlite3.connect('databse.db')
    cursor = conn.cursor()
    cursor.execute("update students set status = 'accepted' where id = '"+str(Id)+"'")
    conn.commit()
    cursor.execute("select * from students where id = '"+str(Id)+"'")
    row = cursor.fetchone()
    email = row[3]
    name = row[1] +' '+ row[2] 
    send_email('placifya@gmail.com', 'eboc pggz yoca bfuy', email, 'Student Registration', f'Hi {name}, Your student registration profile accepted by admin. you can access student portal now')
    cursor.execute("select * from students")
    students = cursor.fetchall()
    return render_template('studentlist.html', students=students)

@app.route('/addcompany', methods=['GET', 'POST'])
def addcompany():
    if request.method == 'POST':
        name = request.form['name']
        website = request.form['website']
        industry = request.form['industry']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        city = request.form['city']
        country = request.form['country']
        hr_name = request.form['hr_name']
        hr_phone = request.form['hr_phone']
        hr_email = request.form['hr_email']
        description = request.form['description']
        established_date = request.form['established_date']
        employees = request.form['employees']
        
        file = request.files['logo']

        filename = secure_filename(file.filename)
        logo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(logo_path)
        logo_path = filename  # Store relative path

        upper = random.choice(string.ascii_uppercase)
        lower = random.choice(string.ascii_lowercase)
        digit = random.choice(string.digits)
        special = random.choice(string.punctuation)
        remaining = random.choices(string.ascii_letters + string.digits + string.punctuation, k=4)
        password_list = [upper, lower, digit, special] + remaining
        random.shuffle(password_list)
        password = ''.join(password_list)
        hash_password = generate_password_hash(password)
        conn = sqlite3.connect('databse.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO companies (
                name, website, industry, phone, email, address, city, country,
                hr_name, hr_phone, hr_email, description, established_date, employees, logo_path, password
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name, website, industry, phone, email, address, city, country,
            hr_name, hr_phone, hr_email, description, established_date, employees, logo_path, hash_password
        ))
        conn.commit()
        conn.close()
        
        send_email('placifya@gmail.com', 'eboc pggz yoca bfuy', hr_email, 'Company Registration', f'Hi {name}, Username: {hr_email} and password: {password}. These are your login credantials for company portal')
        return redirect(url_for('companylist'))
    return render_template('addcompany.html')

@app.route('/companylist')
def companylist():
    conn = sqlite3.connect('databse.db')
    cursor = conn.cursor()
    cursor.execute("select * from companies")
    companies = cursor.fetchall()
    return render_template('companylist.html', companies=companies)

@app.route('/deletecompany/<Id>')
def deletecompany(Id):
    conn = sqlite3.connect('databse.db')
    cursor = conn.cursor()
    cursor.execute("delete from companies where id = ?", [Id])
    conn.commit()
    cursor.execute("select * from companies")
    companies = cursor.fetchall()
    return render_template('companylist.html', companies=companies)

@app.route('/deletejob/<Id>')
def deletejob(Id):
    conn = sqlite3.connect('databse.db')
    cursor = conn.cursor()
    cursor.execute("delete from jobs where id = ?", [Id])
    conn.commit()
    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()
    conn.close()
    return render_template('joblist.html', jobs=jobs)

@app.route('/admindashboard')
def admindashboard():
    conn = sqlite3.connect('databse.db')
    cursor = conn.cursor()
    cursor.execute("select * from students")
    students = cursor.fetchall()
    total_students = len(students)
    cursor.execute("select * from companies")
    companies = cursor.fetchall()
    total_companies = len(companies)
    cursor.execute("select * from jobs")
    jobs = cursor.fetchall()
    total_jobs = len(jobs)
    cursor.execute("select * from appliedjobs")
    appliedjobs = cursor.fetchall()
    total_appliedjobs = len(appliedjobs)
    cursor.execute("select * from appliedjobs where status = 'pending'")
    pendingjobs = cursor.fetchall()
    total_pendingjobs = len(pendingjobs)
    cursor.execute("select * from appliedjobs where status = 'accepted'")
    acceptedjobs = cursor.fetchall()
    total_acceptedjobs = len(acceptedjobs)
    cursor.execute("select * from appliedjobs where status = 'rejected'")
    rejectedjobs = cursor.fetchall()
    total_rejectedjobs = len(rejectedjobs)

    cursor.execute("select * from students where degree = 'B.Tech'")
    btech = len(cursor.fetchall())

    cursor.execute("select * from students where degree = 'M.Tech'")
    mtech = len(cursor.fetchall())

    cursor.execute("select * from students where degree = 'B.Sc'")
    bsc = len(cursor.fetchall())

    cursor.execute("select * from students where degree = 'M.Sc'")
    msc = len(cursor.fetchall())

    return render_template('admindashboard.html', degree = [btech, mtech, bsc, msc], total_rejectedjobs=total_rejectedjobs, total_acceptedjobs=total_acceptedjobs, total_pendingjobs=total_pendingjobs, total_appliedjobs=total_appliedjobs, total_jobs=total_jobs, total_students=total_students, total_companies=total_companies)

@app.route('/postjob', methods=['GET', 'POST'])
def postjob():
    if request.method == 'POST':
        # Get form data
        job_data = {
            'job_title': request.form['job_title'],
            'job_type': request.form['job_type'],
            'location': request.form['location'],
            'job_description': request.form['job_description'],
            'degree_required': request.form['degree_required'],
            'branch_required': request.form['branch_required'],
            'min_cgpa': float(request.form['min_cgpa']) if request.form['min_cgpa'] else None,
            'max_backlogs': int(request.form['max_backlogs']) if request.form['max_backlogs'] else None,
            'skills_required': request.form['skills_required'],
            'min_salary': float(request.form['min_salary']) if request.form['min_salary'] else None,
            'max_salary': float(request.form['max_salary']) if request.form['max_salary'] else None,
            'posting_date': request.form['posting_date'],
            'deadline': request.form['deadline']
        }

        # Validate dates
        posting_date = datetime.strptime(job_data['posting_date'], '%Y-%m-%d')
        deadline = datetime.strptime(job_data['deadline'], '%Y-%m-%d')

        conn = sqlite3.connect('databse.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO jobs (
                company_name, job_title, job_type, location, job_description,
                degree_required, branch_required, min_cgpa, max_backlogs, skills_required,
                min_salary, max_salary, posting_date, deadline
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
        ''', (
            session['company_name'], job_data['job_title'], job_data['job_type'], job_data['location'],
            job_data['job_description'], job_data['degree_required'],
            job_data['branch_required'], job_data['min_cgpa'],
            job_data['max_backlogs'], job_data['skills_required'],
            job_data['min_salary'], job_data['max_salary'],
            job_data['posting_date'], job_data['deadline']
        ))
        
        conn.commit()
        conn.close()
        return redirect(url_for('joblist'))
    return render_template('postjob.html')

@app.route('/updatejob', methods=['GET', 'POST'])
def updatejob():
    if request.method == 'POST':
        job_data = {
        'job_id': request.form['job_id'],
        'job_title': request.form['job_title'],
        'job_type': request.form['job_type'],
        'location': request.form['location'],
        'job_description': request.form['job_description'],
        'degree_required': request.form['degree_required'],
        'branch_required': request.form['branch_required'],
        'min_cgpa': float(request.form['min_cgpa']) if request.form['min_cgpa'] else None,
        'max_backlogs': int(request.form['max_backlogs']) if request.form['max_backlogs'] else None,
        'skills_required': request.form['skills_required'],
        'min_salary': float(request.form['min_salary']) if request.form['min_salary'] else None,
        'max_salary': float(request.form['max_salary']) if request.form['max_salary'] else None,
        'posting_date': request.form['posting_date'],
        'deadline': request.form['deadline']
    }

    # Validate dates
    posting_date = datetime.strptime(job_data['posting_date'], '%Y-%m-%d')
    deadline = datetime.strptime(job_data['deadline'], '%Y-%m-%d')

    conn = sqlite3.connect('databse.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE jobs SET
            job_title = ?,
            job_type = ?,
            location = ?,
            job_description = ?,
            degree_required = ?,
            branch_required = ?,
            min_cgpa = ?,
            max_backlogs = ?,
            skills_required = ?,
            min_salary = ?,
            max_salary = ?,
            posting_date = ?,
            deadline = ?
        WHERE id = ?
    ''', (
        job_data['job_title'],
        job_data['job_type'],
        job_data['location'],
        job_data['job_description'],
        job_data['degree_required'],
        job_data['branch_required'],
        job_data['min_cgpa'],
        job_data['max_backlogs'],
        job_data['skills_required'],
        job_data['min_salary'],
        job_data['max_salary'],
        job_data['posting_date'],
        job_data['deadline'],
        job_data['job_id']
    ))

    conn.commit()
    conn.close()
    return redirect(url_for('joblist'))

@app.route('/joblist')
def joblist():
    conn = sqlite3.connect('databse.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM jobs where company_name = ?", [session['company_name']])
    jobs = cursor.fetchall()
    conn.close()
    
    return render_template('joblist.html', jobs=jobs)

@app.route('/viewrequests/<Id>')
def viewrequests(Id):
    conn = sqlite3.connect('databse.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM appliedjobs where job_id = ?", [Id])
    jobs = cursor.fetchall()
    conn.close()
    
    return render_template('viewrequests.html', jobs=jobs)

@app.route('/editjob/<Id>')
def editjob(Id):
    conn = sqlite3.connect('databse.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM jobs where id = ?", [Id])
    job = cursor.fetchone()
    conn.close()
    return render_template('editjob.html', job=job)

@app.route('/jobs')
def jobs():
    conn = sqlite3.connect('databse.db')
    cursor = conn.cursor()
    
    file = list(session['user'])[22].replace('\\', '/')
    data = ResumeParser(file).get_extracted_data()
    user_skills = data['skills']

    # Fetch all jobs
    cursor.execute("SELECT * FROM jobs")
    all_jobs = cursor.fetchall()

    # Helper to count matched skills
    def count_skill_matches(job_skills, user_skills):
        if not job_skills:
            return 0
        job_skills_list = [skill.strip().lower() for skill in job_skills.split(',')]
        return sum(1 for skill in user_skills if skill.lower() in job_skills_list)

    # List of (match_count, full_job_row)
    scored_jobs = [
        (count_skill_matches(job[10], user_skills), job) for job in all_jobs  # index 10 = skills_required
    ]

    # Sort by match count descending
    sorted_jobs = sorted(scored_jobs, key=lambda x: x[0], reverse=True)

    return render_template('jobs.html', jobs=sorted_jobs)

@app.route('/appliedjobs')
def appliedjobs():
    conn = sqlite3.connect('databse.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM appliedjobs where email = ?", [list(session['user'])[3]])
    jobs = cursor.fetchall()
    conn.close()
    
    return render_template('appliedjobs.html', jobs=jobs)

@app.route('/apply/<Id>')
def apply(Id):
    conn = sqlite3.connect('databse.db')
    cursor = conn.cursor()
    cursor.execute("select * from appliedjobs where job_id = ? and email = ?", [Id, list(session['user'])[3]])
    res = cursor.fetchall()
    if res:
        file = list(session['user'])[22].replace('\\', '/')
        data = ResumeParser(file).get_extracted_data()
        user_skills = data['skills']

        # Fetch all jobs
        cursor.execute("SELECT * FROM jobs")
        all_jobs = cursor.fetchall()

        # Helper to count matched skills
        def count_skill_matches(job_skills, user_skills):
            if not job_skills:
                return 0
            job_skills_list = [skill.strip().lower() for skill in job_skills.split(',')]
            return sum(1 for skill in user_skills if skill.lower() in job_skills_list)

        scored_jobs = [
            (count_skill_matches(job[10], user_skills), job) for job in all_jobs
        ]
        sorted_jobs = sorted(scored_jobs, key=lambda x: x[0], reverse=True)

        return render_template('jobs.html', jobs=sorted_jobs, msg="You are already applied for this job")
    
    else:
        cursor.execute("select * from appliedjobs where status = 'accepted' and email = ?", [list(session['user'])[3]])
        res2 = cursor.fetchall()
        if len(res2) == 2:
            file = list(session['user'])[22].replace('\\', '/')
            data = ResumeParser(file).get_extracted_data()
            user_skills = data['skills']

            cursor.execute("SELECT * FROM jobs")
            all_jobs = cursor.fetchall()

            def count_skill_matches(job_skills, user_skills):
                if not job_skills:
                    return 0
                job_skills_list = [skill.strip().lower() for skill in job_skills.split(',')]
                return sum(1 for skill in user_skills if skill.lower() in job_skills_list)

            scored_jobs = [
                (count_skill_matches(job[10], user_skills), job) for job in all_jobs
            ]
            sorted_jobs = sorted(scored_jobs, key=lambda x: x[0], reverse=True)
            return render_template('jobs.html', jobs=sorted_jobs, msg="You are already selected for 2 jobs. limit exceeded")
        else:
            cursor.execute("select * from jobs where id = ?", [int(Id)])
            row = list(cursor.fetchone())[:-1]
            row.append(list(session['user'])[3])
            row.append(list(session['user'])[1]+' '+list(session['user'])[2])
            row.append(list(session['user'])[4])
            row.append(list(session['user'])[18])
            row.append(list(session['user'])[10])
            row.append(list(session['user'])[11])
            row.append('pending')

            cursor.execute("insert into appliedjobs values (NULL, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", row)
            conn.commit()

            return redirect(url_for('appliedjobs'))

@app.route('/Accept/<Id>')
def Accept(Id):
    conn = sqlite3.connect('databse.db')
    cursor = conn.cursor()
    cursor.execute("update appliedjobs set status = 'accepted' where id = ?", [Id])
    conn.commit()
    return redirect(url_for('joblist'))

@app.route('/Reject/<Id>')
def Reject(Id):
    conn = sqlite3.connect('databse.db')
    cursor = conn.cursor()
    cursor.execute("update appliedjobs set status = 'rejected' where id = ?", [Id])
    conn.commit()
    return redirect(url_for('joblist'))

@app.route('/resetpassword', methods = ['POST', 'GET'])
def resetpassword():
    if request.method == 'POST':
        conn = sqlite3.connect('databse.db')
        cursor = conn.cursor()
        password = request.form['password']
        hash_password = generate_password_hash(password)
        cursor.execute("update students set password = ? where id = ?", [hash_password, list(session['user'])[0]])
        conn.commit()
        return render_template('index.html', msg="Password reset successfully")
    return render_template('resetpassword.html')

@app.route('/companypassword', methods = ['POST', 'GET'])
def companypassword():
    if request.method == 'POST':
        conn = sqlite3.connect('databse.db')
        cursor = conn.cursor()
        password = request.form['password']
        hash_password = generate_password_hash(password)
        cursor.execute("update companies set password = ? where id = ?", [hash_password, session['cid']])
        conn.commit()
        return render_template('index.html', msg="Password reset successfully")
    return render_template('companypassword.html')

@app.route('/analyse', methods = ['POST', 'GET'])
def analyse():
    if request.method == 'POST':
        conn = sqlite3.connect('databse.db')
        cursor = conn.cursor()
        file = request.form['file']
        data = ResumeParser('static/uploads/'+file).get_extracted_data()
        resumes = []
        if data['name']:
            resumes.append(f"Name: {data['name']}")
        if data['email']:
            resumes.append(f"Email: {data['email']}")
        if data['mobile_number']:
            resumes.append(f"Mobile Number: {data['mobile_number']}")
        if data['skills']:
            resumes.append(f"Skills: {data['skills']}")
        if data['college_name']:
            resumes.append(f"College Name: {data['college_name']}")
        if data['degree']:
            resumes.append(f"Degree: {data['degree']}")
        if data['company_names']:
            resumes.append(f"Company Names: {data['company_names']}")
        if data['no_of_pages']:
            resumes.append(f"No Of Pages: {data['no_of_pages']}")
        if data['total_experience']:
            resumes.append(f"Total Experience: {data['total_experience']}")

        import pickle
        import re

        # Load the trained classifier
        clf = pickle.load(open('clf.pkl', 'rb'))
        tfidf = pickle.load(open('tfidf.pkl', 'rb'))

        def cleanResume(txt):
            cleanText = re.sub(r'http\S+\s', ' ', txt)
            cleanText = re.sub(r'RT|cc', ' ', cleanText)
            cleanText = re.sub(r'#\S+\s', ' ', cleanText)
            cleanText = re.sub(r'@\S+', '  ', cleanText)  
            cleanText = re.sub(r'[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleanText)
            cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText) 
            cleanText = re.sub(r'\s+', ' ', cleanText)
            return cleanText

        # Clean the input resume
        cleaned_resume = cleanResume(str(resumes))

        # Transform the cleaned resume using the trained TfidfVectorizer
        input_features = tfidf.transform([cleaned_resume])

        # Make the prediction using the loaded classifier
        prediction_id = clf.predict(input_features)[0]

        # Map category ID to category name
        category_mapping = {
            15: "Java Developer",
            23: "Testing",
            8: "DevOps Engineer",
            20: "Python Developer",
            24: "Web Designing",
            12: "HR",
            13: "Hadoop",
            3: "Blockchain",
            10: "ETL Developer",
            18: "Operations Manager",
            6: "Data Science",
            22: "Sales",
            16: "Mechanical Engineer",
            1: "Arts",
            7: "Database",
            11: "Electrical Engineering",
            14: "Health and fitness",
            19: "PMO",
            4: "Business Analyst",
            9: "DotNet Developer",
            2: "Automation Testing",
            17: "Network Security Engineer",
            21: "SAP Developer",
            5: "Civil Engineer",
            0: "Advocate",
        }

        category_name = category_mapping.get(prediction_id, "Unknown")

        resumes.append(f'Recommended Job is : {category_name}')
        return render_template('analyse.html', resumes=resumes)
    return render_template('analyse.html')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)