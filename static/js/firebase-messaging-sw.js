importScripts('https://www.gstatic.com/firebasejs/9.9.3/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/9.9.3/firebase-messaging.js');

firebase.initializeApp({
    apiKey: "AIzaSyBcMlyHrjGtdBAoNH6-USpCa2KRjilOYOM",
    authDomain: "universityweb-90663.firebaseapp.com",
    projectId: "universityweb-90663",
    storageBucket: "universityweb-90663.appspot.com",
    messagingSenderId: "374031309473",
    appId: "1:374031309473:web:bdccf11152504f8d356ee0"
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
    console.log('Received background message ', payload);
    const notificationTitle = payload.notification.title;
    const notificationOptions = {
        body: payload.notification.body,
        icon: '/static/images/android-chrome-192x192.png'
    };

    self.registration.showNotification(notificationTitle, notificationOptions);
});
