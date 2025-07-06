import sqlite3

connection = sqlite3.connect("databse.db")
cursor = connection.cursor()

dummy_jobs = [
    (
        'TechNova Inc.', 'Software Engineer', 'Full-Time', 'Bangalore, India',
        'Develop and maintain web applications using modern frameworks.',
        'B.Tech', 'CSE, IT', 7.0, 2, 'Python, Django, SQL, Git',
        600000, 1000000, '2025-05-10', '2025-06-01'
    ),
    (
        'DataCore Solutions', 'Data Analyst', 'Full-Time', 'Hyderabad, India',
        'Analyze business data to derive actionable insights.',
        'B.Sc', 'Statistics, CSE', 6.5, 1, 'Excel, SQL, Python, Power BI',
        500000, 800000, '2025-05-11', '2025-06-10'
    ),
    (
        'InnovaTech', 'Backend Developer', 'Full-Time', 'Pune, India',
        'Build scalable backend services and APIs.',
        'B.Tech', 'CSE, IT', 7.2, 2, 'Node.js, Express, MongoDB',
        650000, 950000, '2025-05-12', '2025-06-15'
    ),
    (
        'GreenSoft Ltd.', 'QA Engineer', 'Full-Time', 'Chennai, India',
        'Conduct software testing and report bugs.',
        'B.Tech', 'CSE, ECE', 6.8, 3, 'Selenium, JIRA, Python',
        400000, 700000, '2025-05-12', '2025-06-05'
    ),
    (
        'BrightWare', 'Frontend Developer', 'Internship', 'Remote',
        'Create intuitive UIs with modern frontend technologies.',
        'B.Tech', 'CSE, IT', 7.5, 0, 'React, JavaScript, HTML, CSS',
        15000, 30000, '2025-05-10', '2025-05-30'
    ),
    (
        'CloudAxis', 'DevOps Engineer', 'Full-Time', 'Delhi, India',
        'Manage CI/CD pipelines and infrastructure automation.',
        'B.Tech', 'CSE, IT', 7.0, 1, 'AWS, Docker, Jenkins, Linux',
        700000, 1100000, '2025-05-09', '2025-06-12'
    ),
    (
        'CyberCore', 'Security Analyst', 'Full-Time', 'Mumbai, India',
        'Monitor and analyze security threats and incidents.',
        'B.Tech', 'CSE, IT', 7.5, 2, 'Wireshark, Python, SIEM Tools',
        800000, 1200000, '2025-05-11', '2025-06-20'
    ),
    (
        'NetFusion', 'Network Engineer', 'Full-Time', 'Kolkata, India',
        'Design and troubleshoot enterprise networks.',
        'B.Tech', 'CSE, ECE', 6.5, 2, 'Cisco, Networking, Linux',
        550000, 900000, '2025-05-10', '2025-06-07'
    ),
    (
        'AI Logic', 'Machine Learning Engineer', 'Full-Time', 'Remote',
        'Build and train ML models for various applications.',
        'M.Tech', 'CSE, ECE', 8.0, 1, 'Python, TensorFlow, Scikit-learn',
        900000, 1400000, '2025-05-08', '2025-06-14'
    ),
    (
        'FinSmart', 'Business Analyst', 'Full-Time', 'Gurgaon, India',
        'Bridge technical and business teams to improve services.',
        'MBA', 'Any', 6.0, 0, 'Excel, Tableau, SQL, Communication',
        600000, 950000, '2025-05-10', '2025-06-10'
    ),
    (
        'AlgoNext', 'Quantitative Analyst', 'Full-Time', 'Mumbai, India',
        'Develop and implement quantitative models for finance.',
        'B.Tech', 'Mathematics, CSE', 8.2, 0, 'Python, R, MATLAB',
        1000000, 1800000, '2025-05-12', '2025-06-15'
    ),
    (
        'MobiTech', 'Mobile App Developer', 'Full-Time', 'Bangalore, India',
        'Design and develop Android and iOS mobile apps.',
        'B.Tech', 'CSE, IT', 7.0, 1, 'Flutter, Kotlin, Swift',
        650000, 950000, '2025-05-11', '2025-06-05'
    ),
    (
        'EcoSoft', 'Environmental Data Analyst', 'Contract', 'Remote',
        'Analyze data for environmental impact assessments.',
        'B.Sc', 'Environmental Science, Statistics', 6.5, 1,
        'Excel, Python, R', 450000, 700000, '2025-05-09', '2025-06-09'
    ),
    (
        'Quantum Systems', 'AI Researcher', 'Full-Time', 'Remote',
        'Conduct research in AI/ML for cutting-edge applications.',
        'Ph.D', 'CSE, ECE', 9.0, 0, 'Python, PyTorch, Research Papers',
        1500000, 2500000, '2025-05-12', '2025-06-30'
    ),
    (
        'HealthLink', 'Bioinformatics Engineer', 'Full-Time', 'Hyderabad, India',
        'Develop tools and pipelines for genomic data analysis.',
        'M.Tech', 'Bioinformatics, CSE', 7.5, 1,
        'Python, R, Bioconductor', 800000, 1300000, '2025-05-10', '2025-06-20'
    ),
    (
        'RetailGenix', 'E-Commerce Analyst', 'Internship', 'Mumbai, India',
        'Support e-commerce analytics and dashboarding.',
        'BBA', 'Any', 6.0, 0, 'Excel, SQL, Google Analytics',
        10000, 20000, '2025-05-11', '2025-06-01'
    ),
    (
        'AutoBrain', 'Embedded Systems Engineer', 'Full-Time', 'Pune, India',
        'Develop firmware for automotive embedded systems.',
        'B.Tech', 'ECE, EEE', 7.0, 2, 'C, C++, RTOS, CAN',
        700000, 1100000, '2025-05-09', '2025-06-18'
    ),
    (
        'CloudHive', 'Cloud Architect', 'Full-Time', 'Delhi, India',
        'Design and oversee cloud architecture for enterprise apps.',
        'B.Tech', 'CSE, IT', 8.0, 1, 'AWS, Azure, Kubernetes',
        1200000, 2000000, '2025-05-10', '2025-06-25'
    ),
    (
        'SecureNet', 'Penetration Tester', 'Full-Time', 'Bangalore, India',
        'Perform security audits and penetration testing.',
        'B.Tech', 'CSE, IT', 7.5, 0, 'Metasploit, Kali Linux, Python',
        850000, 1300000, '2025-05-12', '2025-06-30'
    ),
    (
        'EduWorks', 'EdTech Content Developer', 'Part-Time', 'Remote',
        'Create technical learning content for students and professionals.',
        'Any', 'Any', 6.0, 3, 'Teaching, Python, Writing Skills',
        300000, 500000, '2025-05-11', '2025-06-15'
    )
]

