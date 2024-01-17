import mysql.connector
from faker import Faker
import random
from datetime import datetime
import csv 
def createConnection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="job_application_tracker"
    )
    cursor = connection.cursor()
    return cursor,connection

def display(cursor):
    tableName = input("Enter name of Table to display (Applications / Applicants / Jobs): ").lower()
    if tableName=="applications":
        cursor.execute("SELECT * FROM applications")
        result3 = cursor.fetchall()
        for row in result3:
            print(row)
    elif tableName == "applicants":
        cursor.execute("SELECT * FROM applicants")
        result1 = cursor.fetchall()
        for row in result1:
            print(row)
    elif tableName == "jobs":
        cursor.execute("SELECT * FROM jobs")
        result2 = cursor.fetchall()
        for row in result2:
            print(row)
    else:
        print("{tableName} not found in database")
        
def generateApplicantsTable(fake, cursor,connection):
    cursor.execute("SELECT COUNT(*) FROM applicants")
    current_count = cursor.fetchone()[0]

    if current_count<100:
        for _ in range(100):
            name = fake.name()
            email = fake.email()
            phone = fake.phone_number()
            query = "INSERT INTO applicants(name,email,phone) VALUES(%s,%s,%s)"
            cursor.execute(query, (name, email, phone))
    connection.commit()

def generateJobsTable(fake, cursor,connection):
    cursor.execute("SELECT COUNT(*) FROM jobs")
    current_count = cursor.fetchone()[0]
    if current_count<100:
        for _ in range(100):
            title = fake.job()
            company = fake.company()
            location = fake.city()
            posting_date = fake.date_between(start_date="-45d", end_date='today')
            query = "INSERT INTO jobs(title,company,location,posting_date) VALUES(%s,%s,%s,%s)"
            cursor.execute(query, (title, company, location, posting_date))
    connection.commit()
    
def generateApplicationsTable(fake, cursor, connection):
    # Fetch existing applicant_ids from the applicants table
    cursor.execute("SELECT applicant_id FROM applicants LIMIT 100")
    current_count = cursor.fetchone()[0]
    existing_applicant_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("Select COUNT(applicant_id) from applications")
    count = cursor.fetchone()[0]
    if count<100:    
        for _ in range(100):
            application_date = fake.date_between(start_date="-45d", end_date='today')
            status = random.choice(["Accepted", "Pending", "Rejected"])

            # Choose a valid applicant_id from existing values
            applicant_id = random.choice(existing_applicant_ids)

            # Choose a random job_id (ensure it exists in the jobs table)
            cursor.execute("SELECT job_id FROM jobs")
            existing_job_ids = [row[0] for row in cursor.fetchall()]
            job_id = random.choice(existing_job_ids)

            query = "INSERT INTO applications(applicant_id, job_id, application_date, status) VALUES(%s, %s, %s, %s)"
            cursor.execute(query, (applicant_id, job_id, application_date, status))

    connection.commit()

def addApplication(cursor,connection):
    print("Add Application details: ")
    applicant_name = input("Enter name of Applicant: ")
    email = input("Enter Email: ")
    phone = input("Enter Phone Number: ")
    job_title = input("Enter job Title: ")
    company = input("Enter Company name: ")
    location = input("Enter Location: ")
    # check for existing Applicant
    query = "SELECT applicant_id FROM applicants where name=%s and email = %s"
    cursor.execute(query,(applicant_name,email))
    existingApplicant = cursor.fetchone()
    if not existingApplicant:
        query = "Insert INTO applicants(name,email,phone) VALUES(%s,%s,%s)"
        cursor.execute(query,(applicant_name,email,phone))
        connection.commit()
        applicant_id=cursor.lastrowid
        print("Applicant ID is ",applicant_id)
    else:
        print("Applicant exists")
        applicant_id=existingApplicant[0]
    
    # check for existing job
    query = "SELECT job_id FROM jobs where title=%s and company = %s"
    cursor.execute(query,(job_title,company))
    existingJob = cursor.fetchone()
    if not existingJob:
        query = "Insert INTO jobs(title,company,location) VALUES(%s,%s,%s)"
        cursor.execute(query,(job_title,company,location))
        connection.commit()
        job_id=cursor.lastrowid
        print("Job ID is ",job_id)

    else:
        print("Job exists")
        job_id=existingJob[0]
    
    query="INSERT INTO applications(applicant_id,job_id,application_date,status) VALUES(%s,%s,%s,%s)"
    application_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "Pending"
    cursor.execute(query,(applicant_id,job_id,application_date,status))
    connection.commit()
    print("Application submitted successfully")
        
def updateStatus(cursor,connection):
    app_id = input("Enter ApplicationID to update: ")
    # check if the applicantion ID exists
    query = "SELECT * FROM application WHERE application_id=%s"
    cursor.execute(query,(app_id))
    application=cursor.fetchone()
    if application:
        new_status = input("Enter the updated status: ")
        # Validate the status
        if new_status.lower() not in ["accepted", "rejected", "pending"]:
            print("Invalid status. Please enter Accepted, Rejected, or Pending.")
            return
            query= "UPDATE applications SET status = %s WHERE application_id=%s"
        cursor.execute(query,(new_status,app_id))
        connection.commit()
        print("Application Updated")
    else:
        print("Application with ID {app_id} not found")
    
