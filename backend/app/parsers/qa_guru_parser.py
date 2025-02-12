import httpx
from bs4 import BeautifulSoup
import json
import asyncio
from datetime import datetime
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class QaGuruParser:
    BASE_URL = "https://qa.guru"
    
    async def parse_courses(self) -> List[Dict[str, Any]]:
        """Parse courses from qa.guru and return structured data"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.BASE_URL)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                courses_data = []
                
                # Find the courses section
                courses_section = soup.find('section', {'id': 'courses'})
                if not courses_section:
                    logger.error("Courses section not found")
                    return []
                
                # Find all course cards
                course_cards = courses_section.find_all('div', class_='card')
                
                for card in course_cards:
                    course = {
                        'title': self._get_title(card),
                        'description': self._get_description(card),
                        'price': self._get_price(card),
                        'duration': self._get_duration(card),
                        'start_date': self._get_start_date(card),
                        'program': self._get_program(card),
                        'features': self._get_features(card),
                        'school': {
                            'name': 'qa.guru',
                            'address': 'https://qa.guru',
                            'logo': 'https://qa.guru/logo.png'
                        },
                        'platform': {
                            'name': 'Telegram',
                            'url': 'https://t.me/qa_automation_course',
                            'logo': 'https://telegram.org/logo.png'
                        },
                        'categories': ['automation', 'testing', 'python'],
                        'engineer_level': self._get_level(card),
                        'students_amount': self._get_students_amount(card),
                        'rating': 4.8  # Default rating as it's not shown on the page
                    }
                    courses_data.append(course)
                
                logger.info(f"Successfully parsed {len(courses_data)} courses from qa.guru")
                return courses_data
                
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred while parsing qa.guru: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error occurred while parsing qa.guru: {str(e)}")
            return []

    def _get_title(self, card) -> str:
        """Extract course title"""
        title_elem = card.find('h3')
        return title_elem.text.strip() if title_elem else "Unknown Course"

    def _get_description(self, card) -> str:
        """Extract course description"""
        desc_elem = card.find('div', class_='description')
        return desc_elem.text.strip() if desc_elem else ""

    def _get_price(self, card) -> float:
        """Extract course price"""
        try:
            price_elem = card.find('div', class_='price')
            if price_elem:
                price_text = price_elem.text.strip()
                # Extract numbers from string like "29 900 ₽"
                price = float(''.join(filter(str.isdigit, price_text)))
                return price
            return 0.0
        except (ValueError, AttributeError):
            return 0.0

    def _get_duration(self, card) -> str:
        """Extract course duration"""
        duration_elem = card.find('div', class_='duration')
        if duration_elem:
            # Convert duration text to standard format
            duration_text = duration_elem.text.strip()
            if 'месяц' in duration_text:
                weeks = int(duration_text.split()[0]) * 4
                return f"{weeks} weeks"
        return "8 weeks"

    def _get_start_date(self, card) -> str:
        """Extract course start date"""
        date_elem = card.find('div', class_='start-date')
        return date_elem.text.strip() if date_elem else "По набору группы"

    def _get_program(self, card) -> List[str]:
        """Extract course program topics"""
        program_elem = card.find('ul', class_='program')
        if program_elem:
            return [item.text.strip() for item in program_elem.find_all('li')]
        return []

    def _get_features(self, card) -> List[str]:
        """Extract course features"""
        features_elem = card.find('ul', class_='features')
        if features_elem:
            return [item.text.strip() for item in features_elem.find_all('li')]
        return []

    def _get_level(self, card) -> str:
        """Extract engineer level"""
        level_elem = card.find('div', class_='level')
        if level_elem:
            text = level_elem.text.strip().lower()
            if 'senior' in text or 'продвинутый' in text:
                return 'senior'
            elif 'middle' in text or 'средний' in text:
                return 'middle'
        return 'junior'

    def _get_students_amount(self, card) -> int:
        """Extract number of students"""
        try:
            students_elem = card.find('div', class_='students')
            if students_elem:
                return int(''.join(filter(str.isdigit, students_elem.text)))
            return 0
        except (ValueError, AttributeError):
            return 0

async def save_courses_to_json():
    """Parse courses and save to JSON file"""
    parser = QaGuruParser()
    courses = await parser.parse_courses()
    
    if courses:
        # Create data directory if it doesn't exist
        data_dir = Path(__file__).parent.parent / "data"
        data_dir.mkdir(exist_ok=True)
        
        # Save to JSON file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = data_dir / f"qa_guru_courses_{timestamp}.json"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({
                'source': QaGuruParser.BASE_URL,
                'parsed_at': datetime.now().isoformat(),
                'courses': courses
            }, f, ensure_ascii=False, indent=2)
            
        logger.info(f"Courses data saved to {file_path}")
        return file_path
    else:
        logger.error("No courses data to save")
        return None

if __name__ == "__main__":
    asyncio.run(save_courses_to_json()) 