<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Employee Management System - Copilot Instructions

This is a Flask-based employee management system with Arabic and English support for managing employee data, passport status, and card expiry tracking.

## Project Context
- **Language**: Python with Flask framework
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Localization**: Arabic (RTL) and English support
- **Purpose**: Employee management with passport and ID card status tracking

## Code Style Guidelines
- Use Arabic comments for business logic
- Follow Flask best practices
- Use SQLAlchemy for database operations
- Maintain responsive design with Bootstrap
- Implement proper error handling
- Use meaningful variable names in both Arabic and English contexts

## Database Schema
- Companies table: company_code, company_name_eng, company_name_ara
- Jobs table: job_code, job_eng, job_ara  
- Employees table: staff_no, staff_name, staff_name_ara, job_code, pass_no, nationality_code, company_code, card_no, card_expiry_date, create_date_time

## Key Features to Maintain
- Multi-language search functionality
- Passport status tracking (available/missing)
- Card status tracking (valid/expiring/expired/missing)
- Real-time statistics dashboard
- Responsive Arabic/English UI
- Advanced filtering capabilities

## Security Considerations
- Input validation for search queries
- SQL injection prevention through SQLAlchemy
- Secure handling of employee personal data
- Local data storage (no external data transmission)

When generating code:
- Prioritize Arabic language support in UI text
- Ensure proper RTL text direction handling
- Maintain consistent database relationships
- Follow Flask application structure
- Include proper error handling and user feedback