cursor.executemany('''
    INSERT INTO jobs (
        company_name, job_title, job_type, location, job_description,
        degree_required, branch_required, min_cgpa, max_backlogs,
        skills_required, min_salary, max_salary, posting_date, deadline
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', dummy_jobs)

connection.commit()


import random
import string

def generate_password(length=8):
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    return ''.join(random.choice(chars) for _ in range(length))

company_names = [
    'TechNova Inc.', 'DataCore Solutions', 'InnovaTech', 'GreenSoft Ltd.',
    'BrightWare', 'CloudAxis', 'CyberCore', 'NetFusion',
    'AI Logic', 'FinSmart', 'AlgoNext', 'MobiTech', 'EcoSoft',
    'Quantum Systems', 'HealthLink', 'RetailGenix', 'AutoBrain',
    'CloudHive', 'SecureNet', 'EduWorks'
]

company_data = []

for name in company_names:
    company_data.append((
        name,
        f"https://www.{name.lower().replace(' ', '').replace('.', '')}.com",
        "Technology",
        "+91-9876543210",
        f"info@{name.lower().replace(' ', '').replace('.', '')}.com",
        "123 Tech Park",
        "Bangalore",
        "India",
        "Raj Sharma",
        "+91-9123456780",
        f"hr@{name.lower().replace(' ', '').replace('.', '')}.com",
        "Leading firm in tech and innovation.",
        "2010-01-01",
        random.randint(50, 500),
        f"/logos/{name.lower().replace(' ', '_').replace('.', '')}.png",
        generate_password()
    ))

cursor.executemany('''
    INSERT INTO companies (
        name, website, industry, phone, email,
        address, city, country, hr_name, hr_phone, hr_email,
        description, established_date, employees, logo_path, password
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', company_data)

import random
import string
from datetime import datetime, timedelta

def generate_password(length=8):
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    return ''.join(random.choice(chars) for _ in range(length))

def random_date(start, end):
    return (start + timedelta(days=random.randint(0, (end - start).days))).strftime('%Y-%m-%d')

first_names = ['Aarav', 'Sanya', 'Ishaan', 'Meera', 'Karan', 'Priya', 'Raj', 'Neha', 'Amit', 'Anika']
last_names = ['Sharma', 'Verma', 'Patel', 'Reddy', 'Khan', 'Singh', 'Joshi', 'Gupta', 'Das', 'Mehta']
branches = ['Computer Science', 'Electrical', 'Mechanical', 'Civil', 'Electronics']
degrees = ['B.Tech', 'M.Tech', 'B.Sc','M.Sc']

students = []

for i in range(10):
    fname = first_names[i]
    lname = last_names[i]
    email = f"{fname.lower()}.{lname.lower()}@university.edu"
    phone = f"+91-9{random.randint(100000000, 999999999)}"
    parent_phone = f"+91-8{random.randint(100000000, 999999999)}"
    dob = random_date(datetime(2000, 1, 1), datetime(2004, 12, 31))
    gender = random.choice(['Male', 'Female'])
    address = f"{random.randint(100,999)} Sample Street, Cityville"
    student_id = f"S{i+1001:04d}"
    degree = random.choice(degrees)
    branch = random.choice(branches)
    cgpas = [round(random.uniform(6.5, 9.5), 2) for _ in range(6)]
    cgpa_total = round(sum(cgpas) / len(cgpas), 2)
    backlogs = random.randint(0, 2)
    join_date = '2021-08-01'
    passout_date = '2025-05-31'
    resume_path = f"/resumes/{student_id}.pdf"
    password = generate_password()

    students.append((
        fname, lname, email, phone, dob, parent_phone, gender,
        address, student_id, degree, branch,
        cgpas[0], cgpas[1], cgpas[2], cgpas[3], cgpas[4], cgpas[5],
        cgpa_total, backlogs, join_date, passout_date,
        resume_path, password
    ))

cursor.executemany('''
    INSERT INTO students (
        first_name, last_name, email, phone, dob, parent_phone, gender,
        address, student_id, degree, branch,
        cgpa1, cgpa2, cgpa3, cgpa4, cgpa5, cgpa6,
        cgpa_total, backlogs, join_date, passout_date,
        resume_path, password, status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
''', students)

connection.commit()

# # Sample list of user skills
# user_skills = ['Python', 'Django', 'SQL', 'React', 'AWS']

# # Fetch all jobs
# cursor.execute("SELECT * FROM jobs")
# all_jobs = cursor.fetchall()

# # Get column names
# columns = [desc[0] for desc in cursor.description]

# # Helper to count matched skills
# def count_skill_matches(job_skills, user_skills):
#     if not job_skills:
#         return 0
#     job_skills_list = [skill.strip().lower() for skill in job_skills.split(',')]
#     return sum(1 for skill in user_skills if skill.lower() in job_skills_list)

# # List of (match_count, full_job_row)
# scored_jobs = [
#     (count_skill_matches(job[10], user_skills), job) for job in all_jobs  # index 10 = skills_required
# ]

# # Sort by match count descending
# sorted_jobs = sorted(scored_jobs, key=lambda x: x[0], reverse=True)

# # Extract only the job rows (discarding the match count)
# sorted_job_rows = [job for _, job in sorted_jobs]

# # Print all jobs sorted by matched skills
# print(sorted_job_rows)
