import { initializeApp } from "https://www.gstatic.com/firebasejs/9.9.3/firebase-app.js";
import { getMessaging, getToken, onMessage } from "https://www.gstatic.com/firebasejs/9.9.3/firebase-messaging.js";

const firebaseConfig = {
    apiKey: "AIzaSyBcMlyHrjGtdBAoNH6-USpCa2KRjilOYOM",
    authDomain: "universityweb-90663.firebaseapp.com",
    projectId: "universityweb-90663",
    storageBucket: "universityweb-90663.appspot.com",
    messagingSenderId: "374031309473",
    appId: "1:374031309473:web:bdccf11152504f8d356ee0"
};

const app = initializeApp(firebaseConfig);

const messaging = getMessaging(app);

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('university_website/static/js/firebase-messaging-sw.js')
    .then((registration) => {
        console.log('Service Worker registered with scope:', registration.scope);
    })
    .catch((error) => {
        console.error('Service Worker registration failed:', error);
    });
}

function requestNotificationPermission() {
    console.log('Requesting notification permission...');
    Notification.requestPermission().then((permission) => {
        if (permission === 'granted') {
            console.log('Notification permission granted.');
            getToken(messaging, { vapidKey: 'BJUhmkSUPM9xAQ8lf1olPDZSdjOwz2yA94OK605LTKMoIcoYSwGh91F2oEtDQ4gJqVPue_v_-YAeX6IPerpxnQc' }).then((currentToken) => {
                if (currentToken) {
                    console.log('FCM Token:', currentToken);
                } else {
                    console.log('No registration token available. Request permission to generate one.');
                }
            }).catch((err) => {
                console.log('An error occurred while retrieving token. ', err);
            });
        } else {
            console.log('Unable to get permission to notify.');
        }
    });
}

onMessage(messaging, (payload) => {
    console.log('Message received. ', payload);
    const notificationTitle = payload.notification.title;
    const notificationOptions = {
        body: payload.notification.body,
        icon: '/static/images/android-chrome-192x192.png'
    };

    new Notification(notificationTitle, notificationOptions);
});

window.onload = function() {
    requestNotificationPermission();
};
