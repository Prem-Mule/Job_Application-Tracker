# JobAppTracker

## Overview

JobAppTracker is a Python and MySQL-based application designed to streamline job application management. Easily track applications, update statuses, apply filters, and export data for an organized job search experience.

## Features

- **Application Management:** Add, update, and delete job applications.
- **Status Tracking:** Efficiently track application statuses (Accepted, Pending, Rejected).
- **Filter Applications:** Apply filters by status, applicant, or job title.
- **Export Data:** Export application data to a CSV file for easy analysis.

## Getting Started

1. **Install Dependencies:**
    ```bash
    pip install mysql-connector-python faker
    ```

2. **Setup MySQL Database:**
    - Create a MySQL database named `job_application_tracker`.
    - Update connection details in `createConnection()` function in the script.

3. **Run the Application:**
    ```bash
    python job_application_tracker.py
    ```

## Usage

- Follow the on-screen menu to interact with the application.
- Choose options to display applications, add applications, update status, and more.

## Contributing

Contributions are welcome! Fork the repository and create a pull request with your enhancements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Happy job hunting! 🚀