def deleteApplication(cursor,connection):
    app_id = input("Enter the ID of Application to delete: ")
    # check if the applicantion ID exists
    query = "SELECT * FROM application WHERE application_id=%s"
    cursor.execute(query,(app_id))
    application=cursor.fetchone()
    if application:
        query = "DELETE FROM applications WHERE application_id = %s"
        cursor.execute(query,(app_id))
        connection.commit()
        print("Application Deleted")
    else:
        print("Application with ID {app_id} not found")

def filterApplication(cursor,connection):
    print("1. By Status")
    print("2. By Applicant")
    print("3. By Job")
    choice = input("Enter your choice (1-3): ")    
    if choice=="1":
        # filter by status
        status = input("Enter Status to filter by(Accepted/Rejected/Pending)")
        query="""SELECT applications.application_id,applicants.name,jobs.title,applications.application_date,applications.status FROM applications JOIN applicants ON applications.applicant_id=applicants.applicant_id JOIN jobs ON applications.job_id = jobs.job_id WHERE applications.status = %s"""
        cursor.execute(query,(status,))
        print("hello")
        result= cursor.fetchall()
        connection.commit()
        if result:
            print("Filtered Applications: ")
            for row in result:
                print(row)
        else:
            print("No applications found")
    elif choice=="2":
        name = input("Enter the name of the applicant to filter by: ")
        query = "SELECT applications.application_id,applicants.name,jobs.title,applications.application_date,applications.status FROM applications JOIN applicants ON applications.applicant_id=applicants.applicant_id JOIN jobs ON applications.job_id = jobs.job_id WHERE applicants.name = %s"
        cursor.execute(query,(name,))
        result= cursor.fetchall()
        connection.commit()
        if result:
            print("Filtered Applications: ")
            for row in result:
                print(row)
        else:
            print("No applications found")    
    elif choice =="3":
        title = input("Enter the title of the job to filter by: ")
        query = "SELECT applications.application_id,applicants.name,jobs.title,applications.application_date,applications.status FROM applications JOIN applicants ON applications.applicant_id=applicants.applicant_id JOIN jobs ON applications.job_id = jobs.job_id WHERE jobs.title = %s"
        cursor.execute(query,(title,))
        result= cursor.fetchall()
        connection.commit()
        if result:
            print("Filtered Applications: ")
            for row in result:
                print(row)
        else:
            print("No applications found")
    else:
        print("Invalid choice. Please enter a number between 1 and 3.")
        
def generateStatistics(cursor,connection):
        query = "SELECT status,COUNT(application_id) FROM applications GROUP BY status"
        cursor.execute(query)
        result = cursor.fetchall()
        print("\nApplication Statistics:")
        print("Status       | Count")
        print("-" * 25)
        for row in result:
            print(row)
        connection.commit()
        
def customQueries(cursor,connection):
    customQuery = input("Enter your custom Query: ")
    try:
        cursor.execute(customQuery)
        result = cursor.fetchall()
        if result:
            print("results \n")
            for row in result:
                print(row)
    except Exception as e:
        print("Error executing the Query ",e)
        
def exportCSV(cursor,connection):
    try:
        query = "SELECT applications.application_id,applicants.name,jobs.title,applications.application_date,applications.status FROM applications JOIN applicants ON applications.applicant_id=applicants.applicant_id JOIN jobs ON applications.job_id = jobs.job_id "
        cursor.execute(query)
        result_data = cursor.fetchall()
        file_path = "job_application.csv"
        with open(file_path,mode='w',newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(["Application ID","Applicant Name","Job Title","Application Date","Application Status"])
            csv_writer.writerows(result_data)
            print(f"Applications data exported to {file_path} successfully.")
    except Exception as e:
        print("Error exporting applications data: {e}")

def closeConnection(cursor,connection):
    cursor.close()
    connection.close()
def main():
    fake = Faker()
    cursor,connection = createConnection()
    generateApplicantsTable(fake, cursor,connection)
    generateJobsTable(fake, cursor,connection)
    generateApplicationsTable(fake, cursor,connection)
    
    while True:
        print("\nJob Application Tracker Menu:")
        print("1. Display Applications")
        print("2. Add Application")
        print("3. Update Application Status")
        print("4. Delete Application ")
        print("5. Get statistics")
        print("6. Apply Filter Applications")
        print("7. Custom Queries")
        print("8. export as csv file")
        print("9. Exit")

        choice = input("Enter your choice (1-9): ")

        if choice == "1":
            display(cursor)
        elif choice == "2":
            addApplication(cursor,connection)
        elif choice == "3":
            updateStatus(cursor,connection)
        elif choice == "4":
            deleteApplication(cursor,connection)
        elif choice == "5":
            generateStatistics(cursor,connection)
        elif choice == "6":
            filterApplication(cursor,connection)
        elif choice == "7":
            customQueries(cursor,connection)
        elif choice == "8":
            exportCSV(cursor,connection)
        elif choice == "9":
            print("Exiting the application. Goodbye!")
            closeConnection(cursor,connection)
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 9.")
if __name__ == "__main__":
    main()