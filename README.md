# Monitoraggio Moduli

Hey! I made this tool to make managing JotForm submissions way easier. With "Monitoraggio Moduli", you can view, manage, and bulk delete your JotForm submissions, all without having to deal with the JotForm website, which can be slow and a pain to use, especially if you're dealing with a ton of submissions.

The project is available and publicly accessible through **GitHub Pages** at this link: [Monitoraggio Moduli](https://concordatofacile.github.io/monitoraggio-moduli/).

**Note**: This tool was designed for internal use, meant for my colleagues and clients. Accessing the program requires a password, which will be associated with a specific JotForm API key for each user. If you want to use this program for your own personal stuff, you'll need to tweak the HTML code to remove the authentication request.

## What's It For?

This program lets you:

*   **See all your JotForm forms**: Get a clean, organized list of all your forms.
*   **Check submission status**: See how many submissions each form has received and when the last one came in.
*   **Bulk delete submissions**: You can select one or more forms and delete all their submissions with a single click. This is super helpful for clearing out old submissions and keeping your data tidy.
*   **Automatic Updates**: The program updates itself automatically so you always see the latest data.

## How to Get Started

Since the program is publicly available through Github Pages, you don't need to download the repository locally to use it unless you want to make changes to the source code.

But, if you still want to download the repo to modify it, follow these steps:

1. **Download the Project**:
    *   Go to the main page of the repository on GitHub.
    *   Click the green "Code" button.
    *   Select "Download ZIP" to download the compressed project file to your computer.

2. **Extract the ZIP File**:
    *   Once downloaded, find the ZIP file in your downloads folder (or wherever you saved it).
    *   Extract the contents of the ZIP file to a folder of your choice on your computer.

3. **Launch the Program**:
    *   Open the extracted folder.
    *   Find the `index.html` file and open it with your favorite browser (e.g., Chrome, Firefox, Safari, etc.).

4. **Authentication**:
    *   The program will ask you to enter a password. Even if you download the program locally, you will still be asked for a password unless you modify the source code. Once you enter a valid password (as I said, valid passwords are associated with a specific Jotform API key for each user), you will be able to use the program.
    *   If you're a colleague or client of mine, hit me up to get the password and your associated API key. Otherwise, modify the source code to remove the authentication request.

5. **Enter Your API Key**:
    *   Once you've entered the correct password, the program will ask if you want to load the default API key associated with your account. If you say yes, your API key will be loaded automatically. Otherwise, you can manually enter your JotForm API key. You can find it in your JotForm account settings.

## Use Cases and Examples

Here are a few scenarios where this tool can come in handy:

### Example 1: Periodic Submission Cleanup

Imagine you have a contact form on your website that gets a lot of submissions every day. After a while, you might want to delete the older submissions to keep your data organized. With "Monitoraggio Moduli", you can:

1. Retrieve all your forms.
2. Select the contact form.
3. Click "Delete Selected Submissions" to wipe out all submissions for that form.

### Example 2: Quick Check of Recent Submissions

If you have a form for event registrations, you can use this tool to quickly check when the last submission was made. This helps you see if there have been any new registrations without having to log into the JotForm site.

### Example 3: Managing Multiple Forms

If you manage different forms for various purposes (e.g., feedback, orders, support, etc.), this tool gives you a complete overview of all your forms in one place. You can see which forms are active, how many submissions they have, and when the last submission was made.

## Disclaimer and Updates

This repository might be updated at any time. These updates might make this README file obsolete. I don't guarantee that I'll update the README to reflect the changes made to the repository. I recommend checking out the code and project structure for the most up-to-date info.
