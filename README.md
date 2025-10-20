![Selenium Banner](docs/images/selenium_python_logo.png)

<h1 align="center"><strong>UI Selenium Automation Project</strong></h1>

### ⚠️ Important Note on Test Environment and "DevTools" Interaction

This test suite is designed to run in a **controlled educational testing environment** (such as TripleTen's ContainerHub or similar platforms), where the application under test includes a **simulated browser DevTools panel** as part of its **visible HTML DOM**.

In a real-world scenario, **Selenium cannot interact with the actual browser DevTools** (e.g., Network tab, Console, etc.), because those are part of the browser’s internal UI—not the web page’s HTML. However, in this specific environment:

- The test page **embeds a fake "Network" panel** directly into the page using standard HTML elements (e.g., `<div class="tab">Network</div>`, `<div class="name">`, `<div class="preview">`, etc.).
- These elements are **fully accessible via Selenium** because they exist in the document object model (DOM) like any other button or input field.
- Therefore, tests such as `test_09_select_tab` through `test_13_copy_number` **successfully extract verification codes** by interacting with this simulated panel—not the real DevTools.

#### Example of Simulated DevTools HTML (visible in page source):
```html
<div class="tab">Network</div>
<div class="name">
  <div>POST /api/auth/verification</div>
</div>
<div class="preview">
  <div>123</div> <!-- This is the SMS code -->
</div>
```

Because of this setup, the following test logic **works as intended** in this environment:
```python
network_tab = driver.find_element(By.XPATH, "//div[@class='tab'][text()='Network']")
network_tab.click()

code_element = driver.find_element(By.XPATH, "//div[@class='preview']/div")
sms_code = code_element.text  # Returns "123"
```

> 🔒 **Do not expect this approach to work on real websites.**  
> This technique is **only valid in this specific training environment**, where the "DevTools" are part of the app’s UI for educational purposes.

If you run these tests against a standard production website, they will **fail** because the required DOM elements won’t exist.

 
## **Automated tests to verify the functionality of an urban transportation app called Urban Routes**

- Definition of locators and methods used in the `UrbanRoutesPage` class  
- Definition of test cases in the `TestUrbanRoutes` class  
- Automated tests covering the complete taxi booking workflow:
  - Setting a pickup address  
  - Selecting a fare option  
  - Filling in a valid phone number  
  - Adding a valid credit card  
  - Writing a message for the driver  
  - Requesting additional services  
  - Ordering a taxi by clicking the corresponding button  
  - Waiting for the driver’s information, license plate, and estimated arrival time to appear in the modal

# **Python and Pytest Verification & Installation**
![Static Badge](https://img.shields.io/badge/Python_3.12-blue) ![Static Badge](https://img.shields.io/badge/Pytest_8.4.1-green)

This file outlines the steps to verify whether Python is installed in your development environment, how to install it if missing, and how to check for pytest installation and run tests using pytest.

## **Verifying Python Installation on Windows**

To check if Python is installed, open a Git Bash terminal and run the following command:

```bash
python --version
```

If that doesn't work, try:

```bash
python3 --version
```

If you don’t have Git Bash installed, you can download it for Windows from [here](https://git-scm.com/download/win).  
On macOS, Git Bash is not required because a default terminal (zsh) is already available, but you can still download Git from [here](https://git-scm.com/downloads).

If Python is installed, this command will display the installed version. If not, you’ll see an error indicating that `'python'` is not recognized as a command.

### **Installing Python**

If Python is not installed, follow these steps based on your operating system:

**![Static Badge](https://img.shields.io/badge/Windows-blue):**

- Go to the official Python website: [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)  
- Download the appropriate installer for your system  
- Run the installer and follow the on-screen instructions

**![Static Badge](https://img.shields.io/badge/Mac-black):**

You can install Python using Homebrew from the terminal:

```bash
brew install python
```

or, if that fails:

```bash
brew install python3
```

Alternatively, download the installer from the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)

**![Static Badge](https://img.shields.io/badge/Linux-purple):**

Most Linux distributions include Python by default. You can install or update it using your distribution’s package manager. For example, on Ubuntu or Debian, run:

```bash
sudo apt-get update
sudo apt-get install python3
```

## **Verifying Pytest Installation**

To check if pytest is installed, run the following command in your terminal:

```bash
pytest --version
```

If pytest is installed, it will display the version number. If not, you’ll get an error indicating that `'pytest'` is not recognized.

If pytest is not installed, you can install it using `pip`, Python’s package manager:

```bash
pip install -U pytest
```

## **Running Tests with Pytest**

Once pytest is installed, you can run your tests as follows:

- In your terminal, navigate to the directory containing your test files  
- Run the command:

```bash
pytest
```

This will execute all tests in the current directory and its subdirectories.

> **Note:** This is a general guide. Steps may vary slightly depending on your operating system and specific environment configuration.

This should provide a clear, step-by-step reference for verifying Python, installing it if needed, checking for pytest, and running automated tests once everything is set up.