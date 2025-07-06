import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from collections import defaultdict

def Generate_Graph():
    import sqlite3
    conn = sqlite3.connect('databse.db')
    cursor = conn.cursor()
    cursor.execute("select * from students")
    students = cursor.fetchall()
    total_students = len(students)
    # Convert to DataFrame for easier manipulation
    columns = ['id', 'first_name', 'last_name', 'email', 'phone1', 'dob', 'phone2', 
            'gender', 'address', 'student_id', 'degree', 'major', 'grade1', 'grade2', 
            'grade3', 'grade4', 'grade5', 'grade6', 'grade7', 'status', 
            'enrollment_date', 'graduation_date', 'resume_path', 'password', 'last_updated']

    df = pd.DataFrame(students, columns=columns)

    # Plot 1: Student Distribution by Degree Program
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, y='degree', order=df['degree'].value_counts().index, palette='viridis')
    plt.title('Student Distribution by Degree Program')
    plt.xlabel('Number of Students')
    plt.ylabel('Degree Program')
    plt.tight_layout()
    plt.savefig('static/stu/student_distribution_by_degree.png')
    plt.close()

    # Plot 2: Gender Distribution
    plt.figure(figsize=(8, 6))
    gender_counts = df['gender'].value_counts()
    plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', 
            colors=['skyblue', 'lightcoral'], startangle=90)
    plt.title('Gender Distribution of Students')
    plt.savefig('static/stu/gender_distribution.png')
    plt.close()

    # Plot 3: Average Grades by Major
    # Convert grade columns to numeric
    grade_cols = ['grade1', 'grade2', 'grade3', 'grade4', 'grade5', 'grade6', 'grade7']
    df[grade_cols] = df[grade_cols].apply(pd.to_numeric)

    # Calculate average grade for each student
    df['avg_grade'] = df[grade_cols].mean(axis=1)

    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='major', y='avg_grade', palette='Set2')
    plt.title('Distribution of Average Grades by Major')
    plt.xlabel('Major')
    plt.ylabel('Average Grade')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/stu/grades_by_major.png')
    plt.close()


    # Plot 3: Average Grades by Major
    # Convert grade columns to numeric
    grade_cols = ['grade1', 'grade2', 'grade3', 'grade4', 'grade5', 'grade6', 'grade7']
    df[grade_cols] = df[grade_cols].apply(pd.to_numeric)

    # Calculate average grade for each student
    df['avg_grade'] = df[grade_cols].mean(axis=1)

    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='major', y='avg_grade', palette='Set2')
    plt.title('Distribution of Average Grades by Major')
    plt.xlabel('Major')
    plt.ylabel('Average Grade')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/stu/grades_by_major.png')
    plt.close()

    # Plot 4: Enrollment Status Distribution
    status_map = {0: 'Inactive', 1: 'Active', 2: 'Graduated'}
    df['status_label'] = df['status'].map(status_map)

    plt.figure(figsize=(8, 6))
    sns.countplot(data=df, x='status_label', order=['Active', 'Inactive', 'Graduated'], 
                palette='pastel')
    plt.title('Student Enrollment Status')
    plt.xlabel('Status')
    plt.ylabel('Count')
    plt.savefig('static/stu/enrollment_status.png')
    plt.close()


    # Plot 5: Age Distribution
    from datetime import datetime

    # Calculate age from DOB
    df['dob'] = pd.to_datetime(df['dob'])
    current_year = datetime.now().year
    df['age'] = current_year - df['dob'].dt.year

    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='age', bins=10, kde=True, color='teal')
    plt.title('Age Distribution of Students')
    plt.xlabel('Age')
    plt.ylabel('Number of Students')
    plt.savefig('static/stu/age_distribution.png')
    plt.close()

    # Plot 6: Correlation Heatmap of Grades
    plt.figure(figsize=(10, 8))
    grade_corr = df[grade_cols].corr()
    sns.heatmap(grade_corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation Between Different Grade Components')
    plt.savefig('static/stu/grade_correlation.png')
    plt.close()


    # Plot 7: Gender Distribution by Major
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, x='major', hue='gender', palette='Set2')
    plt.title('Gender Distribution Across Majors')
    plt.xlabel('Major')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.legend(title='Gender')
    plt.tight_layout()
    plt.savefig('static/stu/gender_by_major.png')
    plt.close()