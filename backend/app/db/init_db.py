from datetime import datetime
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import CourseDB, SchoolDB, PlatformDB

def init_db():
    db = SessionLocal()
    try:
        # Clear existing data first
        print("Clearing existing data...")
        db.query(CourseDB).delete()
        db.query(PlatformDB).delete()
        db.query(SchoolDB).delete()
        db.commit()
        print("Existing data cleared successfully")

        # Create schools
        print("Creating schools...")
        schools = [
            SchoolDB(
                name="qa.guru",
                address="https://qa.guru",
                logo="https://qa.guru/logo.png",
                foundation_date=datetime(2020, 1, 1).date()
            ),
            SchoolDB(
                name="learnqa.ru",
                address="https://learnqa.ru",
                logo="https://learnqa.ru/logo.png",
                foundation_date=datetime(2019, 1, 1).date()
            ),
            SchoolDB(
                name="Software-Testing",
                address="https://software-testing.ru",
                logo="https://software-testing.ru/logo.png",
                foundation_date=datetime(2018, 1, 1).date()
            ),
            SchoolDB(
                name="Udemy",
                address="https://udemy.com",
                logo="https://udemy.com/logo.png",
                foundation_date=datetime(2010, 1, 1).date()
            ),
            SchoolDB(
                name="Coursera",
                address="https://coursera.org",
                logo="https://coursera.org/logo.png",
                foundation_date=datetime(2012, 4, 1).date()
            ),
            SchoolDB(
                name="Pluralsight",
                address="https://pluralsight.com",
                logo="https://pluralsight.com/logo.png",
                foundation_date=datetime(2004, 5, 1).date()
            ),
            SchoolDB(
                name="TestPro",
                address="https://testpro.io",
                logo="https://testpro.io/logo.png",
                foundation_date=datetime(2019, 6, 1).date()
            ),
            SchoolDB(
                name="OTUS",
                address="https://otus.ru",
                logo="https://otus.ru/logo.png",
                foundation_date=datetime(2016, 9, 1).date()
            ),
            SchoolDB(
                name="SkillFactory",
                address="https://skillfactory.ru",
                logo="https://skillfactory.ru/logo.png",
                foundation_date=datetime(2016, 3, 1).date()
            ),
            SchoolDB(
                name="GeekBrains",
                address="https://geekbrains.ru",
                logo="https://geekbrains.ru/logo.png",
                foundation_date=datetime(2014, 8, 1).date()
            ),
            SchoolDB(
                name="Hexlet",
                address="https://hexlet.io",
                logo="https://hexlet.io/logo.png",
                foundation_date=datetime(2015, 7, 1).date()
            )
        ]
        for school in schools:
            db.add(school)
        db.commit()
        print("Schools created successfully")

        # Create platforms
        print("Creating platforms...")
        platforms = [
            PlatformDB(
                name="Telegram",
                url="https://telegram.org",
                logo="https://telegram.org/logo.png",
                description="Messaging platform with channels and educational groups",
                features=["Private channels", "Group chats", "File sharing", "Video calls"]
            ),
            PlatformDB(
                name="Website",
                url="https://learnqa.ru",
                logo="https://learnqa.ru/logo.png",
                description="LearnQA education platform",
                features=["Video courses", "Interactive exercises", "Community", "Code reviews"]
            ),
            PlatformDB(
                name="Zoom",
                url="https://zoom.us",
                logo="https://zoom.us/logo.png",
                description="Video conferencing platform",
                features=["Live sessions", "Screen sharing", "Breakout rooms", "Recording"]
            ),
            PlatformDB(
                name="Discord",
                url="https://discord.com",
                logo="https://discord.com/logo.png",
                description="Community platform with voice and text channels",
                features=["Voice channels", "Text channels", "Screen sharing", "Bot integration"]
            ),
            PlatformDB(
                name="YouTube",
                url="https://youtube.com",
                logo="https://youtube.com/logo.png",
                description="Video sharing platform with educational content",
                features=["Video streaming", "Live sessions", "Comments", "Playlists"]
            )
        ]
        for platform in platforms:
            db.add(platform)
        db.commit()
        print("Platforms created successfully")

        # Get references to all schools
        print("Getting school references...")
        qa_guru = db.query(SchoolDB).filter_by(name="qa.guru").first()
        learnqa = db.query(SchoolDB).filter_by(name="learnqa.ru").first()
        software_testing = db.query(SchoolDB).filter_by(name="Software-Testing").first()
        udemy = db.query(SchoolDB).filter_by(name="Udemy").first()
        coursera = db.query(SchoolDB).filter_by(name="Coursera").first()
        pluralsight = db.query(SchoolDB).filter_by(name="Pluralsight").first()
        testpro = db.query(SchoolDB).filter_by(name="TestPro").first()
        otus = db.query(SchoolDB).filter_by(name="OTUS").first()
        skillfactory = db.query(SchoolDB).filter_by(name="SkillFactory").first()
        geekbrains = db.query(SchoolDB).filter_by(name="GeekBrains").first()
        hexlet = db.query(SchoolDB).filter_by(name="Hexlet").first()

        print("Getting platform references...")
        telegram = db.query(PlatformDB).filter_by(name="Telegram").first()
        website = db.query(PlatformDB).filter_by(name="Website").first()
        zoom = db.query(PlatformDB).filter_by(name="Zoom").first()
        discord = db.query(PlatformDB).filter_by(name="Discord").first()
        youtube = db.query(PlatformDB).filter_by(name="YouTube").first()

        # Create courses
        print("Creating courses...")
        courses = [
            CourseDB(
                title="Python Automation",
                description="Learn Python from scratch with focus on test automation",
                instructor="John Doe",
                duration="8 weeks",
                price=99.99,
                school_id=qa_guru.id,
                platform_id=telegram.id,
                categories=["python", "automation", "testing"],
                engineer_level="junior",
                students_amount=150,
                rating=4.5
            ),
            CourseDB(
                title="Advanced Selenium WebDriver",
                description="Master web testing with Selenium and Python",
                instructor="Jane Smith",
                duration="12 weeks",
                price=149.99,
                school_id=learnqa.id,
                platform_id=website.id,
                categories=["testing", "selenium", "automation"],
                engineer_level="middle",
                students_amount=200,
                rating=4.8
            ),
            CourseDB(
                title="API Testing Masterclass",
                description="Complete guide to API testing with Postman and Python",
                instructor="Bob Wilson",
                duration="6 weeks",
                price=79.99,
                school_id=software_testing.id,
                platform_id=zoom.id,
                categories=["api", "testing", "postman"],
                engineer_level="junior",
                students_amount=300,
                rating=4.7
            ),
            CourseDB(
                title="Performance Testing Pro",
                description="Learn JMeter and K6 for performance testing",
                instructor="Alice Brown",
                duration="10 weeks",
                price=199.99,
                school_id=qa_guru.id,
                platform_id=discord.id,
                categories=["performance", "jmeter", "k6"],
                engineer_level="senior",
                students_amount=100,
                rating=4.9
            ),
            CourseDB(
                title="Mobile Testing Fundamentals",
                description="Mobile testing with Appium and XCUITest",
                instructor="Charlie Davis",
                duration="8 weeks",
                price=129.99,
                school_id=learnqa.id,
                platform_id=youtube.id,
                categories=["mobile", "appium", "testing"],
                engineer_level="middle",
                students_amount=250,
                rating=4.6
            ),
            CourseDB(
                title="Security Testing Basics",
                description="Introduction to security testing and tools",
                instructor="Eva Green",
                duration="6 weeks",
                price=149.99,
                school_id=software_testing.id,
                platform_id=website.id,
                categories=["security", "testing", "owasp"],
                engineer_level="middle",
                students_amount=180,
                rating=4.7
            ),
            CourseDB(
                title="Test Automation Architecture",
                description="Design and implement robust test frameworks",
                instructor="Frank Miller",
                duration="10 weeks",
                price=299.99,
                school_id=qa_guru.id,
                platform_id=discord.id,
                categories=["architecture", "automation", "python"],
                engineer_level="senior",
                students_amount=120,
                rating=4.9
            ),
            CourseDB(
                title="CI/CD for QA Engineers",
                description="Master CI/CD tools and practices for QA",
                instructor="Grace Lee",
                duration="8 weeks",
                price=179.99,
                school_id=coursera.id,
                platform_id=zoom.id,
                categories=["devops", "ci-cd", "jenkins"],
                engineer_level="middle",
                students_amount=220,
                rating=4.8
            ),
            CourseDB(
                title="Cypress Testing Framework",
                description="Modern web testing with Cypress.io",
                instructor="David Chen",
                duration="6 weeks",
                price=149.99,
                school_id=pluralsight.id,
                platform_id=website.id,
                categories=["cypress", "javascript", "testing"],
                engineer_level="middle",
                students_amount=280,
                rating=4.7
            ),
            CourseDB(
                title="Load Testing with Gatling",
                description="Performance testing using Scala and Gatling",
                instructor="Sarah Johnson",
                duration="8 weeks",
                price=189.99,
                school_id=testpro.id,
                platform_id=zoom.id,
                categories=["performance", "gatling", "scala"],
                engineer_level="senior",
                students_amount=150,
                rating=4.8
            ),
            CourseDB(
                title="Playwright Automation",
                description="Modern web testing with Playwright",
                instructor="Mike Zhang",
                duration="7 weeks",
                price=159.99,
                school_id=otus.id,
                platform_id=discord.id,
                categories=["playwright", "typescript", "automation"],
                engineer_level="middle",
                students_amount=190,
                rating=4.6
            ),
            CourseDB(
                title="TestNG Framework Mastery",
                description="Advanced Java testing with TestNG",
                instructor="Linda Kumar",
                duration="9 weeks",
                price=199.99,
                school_id=skillfactory.id,
                platform_id=youtube.id,
                categories=["java", "testng", "automation"],
                engineer_level="senior",
                students_amount=160,
                rating=4.7
            ),
            CourseDB(
                title="Robot Framework Basics",
                description="Test automation with Robot Framework",
                instructor="Peter Anderson",
                duration="6 weeks",
                price=129.99,
                school_id=geekbrains.id,
                platform_id=website.id,
                categories=["robot-framework", "python", "automation"],
                engineer_level="junior",
                students_amount=220,
                rating=4.5
            ),
            CourseDB(
                title="Cucumber BDD",
                description="Behavior Driven Development with Cucumber",
                instructor="Rachel White",
                duration="7 weeks",
                price=169.99,
                school_id=hexlet.id,
                platform_id=zoom.id,
                categories=["bdd", "cucumber", "testing"],
                engineer_level="middle",
                students_amount=240,
                rating=4.6
            ),
            CourseDB(
                title="Docker for QA",
                description="Containerization basics for QA engineers",
                instructor="Tom Brown",
                duration="5 weeks",
                price=139.99,
                school_id=qa_guru.id,
                platform_id=discord.id,
                categories=["docker", "devops", "containers"],
                engineer_level="middle",
                students_amount=270,
                rating=4.8
            ),
            CourseDB(
                title="Test Data Management",
                description="Managing test data effectively",
                instructor="Emma Davis",
                duration="4 weeks",
                price=99.99,
                school_id=learnqa.id,
                platform_id=website.id,
                categories=["data", "testing", "management"],
                engineer_level="middle",
                students_amount=180,
                rating=4.4
            ),
            CourseDB(
                title="GraphQL API Testing",
                description="Testing GraphQL APIs with various tools",
                instructor="James Wilson",
                duration="6 weeks",
                price=159.99,
                school_id=software_testing.id,
                platform_id=youtube.id,
                categories=["graphql", "api", "testing"],
                engineer_level="senior",
                students_amount=140,
                rating=4.7
            ),
            CourseDB(
                title="Test Design Techniques",
                description="Advanced test case design methods",
                instructor="Maria Garcia",
                duration="8 weeks",
                price=179.99,
                school_id=coursera.id,
                platform_id=zoom.id,
                categories=["test-design", "methodology", "testing"],
                engineer_level="middle",
                students_amount=290,
                rating=4.9
            ),
            CourseDB(
                title="AI in Testing",
                description="Using AI and ML in test automation",
                instructor="Alex Turner",
                duration="10 weeks",
                price=249.99,
                school_id=udemy.id,
                platform_id=discord.id,
                categories=["ai", "ml", "automation"],
                engineer_level="senior",
                students_amount=130,
                rating=4.8
            ),
            CourseDB(
                title="Visual Regression Testing",
                description="Automated visual testing techniques",
                instructor="Sophie Chen",
                duration="5 weeks",
                price=119.99,
                school_id=pluralsight.id,
                platform_id=website.id,
                categories=["visual", "regression", "testing"],
                engineer_level="middle",
                students_amount=210,
                rating=4.6
            )
        ]
        for course in courses:
            db.add(course)
        db.commit()
        print("Courses created successfully")

        print("Database initialized successfully!")

    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 