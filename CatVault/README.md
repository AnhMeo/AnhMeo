# Overview

As a software engineer and aspiring Cybersecurity architect who is passionate about enhancing my skills in mobile application development and security, I am working on building a robust and secure note-taking app to deepen my understanding of encryption, authentication, and React Native development. This project serves as a practical exploration of integrating secure storage and user authentication into a functional mobile application.

The CatVault app is a secure note-taking application designed for users who want to protect their sensitive information with a PIN. To use the app, start by setting a 4-digit PIN on the authentication screen that appears upon first launch. Once authenticated, navigate to the Home screen and tap "Create Note" to access the Notes screen. Here, you can type a note, save it (with an option to save unencrypted if encryption fails), view saved notes, and delete them. Notes are protected by the PIN, and the app provides feedback if encryption or decryption issues occur.

My purpose for creating this app is to gain hands-on experience with secure data handling, implement a user-friendly interface, and troubleshoot real-world challenges like encryption failures in a mobile environment, all while building a portfolio piece to showcase my growing expertise.

[Software Demo Video](https://www.youtube.com/watch?v=_u-jgvHCRpo)

# Development Environment

The app was developed using Visual Studio Code as the primary IDE, with the Expo Go platform for testing on an Android emulator. The build process utilized the Expo CLI for managing the development workflow.

The programming language used is TypeScript, enhancing JavaScript with static typing for better scalability and error checking. Key libraries include React Native for the UI and navigation, Expo for cross-platform development and native modules (e.g., expo-secure-store, expo-crypto, expo-local-authentication), and crypto-js for encryption functionalities.

# Useful Websites

* [Expo Documentation](https://docs.expo.dev/)
* [React Native Documentation](https://reactnative.dev/docs/getting-started)
* [CryptoJS Official site](https://cryptojs.gitbook.io/docs)

# Future Work

* Improve encryption reliability by testing on physical devices and resolving native crypto module issues.
* Add support for biometric authentication as a primary login method on supported devices
* Add camera and photo feature
* Add ability to store other types of files (.docx, .pptx, etc.)