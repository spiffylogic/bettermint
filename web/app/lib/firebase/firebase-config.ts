// https://blog.stackademic.com/setting-up-firebase-authentication-with-next-13-app-router-using-server-components-03fbcab254e4

import { initializeApp, getApps } from "firebase/app";
import { GoogleAuthProvider, getAuth } from "firebase/auth";

export const firebaseConfig = {
    apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
    authDomain: process.env.NEXT_PUBLIC_AUTH_DOMAIN,
    projectId: process.env.NEXT_PUBLIC_PROJECT_ID,
    appId: process.env.NEXT_PUBLIC_APP_ID
};

export const firebaseApp =
  getApps().length === 0 ? initializeApp(firebaseConfig) : getApps()[0];
export const firebaseAuth = getAuth(firebaseApp);
export const provider = new GoogleAuthProvider();